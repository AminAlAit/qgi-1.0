import matplotlib.pyplot as plt
import matplotlib        as plt
import dataPrep          as dp
import stumpy            as sp
import numpy             as np

def isin(subseq, seq, debug = False):
    """
    Checks if subseq is in seq, if not, returns [False], if so, returns 
    [True, [4, 5, 6]], such that [4, 5, 6] are example indexes of where
    the subseq is in seq. 
    """
    if subseq[0] not in seq:
        return [False, 1] #first item in subseq does not exist in seq
    elif(seq.index(subseq[0]) + len(subseq) > len(seq)):
        return [False, 2] #subseq's first element does exist in seq, but seq does not contain all of the subseq
    else:
        firstInd = []
        for i in range(len(seq)):
            if seq[i] is not np.nan or seq[i] != "nan":
                if seq[i] == subseq[0]:
                    firstInd.append(i)
        if(len(firstInd) >= 2 and debug):
            print("First value of the subseq was found in multiple indexes of the full seq: ", firstInd)
        for k in firstInd:
            seqIndex      = k
            j             = 0
            commonIndexes = []
            for i in range(k, k + len(subseq)):
                if (seq[i] == subseq[j]):
                    commonIndexes.append(seqIndex)
                    j        += 1
                    seqIndex += 1
            if(len(commonIndexes) == len(subseq)):
                return [True, commonIndexes]
            else:
                continue
        return [False, 3]

def findPattern(DF1, DF2, patternLength): #ignore_trivial = True
    """
    """
    DF1 = dp.missingToNaNs(DF1, 0)
    DF2 = dp.missingToNaNs(DF2, 0)
    
    #DF1 = dp.removeNaNFromDF(DF1)
    #DF2 = dp.removeNaNFromDF(DF2)
    
    country1_mp = sp.stump(
        T_A            = DF1.iloc[:, 0].astype(float), 
        m              = patternLength, 
        T_B            = DF2.iloc[:, 0].astype(float), 
        ignore_trivial = False)
    
    country1_motif_index = country1_mp[:, 0].argmin()
    country1_motif_index = country1_mp[:, 0].argmin()
    country2_motif_index = country1_mp[country1_motif_index, 1]
    country1Arr          = DF1.iloc[country1_motif_index: country1_motif_index + patternLength].values
    country2Arr          = DF2.iloc[country2_motif_index: country2_motif_index + patternLength].values

    return [country1_mp, country1_motif_index, country2_motif_index, country1Arr, country2Arr]

def getMatchingDFs(country1, country2, debug = False):
    """
    country1: [country1Arr, DF1]
    country2: [country2Arr, DF2]
    """

    #country1SEQ = []
    #for i in country1[0]:
    #    country1SEQ.append(i[0])
    #country2SEQ = []
    #for i in country2[0]:
    #    country2SEQ.append(i[0])
    
    if True:
        print("-----")
        print("Pattern `country1[0]`")
        print(country1[0])
        print("-----")
        print("Country 1 DF `country1[1]`")
        print(country1[1])
        print(list(country1[1].iloc[:, 0]))
        print("--------------")
        print("Match `country2[0]`")
        print(country2[0])
        print("-----")
        print("Country 2 DF `country2[1]`")
        print(country2[1])
        print(list(country2[1].iloc[:, 0]))
        print("###########################")
    
    isinCountry1 = isin(country1[0], list(country1[1].iloc[:, 0]), debug)
    isinCountry2 = isin(country2[0], list(country2[1].iloc[:, 0]), debug)

    if (isinCountry1[0]):
        #print("Pattern from " + country1[2])
        pattern = country1[1].iloc[isinCountry1[1]]
        #print(pattern)
    else:
        print(list(country1[1].iloc[:, 0]))
        print(country1[0])
    #print("-----------")
    if (isinCountry2[0]):
        #print("Best match with " + country2[2])
        #print(isinCountry2[1])
        #print(country2[3])
        match = country2[1].iloc[isinCountry2[1]]
        #print(match)
    return [pattern, match]