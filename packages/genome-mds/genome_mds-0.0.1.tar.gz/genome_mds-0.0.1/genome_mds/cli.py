"""Console script for genome_mds."""
import argparse
import sys
import pkg_resources

from streamlit import cli as stcli

def main():
    """Console script for genome_mds."""
    parser = argparse.ArgumentParser(description='Genome-MDS\n Version : 0.0.1')
    parser.add_argument('-M',action='store',dest='max_size',help='Limit of a maximum size for uploadling files (defaul:200 Mb)',default=200)
    parser.add_argument('-v',action='version',version='Version : 0.0.1')

    print ("============================================================================")
    print ("                              Genome-MDS                                    ")
    print ("              a graphical two-dimensional comparison tool                   ")
    print ("                         for prokaryotic genomes                            ")
    print ("                                                                            ")
    print ("                          > Version : 0.0.1                                 ")
    print ("                          > Developed by K.I.                               ")
    print ("                          > Lisence: MIT                                    ")
    print ("============================================================================")

    args = parser.parse_args()

    if args.max_size == 200:
        sys.argv= ["streamlit", "run","--server.address","localhost","{0}".format(pkg_resources.resource_filename('genome_mds','core.py'))]
    else:
        sys.argv= ["streamlit", "run","--server.address","localhost","--server.maxUploadSize={0}".format(int(args.max_size)),"{0}".format(pkg_resources.resource_filename('genome_mds','core.py'))]
    sys.exit(stcli.main())
