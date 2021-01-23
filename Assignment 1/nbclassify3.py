import os
import sys
import glob
import string
import math

def countWordsFromTestData(filePath):
    if not sys.argv[1].endswith('/'):
        sys.argv[1] += '/'
    for root, directories, files in os.walk(sys.argv[1]):
        filePath.extend(glob.glob(root + '/**.txt'))

def readModelFile(wordMap):
    f = open("nbmodel.txt", "r")
    data = f.readlines()
    f.close()
    temp = data[0].split()
    positiveTruthful = float(temp[0])
    positiveDeceptive = float(temp[1])
    negativeTruthful = float(temp[2])
    negativeDeceptive = float(temp[3])
    for num in range(1, len(data)):
        word = data[num].split()
        probabilityList = []
        for num in range(1, len(word)):
            probabilityList.append(float(word[num]))
        wordMap[word[0]] = probabilityList
    return positiveTruthful, positiveDeceptive, negativeTruthful, negativeDeceptive

def returnClass(val, resultPT, resultPD, resultNT, resultND):
    if val == resultPT:
        return "truthful positive"
    elif val == resultPD:
        return "deceptive positive"
    elif val == resultNT:
        return "truthful negative"
    else:
        return "deceptive negative"

def classifyFiles(positiveTruthful, positiveDeceptive, negativeTruthful, negativeDeceptive, filePath, ignore, wordMap):
    with open("nboutput.txt", "w+") as out:
        for file in filePath:
            resultPT = -math.log(positiveTruthful);
            resultPD = -math.log(positiveDeceptive);
            resultNT = -math.log(negativeTruthful);
            resultND = -math.log(negativeDeceptive);
            with open(file, 'r') as f:
                text = str(f.read())
                words = text.lower().strip().split()
                for word in words:
                    if word in ignore:
                        continue
                    token = word.translate(str.maketrans('', '', string.punctuation))
                    if token not in wordMap:
                        continue
                    pTruth = -math.log(wordMap[token][0])
                    pDeceptive = -math.log(wordMap[token][1])
                    nTruth = -math.log(wordMap[token][2])
                    nDeceptive = -math.log(wordMap[token][3])
                    resultPT += pTruth
                    resultPD += pDeceptive
                    resultNT += nTruth
                    resultND += nDeceptive
                list = [resultPT, resultPD, resultNT, resultND]
                maxVal = min(list)
            writeOutputFile(returnClass(maxVal, resultPT, resultPD, resultNT, resultND), file, out)

def writeOutputFile(switchCond, file, out):
    out.write("%s %s" % (switchCond, file))
    out.write("\n")

def main():
    ignore = ["the", "i", "soon", "all", "stay", "stayed", "hers", "rooms", "his", "with", "they", "we", "hotel", "you",
              "me", "a", "so", "our", "had", "home", "made", "everything", "here", "what", "very", "on", "that", "then",
              "are", "can", "when", "has", "am", "an", "us", "as", "it", "location", "time", "would", "knew", "she",
              "do", "be", "supper", "pier", "those", "was", "your", "could", "its", "city", "im", "at", "again", "trip",
              "also", "if", "which", "this", "there", "them", "of", "how", "just", "did", "by", "my", "have", "and",
              "outside", "hotels", "place", "tower", "sofitel", "their", "where", "were", "is", "he", "service", "room",
              "door", "chicago", "ask", "for", "in", "anniversary", "weekend", "her", "out", "one", "mine", "from",
              "to", "water", "hilton", "staying", "husbands", "wifes", "about", "get", "myself", "ours", "ourselves",
              "these", "now", "theirs", "themselves", "does"]

    wordMap = {}
    filePath = []

    positiveTruthful, positiveDeceptive, negativeTruthful, negativeDeceptive = readModelFile(wordMap)
    countWordsFromTestData(filePath)
    classifyFiles(positiveTruthful, positiveDeceptive, negativeTruthful, negativeDeceptive, filePath, ignore, wordMap)

if __name__ == "__main__":
    main()