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

    subseq = dp.stringedListToInt(subseq)
    seq    = dp.stringedListToInt(seq)

    firstItemNaN = 0
    while str(subseq[0]) == "nan" and str(seq[0]) == "nan":
        firstItemNaN += 1
        seq    = seq[1:]
        subseq = subseq[1:]

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
                if firstItemNaN > 0:
                    for _ in range(firstItemNaN):
                        seq.insert(0, np.nan)
                        subseq.insert(0, np.nan)
                
                return [True, commonIndexes]
            else:
                print("isin 3 continue")
                continue
        return [False, 3]

def findPattern(DF1, DF2, patternLength): #ignore_trivial = True
    """ """

    DF1 = dp.missingToNaNs(DF1, 0)
    DF2 = dp.missingToNaNs(DF2, 0)
    
    #DF1 = dp.removeNaNFromDF(DF1)
    #DF2 = dp.removeNaNFromDF(DF2)
    
    country1_mp = sp.stump(
        T_A            = DF1.iloc[:, 0].astype(float), 
        m              = patternLength, 
        T_B            = DF2.iloc[:, 0].astype(float), 
        ignore_trivial = False)
    
    
    country1_motif_index = country1_mp[:, 0].argmin() # index of the smallest value for country 1
    country2_motif_index = country1_mp[country1_motif_index, 1] # index of the smallest value for country 2

    patternFound = True
    if country1_motif_index == -1 or country2_motif_index == -1:
        patternFound = False

    country1Arr = DF1.iloc[country1_motif_index: country1_motif_index + patternLength].values
    country2Arr = DF2.iloc[country2_motif_index: country2_motif_index + patternLength].values
    
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
        print("PF3-----------------------")
        print("Pattern (subsequence) `country1[0]` (", list(country1[1])[0], ")")
        print(country1[0])
        print("PF4-----------------------")
        print("Country 1 DF (sequence) `country1[1]` (", list(country1[1])[0], ")")
        print(list(country1[1].iloc[:, 0]))
        print("PF5-----------------------")
        print("Match (subsequence) `country2[0]` (", list(country2[1])[0], ")")
        print(country2[0])
        print("PF6-----------------------")
        print("Country 2 DF (sequence) `country2[1]` (", list(country2[1])[0], ")")
        print(list(country2[1].iloc[:, 0]))
        print("PF7-----------------------")
    
    isinCountry1 = isin(country1[0], list(country1[1].iloc[:, 0]), debug)
    isinCountry2 = isin(country2[0], list(country2[1].iloc[:, 0]), debug)

    print("Pattern of country 1", list(country1[1])[0], "has its subsequence pattern matched with big sequence under the following indexes: ")
    print(isinCountry1)
    print("PF8-----------------------")
    print("Pattern of country 2", list(country2[1])[0], "has its subsequence pattern matched with big sequence under the following indexes: ")
    print(isinCountry2)
    print("PF9-----------------------")
    
    ## if subsequence 1 was found in sequence 1
    if (isinCountry1[0]):
        #print("Pattern from " + country1[2])
        pattern = country1[1].iloc[isinCountry1[1]]
        #print(pattern)
    ## else, the subsequence 1 was not found in the sequence 1
    else:
        print(list(country1[1].iloc[:, 0]))
        print(country1[0])
    
    ## if subsequence 2 was found in sequence 2
    if (isinCountry2[0]):
        #print("Best match with " + country2[2])
        #print(isinCountry2[1])
        #print(country2[3])
        match = country2[1].iloc[isinCountry2[1]]
        #print(match)
    ## else, subsequence 2 was not found in sequence 2
    else:
        print(list(country2[1].iloc[:, 0]))
        print(country2[0])
    
    return [pattern, match]