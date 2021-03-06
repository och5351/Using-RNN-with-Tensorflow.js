import numpy as np
import re
from eunjeon import Mecab
import random

class MyUtil:
    m = Mecab()

    def to_Catgorical(self, x, i=0):
        result = 0
        if type(x) == dict:
            result = np.arange(len(x) * (len(x) + 1)).reshape(len(x), len(x) + 1)
            if i == 0:
                i = len(x) + 1
            for count in range(len(x)):
                for insertNum in range(i):
                    if insertNum == count + 1:
                        result[count][insertNum] = 1
                    else:
                        result[count][insertNum] = 0

        else:
            result = np.arange(len(x) * 10).reshape(len(x), 10)
            for k in range(len(x)):
                if i == 0:
                    i = x[k]

                for j in range(i):
                    if j == x[k]:
                        result[k][j] = 1
                    else:
                        result[k][j] = 0

        return result


    def BagOfWords(self, token):
        word2index = {}
        bow = []
        temp = []

        for voca in token:
            if voca not in word2index.keys():
                word2index[voca] = len(word2index) + 1
                # token을 읽으면서, word2index에 없는 (not in) 단어는 새로 추가하고, 이미 있는 단어는 넘깁니다.
                bow.insert(len(word2index) - 1, 1)
            # BoW 전체에 전부 기본값 1을 넣어줍니다. 단어의 개수는 최소 1개 이상이기 때문입니다.
            else:
                index = word2index.get(voca) - 1
                # 재등장하는 단어의 인덱스를 받아옵니다.
                bow[index] = bow[index] + 1
                # 재등장한 단어는 해당하는 인덱스의 위치에 1을 더해줍니다. (단어의 개수를 세는 것입니다.)

        return word2index, bow

    # 스탑워드 적용
    def stopWord(self, wordList, stopwordsList):

        for count in range(len(wordList)):
            if len(wordList) <= count:
                return wordList
            if stopwordsList.__contains__(wordList[count]):
                del wordList[count]

        return wordList


    def tf_idf(self, articleMemory, articleCount, words):

        tfidf = np.zeros(articleCount*len(words)).reshape(articleCount, len(words))

        for count in range(articleCount):
            for wordCount in range(len(words)):

                    tfidf[count][wordCount] = articleMemory[count].count(words[wordCount])

        documentCount = tfidf.shape[0]
        wordCount = tfidf.shape[1]


        for docCount in range(documentCount):
            for wCount in range(wordCount):
                if tfidf[docCount][wCount] != 0:
                    tfidf[docCount][wCount] = np.log(articleCount/(tfidf[docCount][wCount]+1))


        return tfidf

    def wordNormalization(self, x):
        result = []
        for count in range(len(x)):
            result.append(re.sub("(\.)", "", x[count]))
        return result

    def divideMorpheme(self,x):
        for count in range(len(x)):
            x[count] = self.m.morphs(x[count])
        return x

    def initWeight(self, x):
        tempW = np.random.normal(0, 1, x)
        tempW = np.expand_dims(tempW, axis=0)
        return tempW

    def gradient_descent(self, x, y, epoch, eta=0.01):
        b = 0
        w = self.initWeight(x.shape[1])
        for i in range(epoch):
            y_predict = np.sum(x[epoch] * w) + b
            # 크로스 엔트로피 손실 미분
            error = y[epoch] - y_predict

            w_diff = -(1 / len(x[epoch])) * sum(x[epoch] * error)
            b_diff = -(1 / len(x[epoch])) * sum(y - y_predict)
            w = w - eta * w_diff
            b = b - eta * b_diff

            print("예측 값 ")
            if i % 100 == 0:
                print("epoch = %.f error = %.f" % (i, error))

    def randomBox(self, x, y, randomFrequence):

        for count in range(randomFrequence):
            shake1 = random.randrange(0, len(x))
            shake2 = random.randrange(0, len(x))
            temp = x[shake1]
            x[shake1] = x[shake2]
            x[shake2] = temp
            temp = y[shake1]
            y[shake1] = y[shake2]
            y[shake2] = temp

        return x, y