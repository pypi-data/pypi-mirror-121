# -*- coding: utf-8 -*-

import streamlit as st
from Bio import Entrez
import pandas as pd
import subprocess
from subprocess import PIPE
import re
import time
import os
import gzip
import glob
import base64
import numpy as np
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CustomJS, HoverTool
from streamlit_bokeh_events import streamlit_bokeh_events
from sklearn.manifold import MDS
import zipfile
from PIL import Image
import sys

sys.path.append(os.getcwd())
sys.path.append('../genome_mds')

import genome_mds

top_image = Image.open("{0}/img/logo.png".format(genome_mds.__path__[0]))

st.set_page_config(page_title="Genome-MDS",page_icon = "{0}/img/logo.png".format(genome_mds.__path__[0]), layout = 'wide')

def decompress(infile, outfile):
    with open(infile, 'rb') as inf, open(outfile, 'w', encoding='utf8') as outf:
        decom_str = gzip.decompress(inf.read()).decode('utf-8')
        outf.write(decom_str)

def get_lines(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,encoding='utf-8')
    while True:
        line = proc.stdout.readline()
        if line:
            yield line
        if not line and proc.poll() is not None:
            break

def mat2df(path_to_matrix):
    seq_num = int(pd.read_table(path_to_matrix,nrows=1,header=None)[0])
    _raw = pd.read_table(path_to_matrix,sep="\t",skiprows=1,index_col=0,header=None,names=[i for i in range(seq_num+1)])
    new_names = []
    for f in _raw.index:
      new_names.append([ i for i in re.split('/|.f|.gz|.zip|.tar.gz',f)[::-1] if len(i)> 0][1])
    _raw.columns = new_names
    _raw.index = new_names
    _raw_t = _raw.T.copy()
    np.fill_diagonal(_raw.to_numpy(),100)
    np.fill_diagonal(_raw_t.to_numpy(),0)
    _raw = _raw.fillna(0)
    _raw_t = _raw_t.fillna(0)
    raw = _raw + _raw_t
    return seq_num, round((100-raw)/100,5)

def remove_glob(pathname, recursive=True):
    for p in glob.glob(pathname, recursive=recursive):
        if os.path.isfile(p):
            os.remove(p)

