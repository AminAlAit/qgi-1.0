import patternValidator as pv
import patternFinder    as pf
import dataPrep         as dp
import khartoush        as kh
import pandas           as pd
import numpy            as np
import viz


def pattsToDashDF(df):
    #"""
    #This function takes in a dataframe (df) and returns a dataframe (dashDF) with a summary of all patterns in the input
    #dataframe along with various indicators such as the countries involved in the pattern, the pattern length, the rank of
    #the pattern, the number of indicators and the indicators themselves, as well as dictionary containing the years of
    #pattern occurrence and the count of patterns for each year.
    #
    #Args:
    #df: a pandas dataframe containing patterns
    #
    #Returns:
    #dashDF: a pandas dataframe summarizing all patterns and indicators
    #"""

    # Display the start time of the function
    kh.displayTime(0)

    # Create an empty dataframe with the required columns
    dashDF = pd.DataFrame(columns = ["Country 1", "Country 2", "Years C1", "Years C2", "Pattern Length", "Rank", "Nb of Indicators", "Indicators", "C1 Stats Dictionary"])
    
    # Clean up the dataframe by converting string lists into actual lists and dropping unnamed columns
    df     = dp.recoverStringedListInDFCols(dp.unnamedCleanDF(df), [3, 4, 5, 6])

    # Iterate over unique patterns and unique countries involved in the patterns
    for patt in list(set(df["Pattern Length"])):
        for c1 in list(set(df["Pattern Country"])):
            dfC1 = df[(df["Pattern Country"] == c1)].reset_index(drop = True)

            pattIndRange = []
            for i in range(len(dfC1)):
                if dfC1["Pattern Index"][i][0] not in pattIndRange:
                    pattIndRange.append(int(dfC1["Pattern Index"][i][0]))

            pattIndRange       = sorted(list(set(pattIndRange)), key = abs, reverse = False)
            pattIndRangeCounts = [np.nan for i in range(len(pattIndRange))]

            for i in range(len(dfC1)):
                if (str(pattIndRangeCounts[pattIndRange.index(dfC1["Pattern Index"][i][0])]) == "nan"):
                    pattIndRangeCounts[pattIndRange.index(dfC1["Pattern Index"][i][0])] = 1
                else:
                    pattIndRangeCounts[pattIndRange.index(dfC1["Pattern Index"][i][0])] += 1

            dic = {
                "Years":          pattIndRange,
                patt + "-Pattern Counts": pattIndRangeCounts
            }

            for i in list(dfC1.index):
                Country1   = dfC1["Pattern Country"][i]
                Country2   = dfC1["Match Country"][i]
                Indicator  = dfC1["Index"][i]
                Years1     = dfC1["Pattern Index"][i]
                Years2     = dfC1["Match Index"][i]
                PatternLen = dfC1["Pattern Length"][i]
                Rank       = dfC1["Rank"][i]

                if PatternLen in list(dashDF["Pattern Length"]):
                    slicerDF = dashDF[(dashDF["Pattern Length"] == PatternLen)]
                    if Country1 in list(slicerDF["Country 1"]):
                        slicerDF = slicerDF[(slicerDF["Country 1"] == Country1)]
                        if Country2 in list(slicerDF["Country 2"]):
                            slicerDF = slicerDF[(slicerDF["Country 2"] == Country2)]
                            slicerDF = dp.stringCols(slicerDF, [2, 3])
                            if str(Years1) in list(slicerDF["Years C1"]):
                                slicerDF = slicerDF[(slicerDF["Years C1"] == str(Years1))]
                                if str(Years2) in list(slicerDF["Years C2"]):
                                    slicerDF = slicerDF[(slicerDF["Years C2"] == str(Years2))]
                                    slicerDF = dp.recoverStringedListInDFCols(slicerDF, [2, 3])
                                    if Indicator not in list(slicerDF["Indicators"])[0]:
                                        ind      = list(slicerDF.index)[0]
                                        tempList = dashDF.iloc[ind, 7]
                                        tempList.append(Indicator)
                                        dashDF.iloc[ind, 7] = tempList
                                        dashDF.iloc[ind, 6] = len(tempList)
                                    else:
                                        #print("1111111")
                                        print(slicerDF)
                                else:
                                    #print("222222222")
                                    dashDF.loc[len(dashDF.index)] = [Country1, Country2, Years1, Years2, PatternLen, Rank, 1, [Indicator], dic]
                            else:
                                #print("3333333333")
                                dashDF.loc[len(dashDF.index)] = [Country1, Country2, Years1, Years2, PatternLen, Rank, 1, [Indicator], dic]
                        else:
                            #print("444444444444444")
                            dashDF.loc[len(dashDF.index)] = [Country1, Country2, Years1, Years2, PatternLen, Rank, 1, [Indicator], dic]
                    else:
                        #print("55555555555")
                        dashDF.loc[len(dashDF.index)] = [Country1, Country2, Years1, Years2, PatternLen, Rank, 1, [Indicator], dic]

    dashDF = dashDF.sort_values(["Nb of Indicators", "Country 1", "Country 2"], ascending = [False, True, True]).reset_index(drop = True)
    dashDF.to_csv("DASH.csv")
    kh.displayTime(0)
    return dashDF

