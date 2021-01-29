import os
import sys
import json

def calculateTransitionProbability(posBigramSequenceCount, posTrigramSequenceCount, tagCount):
    bigramDict = {}
    trigramRowTotalDict = {}
    for cur, valueOne in posBigramSequenceCount.items():
        bigramDict[cur] = sum(posBigramSequenceCount[cur].values())
    bigramDict['<empty'] = bigramDict['<start>']
    posBigramSequenceCount['<start>'] = {}
    posBigramSequenceCount['<start>']['<empty>'] = bigramDict['<start>']
    posBigramSequenceCount['<empty>'] = {}
    posBigramSequenceCount['<empty>']['<start>'] = bigramDict['<start>']
    for cur, value in posTrigramSequenceCount.items():
        if cur not in trigramRowTotalDict:
            trigramRowTotalDict[cur] = 0
        for prevOne, valueOne in posTrigramSequenceCount[cur].items():
            trigramRowTotalDict[cur] += sum(posTrigramSequenceCount[cur][prevOne].values())
        for prevOne, valueOne in posTrigramSequenceCount[cur].items():
            for prevTwo, valueTwo in posTrigramSequenceCount[cur][prevOne].items():
                posTrigramSequenceCount[cur][prevOne][prevTwo] = (valueTwo + 1) / (posBigramSequenceCount[prevOne][prevTwo] + len(tagCount) + 3)
    return posTrigramSequenceCount

def calculateEmissionProbability(wordTagCount, tagCount):
    for word, tag in wordTagCount.items():
        for key, value in wordTagCount[word].items():
            wordTagCount[word][key] = value / tagCount[key]
    return wordTagCount

def getTrigramTagPosSequenceCount(lines):
    posTagSequence = {}
    for line in lines:
        words = line.split()
        words.insert(0, "<start>")
        words.append("<end>")
        first = "<start>"
        second = "<empty>"
        for word in words:
            tag = ""
            tagIndex = word.rfind('/')
            if tagIndex == -1:
                if word == "<start>":
                    tag = "<start>"
                elif word == "<end>":
                    tag = "<end>"
            else:
                tag = word[tagIndex + 1 :]
            #tag = tag.lower()
            if tag not in posTagSequence:
                posTagSequence[tag] = {}
            if second not in posTagSequence[tag]:
                posTagSequence[tag][second] = {}
            if first not in posTagSequence[tag][second]:
                posTagSequence[tag][second][first] = 1
            else:
                posTagSequence[tag][second][first] += 1
            first = second
            second = tag
    return posTagSequence

def getBigramTagPosSequenceCount(lines):
    posTagSequence = {}
    for line in lines:
        words = line.split()
        words.insert(0, "<start>")
        words.append("<end>")
        prev = "<empty>"
        for word in words:
            tag = ""
            tagIndex = word.rfind('/')
            if tagIndex == -1:
                if word == "<start>":
                    tag = "<start>"
                elif word == "<end>":
                    tag = "<end>"
            else:
                tag = word[tagIndex + 1 :]
            #tag = tag.lower()
            if tag not in posTagSequence:
                posTagSequence[tag] = {}
            if prev not in posTagSequence[tag]:
                posTagSequence[tag][prev] = 1
            else:
                posTagSequence[tag][prev] += 1
            prev = tag
    return posTagSequence

def getWordTagMapAndTagCount(lines):
    wordTagCount = {}
    tagCount = {}
    for line in lines:
        words = line.split()
        for word in words:
            tagIndex = word.rfind('/')
            term = word[: tagIndex]
            tag = word[tagIndex + 1 :]
            if tag not in tagCount:
                tagCount[tag] = 1
            else:
                tagCount[tag] += 1
            #term = term.lower()
            if term not in wordTagCount:
                wordTagCount[term] = {}
                wordTagCount[term][tag] = 1
            else:
                if tag not in wordTagCount[term]:
                    wordTagCount[term][tag] = 1
                else:
                    wordTagCount[term][tag] += 1
    return wordTagCount, tagCount

def writeModelOutputFile(transitionProbability, emissionProbability, tagCount):
    file = open("hmmmodel.txt", "w", encoding="utf8")
    dumpDict = {'TransitionProbability': transitionProbability, 'EmissionProbability' : emissionProbability, 'TagCount': tagCount}
    file.write(json.dumps(dumpDict, indent=2))
    file.close()

def parseLinesInSentence(lines):
    tagCount = {}
    wordTagCount = {}
    posBigramSequenceCount = {}
    posTrigramSequenceCount = {}
    emissionProbability = {}
    transitionProbability = {}
    wordTagCount, tagCount = getWordTagMapAndTagCount(lines)
    posBigramSequenceCount = getBigramTagPosSequenceCount(lines)
    posTrigramSequenceCount = getTrigramTagPosSequenceCount(lines)
    emissionProbability = calculateEmissionProbability(wordTagCount, tagCount)
    transitionProbability = calculateTransitionProbability(posBigramSequenceCount, posTrigramSequenceCount, tagCount)
    writeModelOutputFile(transitionProbability, emissionProbability, tagCount)

def readDataFromInputFile(path):
    lines = []
    with open(path, 'r', encoding="utf8") as f:
        lines = f.readlines()
    parseLinesInSentence(lines)

def getTrainingDataFile():
    for root, directories, files in os.walk(sys.argv[1]):
        for file in files:
            if 'it_isdt_train_tagged' in file:
                readDataFromInputFile(os.path.join(root, file))

def main():
    #getTrainingDataFile()
    readDataFromInputFile(sys.argv[1])

if __name__ == "__main__":
    main()