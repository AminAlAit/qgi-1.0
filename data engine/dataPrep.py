from itertools import groupby, islice
from datetime import datetime as dt
import matplotlib.pyplot      as plt
import pandas                 as pd
import numpy                  as np
import patternEngine          as pe
import platform
import pathlib
import pickle
import math
import ast
import os 

#otherCountryDF = df[(df["Pattern Country"] == country_2) & (df["Match Country"] == country_1)]
#otherCountryIndex = list(otherCountryDF.index)[0]
#country_12        = otherCountryDF["Pattern Country"]

countriesPatternsPath           = r"C:\Users\NEW\Desktop\Projects\FIFADash\trojan\countries patterns\\"
#countriesFolderPath             = r"C:\Users\Amin\Desktop\trojan\trojan\countries patterns\\"
countriesCSVPath                = r"C:\Users\NEW\Desktop\Projects\FIFADash\trojan\countries\countries.csv"
showcasePath                    = r"C:\Users\NEW\Desktop\Projects\FIFADash\trojan\showcase"
trojanPath                      = r"C:\Users\NEW\Desktop\Projects\FIFADash\trojan"
dataBankPath                    = r"C:\Users\NEW\Desktop\Projects\FIFADash\trojan\data bank"

stocker_indexes_path            = r"C:\Users\NEW\Desktop\Projects\FIFADash\trojan\stockers\index_stocker.csv"
checkersIndexPath               = r"C:\Users\NEW\Desktop\Projects\FIFADash\trojan\checkers\indexes.csv"

allSortedPatternsPickle         = r"C:\Users\Amin\Desktop\trojan\trojan\countries patterns\allSortedPatterns.pickle"
allSortedPatternsShowcasePickle = r"C:\Users\Amin\Desktop\trojan\trojan\showcase\allSortedPatternsShowcase.pkl"

SINGLE_SUB_VALIDATE_ESSENTIAL_COLS = ["Year", "Country"]
SIGNLE_SUB_VALIDATE_NB_ROWS        = 10
SINGLE_SUB_VALIDATE_NB_COLS        = 3

#################################################################
################# Index Candidates & Diagnosis ##################
#################################################################
def get_candidates_percentage():
    df      = get_index_stocker()
    Trues   = 0
    Falsies = 0
    NaNs    = 0
    labels  = ["Up to date", "Out of date", "Legacy"]

    for i in list(df["Patternized"]):
        if i == True:
            Trues += 1
        elif i == False:
            Falsies += 1
        elif math.isnan(i):
            NaNs += 1

    values = [Trues, Falsies, NaNs]
    colors = ['#8EB897', '#4F6272', '#DD7596']

    # Use it thanks to the color argument
    return plt.pie(values, labels = labels, labeldistance = 1.15, wedgeprops = {"linewidth" : 1, "edgecolor" : "white"}, colors = colors);


def get_index_stocker():
    return pd.read_csv(stocker_indexes_path).drop("Unnamed: 0", axis = 1)


def add_index_to_stocker(indexPath: str):
    df = pd.read_csv(stocker_indexes_path).drop("Unnamed: 0", axis = 1)
    if indexPath == "":
        return 0
    elif indexPath in list(df["Path"]):
        return 1
    else:
        df = pd.read_csv(stocker_indexes_path).drop("Unnamed: 0", axis = 1)
        indexes     = list(df["Index"])
        patternized = list(df["Patternized"])
        last_update = list(df["Last Updated"])
        paths       = list(df["Path"])

        indexes.append(indexPath.split("\\")[-1])
        patternized.append(False)
        last_update.append(get_modification_date(indexPath))
        paths.append(indexPath)
        
        new_index_stocker                 = pd.DataFrame()
        new_index_stocker["Index"]        = indexes
        new_index_stocker["Patternized"]  = patternized
        new_index_stocker["Last Updated"] = last_update
        new_index_stocker["Path"]         = paths
        new_index_stocker.to_csv(stocker_indexes_path)

        return new_index_stocker
    

def remove_index_from_stocker(indexName: str):
    df = pd.read_csv(stocker_indexes_path).drop("Unnamed: 0", axis = 1)
    if indexName == "":
        return 0
    elif indexName not in list(df["Index"]):
        return 1
    else:
        df = pd.read_csv(stocker_indexes_path).drop("Unnamed: 0", axis = 1)
        df = df[df["Index"] != indexName]
        df.to_csv(stocker_indexes_path)
        return df
    

def index_name_in_stocker(indexName: str):
    if indexName == "":
        return {}
    else:
        df = pd.read_csv(stocker_indexes_path).drop("Unnamed: 0", axis = 1)
        if indexName in list(df["Index"]):
            return True
        else:
            return False
        