def findAllPatterns(path, dropCols, patternInterval, debug = False, fixYears = None):
    kh.displayTime(0)

    df = dp.getDF(path)

    ## DF grooming
    if fixYears is not None:
        df = dp.fixYears(df, fixYears)

    if len(dropCols) > 0:
        for colName in dropCols:
            df = df.drop(colName, axis = 1)

    ## Initializations
    countryNames  = dp.getCountyNames(df)
    indexes       = dp.getIndexes(df)

    patternCountry = []
    matchCountry   = []
    indexCol       = []
    patternValues  = []
    patternIndex   = []
    matchValues    = []
    matchIndex     = []
    rank           = []
    score          = []
    pearCorrScore  = []
    EucScore       = []
    MAPEScore      = []
    DTWScore       = []
    CBDScore       = []
    patternLength  = []

    dumpDF         = pd.DataFrame(columns = ["Country", "Index", "Pattern Length", "Values"])
    haveDump       = False

    for patt in patternInterval:
        for index in indexes:
            for country in countryNames:
                otherCountries = dp.getCountyNames(df)
                otherCountries.remove(country)
                for otherCountry in otherCountries:
                    res = findPattern2Countries(df, [country, otherCountry], index, patt, debug = False)
                    if(res[0]):
                        patternCountry.append(list(res[1])[0])
                        matchCountry.append(list(res[2])[0])
                        indexCol.append(index)
                        patternValues.append(list(res[1].iloc[:, 0]))
                        patternIndex.append(list(res[1].index))
                        matchValues.append(list(res[2].iloc[:, 0]))
                        matchIndex.append(list(res[2].index))
                        rank.append(res[3][1])
                        score.append(res[3][0])
                        pearCorrScore.append(res[3][2])
                        EucScore.append(res[3][3])
                        MAPEScore.append(res[3][4])
                        DTWScore.append(res[3][5])
                        CBDScore.append(res[3][6])
                        patternLength.append(patt)
                    else:
                        haveDump = True
                        #print("$$$$$$$ COULDN'T FIND PATTERN $$$$$$$")
                        #print("Not enough data")
                        if res[1] == 1:
                            if country not in list(dumpDF["Country"]):
                                print("C1:", country, "- Index:", index, "- PattLength:", patt)
                                print(list(res[2][list(res[2])[0]]))
                                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                                dumpDF.loc[len(dumpDF.index)] = [country, index, patt, list(res[2][list(res[2])[0]])]
                        elif res[1] == 2:
                            if otherCountry not in list(dumpDF["Country"]):
                                print("C2:", otherCountry, "- Index:", index, "- PattLength:", patt)
                                print(list(res[2][list(res[2])[0]]))
                                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                                dumpDF.loc[len(dumpDF.index)] = [otherCountry, index, patt, list(res[2][list(res[2])[0]])]

    allLists = [patternCountry,     matchCountry,   indexCol, patternValues,    patternIndex,    matchValues,    matchIndex,    rank,   score,   pearCorrScore,       EucScore,          MAPEScore,    DTWScore,    CBDScore,    patternLength]
    colNames = ["Pattern Country", "Match Country", "Index", "Pattern Values", "Pattern Index", "Match Values", "Match Index", "Rank", "Score", "Correlation Score", "Euclidean Score", "MAPE Score", "DTW Score", "CBD Score", "Pattern Length"]

    mainDF = pd.DataFrame()
    for i in range(len(allLists)):
        mainDF[colNames[i]] = allLists[i]
    
    mainDF.to_csv("DF.csv")
    kh.displayTime(1)

    if haveDump:
        dumpDF.to_csv("dumped.csv")
        return [mainDF, dumpDF]
    return mainDF

