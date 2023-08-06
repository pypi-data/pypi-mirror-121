import argparse
import numpy as np
import re


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",
                        metavar="<in.fasta>",
                        help="FASTA or Sequence file",
                        required=True)
    parser.add_argument("-o", "--output",
                        metavar="<out.npy>",
                        help="Numpy .npy format",
                        required=True)
    parser.add_argument("-t", "--type",
                        metavar="<dna/rna/protein>",
                        choices=['dna', 'rna', 'protein'],
                        help="Sequence type (DNA/RNA/Protein)",
                        required=True)
    parser.add_argument("-a", "--ambiguous",
                        help="Accept ambiguous characters",
                        action="store_true",)
    parser.add_argument('-v', '--version', action='version', version='0.0.1')
    args = parser.parse_args()
    return args


def load_fasta(fasta_file):
    with open(fasta_file, "r") as f:
        content = f.read()
        regex = re.compile("(>.*?)\n([A-Za-z\n]*)", re.DOTALL)
        wrap_fasta = re.findall(regex, content)
        seq = list()
        append = seq.append
        if wrap_fasta:
            for i in wrap_fasta:
                append(i[1].replace('\n', '').upper())
        else:
            seq = content.splitlines()
    return seq


def define_alphabet(seqtype, ambiguous):
    if seqtype == "dna":
        alphabet = "ACGT"
        if ambiguous:
            alphabet += "NVHDBMRWSYK"
    elif seqtype == "rna":
        alphabet = "ACGU"
        if ambiguous:
            alphabet += "NVHDBMRWSYK"
    elif seqtype == "protein":
        alphabet = "ACDEFGHIKLMNPQRSTVWY"
        if ambiguous:
            alphabet += "XBZJ"
    return alphabet


def seq2onehot(seq, type, ambiguous):
    alphabet = define_alphabet(type, ambiguous)
    onehot = np.zeros([len(seq), len(seq[0]), len(alphabet)])
    for i, s in enumerate(seq):
        s_list = list(alphabet + s)
        alphabet_categorical = np.unique(s_list, return_inverse=True)[1]
        alphabet_categorical = np.expand_dims(alphabet_categorical, 0)
        oh = np.eye(len(alphabet), dtype=np.uint8)[alphabet_categorical]
        oh = oh[:, len(alphabet):]
        onehot[i] = oh
    return onehot


def main():
    args = parse()
    seq = load_fasta(args.input)
    onehot = seq2onehot(seq, args.type, args.ambiguous)
    np.save(args.output, onehot)


if __name__ == "__main__":
    main()
