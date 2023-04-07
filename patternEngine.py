from  collections       import Counter
#import patternValidator as pv
#import countriesIndex   as ci
#import patternFinder    as pf
#import khartoush        as kh
import dataPrep         as dp
import pandas           as pd
import numpy            as np
import pickle
import viz
import os

countriesFolderPath   = "/workspace/qgi\\trojan\\countries patterns\\"
countriesPatternsPath = r"/workspace/qgi\trojan\countries patterns\\"
projectPath           = r"/workspace/qgi"
showcasePath          = r"/workspace/qgi\trojan\showcase\\"

def engine(patternize:   bool = True, filter:       bool = True, 
           refine:       bool = True, sortPatterns: bool = True, 
           showcaseCond: bool = True):
    
    if patternize:
        freshCutIndexes = dp.getFreshCutIndexes()
        for freshCutIndex in freshCutIndexes:
            res = patternizeThisIndex(indexPath = freshCutIndex)
            print("$$$$$$$$$$$ ", freshCutIndex.split("\\")[-1], " $$$$$$$$$$$")
            print("Duration: ", str(res[-1]))
            print("$$$$$$$$$$$ ", freshCutIndex.split("\\")[-1], " $$$$$$$$$$$")
    
    if filter:
        ## Country Filter
        # Creating individual dataframes (csv) for each country by taking their patterns from each patternized index
        patternized_indexes = []
        for root, dirs, files in os.walk(projectPath):
            for file in files:
                if file.endswith("Index_PATTERNS_DF.csv"):
                    patternized_indexes.append(os.path.join(root, file))

        for path in patternized_indexes:
            dp.countryFilter(pd.read_csv(path).drop("Unnamed: 0", axis = 1), countriesPatternsPath)

    if refine:
        ## Refining: creating individual dictionaries
        # Refining the separate country dataframes into dictionaries
        for country in os.listdir(countriesPatternsPath):
            country = country.split("_")[0]
            df      = pd.read_csv(countriesFolderPath + country + "_PATTERNS_DF.csv").drop("Unnamed: 0", axis = 1)

            countryDict = {}
            for pattLen in list(set(df["Pattern Length"])):
                pattIndexStarts  = list(set(df[df["Pattern Length"] == pattLen]["Pattern Index Start"]))
                countryDict[pattLen] = {}

                for pattIndexStart in pattIndexStarts:
                    dfTemp       = df[df["Pattern Length"] == pattLen]
                    dfTemp       = dfTemp[dfTemp["Pattern Index Start"] == pattIndexStart]
                    temp         = list(dfTemp["Match Country"])
                    countryCount = pd.DataFrame.from_dict(Counter(temp), orient = "index")
                    countryCount = countryCount[countryCount[list(countryCount)[0]] >= 2]
                    countryDict[pattLen][pattIndexStart] = {}

                    for countryMatch in list(countryCount.index):
                        countriesMatchDF = dfTemp[dfTemp["Match Country"] == countryMatch]
                        temp             = list(countriesMatchDF["Match Index Start"])
                        matchIndexStarts = pd.DataFrame.from_dict(Counter(temp), orient = "index")
                        matchIndexStarts = matchIndexStarts[matchIndexStarts[list(matchIndexStarts)[0]] >= 2]

                        for matchIndexStart in list(matchIndexStarts.index):
                            countriesMatchIndexStartDF = countriesMatchDF[countriesMatchDF["Match Index Start"] == matchIndexStart]
                            countryDict[pattLen][pattIndexStart][countryMatch] = countriesMatchIndexStartDF

            with open(countriesFolderPath + country + "_REFINED_DICT.pkl", "wb") as f:
                pickle.dump(countryDict, f)

    if sortPatterns:
        allSortedPatterns = dp.getAllSortedPatterns()

    if showcaseCond:
        showcase(allSortedPatterns)
    
    return allSortedPatterns