def findPattern2Countries(path, names, index, patternLen, interval = None, dropCols = None, debug = False):
    # Extracting 2 Country dataframes
    print("///////////////////")
    print(names)
    print(path)
    print(index)
    print(dropCols)
    print("///////////////////")
    df1, df2 = dp.return2CountriesDFs(path, names, index, dropCols)
    print(df1)
    print("----")
    print(df2)
    print("///////////////////")

    # Finding patterns 
    if (isinstance(interval, list)):
        res = recognizePattern2Countries(df1, df2, patternLen, interval = interval, debug = False)
    elif(interval is None):
        res = recognizePattern2Countries(df1, df2, patternLen, debug = False)
    
    if(res[0]):
        pattern = res[1]
        match   = res[2]

        # Validating patterns
        res = pv.validatePatterns(pattern, match)

        if (debug):
            print(pattern)
            print(match)
            print(res[1], "with score of", res[0])
            print("Pearson Correlation score:", res[2])
            print("Euclidean distance score:", res[3])
            print("MAPE distance score:", res[4])
            print("DTW score:", res[5])
            print("CBD score:", res[6])
        
        return [True, pattern, match, res]
    else:
        return [False, res[1], res[2]]

def recognizePattern2Countries(DF1, DF2, patternLength, interval = None, debug = False):
    """
    country1: [df1, name1, color1]
    country2: [df2, name2, color2]
    """
    
    res1 = dp.verdictOnNaNs(DF1, patternLength)
    res2 = dp.verdictOnNaNs(DF2, patternLength)

    print(list(DF1)[0], res1)
    print(list(DF2)[0], res2)

    if (res1 and res2):
        if interval is not None and len(interval) == 4:
            DF1["Year"] = DF1.index
            DF2["Year"] = DF2.index
            DF1 = DF1[DF1["Year"].between(interval[0], interval[1])] 
            DF2 = DF2[DF2["Year"].between(interval[2], interval[3])]
            DF1 = DF1.set_index("Year")
            DF2 = DF2.set_index("Year")
            print("Dataframes successfully cut according to passed intervals. ")
        elif interval is None or len(interval) == 0:
            DF1["Year"] = DF1.index
            DF2["Year"] = DF2.index
            DF1 = DF1.set_index("Year")
            DF2 = DF2.set_index("Year")

        # Finding the pattern and producing the matrix profile for country 1, as well as the values arrays (common patterns in)/for each country
        res                  = pf.findPattern(DF1, DF2, patternLength)
        country1_mp          = res[0]
        country1_motif_index = res[1]
        country2_motif_index = res[2]
        country1Arr          = res[3]
        country2Arr          = res[4]
        country1SEQ = []
        for i in country1Arr:
            country1SEQ.append(i[0])
        country2SEQ = []
        for i in country2Arr:
            country2SEQ.append(i[0])
        pattern, match       = pf.getMatchingDFs([country1SEQ, DF1], [country2SEQ, DF2], debug = debug)

        ## cosmetics
        #if (debug):
        #    plt.style.use('https://raw.githubusercontent.com/TDAmeritrade/stumpy/main/docs/stumpy.mplstyle')
        #    fig1 = viz.plot1([list(DF1.iloc[:, 0]), DF1, name1, alpha1, color1], [list(DF2.iloc[:, 0]), DF2, name2, alpha2, color2])
        #    fig2 = viz.plot2([DF1, alpha1, name1, color1], [DF2, alpha2, name2, color2], index_full)
        #    viz.text1(country1_mp, country1_motif_index)
        #    fig3 = viz.plot3(country1_motif_index, country1_mp)  
        #    viz.text2(country1_mp, name1, name2) 
        #    fig4 = viz.plot4([country1Arr, name1, color1], [country2Arr, name2, color2], index_full)
        #    fig5 = viz.plot5([pattern, alpha1, name1, color1], [match, alpha2, name2, color2], index_full)
        
        return [True, pattern, match]
    else:
        if(not res1):
            return [False, 1, DF1]
        elif(not res2):
            return [False, 2, DF2]