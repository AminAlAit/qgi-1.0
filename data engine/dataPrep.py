from itertools import groupby, islice
from datetime import datetime as dt
import pandas                 as pd
import numpy                  as np

#otherCountryDF = df[(df["Pattern Country"] == country_2) & (df["Match Country"] == country_1)]
#otherCountryIndex = list(otherCountryDF.index)[0]
#country_12        = otherCountryDF["Pattern Country"]

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

def trimNaNs(df):
    

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
                    data.append(list(nameDF[(nameDF["Year"] == years[i])][index])[0])
                else:
                    data.append(np.nan)
        else:
            data = list(df[(df["Country"] == name)][index])
    
    #for name in countryNamesList:
        dfs.append(pd.DataFrame(
            data    = data, #list(df[(df["Country"] == name)][index]), 
            index   = years, 
            columns = [name]))
    return dfs

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