def showcase(
        allSortedPatterns: dict  = None, 
        minCorrelation:    float = 0.9, 
        patternLength:     int   = 6, 
        diffStarts:        bool  = True):
    
    if allSortedPatterns is None:
        return {}
    
    # The default patterns showcase are with 90% correlation, and pattern Index start != match index start, and pattern length >= 3
    allSortedPatternsDiffShowcase = dp.filterSortedPatternDict(
        sortedPatternsDict           = allSortedPatterns, 
        corrScore                    = minCorrelation, 
        pattLength                   = patternLength, 
        onlyDifferentPattIndexStarts = diffStarts)

    # saving the showcasing dataframe
    with open(showcasePath + "allSortedPatternsDiffShowcase.pkl", "wb") as f:
        pickle.dump(allSortedPatternsDiffShowcase, f)

    # saving the countries lists
    countries                = list(allSortedPatterns.keys())
    countriesShowcase        = list(allSortedPatternsDiffShowcase.keys())
    patternCountries         = []
    matchCountries           = []
    patternCountriesShowcase = []
    matchCountriesShowcase   = []

    for i in range(len(countries)):
        patternCountries.append(dp.removeNumbersFromString(countries[i].split("-")[0]))
        matchCountries.append(dp.removeNumbersFromString(countries[i].split("-")[-1]))
    patternCountries = list(set(patternCountries))
    matchCountries   = list(set(matchCountries))

    for i in range(len(countriesShowcase)):
        patternCountriesShowcase.append(dp.removeNumbersFromString(countriesShowcase[i].split("-")[0]))
        matchCountriesShowcase.append(dp.removeNumbersFromString(countriesShowcase[i].split("-")[-1]))
    patternCountriesShowcase = list(set(patternCountriesShowcase))
    matchCountriesShowcase   = list(set(matchCountriesShowcase))

    pd.DataFrame({"Pattern Countries":          patternCountries}).to_csv(showcasePath         + "patternCountries.csv")
    pd.DataFrame({"Match Countries":            matchCountries}).to_csv(showcasePath           + "matchCountries.csv")
    pd.DataFrame({"Pattern Countries Showcase": patternCountriesShowcase}).to_csv(showcasePath + "patternCountriesShowcase.csv")
    pd.DataFrame({"Pattern Countries Showcase": matchCountriesShowcase}).to_csv(showcasePath   + "matchCountriesShowcase.csv")

def patternizeThisIndex(indexPath: str, 
                        patternInterval: list = [3, 4, 5, 6, 7, 8, 9, 10], 
                        dropCols: list        = [], 
                        fixYears: list        = [".01", ".06"]):
    ci.countriesInit()
    outputPath = dp.getOutputDir(indexPath)
    res     = findAllPatterns(indexPath, outputPath, dropCols, patternInterval, fixYears = fixYears) 
    pattsDF = res[0]
    if len(res) > 1:
        dumpDF = res[1]
    
    return res

def pattsToDashDF(df):
    """
        This function takes in a dataframe (df) and returns a dataframe (dashDF) with a summary of all patterns in the input
        dataframe along with various indicators such as the countries involved in the pattern, the pattern length, the rank of
        the pattern, the number of indicators and the indicators themselves, as well as dictionary containing the years of
        pattern occurrence and the count of patterns for each year.
    
        Args:
            df: a pandas dataframe containing patterns
    
        Returns:
            dashDF: a pandas dataframe summarizing all patterns and indicators
    """

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

def findAllPatterns(path, outPath, dropCols, patternInterval, debug = False, fixYears = None):
    indexName = path.split("\\")[-1].split(".")[0]
    
    startTime = kh.displayTime(0)

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
                        print("$$$$$$$ COULDN'T FIND PATTERN $$$$$$$")
                        print("Not enough data")
                        
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
    
    mainDF.to_csv(outPath + indexName + "_PATTERNS_DF.csv")
    endTime = kh.displayTime(1)

    print("START TIME")
    print(startTime)
    print("END TIME")
    print(endTime)
    print("DIFFERENCE")
    print(endTime - startTime)

    if haveDump:
        dumpDF.to_csv(outPath + indexName + "_DUMPED_COUNTRIES.csv")
        return [mainDF, dumpDF, endTime - startTime]
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

    #print(list(DF1)[0], res1)
    #print(list(DF2)[0], res2)

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

        ## Pattern not found: Matrix Profile has 'inf' and '-1' values for country 1
        if len(country1Arr) == 0:
            return [False, 1, DF1]

        ## Pattern not found: Matrix Profile has 'inf' and '-1' values for country 2
        elif len(country2Arr) == 0:
            return [False, 2, DF2]

        ## Pattern found, get matching dataframes
        else:
            country1SEQ = []
            for i in country1Arr:
                country1SEQ.append(i[0])
            country2SEQ = []
            for i in country2Arr:
                country2SEQ.append(i[0])
            pattern, match = pf.getMatchingDFs([country1SEQ, DF1], [country2SEQ, DF2], debug = debug)
            return [True, pattern, match]
    
    else:
        if(not res1):
            return [False, 1, DF1]
        elif(not res2):
            return [False, 2, DF2]
