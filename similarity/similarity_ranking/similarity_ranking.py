import os
import subprocess
import re

FASTTEXT = os.path.join(os.getcwd(), "fasttext")
TITLE_RE_PATTERN = r'(?P<score>1|0.\d+)\s(\d+)\s(?P<title>((\S+\s?)+))'


def loadModel(model, corpus, nbest):
    return subprocess.Popen((FASTTEXT, 'nnSent', model, corpus, nbest),
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)


def similarityRanking(proc, title):
    print("\n*** Find the similar books for ", title, " ***")
    lines = []
    proc.stdin.write(str.encode(title + '\n'))
    proc.stdin.flush()
    while True:
        line = proc.stdout.readline()
        if line == b'\n':
            break
        else:
            lines.append(line.decode("utf-8").strip())
    return lines


def terminateProc(proc):
    proc.stdin.close()
    proc.terminate()
    print("***Process terminated***")


def printList(list):
    for l in list:
        match = re.match(TITLE_RE_PATTERN, l)
        if match is not None:
            print(match.groupdict())


if __name__ == '__main__':
    proc = loadModel('model.bin', 'titleSet.txt', '30')
    lines = similarityRanking(proc, "Animal Farm")
    printList(lines)
    lines = similarityRanking(proc, "Dracula")
    printList(lines)
    lines = similarityRanking(proc, "Frankenstein")
    printList(lines)
    lines = similarityRanking(proc, "pigs")
    printList(lines)
    lines = similarityRanking(proc, "The Bible")
    printList(lines)
    terminateProc(proc)
