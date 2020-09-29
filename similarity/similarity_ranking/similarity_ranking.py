import os
import subprocess
import re


class SimilarityRanking(object):
    FASTTEXT = os.path.join(os.getcwd(), "fasttext")
    TITLE_RE_PATTERN = r'(?P<score>1|0.\d+)\s(\d+)\s(?P<title>((\S+\s?)+))'

    def __init__(self):
        pass

    def loadModel(self, model, corpus, nbest):
        return subprocess.Popen((self.FASTTEXT, 'nnSent', model, corpus, nbest),
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

    def similarityRanking(self, proc, title):
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

    def terminateProc(self, proc):
        proc.stdin.close()
        proc.terminate()
        print("***Process terminated***")

    def printList(self, list):
        for l in list:
            match = re.match(self.TITLE_RE_PATTERN, l)
            if match is not None:
                print(match.groupdict())


if __name__ == '__main__':
    similarityRanker = SimilarityRanking()
    proc = similarityRanker.loadModel('model.bin', 'titleSet.txt', '30')
    lines = similarityRanker.similarityRanking(proc, "Animal Farm")
    similarityRanker.printList(lines)
    lines = similarityRanker.similarityRanking(proc, "Dracula")
    similarityRanker.printList(lines)
    lines = similarityRanker.similarityRanking(proc, "Frankenstein")
    similarityRanker.printList(lines)
    lines = similarityRanker.similarityRanking(proc, "pigs")
    similarityRanker.printList(lines)
    lines = similarityRanker.similarityRanking(proc, "The Bible")
    similarityRanker.printList(lines)
    similarityRanker.terminateProc(proc)
