import sys

def compare(inputLines, outputLines):
    correct = 0
    inCorrect = 0
    for input, output in zip(inputLines, outputLines):
        inputWords = input.split()
        outputWords = output.split()
        for inWord, outWord in zip(inputWords, outputWords):
            if inWord == outWord:
                correct += 1
            else:
                inCorrect += 1
    return correct, inCorrect

def readFile(path):
    lines = []
    with open(path, "r", encoding="utf8")as f:
        lines = f.readlines()
    return lines

def main():
    inputLines = readFile("hmm-training-data\it_isdt_dev_tagged.txt")
    outputLines = readFile("hmmoutput.txt")
    correct, inCorrect = compare(inputLines, outputLines)
    print(correct)
    print(correct + inCorrect)
    print(correct/ (correct + inCorrect))

if __name__ == "__main__":
    main()