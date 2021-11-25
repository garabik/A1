#!/usr/bin/python3

# read vertical conll-u file on stdin
# calculates some statistics of sentence lengths (and plots a distribution)
# output files are put in current working directory, named 'curlicat-sentence*'

import sys, statistics

from collections import Counter

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter


def get_conll_sentence_lengths(conll):
    "read lines from conll iterator until an empty line (i.e. sentence break) is encountered"
    "yield length of the sentence"
    slen = 0
    for l in conll:
        if l.startswith('#'):
            continue
        line = l.strip()
        if line=='':
            if slen > 0:
                yield slen
                slen = 0
        else:
            slen += 1
    if slen > 0:
        yield slen

def pprint_hist(hist, scount, output):
    "pretty-print a histogram"
    of = open(output, 'w')
    print('# distribution of sentences by their length', file=of)
    print('# length\tcount\tratio', file=of)
    for k in sorted(hist.keys()):
        ratio = hist[k] / scount
        print(k, hist[k], ratio, sep='\t', file=of)

def print_stats(hist, scount, output):
    thr = 10

    of = open(output, 'w')
    data = list(hist.elements())
    mean = statistics.mean(data)
    median = statistics.median(data)
    mode = statistics.mode(data)
    stdev = statistics.stdev(data)
    longest = max(hist.keys())

    below_thr = sum(kv[1] for kv in hist.items() if kv[0]<thr)  # nr. of sentences of length below threshold
    above_eq_thr = sum(kv[1] for kv in hist.items() if kv[0]>=thr) # nr. of sentences of length above or equal the threshold


    print(f'''number of sentences = {scount}
number of sentences shorter than {thr}: {below_thr}
number of sentences longer or equal {thr}: {above_eq_thr}
mean = {mean}
median = {median}
mode = {mode}
stdev = {stdev}
longest sentence = {longest} tokens

''', file = of)

def plot_stats(hist, output):
    X, Y = zip(*hist.items())
    plt.xscale('log')
    plt.yscale('log')

    ax = plt.gca()
    for axis in [ax.xaxis, ax.yaxis]:
        formatter = ScalarFormatter()
        axis.set_major_formatter(formatter)
    plt.xlabel('Sentence length [token]')
    plt.ylabel('Number of sentences')
    plt.grid(True)
    plt.bar(X, Y)
    plt.savefig(output)


if __name__=='__main__':
    dr = './'
    shist = Counter() # distribution of sentence lengths
    scount = 0 # total number of sentences
    for slen in get_conll_sentence_lengths(sys.stdin):
        shist[slen] += 1
        scount += 1
    pprint_hist(shist, scount, output=dr+'curlicat-sentence_histogram.txt')
    print_stats(shist, scount, output=dr+'curlicat-sentence_statistics.txt')
    plot_stats(shist, output=dr+'curlicat-sentence_distribution.pdf')

