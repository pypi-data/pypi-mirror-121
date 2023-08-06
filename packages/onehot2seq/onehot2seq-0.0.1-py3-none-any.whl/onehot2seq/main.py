import argparse
import numpy as np


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",
                        help="Numpy npy file", required=True)
    parser.add_argument("-o", "--output",
                        help="FASTA or text file", required=True)
    parser.add_argument("-t", "--type",
                        metavar="<dna/rna/protein>",
                        choices=['dna', 'rna', 'protein'],
                        help="Sequence type (DNA/RNA/Protein)",
                        required=True)
    parser.add_argument("-a", "--ambiguous",
                        help="Accept ambiguous characters",
                        action="store_true",)
    parser.add_argument("-f", "--format",
                        choices=['txt', 'fasta'],
                        default="txt",
                        help="FASTA or text file (defalt:txt)")
    parser.add_argument('-v', '--version', action='version', version='0.0.1')
    args = parser.parse_args()
    return args


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


def decode_to_seq(onehot, alphabet):
    seq = list()
    append = seq.append
    for i in onehot:
        s = ''.join([alphabet[s] for s in i.nonzero()[1]])
        append(s)
    return seq


def format_to_fasta(seq):
    headers = ['>seq' + str(s) for s in list(range(1, len(seq) + 1))]
    output = ['\n'.join((h, s)) for h, s in zip(headers, seq)]
    output = "\n".join(output) + "\n"
    return output


def main():
    args = parse()
    onehot = np.load(args.input)
    alphabet = define_alphabet(args.type, args.ambiguous)
    seq = decode_to_seq(onehot, alphabet)
    if args.format == "fasta":
        output = format_to_fasta(seq)
    else:
        output = "\n".join(seq) + "\n"

    with open(args.output, "w", newline="\n") as f:
        f.write(output)


if __name__ == "__main__":
    main()
