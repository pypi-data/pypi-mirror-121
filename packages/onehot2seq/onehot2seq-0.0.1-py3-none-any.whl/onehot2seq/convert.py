

def toACGT(onehot):
    alphabets = "ACGT"
    seq = list()
    append = seq.append
    for i in onehot:
        _ = ''.join([alphabets[s] for s in i.nonzero()[1]])
        append(_)
    return seq


def toACGU(data):
    seq = list()
    append = seq.append
    for i in range(len(data)):
        if data[i][0] == 1:
            append("A")
        elif data[i][1] == 1:
            append("C")
        elif data[i][2] == 1:
            append("G")
        elif data[i][3] == 1:
            append("U")
    return ''.join(seq)
