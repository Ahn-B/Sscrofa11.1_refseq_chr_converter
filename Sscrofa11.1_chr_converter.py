#!/usr/bin/env python


"""

Author: ByeongYong Ahn
E-mail: byahn1123@gmail.com

"""


chr_dic = {'NC_010443.5': 'chr1', 'NC_010444.4': 'chr2', 'NC_010445.4': 'chr3', 'NC_010446.5': 'chr4',
           'NC_010447.5': 'chr5', 'NC_010448.4': 'chr6', 'NC_010449.5': 'chr7', 'NC_010450.4': 'chr8',
           'NC_010451.4': 'chr9', 'NC_010452.4': 'chr10', 'NC_010453.5': 'chr11', 'NC_010454.4': 'chr12',
           'NC_010455.5': 'chr13', 'NC_010456.5': 'chr14', 'NC_010457.5': 'chr15', 'NC_010458.4': 'chr16',
           'NC_010459.5': 'chr17', 'NC_010460.4': 'chr18', 'NC_010461.5': 'chrX', 'NC_010462.3': 'chrY',
           'NC_000845.1': 'chrMT'}


class Help:
    def __init__(self):
        msg = 'Chromosome converter for RefSeq gff of Sscrofa11.1\n\n' \
              'python [this script] [input_gff] [output_gff]\n'
        print(msg)


def open_file(infile):
    import gzip
    if infile.endswith('.gz'):
        fr = gzip.open(infile, 'rt')
    else:
        fr = open(infile, 'r')
    return fr


def is_fa(file_name):
    fasta_list = ['fna', 'fna.gz', 'fa', 'fa.gz', 'fasta', 'fasta.gz']

    for element in fasta_list:
        if file_name.endswith(element):
            return True


class Convert:
    def __init__(self, infile, outfile):
        self.fw = open(outfile, 'w')
        self.fr = open_file(infile)

    def chr_in_gff(self):

        for line in self.fr:
            if line.startswith('#'):
                self.fw.write(line)
                continue

            line = line.rstrip()
            cols = line.split('\t')
            chr_col = cols[0]

            if chr_col in chr_dic:
                self.fw.write('{}\t{}\n'.format(chr_dic[chr_col], '\t'.join(cols[1:])))
            else:
                self.fw.write('{}\n'.format(line))

    def chr_in_fasta(self):
        for line in self.fr:
            if line.startswith('>'):
                chr_start = 1
                chr_end = line.find(' ')
                chromosome = line[chr_start: chr_end]

                if chromosome in chr_dic:
                    line = line.replace(chromosome, chr_dic[chromosome])

                self.fw.write(line)
            else:
                self.fw.write('{}'.format(line))


def main():
    import sys

    if len(sys.argv) < 2:
        Help()
        sys.exit()

    infile = sys.argv[1]
    outfile = sys.argv[2]

    convert = Convert(infile, outfile)
    if infile.endswith('gff.gz') or infile.endswith('gff') or infile.endswith('gtf') or infile.endswith('gtf.gz'):
        convert.chr_in_gff()

    elif is_fa(infile):
        convert.chr_in_fasta()


if __name__ == "__main__":
    main()
    # EOF