def main():
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    top_col1, top_col2, top_col3 = st.columns(3)
    with top_col1:
        st.write("")

    with top_col2:
        st.image(top_image,width=180)

    with top_col3:
        st.write("")

    st.header('STEP1: Set output prefix')
    OUT_DIR = st.text_input(label='Input prefix name', value='')
    tmp_seqs_dir = "{0}/working_directory".format(OUT_DIR)

    try:
        if not os.path.isdir("{0}/working_directory".format(OUT_DIR)):
            os.makedirs("{0}/working_directory".format(OUT_DIR))
    except OSError:
        st.info("Please input prefix.")
        st.stop()

    st.write('All results and temporary files will be save in','"{0}"'.format(OUT_DIR))

    st.header('STEP2: Upload your genomes')
    multiple_files = st.file_uploader('Upload FASTA files',type=['fasta','fas','fna','fa'], accept_multiple_files=True)
    multiple_files_name = []
    if multiple_files:
        for file in multiple_files:
            with open(os.path.join(tmp_seqs_dir,file.name),"wb") as f:
                f.write(file.getbuffer())
    st.header('STEP3 (Option): Download genomes')
    selected_item = st.radio('Genome sequences will be downloaded according to NCBI Taxnomy ID',
                                 ['None (Default)', 'Download'],index=0)
    if selected_item == 'Download':
        selected_db = st.radio('Select database',
                                 ['RefSeq', 'Genbank'],index=0)
        selected_assembly_level = st.radio('Select assembly level',
                                 ['complete', 'chromosome', 'scaffold', 'contig','all'],index=0)

        mail_address = st.text_input(label='Input your e-mail address. NCBI requires you to specify your email address with each request.',
                            value='')
        if len(mail_address) != 0 and ('@' not in mail_address) and ('.' not in mail_address):
            st.warning('Invalid input. Please check your e-mail address.')

        tax_num = st.number_input(label='Input NCBI Taxonomy IDs.',
                            value=0,
                            )
        if tax_num !=  0:
            try:
                Entrez.email = mail_address
                handle = Entrez.efetch(db="Taxonomy", id=tax_num, retmode="xml")
                records = Entrez.read(handle)
                st.write('Selected organisms: {0}'.format(records[0]['ScientificName']))
                st.info('The list of available genomes is currently being fetched. Please wait for a while.')
                proc_dry_run = subprocess.run("ncbi-genome-download -g '{0}' -n -s genbank -l complete bacteria".format(records[0]['ScientificName']), shell=True, stdout=PIPE, stderr=PIPE, text=True)
                dry_run_stdout = proc_dry_run.stdout
                if len(dry_run_stdout) != 0:
                    dl_seq_num = int([re.findall('\d+',line)[0] for line in re.split("\n",dry_run_stdout) if line.startswith('Considering')][0])
                    dl_seq_list = re.split("\n",dry_run_stdout)[1:-1]
                    with st.expander('Select genomes for download',expanded=True):
                        check_boxes = [st.checkbox(seq_name,key=seq_name,value=True) for seq_name in dl_seq_list]
                        st.write("""After you confirm the above download list, click "Download genomes". The checked genomes will be automatically downloaded.""")
                        if st.button('Download genomes') == True:
                            progress_max = len([seq_name for seq_name, checked in zip(dl_seq_list, check_boxes) if checked])
                            selected_seq = ",".join([re.split('\t',i)[0] for i in [seq_name for seq_name, checked in zip(dl_seq_list, check_boxes) if checked]])
                            proc_dl_run = subprocess.Popen("""ncbi-genome-download -A '{0}' -s genbank -l complete bacteria -o {1} -F fasta --flat-output""".format(selected_seq,tmp_seqs_dir), shell=True, stdout=PIPE, stderr=PIPE, text=True)
                            st.info('Download has been started. This process may take a while depending on your network environment.')
                            file_num = 0
                            status_text = st.empty()
                            progress_bar = st.progress(0)
                            upload_file_num = int(sum(os.path.isfile(os.path.join(tmp_seqs_dir, name)) for name in os.listdir(tmp_seqs_dir) if name[0] != '.'))
                            while file_num < progress_max:
                                file_num = int(sum(os.path.isfile(os.path.join(tmp_seqs_dir, name)) for name in os.listdir(tmp_seqs_dir) if name[0] != '.'))-upload_file_num
                                percentage = int((float(file_num)/(progress_max))*100)
                                status_text.text(f'Progress: {file_num}/{progress_max}')
                                progress_bar.progress(percentage)
                                time.sleep(1)
                            status_text.text(f'Progress: {progress_max}/{progress_max}')
                            if len([name for name in glob.glob(tmp_seqs_dir+"/*fna.gz")]) == progress_max:
                                for name in glob.glob(tmp_seqs_dir+"/*fna.gz"):
                                    try:
                                        decompress(name,re.split(".fna.gz",name)[0]+".fasta")
                                    except EOFError:
                                        time.sleep(5)
                                        decompress(name,re.split(".fna.gz",name)[0]+".fasta")
                                    status_text.text('Finish! Downloaded genomes were added to the sample list in STEP4.')
                            else:
                                st.stop()
                else:
                    st.warning('Download Errors. Please check Taxonomy ID.')
                    st.stop()

            except IndexError:
                st.warning('Invalid Taxonomy ID')
        else:
            st.write('No downloaded sequences.')
    st.header('STEP4: Distance calculation')
    with st.expander('Select genomes for distance calculation (default:ALL)',expanded=True):
        fasta_list = glob.glob(tmp_seqs_dir+"/*.fa")+glob.glob(tmp_seqs_dir+"/*.fas")+glob.glob(tmp_seqs_dir+"/*.fna")+glob.glob(tmp_seqs_dir+"/*.fasta")
        for name in sorted(fasta_list, key=os.path.getmtime):
            multiple_files_name.append(os.path.basename(name))
        check_boxes_file = [st.checkbox(file_name,key=str(k),value=True) for k,file_name in enumerate(multiple_files_name)]

    with st.expander('Calculation parameters'):
        col1, col2 = st.columns(2)
        with col1:
            kmer_num=st.number_input(label='k-mer size (default:16)',value=16)
        with col2:
            thread_num=st.number_input(label='thread for parallel execution (default:1)',value=1,max_value=int(os.cpu_count()))

    if st.button('Run') == True:
        st.info("Distance calculation has started. Please wait for a while until it is completed.")
        pd.Series([os.path.abspath(tmp_seqs_dir+"/"+file_name) for file_name, checked in zip(multiple_files_name, check_boxes_file) if checked]).to_csv(tmp_seqs_dir+"/seq_list.txt",sep="\t",index=False,header=None)
        ani_run = "fastANI -t {thread} -k {kmer} --ql {genome_list} --rl {genome_list} --matrix -o {tmp_dir}/ani_run".format(genome_list=tmp_seqs_dir+"/seq_list.txt",tmp_dir=tmp_seqs_dir,thread=thread_num,kmer=kmer_num)
        subprocess.run(ani_run,shell=True, stdout=PIPE, stderr=PIPE, text=True)
        st.info('Run complete !')

    st.header('STEP5: Interactive MDS')

    try:
        ani_seq_num, df_dist = mat2df("{tmp_dir}/ani_run.matrix".format(tmp_dir=tmp_seqs_dir))
        mds = MDS(n_components=2,random_state=0,dissimilarity='precomputed')
        mds_res = mds.fit_transform(df_dist)
        df_mds_res = pd.DataFrame(mds_res, columns=['Dimention-1', 'Dimention-2'])
        df_mds_res.index = df_dist.index

        from bokeh.palettes import diverging_palette, Viridis256, Plasma256, Colorblind8
        colors = dict(zip(df_mds_res.index,diverging_palette(Viridis256,Plasma256,ani_seq_num)))
        df_mds_res['colors']=df_mds_res.index.map(colors)
        source = ColumnDataSource(df_mds_res)
        hover = HoverTool(
           tooltips=[
           ("Sample", "@index"),
           ("(Dim-1,Dim-2)", "($x, $y)"),
           ],
           mode="vline",
           show_arrow=True,
        )
        plot = figure(tools="lasso_select,pan,wheel_zoom,reset,save", width=500, height=500)
        plot.circle(x="Dimention-1", y="Dimention-2", line_color = "black",color="colors", source=source, alpha=0.6,size=10)
        plot.xaxis.axis_label = "Dimention-1"
        plot.yaxis.axis_label = "Dimention-2"
        plot.add_tools(hover)
        plot.toolbar.logo = None
        plot.toolbar_location = "above"
        source.selected.js_on_change(
            "indices",
            CustomJS(
                args=dict(source=source),
                code="""
                document.dispatchEvent(
                    new CustomEvent("SelectEvent", {detail: {indices: cb_obj.indices}})
                )
            """,
            ),
        )

        event_result = streamlit_bokeh_events(
            events="SelectEvent",
            bokeh_plot=plot,
            key="foo",
            debounce_time=100,
            refresh_on_update=False
        )

        if event_result is not None:
            if "SelectEvent" in event_result:
                st.write("Check the ones you want to retrieve from the sequences selected in the above MDS.  \n\nThe checked sequences can be obtained from the following generated download link.")
                with st.expander('Selected sequences',expanded=True):
                    indices = event_result["SelectEvent"].get("indices", [])
                    selected_seqs = [st.checkbox(f,key=str(k+100),value=True) for k,f in enumerate(df_dist.index[indices])]
                    fasta_paths = pd.read_csv(tmp_seqs_dir+"/seq_list.txt",header=None)[0].T
                    selected_seqs_path = [file_name for file_name, checked in zip(fasta_paths[indices], selected_seqs) if checked]

                    if len(selected_seqs_path) > 0:
                        with zipfile.ZipFile('{out}/selected_seqs.zip'.format(out=OUT_DIR), 'w', compression=zipfile.ZIP_DEFLATED) as out_zip:
                            for i in selected_seqs_path:
                                out_zip.write('{0}'.format(i), arcname='{0}'.format(os.path.basename(i)))
                        ZipfileDotZip='{out}/selected_seqs.zip'.format(out=OUT_DIR)
                        with open(ZipfileDotZip, "rb") as f:
                            bytes = f.read()
                            b64 = base64.b64encode(bytes).decode()
                            href = f"<a href=\"data:file/zip;base64,{b64}\" download='selected_seqs.zip'>\
                                Download selected sequences\
                            </a>"
                        st.markdown(href, unsafe_allow_html=True)

    except FileNotFoundError:
        pass

if __name__ == '__main__':
    main()