def get_patternized_status_of_this_index(indexName: str):
    df = pd.read_csv(stocker_indexes_path).drop("Unnamed: 0", axis = 1)
    if indexName == "":
        return 0
    elif indexName not in list(df["Index"]):
        return 1
    else:
        return df.iloc[list(df["Index"]).index(indexName), 1]


def set_patternized_status_of_this_index(indexPath: str, status):
    df = pd.read_csv(stocker_indexes_path).drop("Unnamed: 0", axis = 1)
    if indexPath == "":
        return 0
    elif indexPath not in list(df["Path"]):
        return 1
    else:
        df.iloc[list(df["Path"]).index(indexPath), 1] = status
        df.to_csv(stocker_indexes_path)
        return df
    
def set_last_updated_datetime_of_this_index(indexPath: str, date_time):
    df = pd.read_csv(stocker_indexes_path).drop("Unnamed: 0", axis = 1)
    if indexPath == "":
        return 0
    elif indexPath not in list(df["Path"]):
        return 1
    else:
        df.iloc[list(df["Path"]).index(indexPath), 2] = date_time
        df.to_csv(stocker_indexes_path)
        return df


def get_last_update_stocker(indexName: str):
    df = pd.read_csv(stocker_indexes_path).drop("Unnamed: 0", axis = 1)
    if indexName == "":
        return 0
    elif indexName not in list(df["Index"]):
        return 1
    else:
        return df.iloc[list(df["Index"]).index(indexName), 2]


def get_path_of_this_index(indexName: str):
    df = pd.read_csv(stocker_indexes_path).drop("Unnamed: 0", axis = 1)
    if indexName == "":
        return 0
    elif indexName not in list(df["Index"]):
        return 1
    else:
        return df.iloc[list(df["Index"]).index(indexName), 3]


def get_creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    time = np.nan
    if platform.system() == "Windows":
        time = os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            time = stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            time = stat.st_mtime
    
    return dt.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")


