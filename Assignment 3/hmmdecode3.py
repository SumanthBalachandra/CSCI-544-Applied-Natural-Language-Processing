import os
import sys
import json

def writeOutputFile(taggedLines):
    file = open("hmmoutput.txt", "w", encoding="utf8")
    for line in taggedLines:
        file.write(line)
        file.write('\n')
    file.close()

def buildTaggedLines(backPointer, words, tagList):
    sentence = ""
    for i in range(len(words)):
        sentence += words[i] + "/" + tagList[i] + " "
    return sentence

def viterbi(transitionProbability, emissionProbability, possibleTags, lines):
    taggedLines = []
    for line in lines:
        tagList = []
        words = line.split()
        first = words[0]
        pi = {}
        pi[0] = {}
        pi[0]['<start>'] = {}
        backPointer = {}
        backPointer[0] = {}
        backPointer[0]['<start>'] = {}
        # For First word, w = '<empty>', u = '<start>', v = Possible tags for first word
        initialState = possibleTags
        if words[0] in emissionProbability.keys():
            initialState = list(emissionProbability[words[0]].keys())
        maxProbability = 0
        for v in initialState:
            if first in emissionProbability.keys():
                pi[0]['<start>'][v] = transitionProbability[v]['<start>']['<empty>'] * emissionProbability[first][v]
            else:
                pi[0]['<start>'][v] = transitionProbability[v]['<start>']['<empty>'] * 1
            if pi[0]['<start>'][v] > maxProbability:
                maxProbability = pi[0]['<start>'][v]
                backPointer[0]['<start>'][v] = '<empty>'
        second = ''
        if len(words) > 1 and len(words) > 2:
            second = words[1]
        else:
            tagList.append('_')
            tagList.append('_')
            taggedLines.append(buildTaggedLines(backPointer, words, tagList))
        pi[1] = {}
        maxProbability = 0
        backPointer[1] = {}
        for u in initialState:
            pi[1][u] = {}
            backPointer[1][u] = {}
            # For Second word, w = '<start>', u = Possible tags for first word, v = Possible tags for second word
            nextState = possibleTags
            if second in emissionProbability.keys():
                nextState = list(emissionProbability[second].keys())
            for v in nextState:
                if second in emissionProbability.keys():
                    pi[1][u][v] = pi[0]['<start>'][u] * transitionProbability[v][u]['<start>'] * emissionProbability[second][v]
                else:
                    pi[1][u][v] = pi[0]['<start>'][u] * transitionProbability[v][u]['<start>'] * 1
                if pi[1][u][v] > maxProbability:
                    maxProbability = pi[1][u][v]
                    backPointer[1][u][v] = '<start>'
        tagList = []
        for k in range(2, len(words)):
            vState = possibleTags
            uState = possibleTags
            wState = possibleTags
            if words[k - 2] in emissionProbability.keys():
                wState = list(emissionProbability[words[k - 2]].keys())
            if words[k - 1] in emissionProbability.keys():
                uState = list(emissionProbability[words[k - 1]].keys())
            if words[k] in emissionProbability.keys():
                vState = list(emissionProbability[words[k]].keys())
            if k not in pi:
                pi[k] = {}
                backPointer[k] = {}
            maxProbability = 0
            result = ''
            for v in vState:
                if v == '<start>' or v == '<end>':
                    continue
                for u in uState:
                    if u == '<start>' or u == '<end>':
                        continue
                    for w in wState:
                        if u not in pi[k]:
                            pi[k][u] = {}
                            backPointer[k][u] = {}
                        if v not in pi[k][u]:
                            pi[k][u][v] = {}
                            backPointer[k][u][v] = {}
                        if w == '<start>' or w == '<end>':
                            continue
                        if words[k] in emissionProbability.keys():
                            pi[k][u][v] = pi[k - 1][w][u] * transitionProbability[v][u][w] * emissionProbability[words[k]][v]
                        else:
                            pi[k][u][v] = pi[k - 1][w][u] * transitionProbability[v][u][w] * 1
                        if pi[k][u][v] > maxProbability:
                            maxProbability = pi[k][u][v]
                            backPointer[k][u][v] = w
                            result = w
            tagList.append(result)
        k = len(words)
        vState = possibleTags
        uState = possibleTags
        if words[k - 1] in emissionProbability.keys():
            vState = list(emissionProbability[words[k - 1]].keys())
        if words[k - 2] in emissionProbability.keys():
            uState = list(emissionProbability[words[k - 2]].keys())
        maxProbability = 0
        last = ''
        secondLast = ''
        if (k > 2):
            for v in vState:
                if v == '<start>' or v == '<end>' or v == '<empty>':
                    continue
                for u in uState:
                    if u == '<start>' or u == '<end>' or u == '<empty>':
                        continue
                    #print(u, v)
                    probability = pi[k - 1][u][v] * transitionProbability['<end>'][v][u]
                    if probability > maxProbability:
                        maxProbability = probability
                        last = v
                        secondLast = u
            tagList.append(secondLast)
            tagList.append(last)
            taggedLines.append(buildTaggedLines(backPointer, words, tagList))
    writeOutputFile(taggedLines)

def readDataFromInputFile():
    lines = []
    with open(sys.argv[1], 'r', encoding="utf8") as f:
        lines = f.readlines()
    return lines

def generateAllCombination(transitionProbability, possibleTags):
    for cur in possibleTags:
        if cur not in transitionProbability:
            transitionProbability[cur] = {}
        for prevOne in possibleTags:
            if prevOne not in transitionProbability[cur]:
                transitionProbability[cur][prevOne] = {}
            for prevTwo in possibleTags:
                if prevTwo not in transitionProbability[cur][prevOne]:
                    transitionProbability[cur][prevOne][prevTwo] = 1 / len(possibleTags)
    return transitionProbability

def generateWordCombination(emissionProbabilty, possibleTags):
    for word in emissionProbabilty:
        for tag in possibleTags:
            if tag not in emissionProbabilty[word]:
                emissionProbabilty[word][tag] = 0
    return emissionProbabilty

def readModelFile():
    jsonData = {}
    with open("hmmmodel.txt", "r", encoding="utf8") as f:
        jsonData = json.load(f)
    transitionProbability = jsonData['TransitionProbability']
    emissionProbability = jsonData['EmissionProbability']
    possibleTags = list(jsonData['TagCount'].keys())
    possibleTags.append('<start>')
    possibleTags.append('<end>')
    possibleTags.append('<empty>')
    transitionProbability = generateAllCombination(transitionProbability, possibleTags)
    return transitionProbability, emissionProbability, possibleTags

def main():
    transitionProbability = {}
    emissionProbability = {}
    possibleTags = []
    lines = []
    transitionProbability, emissionProbability, possibleTags = readModelFile()
    lines = readDataFromInputFile()
    viterbi(transitionProbability, emissionProbability, possibleTags, lines)

if __name__ == "__main__":
    main()