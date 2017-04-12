import pandas as pd
import itertools
import math
from collections import defaultdict, OrderedDict
import sys

import collections

l1=sys.argv
print l1

# fileP = open("/home/kgodse/PycharmProjects/DataMining/ratings-dataset.tsv","rU")
fileP = open(l1[1],'r')
temp = [r.split('\t')  for r in fileP.read().split('\n')]
# print temp

userid = []
for i in range(0, len(temp)-1):
    userid.append(temp[i][0])
userid=list(set(userid))
# print userid

movienames = []
for i in range(0, len(temp)-1):
    movienames.append(temp[i][2])
movienames=list(set(movienames))
# print movienames

ratings = []
for i in range(0, len(temp)-1):
    ratings.append(temp[i][2])
# print ratings

pd.set_option('display.width',1000)

# s = pd.Series(ratings)

uMatrix = pd.DataFrame(index=userid, columns=movienames)
# df = df.fillna(s)


for j in temp:
    uMatrix[j[2]][j[0]]=float(j[1])
    # print j[2]
#uMatrix = uMatrix.fillna(0)
# print uMatrix

# avg = dict()
# avg = \


# ----------------------------------------Adding new avg column------------------------------------------
# sLength = len(df1['a'])
# df1.loc[:,'f'] = p.Series(np.random.randn(sLength), index=df1.index)
# for i in uMatrix:
#     uMatrix[i]
cMatrix = uMatrix.copy()
cMatrix['Average'] = cMatrix.mean(axis=1)

def pearson(user1,user2):

    U1list = []
    U2list = []


    for i in movienames:
        if not math.isnan(uMatrix[i][user1]):
            U1list.append(i)
    for i in movienames:
        if not math.isnan(uMatrix[i][user2]):
            U2list.append(i)

    commonMovies=set(U1list).intersection(set(U2list))
    tUtility = uMatrix.loc[[user1,user2],commonMovies]
    tUtility['Average'] = tUtility.mean(axis=1)
    uMatrix1 = pd.DataFrame(index=[user1,user2], columns=commonMovies)
    # print tUtility
    for x in [user1,user2]:
        for y in commonMovies:
            uMatrix1[y][x] = tUtility[y][x] - tUtility['Average'][x]
    # print uMatrix1
    # ----------------------------------For denominator--------------------------------------------------------------
    summ1 = 0
    summ2 = 0
    # print user1
    # print user2
    for i in commonMovies:

        if not math.isnan(uMatrix1[i][user1]) and not math.isnan(uMatrix1[i][user2]):
            # print uMatrix1[i][user2]**2
            summ1 = summ1 + uMatrix1[i][user1]**2
            summ2 = summ2 + uMatrix1[i][user2]**2
    u1 = math.sqrt(summ1)
    u2 = math.sqrt(summ2)
    # print u1
    # print u2
    # print "this"
    denm = u1*u2
    # ----------------------------------For Numerator--------------------------------------------------------------
    Num = 0
    for i in commonMovies:

        if not math.isnan(uMatrix1[i][user1]) and not math.isnan(uMatrix1[i][user2]):
            # print uMatrix1[i][user2]**2
            r1 = uMatrix1[i][user1]
            r2 = uMatrix1[i][user2]
            multi = r1 * r2
            Num = Num + multi

    P = float(Num)/float(denm)
# PearsonDict += P

    return P


user1 = l1[2]
item = l1[3]
K = int(l1[4])

def k_N(user1,item,K):
    PearsonDict = defaultdict(lambda: 0)
    tempDict={}
    for j in userid:
        if user1 not in j:
            PearsonDict[j]=pearson(user1,j)

    # PearsonDict = itertools.islice(PearsonDict, K)
    # PearsonDict = PearsonDict()
    for u in PearsonDict.keys():
        if not math.isnan(uMatrix[item][u]):
            tempDict[u] = PearsonDict[u]

    sortOD = collections.OrderedDict(sorted(tempDict.items()))
    tempDict = sorted(sortOD.items(), key=lambda kv: kv[1], reverse=True)
    for k in tempDict[0:K]:
        print k[0] + ' ' + str(k[1])
    return tempDict[0:K]


def Predict(user1, item, k_nearest_neighbours):
    tempDict = {}
    tdict=dict(k_nearest_neighbours)
    U1list = []


    for i in movienames:
        if not math.isnan(uMatrix[i][user1]):
            U1list.append(i)

    # for u in tdict.keys():
    #     if not math.isnan(uMatrix[item][u]):
    tempDict=dict(k_nearest_neighbours)

    N = 0
    D=0
    sumTemp1 = 0
    for usr in tempDict.keys():
        count = 0
        sumTemp = 0
        avg = 0
        U2list = []
        for i in movienames:
            if not math.isnan(uMatrix[i][usr]):
                U2list.append(i)

        commonMovies=set(U1list).intersection(set(U2list))
        for x in commonMovies:
            count +=1
            sumTemp += uMatrix[x][usr]

        avg = sumTemp/count

        N += (uMatrix[item][usr]-avg) * tempDict[usr]
        D += abs(tempDict[usr])

    return uMatrix.mean(axis=1)[user1]+(N/D)

# item='The Fugitive'
a=k_N(user1,item,K)

print Predict(user1,item,a)