def get_modification_date(path_to_file):
    """
    Try to get the date that a file was last modified.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    time = np.nan
    if platform.system() == "Windows":
        time = os.path.getmtime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            time = stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            time = stat.st_mtime
    
    return dt.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")


def get_uncommon_list_items(l1, l2):
    uncommon = []
    for i in l1:
        if i not in l2:
            uncommon.append(i)

    return uncommon


def check_two_list_equivalence(l1: list, l2: list):
    return set(l1) == set(l2)


def diagnose_indexes_between_stocker_and_fresh(stocker_indexes, fresh_indexes):
    new_in_stocker = get_uncommon_list_items(stocker_indexes, fresh_indexes)
    new_in_fresh   = get_uncommon_list_items(fresh_indexes, stocker_indexes)

    # We have new fresh indexes
    if len(new_in_fresh) > 0:
        for new_index in new_in_fresh:
            add_index_to_stocker(new_index)

    # We have new stocker index that are NOT in fresh: WE LOST INDEX PATHS, OR INDEX PATHS HAVE MOVED/BEEN EDITED
    if len(new_in_stocker) > 0:
        must_check_indexes = pd.DataFrame()
        must_check_indexes["Checker Index Path"] = new_in_stocker
        must_check_indexes.to_csv(checkersIndexPath)

        print("/////////////////////////////////////////////////")
        print("Caution: must check the status of these indexes: ")
        print(new_in_stocker)
        print("-----------")
        print("Check whether we lost their paths in the folders' structure of the data bank folder. They might have been moved or edited. ")
        print("/////////////////////////////////////////////////")


def get_candidate_indexes(run_index_path_diagnosis: bool = True):
    stocker_indexes = get_index_stocker()["Path"]
    fresh_indexes   = getFreshCutIndexes()

    # Running a quick diagnosis for both our index lists.
    if run_index_path_diagnosis:
        diagnose_indexes_between_stocker_and_fresh(stocker_indexes, fresh_indexes)

    # find index candidates based on patternized status and creation dates
    df         = get_index_stocker()
    candidates = []

    # Combnining them with paths of indexes who's been patternized but their stocker's last modification date is outdated 
    # with respect to fresh's list
    patternized_indexes = df[df["Patternized"] == True]
    for lu in range(len(list(patternized_indexes["Last Updated"]))):
        # Getting the last modification date as registered in index_stocker.csv
        stocker_index_date = patternized_indexes.iloc[lu, 2]
        
        # Getting the real last modification date of that same index
        fresh_index_date   = get_modification_date(patternized_indexes.iloc[lu, 3])
        
        # Checking if our indexes have been updated
        if stocker_index_date < fresh_index_date:
            # Setting the patternized status to False for each index that is out of date. 
            # That way we label it ready to be patternized
            set_patternized_status_of_this_index(patternized_indexes.iloc[lu, 3], False)
            print("Index '", patternized_indexes.iloc[lu, 3].split("\\")[-1], "' is outdated. ")
            print("Its 'patternized' status was set to False. ")

    # Getting paths of un-patternized indexes
    for j in list(df[df["Patternized"] != True]["Path"]):
        print("New index candidate found: '", j.split("\\")[-1], "'")
        candidates.append(j)

    return candidates

#################################################################
########################## Viz & EDA ############################
#################################################################
def getYearsRange(c1df: pd.DataFrame):

    """
    After filtering the main DashDF to select one country and one pattern length, input the resulting dataframe here to 
    get the full years range. 
    """
    
    min1, min2, max1, max2 = [None, None, None, None]
    for i in range(len(c1df)):
    
        if min1 is None:
            min1 = min(ast.literal_eval(list(c1df["Pattern Index"])[i]))
        else:
            min1 = min(min(ast.literal_eval(list(c1df["Pattern Index"])[i])), min1)

        if min2 is None:
            min2 = min(ast.literal_eval(list(c1df["Match Index"])[i]))
        else:
            min2 = min(min(ast.literal_eval(list(c1df["Match Index"])[i])), min2)

        if max1 is None:
            max1 = max(ast.literal_eval(list(c1df["Pattern Index"])[i]))
        else:
            max1 = max(max(ast.literal_eval(list(c1df["Pattern Index"])[i])), max1)

        if max2 is None:
            max2 = max(ast.literal_eval(list(c1df["Match Index"])[i]))
        else:
            max2 = max(max(ast.literal_eval(list(c1df["Match Index"])[i])), max2)

    return list(range(min(min1, min2), max(max1, max2) + 1))

def yearsAdjuster(years: list, patternLen: int, c1pattIndex: list, c1pattValues: list):
    """
    Takes into consideration the full years range when constructing each county's years' list, while it fills the other years, 
    where the pattern has no values in, with NaNs. 
    """

    j               = 0
    newC1pattValues = []
    
    for i in range(len(years)):
        if j < patternLen:
            if years[i] != c1pattIndex[j]:
                newC1pattValues.append(np.nan)
            else:
                newC1pattValues.append(c1pattValues[j])
                j += 1
        else:
            newC1pattValues.append(np.nan)
            
    return newC1pattValues

def C1DF(df: pd.DataFrame, country1: str, patternLen: int, corrScore: int = 1.0):
    c1df = df[df["Pattern Country"] == country1]

    if patternLen in list(set(c1df["Pattern Length"])):
        c1df = c1df[c1df["Pattern Length"] == patternLen]
        c1df = c1df[c1df["Correlation Score"] >= corrScore]
        return c1df
    
    else:
        return {}

def sortDFsInList(l: list, atLeastLength: int = 2):
    lengths = []
    for i in range(len(l)):
        lengths.append(len(l[i]))
    
    maxDFLength = max(lengths)

    sorted = []
    j      = 1
    while maxDFLength - j >= atLeastLength:
        for i in findListIndexes(lengths, maxDFLength - j):
            sorted.append(l[i])
        j += 1
    return sorted

#################################################################
########################### Pickles #############################
#################################################################

def openPickle(path):
    with open(path, "rb") as handle:
        return pickle.load(handle)

def getPatternPickles():
    if "C:\\" in str(pathlib.Path().resolve()):
        return [allSortedPatternsPickle, allSortedPatternsShowcasePickle]
    else:
        return [allSortedPatternsPickle.split("\\")[-1], allSortedPatternsShowcasePickle.split("\\")[-1]]

#################################################################
########################### Patterns ############################
#################################################################
def getAllSortedPatterns(atLeastLength: int = 2, pickleUp = True):
    countryMatches = []

    for refinedDict in os.listdir(countriesPatternsPath):
        if ".pkl" in refinedDict:
            countryName = refinedDict.split("_")[0]
            counryMatches = getCountryMatches(countryName = countryName)
            if counryMatches is not None:
                for i in counryMatches:
                    countryMatches.append(i)
    
    allSortedPatterns = sortDFsInList(countryMatches, atLeastLength)

    ## Transform the sorted list of pattern dataframes into a dictionary and return it
    if pickleUp:
        sortedPatternsDict = {}
        for i in range(len(allSortedPatterns)):
            country1Name       =  list(set(allSortedPatterns[i]["Pattern Country"]))[0]  
            country1PattStart  =  list(set(allSortedPatterns[i]["Pattern Index Start"]))[0]
            patternLength      =  list(set(allSortedPatterns[i]["Pattern Length"]))[0]
            country2Name       =  list(set(allSortedPatterns[i]["Match Country"]))[0]
            country2MatchStart =  list(set(allSortedPatterns[i]["Match Index Start"]))[0]

            dictItemName       =  country1Name + str(country1PattStart) 
            dictItemName       += "-"          + str(patternLength)      + "-"
            dictItemName       += country2Name + str(country2MatchStart)
            sortedPatternsDict[dictItemName] = allSortedPatterns[i]

        with open(showcasePath + "allSortedPatterns.pickle", "wb") as handle:
            pickle.dump(sortedPatternsDict, handle, protocol = pickle.HIGHEST_PROTOCOL)
        
        return sortedPatternsDict

    else:
        return allSortedPatterns

def getCountryMatches(countryName: str = None, pattStart: int = None, pattEnd:       int  = None, 
                      matStart:    int = None, matEnd:    int = None, atLeastLength: int = 2) -> list:

    """
    Filters the individual country Pickles.
    """

    if countryName is None:
        return "Please specify `countryName`. "

    with open(countriesPatternsPath + countryName + "_REFINED_DICT.pkl", "rb") as f:
        countryDict = pickle.load(f)
    
    if len(countryDict) > 0:
        dfs = []
        for pattLen in list(countryDict.keys()):
            for yearStart in list(countryDict[pattLen].keys()):
                for matchCountry in list(countryDict[pattLen][yearStart].keys()):
                    df = countryDict[pattLen][yearStart][matchCountry]
                    
                    if pattStart is not None:
                        df = df[df["Pattern Index Start"] == pattStart]
                    if pattEnd is not None:
                        df = df[df["Pattern Index End"] == pattEnd]
                    if matStart is not None:
                        df = df[df["Match Index Start"] == matStart]
                    if matEnd is not None:
                        df = df[df["Match Index End"] == matEnd]
                    dfs.append(df)
        if len(dfs) > 0:
            sortedDFs = sortDFsInList(dfs, atLeastLength)
            return sortedDFs
        else:
            return None
    else:
        return None

def filterSortedPatternDict(
        sortedPatternsDict: dict = None, corrScore:       float = None, pattLength:                   int  = None, 
        pattIndexStart:     int  = None, matchIndexStart: int   = None, onlyDifferentPattIndexStarts: bool = False):
    """
    Filtering the `allSortedPatterns.pickle`
    """
    
    if sortedPatternsDict is None:
        return "Please pass `sortedPatternsDict`. "

    filtered = {}
    for key, df in sortedPatternsDict.items():
        if corrScore is not None:
            df = df[df["Correlation Score"] >= corrScore]
        
        if pattLength is not None:
            df = df[df["Pattern Length"] >= pattLength]
        
        if pattIndexStart is not None:
            df = df[df["Pattern Index Start"] == pattIndexStart]
        
        if matchIndexStart is not None:
            df = df[df["Match Index Start"] == matchIndexStart]
        
        keepDF = True
        if onlyDifferentPattIndexStarts and len(df) > 0:
            if list(df["Pattern Index Start"])[0] == list(df["Match Index Start"])[0]:
                keepDF = False

        if len(df) > 0 and keepDF:
            filtered[key] = df
    
    allSortedPatternsDiff = {k: v for k, v in sorted(filtered.items(), key = lambda item: len(item[1]), reverse = True)}
    
    if onlyDifferentPattIndexStarts and len(df) > 0:
        with open(countriesPatternsPath + "allSortedPatternsDiff.pickle", "wb") as handle:
                pickle.dump(sortedPatternsDict, handle, protocol = pickle.HIGHEST_PROTOCOL)

    return allSortedPatternsDiff

def patternVsMatcheDF(df: pd.DataFrame) -> pd.DataFrame:
    country1   = list(df["Pattern Country"])[0]
    country2   = list(df["Match Country"])[0]
    patternLen = list(df["Pattern Length"])[0]

    # Getting the full years range
    years = getYearsRange(df)

    # listing the other countries next
    matchCountryIndexes = []
    matchCountryIndexes.append(years)

    # get column names
    colNames = []
    colNames.append("Years")

    # Getting the C1's full-years index values
    for i in range(len(df)):
        c1pattIndex  = ast.literal_eval(list(df["Pattern Index"])[i])
        c1pattValues = ast.literal_eval(list(df["Pattern Values"])[i])
        matchCountryIndexes.append(yearsAdjuster(years, patternLen, c1pattIndex, c1pattValues))

        c2pattIndex  = ast.literal_eval(list(df["Match Index"])[i])
        c2pattValues = ast.literal_eval(list(df["Match Values"])[i])
        matchCountryIndexes.append(yearsAdjuster(years, patternLen, c2pattIndex, c2pattValues))

        colNames.append(country1 + "-" + list(df["Index"])[i])
        colNames.append(country2 + "-" + list(df["Index"])[i])

    dfViz         = pd.DataFrame(matchCountryIndexes).T
    dfViz.columns = colNames
    return dfViz

def patternVsMatchesDF(c1df, country1, patternLen):
    """
    Returns dataframe that lists the chosen pattern country with the matching countries. 
    """

    # Getting the full years range
    years        = getYearsRange(c1df)

    # Getting the C1's full-years index values
    c1pattIndex  = ast.literal_eval(list(c1df["Pattern Index"])[0])
    c1pattValues = ast.literal_eval(list(c1df["Pattern Values"])[0])
    C1Vals       = yearsAdjuster(years, patternLen, c1pattIndex, c1pattValues)

    # listing the other countries next
    matchCountries = []
    matchCountries.append(years)
    matchCountries.append(C1Vals)

    for i in range(len(c1df)):
        c2pattIndex  = ast.literal_eval(list(c1df["Match Index"])[i])
        c2pattValues = ast.literal_eval(list(c1df["Match Values"])[i])
        matchCountries.append(yearsAdjuster(years, patternLen, c2pattIndex, c2pattValues))

    # get column names
    colNames = []
    colNames.append("Years")
    colNames.append(country1)
    for c2s in list(set(c1df["Match Country"])):
        colNames.append(c2s)
    colNames

    dfViz         = pd.DataFrame(matchCountries).T
    dfViz.columns = colNames
    
    return dfViz


#################################################################
######################### Converters ############################
#################################################################
def pickleToDF(pickledDict: dict = None):
    if pickledDict is None:
        return {}
    
    patternID, patternCountry, matchCountry, index, patternValues, patternIndex, matchValues, matchIndex, rank, score, correlationScore, euclideanScore, \
        MAPEScore, DTWScore, CBDScore, patternLength, patternIndexStart, patternIndexEnd, matchIndexStart, matchIndexEnd = [], [], [], [], [], [], [], \
        [], [], [], [], [], [], [], [], [], [], [], [], []

    id = 0
    for key, df in pickledDict.items():
        patternID         += [str(id) + "_" + key for i in range(len(df))]
        patternCountry    += list(df["Pattern Country"])
        matchCountry      += list(df["Match Country"])
        index             += list(df["Index"])
        patternValues     += list(df["Pattern Values"])
        patternIndex      += list(df["Pattern Index"])
        matchValues       += list(df["Match Values"])
        matchIndex        += list(df["Match Index"])
        rank              += list(df["Rank"])
        score             += list(df["Score"])
        correlationScore  += list(df["Correlation Score"])
        euclideanScore    += list(df["Euclidean Score"])
        MAPEScore         += list(df["MAPE Score"])
        DTWScore          += list(df["DTW Score"])
        CBDScore          += list(df["CBD Score"])
        patternLength     += list(df["Pattern Length"])
        patternIndexStart += list(df["Pattern Index Start"])
        patternIndexEnd   += list(df["Pattern Index End"])
        matchIndexStart   += list(df["Match Index Start"])
        matchIndexEnd     += list(df["Match Index End"])
        id                += 1

    df = pd.DataFrame()
    df["Pattern ID"]          = patternID
    df["Pattern Country"]     = patternCountry
    df["Match Country"]       = matchCountry
    df["Index"]               = index
    df["Pattern Values"]      = patternValues
    df["Pattern Index"]       = patternIndex
    df["Match Values"]        = matchValues
    df["Match Index"]         = matchIndex
    df["Rank"]                = rank
    df["Score"]               = score
    df["Correlation Score"]   = correlationScore
    df["Euclidean Score"]     = euclideanScore
    df["MAPE Score"]          = MAPEScore
    df["DTW Score"]           = DTWScore
    df["CBD Score"]           = CBDScore
    df["Pattern Length"]      = patternLength
    df["Pattern Index Start"] = patternIndexStart
    df["Pattern Index End"]   = patternIndexEnd
    df["Match Index Start"]   = matchIndexStart
    df["Match Index End"]     = matchIndexEnd

    return df

def patternsPickleToCSV():
    patternsDictPath, patternsShowcaseDictPath = getPatternPickles()

    patternsDict         = openPickle(patternsDictPath)
    patternsDF           = pickleToDF(patternsDict)
    patternsDF.to_csv(countriesPatternsPath + "allSortedPatterns.csv")

    patternsShowcaseDict = openPickle(patternsShowcaseDictPath)
    patternsShowcaseDF   = pickleToDF(patternsShowcaseDict)
    patternsShowcaseDF.to_csv(showcasePath + "allSortedPatternsShowcase.csv")
#################################################################
######################## Country Names ##########################
#################################################################
def fixCountryName(countryName):
    countries = pd.read_csv(countriesCSVPath).drop("Unnamed: 0", axis = 1)
    indexes   = getDFIndexesOfValue(countries, countryName)

    if len(indexes) > 0:
        for tuple in indexes:
            return countries.iloc[tuple[0], 0]

def getCountryNames() -> list:
    countryNamesList = []
    for country in os.listdir(countriesPatternsPath):
        if ".pkl" in country:
            countryNamesList.append(country.split("_")[0])
    return countryNamesList       

#################################################################
###################### Utility Functions ########################
#################################################################
def getDFIndexesOfValue(df, value):
    """ 
    Get index positions of value in dataframe. 
    """

    listOfPos = list()
    # Get bool dataframe with True at positions where the given value exists
    result = df.isin([value])
    # Get list of columns that contains the value
    seriesObj = result.any()
    columnNames = list(seriesObj[seriesObj == True].index)
    # Iterate over list of columns and fetch the rows indexes where value exists
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
        for row in rows:
            listOfPos.append((row, col))
    # Return a list of tuples indicating the positions of value in the dataframe
    return listOfPos

def findListIndexes(l: list, value) -> list:
    indexes = []
    for i in range(len(l)):
        if l[i] == value:
            indexes.append(i)
    return indexes

#################################################################
####################### Country Filter ##########################
#################################################################
def countryFilter(index_PATTERNS_csv: pd.DataFrame, output_dir: str) -> None:
    for country in list(set(index_PATTERNS_csv["Pattern Country"])):
        country = fixCountryName(country)
        
        if country + "_PATTERNS_DF.csv" in os.listdir(output_dir):
            new = False
        else:
            new = True
        
        dfTemp        = index_PATTERNS_csv[index_PATTERNS_csv["Pattern Country"] == country]
        dfTemp        = dfTemp.reset_index(drop = True)
        PattIndStart  = []
        PattIndEnd    = []
        MatchIndStart = []
        MatchIndEnd   = []

        for row in range(len(dfTemp)):
            PattIndStart.append(ast.literal_eval(dfTemp.iloc[row, 4])[0])
            PattIndEnd.append(ast.literal_eval(dfTemp.iloc[row, 4])[-1])
            MatchIndStart.append(ast.literal_eval(dfTemp.iloc[row, 6])[0])
            MatchIndEnd.append(ast.literal_eval(dfTemp.iloc[row, 6])[-1])

        dfTemp["Pattern Index Start"] = PattIndStart
        dfTemp["Pattern Index End"]   = PattIndEnd
        dfTemp["Match Index Start"]   = MatchIndStart
        dfTemp["Match Index End"]     = MatchIndEnd

        if new:
            dfTemp.to_csv(output_dir + country + "_PATTERNS_DF.csv")
        else:
            oldDF  = pd.read_csv(output_dir + country + "_PATTERNS_DF.csv").drop("Unnamed: 0", axis = 1)
            dfTemp = pd.concat([oldDF, dfTemp])
            dfTemp = dfTemp.drop_duplicates(keep = False)
            dfTemp.to_csv(output_dir + country + "_PATTERNS_DF.csv")

#################################################################
########################### Paths ###############################
#################################################################

def getPatternizedIndexPaths(projectPath: str = trojanPath) -> list:
    patternizedIndexes = []
    for root, dirs, files in os.walk(projectPath):
        for file in files:
            if file.endswith("Index_PATTERNS_DF.csv"):
                patternizedIndexes.append(os.path.join(root, file))
    return patternizedIndexes

def getFreshCutIndexes(dataBankPath: str = dataBankPath):
    freshCutIndexes = []
    for root, dirs, files in os.walk(dataBankPath):
        for file in files:
            ## Ignore every file that ends with 'PATTERNS_DF.csv'
            if not file.endswith("PATTERNS_DF.csv"): 
                ## Ignore every file that ends with 'DUMPED_COUNTRIES.csv'
                if not file.endswith("DUMPED_COUNTRIES.csv"):
                    ## Ignore all sources with "MAIN" in them
                    if not "MAIN" in os.path.join(root, file):
                        ## Ignore anyting from the directory "[SOURCES]"
                        if not "[SOURCES]" in os.path.join(root, file):
                            ## Making sure '.git', nor the files in it, is/are not included in the search
                            if not ".git" in os.path.join(root, file):
                                ## And file must end exclusively end with a '_SINGLE_SUB.csv'
                                if file.endswith("_SINGLE_SUB.csv"):
                                    ## Now we validate the single sub index in 4 simple steps
                                    df = pd.read_csv(str(os.path.join(root, file)))
                                    if SINGLE_SUB_VALIDATE_ESSENTIAL_COLS[0] in list(df):
                                        if SINGLE_SUB_VALIDATE_ESSENTIAL_COLS[1] in list(df):
                                            if len(list(df)) >= SINGLE_SUB_VALIDATE_NB_COLS:
                                                if len(df) >= SIGNLE_SUB_VALIDATE_NB_ROWS:
                                                    freshCutIndexes.append(os.path.join(root, file))

    return freshCutIndexes

def removeNumbersFromString(string: str) -> str:
    return ''.join([i for i in string if not i.isdigit()])

def getOutputDir(path: str):
    """
    For example, the function takes a string path like this:
        'C:\\Users\\Amin\Desktop\\trojan\\trojan\\Numbeo\\Cost of Living\\Cost of Living Index.csv'
    and returns this: 
        'C:\\Users\\Amin\Desktop\\trojan\\trojan\\Numbeo\\Cost of Living\\'
    """

    outp = ""
    for i in path.split("\\")[:-1]:
        outp += i + "\\"
    
    return outp

#################################################################
#################################################################
#################################################################

def mergeDFs(dfsList, refCols):
    df = dfsList[0].merge(dfsList[1], on = refCols, how = "outer")
    if (len(dfsList) > 2):
        for i in range(2, len(dfsList)):
            df = df.merge(dfsList[i], on = refCols, how = "outer")
    return df.sort_values(by = refCols, ascending = True).reset_index(drop = True)

def mergeCSVs(CSVNamesList, url, ext, mergeCols):
    for dfname in CSVNamesList:
        if dfname == CSVNamesList[0]:
            df = pd.read_csv(url + dfname + ext)
        else:
            df = df.merge(pd.read_csv(url + dfname + ext), on = mergeCols, how = "outer")
    return df

def strToDateTime(strObj, format, dateOrTime, NAN):
    """
    Call this function when iterating over the values of a date or a time column 
    to convert (and return) them from string values to time/date values.
    Params: 
        'strObj':     the column string value
        'format':     "%Y.%m.%d" or "%Y-%m-%d" or "%Y/%m/%d" or "%H:%M:%S"
        'dateOrTime': "date" or "time"
        'NAN':        usually 'nan' or 'no time' or 'na' or 'N/A' etc...
    """ 
    if str(strObj) == NAN:
        return np.nan
    elif dateOrTime.lower() == "date":
        return dt.strptime(strObj, format).date()
    elif dateOrTime.lower() == "time":
        return dt.strptime(strObj, format).time()

def dashToNAN(df):
    for j in list(df):
        df[j] = df[j].replace({"b": np.nan})
    return df

def fillUpOnYears(df):
    years       = list(df.index)
    dfVals      = list(df[list(df)[0]])
    filledYears = list(range(years[0], years[len(years) - 1]  + 1))
    vals        = []
    i           = 0
    for j in range(len(filledYears)):
        if filledYears[j] == years[i]:
            vals.append(dfVals[i])
            i += 1
        else:
            vals.append(np.nan)

    df = pd.DataFrame({list(df)[0]: vals,"Year": filledYears})
    return df.set_index("Year", inplace = True)

#def trimNaNs(df):

def return2CountriesDFs(path, countryNamesList, index, dropCols = None):
    if (not isinstance(path, pd.DataFrame)):
        df = pd.read_csv(path)
    else:
        df = path

    if (isinstance(dropCols, list)):
        for colName in dropCols:
            df = df.drop(colName, axis = 1)

    dfs        = []
    years      = np.array(sorted(list(set(df["Year"])), key = abs, reverse = False))
    years      = [int(y) for y in years]
    data2years = list(df[(df["Country"] == countryNamesList[1])]["Year"])
    data2years = [int(y) for y in data2years]

    for name in countryNamesList:
        if len(df[(df["Country"] == name)].index) < len(years):
            data = []
            dataYears = np.array(sorted(list(set(df[(df["Country"] == name)]["Year"])), key = abs, reverse = False))
            dataYears = [int(y) for y in dataYears]
            for i in range(len(years)):
                if years[i] in dataYears:
                    nameDF = stringedYearColToInt(df[(df["Country"] == name)])
                    #print("$$$$$$$$$")
                    #print(list(nameDF[(nameDF["Year"] == years[i])][index])[0])
                    #print("$$$$$$$$$")
                    data.append(list(nameDF[(nameDF["Year"] == years[i])][index])[0])
                else:
                    data.append(np.nan)
        else:
            #print("£££££££££££")
            #print(list(df[(df["Country"] == name)][index]))
            #print("£££££££££££")
            data = list(df[(df["Country"] == name)][index])

        #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        #print(countryNamesList)
        #print(data)
        #print(len(data))
        #print(years)
        #print(len(years))
        #print(name)
        #print(pd.DataFrame(data = data, index = years, columns = [name]))
        #print("----")
        #print(dfs)
        #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    #for name in countryNamesList:
        dfs.append(pd.DataFrame(
            data    = data, #list(df[(df["Country"] == name)][index]), 
            index   = years, 
            columns = [name]))
    return dfs

def zeroesListToCloseToZero(l: list) -> list:
    for index in range(len(l)):
        if l[index] == 0 or l[index] == 0.0 or l[index] == "0" or l[index] == "0.0":
            l[index] = 0.00000000001
    return l

def stringedListToInt(l: list) -> list:
    for i in range(len(l)):
        if isinstance(l[i], str):
            l[i] = float(l[i])
        elif isinstance(l[i], float) and str(l[i]) in ["nan", "N/A", "NaN", "NA", np.nan]:
            l[i] = np.nan
    return l

def verdictOnNaNs(DF, patternLength):
    ValuesBinary = []
    for i in list(DF[list(DF)[0]]):
        if str(i) == "nan":
            ValuesBinary.append(False)
        else:
            ValuesBinary.append(True)
    
    dec = any(sum(1 for _ in islice(g, patternLength)) == patternLength for k, g in groupby(ValuesBinary) if k)
    if False:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(list(DF)[0])
        print(list(DF[list(DF)[0]]))
        print(ValuesBinary)
        print("Decision: ", dec)
    return dec

def missingToNaNs(df, colIndex):
    missingTypes = ["-", "nan", np.nan, " ", "na", "", "n/a"]
    for i in range(len(df.iloc[:, colIndex])):
        if str(df.iloc[i, colIndex]) in missingTypes or df.iloc[i, colIndex] in missingTypes:
            df.iloc[i, colIndex] = np.nan
    return df

def cleanList(l):
    for i in range(len(l)):
        if l[i] in ["-", "nan", np.nan, " ", "na", "", "n/a"]:
            l[i] = np.nan
        elif(isinstance(l[i], str)):
            l[i] = float(i)
    return l

def removeNaNFromDF(df):
    return df[df[list(df)[0]].notna()]

def cleanRemoveNaNs(l1, l2):
    l1         = cleanList(l1)
    l2         = cleanList(l2)
    nanIndexes = []
    for i in range(len(l1)):
        if l1[i] in ["-", "nan", np.nan, " ", "na", "", "n/a"]:
            nanIndexes.append(i)
        if l2[i] in ["-", "nan", np.nan, " ", "na", "", "n/a"]:
            nanIndexes.append(i)
    for i in nanIndexes:
        del l1[i]
        del l2[i]
    return [l1, l2]

def lift(l1, l2):
    if np.nan in l1:
        temp1 = l1
        min1  = min(temp1.remove(np.nan))
    elif "nan" in l1:
        temp1 = l1
        min1  = min(temp1.remove("nan"))
    else:
        min1  = min(l1)
  
    if np.nan in l1:
        temp2 = l2
        min2  = min(temp2.remove(np.nan))
    elif "nan" in l2:
        temp2 = l2
        min2  = min(temp2.remove("nan"))
    else:
        min2 = min(l2)
  
    if min1 < min2:
        for i in range(len(l1)):
            l1[i] += abs(min1)
        for j in range(len(l2)):
            l2[j] += abs(min1)
    else:
        for i in range(len(l1)):
            l1[i] += abs(min2)
        for j in range(len(l2)):
            l2[j] += abs(min2)
    return [l1, l2]

def stringedYearColToInt(df):
    colNames   = list(df)
    yearCol    = list(df["Year"])
    yearCol    = [int(y) for y in yearCol]
    df         = df.drop("Year", axis = 1)
    df["Year"] = yearCol
    return df[colNames]

def fixYears(df, fixYears):
    for i in range(len(df.index)):
        if fixYears[1] in str(df["Year"][i]):
            df = df.drop(index = i)
    for i in list(df.index):
        if fixYears[0] in str(df["Year"][i]):
            df["Year"][i] = int(str(df["Year"][i]).replace(fixYears[0], ""))
    return df

def dfToDashDF(df):
    mainDF   = pd.DataFrame()
    country1 = []
    country2 = []
    platinum = []
    gold     = []
    silver   = []
    bronze   = []
    dfs      = []

    for patt in list(set(df["Pattern Length"])):
        dfs.append(df[(df["Pattern Length"] == patt)])
    
    return dfs

def unnamedCleanDF(df):
    for name in list(df):
        if "Unnamed" in name:
            df = df.drop(name, axis = 1)
    return df

def stringListToList(s):
    s = s.split(",")
    for i in range(len(s)):
        s[i] = s[i].replace(" ", "")
        s[i] = s[i].replace("[", "")
        s[i] = s[i].replace("]", "")
        s[i] = float(s[i])
    return s

def unnamedCleanDF(df):
    for name in list(df):
        if "Unnamed" in name:
            df = df.drop(name, axis = 1)
    return df

def recoverStringedListInDFCols(df, colIndexes):
    df = unnamedCleanDF(df)
    colNames = list(df)
    for col in colIndexes:
        temp = []
        for i in range(len(df.index)):  
            temp.append(stringListToList(df.iloc[i, col]))
        df = df.drop(colNames[col], axis = 1)
        df[colNames[col]] = temp
        df = df.reindex(colNames, axis = 1)
    return df

def stringCols(df, colIndexes):
    for i in range(len(df.index)):
        for col in colIndexes:
            df.iloc[i, col] = str(df.iloc[i, col])
    return df

def getCountyNames(df):
    return sorted(list(set(df["Country"])), reverse = False)

def getDF(path):
    return pd.read_csv(path)

def getIndexes(df):
    indexes = list(df)
    indexes.remove("Country")
    indexes.remove("Year")
    return indexes