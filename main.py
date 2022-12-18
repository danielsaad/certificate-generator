import argparse
import os
import csv
import subprocess

def create_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('svg_file',help='The svg template file with the placeholders.')
    parser.add_argument('csv_file',help='The csv file containing, for each column (key), the data to be replaced.')
    parser.add_argument('output_folder',help='The output folder to store the PDF files.',default='output')
    return parser

def read_csv(csv_file):
    data = []
    with open(csv_file) as csv_f:
        reader = csv.reader(csv_f)
        data = [row for row in reader]
    return data

def replace(svg_file,new_file,data):
    with open(svg_file,'r') as f_in, open(new_file,'w') as f_out:
        pass
            


def process(args):
    os.makedirs(args.output_folder,exist_ok=True)
    data = read_csv(args.csv_file)
    header = data[0]
    tmp_svg_list=[os.path.join(args.output_folder,str(i+1)+'.svg') for i in range(len(data[1:]))]
    pdf_list = [os.path.join(args.output_folder,str(i+1)+'.pdf') for i in range(len(data[1:]))]
    for svg,pdf,row in zip(tmp_svg_list,pdf_list,data[1:]):
        sed_regex= ';'.join(['s/{{ '+ h + ' }}/' + d + '/g' for (h,d) in zip(header,row)])
        sed_command = ['sed',sed_regex,args.svg_file]
        rsvg_command = ['rsvg-convert', '-f', 'Pdf', '-o', pdf, svg]
        with open(svg,'w') as svg_file:
            subprocess.run(sed_command,stdout=svg_file)
            subprocess.run(rsvg_command)
    certificates = os.path.join(args.output_folder,'certificados.pdf')
    pdftk_command = ['pdftk'] + pdf_list + ['cat','output',certificates]
    subprocess.run(pdftk_command)
    for svg,pdf in zip(pdf_list,tmp_svg_list):
        os.remove(svg)
        os.remove(pdf)

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    process(args)