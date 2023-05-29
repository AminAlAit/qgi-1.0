from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype)
import pandas     as pd
import numpy      as np
import streamlit  as st
import subprocess
import pathlib
import pickle
import ast
import sys

patternCountries         = r"/workspace/qgi\trojan\showcase\patternCountries.csv"
matchCountries           = r"/workspace/qgi\trojan\showcase\matchCountries.csv"
patternCountriesShowcase = r"/workspace/qgi\trojan\showcase\patternCountriesShowcase.csv"
matchCountriesShowcase   = r"/workspace/qgi\trojan\showcase\matchCountriesShowcase.csv"

def getPatternDFs():
    if "C:\\" in str(pathlib.Path().resolve()):
        paths = [r"/workspace/qgi\trojan\countries patterns\allSortedPatterns.csv", r"/workspace/qgi\trojan\showcase\allSortedPatternsShowcase.csv"]
    else:
        paths = ["allSortedPatterns.csv", "allSortedPatternsShowcase.csv"]

    return [pd.read_csv(paths[0]).drop("Unnamed: 0", axis = 1), pd.read_csv(paths[1]).drop("Unnamed: 0", axis = 1)]


def filter_all_patterns_df(
    patterns_df:         pd.DataFrame, 
    pattern_id:          str   = None,
    pattern_country:     str   = None, 
    match_country:       str   = None,
    index:               str   = None,
    rank:                str   = None,
    score:               float = None,
    corr:                float = None,
    euc:                 float = None,
    mape:                float = None,
    dtw:                 float = None,
    cbd:                 float = None,
    pattern_length:      int   = None,
    pattern_index_start: int   = None,
    pattern_index_end:   int   = None,
    match_index_start:   int   = None,
    match_index_end:     int   = None) -> pd.DataFrame:
    
    ## Pattern ID
    if pattern_id is not None:
        patterns_df = patterns_df[(patterns_df["Pattern ID"] == pattern_id)]

    ## Countries 1 and 2
    if pattern_country is not None:
        patterns_df = patterns_df[(patterns_df["Pattern Country"] == pattern_country)]

    if match_country is not None:
        patterns_df = patterns_df[(patterns_df["Match Country"] == match_country)]

    ## Index
    if index is not None:
        patterns_df = patterns_df[(patterns_df["Index"] == index)]

    ## Scores
    if rank is not None:
        patterns_df = patterns_df[(patterns_df["Rank"] == rank)]
    
    if score is not None:
        patterns_df = patterns_df[(patterns_df["Score"] >= score)]

    if corr is not None:
        patterns_df = patterns_df[(patterns_df["Correlation Score"] >= corr)]

    if euc is not None:
        patterns_df = patterns_df[(patterns_df["Euclidean Score"] <= euc)]

    if mape is not None:
        patterns_df = patterns_df[(patterns_df["MAPE Score"] <= mape)]

    if dtw is not None:
        patterns_df = patterns_df[(patterns_df["DTW Score"] <= dtw)]

    if cbd is not None:
        patterns_df = patterns_df[(patterns_df["CBD Score"] <= cbd)]

    ## Pattern Length
    if pattern_length is not None:
        patterns_df = patterns_df[(patterns_df["Pattern Length"] == pattern_length)]

    ## Starts and Ends
    if pattern_index_start is not None:
        patterns_df = patterns_df[(patterns_df["Pattern Index Start"] == pattern_index_start)]

    if pattern_index_end is not None:
        patterns_df = patterns_df[(patterns_df["Pattern Index End"] == pattern_index_end)]

    if match_index_start is not None:
        patterns_df = patterns_df[(patterns_df["Match Index Start"] == match_index_start)]

    if match_index_end is not None:
        patterns_df = patterns_df[(patterns_df["Match Index End"] == match_index_end)]

    return patterns_df


def getPatternDFs():
    if "C:\\" in str(pathlib.Path().resolve()):
        paths = [r"/workspace/qgi\trojan\countries patterns\allSortedPatterns.csv", r"/workspace/qgi\trojan\showcase\allSortedPatternsShowcase.csv"]
    else:
        paths = ["allSortedPatterns.csv", "allSortedPatternsShowcase.csv"]

    return [pd.read_csv(paths[0]).drop("Unnamed: 0", axis = 1), pd.read_csv(paths[1]).drop("Unnamed: 0", axis = 1)]


def getPatternCSVs():
    if "C:\\" in str(pathlib.Path().resolve()):
        return [r"/workspace/qgi\trojan\countries patterns\allSortedPatterns.csv", r"/workspace/qgi\trojan\showcase\allSortedPatternsShowcase.csv"]
    else:
        return ["allSortedPatterns.csv", "allSortedPatternsShowcase.csv"]

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df


def getPatternPickles():
    if "C:\\" in str(pathlib.Path().resolve()):
        return [r"/workspace/qgi\trojan\countries patterns\allSortedPatterns.pickle", r"/workspace/qgi\trojan\showcase\allSortedPatternsShowcase.pkl"]
    else:
        return ["allSortedPatterns.pickle", "allSortedPatternsShowcase.pkl"]
    

def install(packages):
    if isinstance(packages, list):
        for package in packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    elif isinstance(packages, str):
        subprocess.check_call([sys.executable, "-m", "pip", "install", packages])


def openPickle(path):
    with open(path, "rb") as handle:
        return pickle.load(handle)


def removeNumbersFromString(string: str) -> str:
    return ''.join([i for i in string if not i.isdigit()])


def getShowcaseCountryNamesLists(normalDict: bool = True, showcaseDict: bool = True):
    lists = {}
    if normalDict:
        lists["patternCountries"] = list(pd.read_csv(patternCountries).drop("Unnamed: 0", axis = 1).iloc[:, 0])
        lists["matchCountries"]   = list(pd.read_csv(matchCountries).drop("Unnamed: 0", axis = 1).iloc[:, 0])
    if showcaseDict:
        lists["patternCountriesShowcase"] = list(pd.read_csv(patternCountriesShowcase).drop("Unnamed: 0", axis = 1).iloc[:, 0])
        lists["matchCountriesShowcase"]   = list(pd.read_csv(matchCountriesShowcase).drop("Unnamed: 0", axis = 1).iloc[:, 0])
    
    return lists

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
