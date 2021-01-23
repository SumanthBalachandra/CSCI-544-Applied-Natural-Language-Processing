import os
import sys
import string

def countTotalNumberOfWords(classes):
    if not sys.argv[1].endswith('/'):
        sys.argv[1] += '/'
    fileNames = []
    for root, directories, files in os.walk(sys.argv[1]):
        for file in files:
            if '.txt' in file and not "MACOSX" in root:
                fileNames.append(os.path.join(root, file))
    fetchFileNames(fileNames, "positive", "truthful", "PositiveTruthful", classes)
    fetchFileNames(fileNames, "positive", "deceptive", "PositiveDeceptive", classes)
    fetchFileNames(fileNames, "negative", "truthful", "NegativeTruthful", classes)
    fetchFileNames(fileNames, "negative", "deceptive", "NegativeDeceptive", classes)

def fetchFileNames(files, className, subClassName, key, classes):
    for file in files:
        if className not in file or subClassName not in file:
            continue
        classes[key].append(file)

def getVocabulary(classes, ignore, vocabulary, classWordMap, classWordCount):
    for key in classes.keys():
        wordMap = {}
        count = 0
        for file in classes[key]:
            with open(file, 'r') as f:
                text = str(f.read())
                words = text.lower().strip().split()
                for word in words:
                    if word in ignore:
                        continue
                    count += 1
                    token = word.translate(str.maketrans('', '', string.punctuation))
                    if token in vocabulary:
                        vocabulary[token] += 1
                    else:
                        vocabulary[token] = 1
                    if token in wordMap:
                        wordMap[token] += 1
                    else:
                        wordMap[token] = 1
        classWordMap[key + 'Map'] = wordMap
        classWordCount[key + "Count"] = count

def calculateProbability(word, f, positiveTruthfulWords, positiveDeceptiveWords, negativeTruthfulWords, negativeDeceptiveWords, vocabulary):
    positiveTruthCount = 0
    positiveDeceptiveCount = 0
    negativeTruthCount = 0
    negativeDeceptiveCount = 0
    if word in positiveTruthfulWords:
        positiveTruthCount = positiveTruthfulWords[word]
    if word in positiveDeceptiveWords:
        positiveDeceptiveCount = positiveDeceptiveWords[word]
    if word in negativeTruthfulWords:
        negativeTruthCount = negativeTruthfulWords[word]
    if word in negativeDeceptiveWords:
        negativeDeceptiveCount = negativeDeceptiveWords[word]
    positiveTruthfulProb = (positiveTruthCount + 1) / (sum(positiveTruthfulWords.values()) + len(vocabulary))
    positiveDeceptiveProb = (positiveDeceptiveCount + 1) / (sum(positiveDeceptiveWords.values()) + len(vocabulary))
    negativeTruthfulProb = (negativeTruthCount + 1) / (sum(negativeTruthfulWords.values()) + len(vocabulary))
    negativeDeceptiveProb = (negativeDeceptiveCount + 1) / (sum(negativeDeceptiveWords.values()) + len(vocabulary))
    f.write("%s %s %s %s %s" % (word, positiveTruthfulProb, positiveDeceptiveProb, negativeTruthfulProb, negativeDeceptiveProb))
    f.write("\n")


def main():
    classes = {"PositiveTruthful": [], "PositiveDeceptive": [], "NegativeTruthful": [], "NegativeDeceptive": []}
    ignore = ["the", "i", "soon", "all", "stay", "stayed", "hers", "rooms", "his", "with", "they", "we", "hotel", "you",
              "me", "a", "so", "our", "had", "home", "made", "everything", "here", "what", "very", "on", "that", "then",
              "are", "can", "when", "has", "am", "an", "us", "as", "it", "location", "time", "would", "knew", "she",
              "do", "be", "supper", "pier", "those", "was", "your", "could", "its", "city", "im", "at", "again", "trip",
              "also", "if", "which", "this", "there", "them", "of", "how", "just", "did", "by", "my", "have", "and",
              "outside", "hotels", "place", "tower", "sofitel", "their", "where", "were", "is", "he", "service", "room",
              "door", "chicago", "ask", "for", "in", "anniversary", "weekend", "her", "out", "one", "mine", "from",
              "to", "water", "hilton", "staying", "husbands", "wifes", "about", "get", "myself", "ours", "ourselves",
              "these", "now", "theirs", "themselves", "does"]

    vocabulary = {}
    classWordCount = {}
    classWordMap = {}
    positiveTruthfulWords = {}
    positiveDeceptiveWords = {}
    negativeTruthfulWords = {}
    negativeDeceptiveWords = {}

    countTotalNumberOfWords(classes)
    getVocabulary(classes, ignore, vocabulary, classWordMap, classWordCount)
    positiveTruthfulWords = classWordMap["PositiveTruthfulMap"]
    positiveDeceptiveWords = classWordMap["PositiveDeceptiveMap"]
    negativeTruthfulWords = classWordMap["NegativeTruthfulMap"]
    negativeDeceptiveWords = classWordMap["NegativeDeceptiveMap"]
    with open("nbmodel.txt", "w+") as f:
        total = len(classes["PositiveTruthful"]) + len(classes["PositiveDeceptive"]) + len(classes["NegativeTruthful"]) + len(classes["NegativeDeceptive"])
        positiveTruth = len(classes["PositiveTruthful"]) / total
        positiveDeceptive = len(classes["PositiveDeceptive"]) / total
        negativeTruth = len(classes["NegativeTruthful"]) / total
        negativeDecpetive = len(classes["NegativeDeceptive"]) / total
        f.write("%s %s %s %s" % (positiveTruth, positiveDeceptive, negativeTruth, negativeDecpetive))
        f.write("\n")
        for word in vocabulary:
            calculateProbability(word, f, positiveTruthfulWords, positiveDeceptiveWords, negativeTruthfulWords, negativeDeceptiveWords, vocabulary)

if __name__ == "__main__":
    main()