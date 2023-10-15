from time                     import gmtime, strftime
from itertools                import groupby, islice
from datetime                 import datetime as dt
from pathlib                  import Path
import matplotlib.pyplot      as plt
import pandas                 as pd
import numpy                  as np
import patternEngine          as pe
import platform
import pathlib
import pickle
import uuid
import glob
import math
import ast
import os

#otherCountryDF = df[(df["Pattern Country"] == country_2) & (df["Match Country"] == country_1)]
#otherCountryIndex = list(otherCountryDF.index)[0]
#country_12        = otherCountryDF["Pattern Country"]

root_trojan_path = str(Path(os.path.dirname(os.getcwd()))).split("\\")
if root_trojan_path[1] == "Users" and root_trojan_path[2] == "Amin":
    countriesPatternsPath                = r"/workspace/qgi\trojan\countries patterns\\"
    countriesCSVPath                     = r"/workspace/qgi\trojan\countries\countries.csv"
    showcasePath                         = r"/workspace/qgi\trojan\showcase\\"
    trojanPath                           = r"/workspace/qgi\trojan"
    dataBankPath                         = r"/workspace/qgi\trojan\data bank"
    
    MAINs_stocker_path                   = r"/workspace/qgi\trojan\stockers\MAINs_stocker.csv"
    index_stocker_path                   = r"/workspace/qgi\trojan\stockers\index_stocker.csv"
    checkersIndexPath                    = r"/workspace/qgi\trojan\checkers\indexes.csv"

    allSortedPatternsPickle              = r"/workspace/qgi\trojan\showcase\allSortedPatterns.pickle"
    allSortedPatternsShowcasePickle      = r"/workspace/qgi\trojan\\showcase\allSortedPatternsShowcase.pkl"
else:
    countriesPatternsPath                = r"/workspace/data\trojan\countries patterns\\"
    countriesCSVPath                     = r"/workspace/data\trojan\countries\countries.csv"
    showcasePath                         = r"/workspace/data\trojan\showcase\\"
    trojanPath                           = r"/workspace/data\trojan"
    dataBankPath                         = r"/workspace/data\trojan\data bank"

    MAINs_stocker_path                   = r"/workspace/data\trojan\stockers\MAINs_stocker.csv"
    index_stocker_path                   = r"/workspace/data\trojan\stockers\index_stocker.csv"
    checkersIndexPath                    = r"/workspace/data\trojan\checkers\indexes.csv"

    allSortedPatternsPickle              = r"/workspace/data\trojan\showcase\allSortedPatterns.pickle"
    allSortedPatternsShowcasePickle      = r"/workspace/data\trojan\showcase\allSortedPatternsShowcase.pkl"

SINGLE_SUB_VALIDATE_ESSENTIAL_COLS       = ["Year", "Country"]
SIGNLE_SUB_VALIDATE_NB_ROWS              = 10
SINGLE_SUB_VALIDATE_NB_COLS              = 3

COUNTRY_PATTERTNS_PATTERN_COUNTRY_COL    = 0
COUNTRY_PATTERTNS_MATCH_COUNTRY_COL      = 1
COUNTRY_PATTERTNS_INDEX_COL              = 2
COUNTRY_PATTERTNS_PATTERN_VALUES_COL     = 3
COUNTRY_PATTERTNS_PATTERN_INDEX_COL      = 4
COUNTRY_PATTERTNS_MATCH_VALUES_COL       = 5
COUNTRY_PATTERNS_MATCH_INDEX_COL         = 6
COUNTRY_PATTERNS_RANK_COL                = 7
COUNTRY_PATTERNS_SCORE_COL               = 8
COUNTRY_PATTERNS_CORRELATION_SCORE_COL   = 9
COUNTRY_PATTERNS_EUCLIDEAN_SCORE_COL     = 10
COUNTRY_PATTERNS_MAPE_SCORE_COL          = 11
COUNTRY_PATTERNS_DTW_SCORE_COL           = 12
COUNTRY_PATTERNS_CBD_SCORE_COL           = 13
COUNTRY_PATTERNS_PATTERN_LENGTH_COL      = 14
COUNTRY_PATTERNS_PATTERN_INDEX_START_COL = 15
COUNTRY_PATTERNS_PATTERN_INDEX_END_COL   = 16
COUNTRY_PATTERNS_MATCH_INDEX_START_COL   = 17
COUNTRY_PATTERNS_MATCH_INDEX_END_COL     = 18

INDEX_STOCKER_FILE_NAME_COL              = 0
INDEX_STOCKER_INDEX_COL                  = 1
INDEX_STOCKER_ID_COL                     = 2
INDEX_STOCKER_ORG_COL                    = 3
INDEX_STOCKER_PATTERNIZED_COL            = 4
INDEX_STOCKER_LAST_UPDATED_COL           = 5
INDEX_STOCKER_MAIN_PATH_COL              = 6
INDEX_STOCKER_PATH_COL                   = 7
INDEX_STOCKER_EXEC_DURATION_COL          = 8

MAINs_STOCKER_ID_COL                     = 0
MAINs_STOCKER_MAIN_INDEX_NAME_COL        = 1
MAINs_STOCKER_ORG_COL                    = 2
MAINs_STOCKER_CUTTED_COL                 = 3
MAINs_STOCKER_MAIN_PATH_COL              = 4
MAINs_STOCKER_SINGLE_SUBS_PATH_COL       = 5
MAINs_STOCKER_SUBS_COUNT_COL             = 6
MAINs_STOCKER_STOCKED_DATE_COL           = 7

#################################################################
################### Initial Data Pipeline #######################
#################################################################
def get_MAINs_to_cut(dataBankPath: str = dataBankPath):
    MAINs = []
    for root, dirs, files in os.walk(dataBankPath):
        for file in files:
            ## Ignore every file that ends with 'PATTERNS_DF.csv'
            if not file.endswith("PATTERNS_DF.csv"): 
                ## Ignore every file that ends with 'DUMPED_COUNTRIES.csv'
                if not file.endswith("DUMPED_COUNTRIES.csv"):
                    ## Ignore anyting from the directory "[SOURCES]"
                    if not "[SOURCES]" in os.path.join(root, file):
                        ## Making sure '.git', nor the files in it, is/are not included in the search
                        if not ".git" in os.path.join(root, file):
                            ## Ignore every file that ends with '_SINGLE_SUB.csv'
                            if not file.endswith("_SINGLE_SUB.csv"):
                                ## Ignore all sources with "MAIN" in them
                                if "MAIN" in str(os.path.join(root, file)).split("\\")[-1]:
                                    MAINs.append(os.path.join(root, file))
    return MAINs


def MAINs_cutter(index_path: str, fixYears = None, region: bool = False, passed_IDs: list = None, debug: bool = False):
    if index_path == "":
        return {}
    
    print(index_path) if debug else None
    df     = pd.read_csv(index_path)
    region = False

    IDs             = []
    index_names     = []
    Orgs            = []
    file_names      = []
    sub_index_path  = []
    MAIN_index_path = []
    
    if "Year" in list(df) and "Country" in list(df):
        cols = list(df)
        cols.remove("Year")
        cols.remove("Country")
        if "Region" in list(df):
            cols.remove("Region") 
            region = True

        i = 0
        # going over the indexes one by one
        for index in cols:
            # Composing the fresh cut dataframe using one index
            single_sub_DF            = pd.DataFrame()
            single_sub_DF["Year"]    = df["Year"]
            single_sub_DF["Country"] = df["Country"]
            single_sub_DF[index]     = df[index]

            if fixYears is not None:
                if isinstance(fixYears, list):
                    if len(fixYears) == 2:
                        single_sub_DF = fixYears(single_sub_DF, fixYears)

            ## Composing the path and name of the single sub index csv file
            org_name                   = index_path.split("\\")[-2]
            index_file_name            = index_path.split("\\")[-1][:-4]

            # Giving the index its ID
            if passed_IDs is None:
                id = str(uuid.uuid4())[:-28]
            else:
                id = passed_IDs[i]
            
            # Adding pre (org name) and post (Index_SINGLE_SUB) signatures
            index_single_sub_file_name = org_name + "----" + id + " Index_SINGLE_SUB" + ".csv"
            index_single_sub_file_name = index_single_sub_file_name.replace(":", " -").replace("\\", "-").replace("/", "-") \
                                                                    .replace("*", "-").replace("?", "-").replace("\"", "'") \
                                                                    .replace(">", "-").replace("<", "-").replace("|", "-")
            
            ## removing the '.csv' to create a directory
            #index_path_cuts_dir = index_path[:-4] + "\\"

            # alternative method
            index_path_cuts_dir = "\\".join(index_path.split("\\")[:-1]) + "\\" + "SINGLE_SUBs" + "\\"

            ## If path does not exist, create it 
            if not os.path.exists(index_path_cuts_dir):
                os.makedirs(index_path_cuts_dir)

            # Save fresh cut dataframe into csv
            single_sub_DF.to_csv(index_path_cuts_dir + index_single_sub_file_name)

            print("Index saved at: ")                               if debug else None
            print(index_path_cuts_dir + index_single_sub_file_name) if debug else None

            # Populating the IDs_index_names_stocker 
            IDs.append(id)
            index_names.append(index)
            Orgs.append(org_name)
            file_names.append(index_file_name)
            MAIN_index_path.append(index_path)
            sub_index_path.append(index_path_cuts_dir + index_single_sub_file_name)
            i += 1
    
    IDs_index_name_stocker = pd.DataFrame()
    IDs_index_name_stocker["ID"]        = IDs
    IDs_index_name_stocker["Index"]     = index_names
    IDs_index_name_stocker["Org"]       = Orgs
    IDs_index_name_stocker["MAIN name"] = file_names
    IDs_index_name_stocker["MAIN Path"] = MAIN_index_path
    IDs_index_name_stocker["Sub Path"]  = sub_index_path
    return IDs_index_name_stocker
#################################################################
########################### Stockers ############################
################# Index Candidates & Diagnosis ##################
#################################################################
def get_MAINs_stocker(debug: bool = False):
    print(root_trojan_path)   if debug else None
    print(MAINs_stocker_path) if debug else None
    df = pd.read_csv(MAINs_stocker_path)
    for col in list(df):
        if "Unnamed: " in col:
            df = df.drop(col, axis = 1)
    
    return df


def get_SUBs_Count_of_this_MAIN(MAIN_path: str):
    df = get_MAINs_stocker()
    if MAIN_path == "":
        return 0
    elif MAIN_path not in list(df["MAIN Path"]):
        return 1
    else:
        return df.iloc[list(df["MAIN Path"]).index(MAIN_path), MAINs_STOCKER_SUBS_COUNT_COL]


def get_candidates_percentage(figsize = (8, 8), fontsize = 12, textcolor = 'white'):
    df      = get_index_stocker()
    Trues   = 0
    Falsies = 0
    NaNs    = 0
    labels  = ["Up to date", "Out of date", "Legacy"]

    for i in list(df.iloc[:, INDEX_STOCKER_PATTERNIZED_COL]):
        if i == True:
            Trues += 1
        elif i == False:
            Falsies += 1
        elif math.isnan(i):
            NaNs += 1

    values = [Trues, Falsies, NaNs]
    colors = ['#8EB897', '#4F6272', '#DD7596']

    #total = sum(values)
    #for i, value in enumerate(values):
    #    percentage = '{:1f}%'.format(value/total * 100)
    #    angle      = (sum(values[:i]) + value / 2) / total * 360
    #    x          = 1.2 * (angle % 180 > 90) - 0.1
    #    y          = 1.2 * (angle % 360 > 180) - 0.1
    #    plt.annotate(percentage, (x, y), color = textcolor, ha = "center", va = "center")

    plt.figure(figsize = figsize)

    return plt.pie(
        values, 
        labels        = labels, 
        labeldistance = 1.15, 
        textprops     = {'fontsize': fontsize, 'color': textcolor},
        wedgeprops    = {"linewidth" : 1, "edgecolor" : "white"}, 
        colors        = colors)


def overwrite_save_MAINs_stocker(df: pd.DataFrame) -> None:
    df.to_csv(MAINs_stocker_path)


def update_MAIN_stocking_date(MAIN_path: str):
    df = get_MAINs_stocker()
    if MAIN_path == "":
        return 0
    elif MAIN_path not in list(df.iloc[:, INDEX_STOCKER_MAIN_PATH_COL]):
        return 1
    else:
        df.iloc[list(df.iloc[:, INDEX_STOCKER_MAIN_PATH_COL]).index(MAIN_path), 7] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        df.to_csv(MAINs_stocker_path)
        return df


def update_MAINs_stocker_SUBs_count():
    MAINs_stocker = get_MAINs_stocker()
    for i in range(len(list(MAINs_stocker.iloc[:, MAINs_STOCKER_MAIN_PATH_COL]))):
        
        SINGLE_SUBs_path = "\\".join(MAINs_stocker.iloc[i, MAINs_STOCKER_MAIN_PATH_COL].split("\\")[:-1]) + "\\SINGLE_SUBs"
        if os.path.isdir(SINGLE_SUBs_path):
            if len(glob.glob(SINGLE_SUBs_path + "\\*.csv")) != MAINs_stocker.iloc[i, MAINs_STOCKER_SUBS_COUNT_COL]:
                set_SUBs_Count_of_this_MAIN(MAINs_stocker.iloc[i, MAINs_STOCKER_MAIN_PATH_COL], len(glob.glob(SINGLE_SUBs_path + "\\*.csv")))
        else:
            set_SUBs_Count_of_this_MAIN(MAINs_stocker.iloc[i, MAINs_STOCKER_MAIN_PATH_COL], 0)


def set_cutted_status_of_this_MAIN(MAIN_path: str, cutted_status: bool):
    df = get_MAINs_stocker()
    if MAIN_path == "":
        return 0
    elif MAIN_path not in list(df.iloc[:, MAINs_STOCKER_MAIN_PATH_COL]):
        return 1
    else:
        df.iloc[list(df.iloc[:, MAINs_STOCKER_MAIN_PATH_COL]).index(MAIN_path), MAINs_STOCKER_CUTTED_COL] = cutted_status
        df.to_csv(MAINs_stocker_path)
        return df

    
def set_SUBs_Count_of_this_MAIN(MAIN_path: str, SUBs_Count: int):
    df = get_MAINs_stocker()
    if MAIN_path == "":
        return 0
    elif MAIN_path not in list(df.iloc[:, MAINs_STOCKER_MAIN_PATH_COL]):
        return 1
    else:
        df.iloc[list(df.iloc[:, MAINs_STOCKER_MAIN_PATH_COL]).index(MAIN_path), MAINs_STOCKER_SUBS_COUNT_COL] = SUBs_Count
        df.to_csv(MAINs_stocker_path)
        return df


def add_MAIN_to_stocker(MAIN: str, cutted: bool = False):
    MAINs_stocker    = get_MAINs_stocker()
    SINGLE_SUBs_path = "\\".join(MAIN.split("\\")[:-1]) + "\\SINGLE_SUBs"
    
    MAINs_stocker.loc[-1] = [
        str(uuid.uuid4())[:8],                                                                                      # id
        MAIN.split("\\")[-1].replace(".csv", "").replace("MAIN", "").replace("-", "").strip(),                  # MAIN Index Name
        MAIN.split("\\")[-2],                                                                                   # Org Name
        cutted,                                                                                                 # Cutted
        MAIN,                                                                                                   # MAIN Path
        "\\".join(MAIN.split("\\")[:-1]) + "\\SINGLE_SUBs"      if os.path.isdir(SINGLE_SUBs_path) else np.nan, # SINGLE SUBs Path
        len(glob.glob(SINGLE_SUBs_path + "\\*_SINGLE_SUB.csv")) if os.path.isdir(SINGLE_SUBs_path) else 0,      # SUBs Count
        dt.now().strftime("%Y-%m-%d %H:%M:%S")]                                                                                               # Stocked Date
    MAINs_stocker.index   = MAINs_stocker.index + 1 
    MAINs_stocker         = MAINs_stocker.sort_index()
    overwrite_save_MAINs_stocker(MAINs_stocker)
    return MAINs_stocker


def get_index_stocker(debug: bool = False):
    print(root_trojan_path)     if debug else None
    print(index_stocker_path) if debug else None
    df = pd.read_csv(index_stocker_path)
    for col in list(df):
        if "Unnamed: " in col:
            df = df.drop(col, axis = 1)
    
    return df


def get_pattern_length_range(index_path: str) -> list:
    df = pd.read_csv(index_path)
    if "Unnamed: 0" in list(df):
        df = df.drop(["Unnamed: 0"], axis = 1)
    years_range = list(set([int(year) for year in list(set(df["Year"]))]))
    years_range.sort()

    pattern_length = []
    if len(years_range) > 2:
        pattern_length.append(3)
    
    if len(years_range) > 3:
        pattern_length.append(len(years_range))
        pattern_length = list(range(pattern_length[0], pattern_length[1]))

    return pattern_length


def reset_index_stocker():
    df = pd.DataFrame()
    df["File Name"]          = []
    df["Index"]              = []
    df["ID"]                 = []
    df["Org Name"]           = []
    df["Patternized"]        = []
    df["Last Updated"]       = []
    df["MAIN Path"]          = []
    df["Path"]               = []
    df["Execution Duration"] = []

    df.to_csv(index_stocker_path)
    return df

def reset_MAINs_stocker():
    df                     = pd.DataFrame()
    df["ID"]               = []
    df["MAIN Index Name"]  = []
    df["Org Name"]         = []
    df["Cutted"]           = []
    df["MAIN Path"]        = []
    df["SINGLE SUBs Path"] = []
    df["SUBs Count"]       = []
    df["Stocked Date"]     = []

    df.to_csv(MAINs_stocker_path)
    return df


def overwrite_save_index_stocker(df: pd.DataFrame) -> None:
    df.to_csv(index_stocker_path)


def add_index_to_stocker(indexPath: str):
    df = get_index_stocker()
    if indexPath == "":
        return 0
    elif indexPath in list(df.iloc[:, INDEX_STOCKER_PATH_COL]):
        return 1
    else:
        file_names  = list(df.iloc[:, INDEX_STOCKER_FILE_NAME_COL])
        indexes     = list(df.iloc[:, INDEX_STOCKER_INDEX_COL])
        IDs         = list(df.iloc[:, INDEX_STOCKER_ID_COL])
        Orgs        = list(df.iloc[:, INDEX_STOCKER_ORG_COL])
        patternized = list(df.iloc[:, INDEX_STOCKER_PATTERNIZED_COL])
        last_update = list(df.iloc[:, INDEX_STOCKER_LAST_UPDATED_COL])
        MAIN_paths  = list(df.iloc[:, INDEX_STOCKER_MAIN_PATH_COL])
        paths       = list(df.iloc[:, INDEX_STOCKER_PATH_COL])
        exec_durs   = list(df.iloc[:, INDEX_STOCKER_EXEC_DURATION_COL])

        file_names.append(indexPath.split("\\")[-1])
        indexes.append(np.nan)
        IDs.append(np.nan)
        Orgs.append(np.nan)
        patternized.append(False)
        last_update.append(get_modification_date(indexPath))
        MAIN_paths.append(np.nan)
        paths.append(indexPath)
        exec_durs.append(np.nan)
        
        new_index_stocker                       = pd.DataFrame()
        new_index_stocker["File Name"]          = file_names
        new_index_stocker["Index"]              = indexes
        new_index_stocker["ID"]                 = IDs
        new_index_stocker["Org Name"]           = Orgs
        new_index_stocker["Patternized"]        = patternized
        new_index_stocker["Last Updated"]       = last_update
        new_index_stocker["MAIN Path"]          = MAIN_paths
        new_index_stocker["Path"]               = paths
        new_index_stocker["Execution Duration"] = exec_durs
        new_index_stocker.to_csv(index_stocker_path)

        return new_index_stocker
    

def delete_list_indexes_from_index_stocker(list_of_indexes: list) -> pd.DataFrame:
    df = get_index_stocker()
    df = df.drop(index = list_of_indexes)
    df.reset_index(drop = True, inplace = True)
    df.to_csv(index_stocker_path)
    return df
    

def remove_index_from_stocker(indexName: str):
    df = get_index_stocker()
    if indexName == "":
        return 0
    elif indexName not in list(df.iloc[:, INDEX_STOCKER_INDEX_COL]):
        return 1
    else:
        df = df[df.iloc[:, INDEX_STOCKER_INDEX_COL] != indexName]
        df.to_csv(index_stocker_path)
        return df
    

def index_name_in_stocker(indexName: str):
    if indexName == "":
        return {}
    else:
        df = get_index_stocker()
        if indexName in list(df.iloc[:, INDEX_STOCKER_INDEX_COL]):
            return True
        else:
            return False
        

def get_patternized_status_of_this_index(indexPath: str):
    df = get_index_stocker()
    if indexPath == "":
        return 0
    elif indexPath not in list(df.iloc[:, INDEX_STOCKER_PATH_COL]):
        return 1
    else:
        return df.iloc[list(df.iloc[:, INDEX_STOCKER_PATH_COL]).index(indexPath), INDEX_STOCKER_PATTERNIZED_COL]


def set_duration_of_this_index(index_path: str, duration):
    df = get_index_stocker()
    if index_path == "":
        return 0
    elif index_path not in list(df.iloc[:, INDEX_STOCKER_PATH_COL]):
        return 1
    else:
        df.iloc[list(df.iloc[:, INDEX_STOCKER_PATH_COL]).index(index_path), INDEX_STOCKER_EXEC_DURATION_COL] = duration
        df.to_csv(index_stocker_path)
        return df


def set_patternized_status_of_this_index(indexPath: str, status):
    df = get_index_stocker()
    if indexPath == "":
        return 0
    elif indexPath not in list(df.iloc[:, INDEX_STOCKER_PATH_COL]):
        return 1
    else:
        df.iloc[list(df.iloc[:, INDEX_STOCKER_PATH_COL]).index(indexPath), INDEX_STOCKER_PATTERNIZED_COL] = status
        df.to_csv(index_stocker_path)
        return df


def set_Index_name_of_this_index(indexPath: str, index_name: str):
    df = get_index_stocker()
    if indexPath == "":
        return 0
    elif indexPath not in list(df.iloc[:, INDEX_STOCKER_PATH_COL]):
        return 1
    else:
        df.iloc[list(df.iloc[:, INDEX_STOCKER_PATH_COL]).index(indexPath), INDEX_STOCKER_INDEX_COL] = index_name
        df.to_csv(index_stocker_path)
        return df


def set_org_name_of_this_index(indexPath: str, org_name: str):
    df = get_index_stocker()
    if indexPath == "":
        return 0
    elif indexPath not in list(df.iloc[:, INDEX_STOCKER_PATH_COL]):
        return 1
    else:
        df.iloc[list(df.iloc[:, INDEX_STOCKER_PATH_COL]).index(indexPath), INDEX_STOCKER_ORG_COL] = org_name
        df.to_csv(index_stocker_path)
        return df
    

def set_MAIN_Path_of_this_index(indexPath: str, MAIN_Path: str):
    df = get_index_stocker()
    if indexPath == "":
        return 0
    elif indexPath not in list(df.iloc[:, INDEX_STOCKER_PATH_COL]):
        return 1
    else:
        df.iloc[list(df.iloc[:, INDEX_STOCKER_PATH_COL]).index(indexPath), INDEX_STOCKER_MAIN_PATH_COL] = MAIN_Path
        df.to_csv(index_stocker_path)
        return df
    

def set_ID_of_this_index(indexPath: str, id: str):
    df = get_index_stocker()
    if indexPath == "":
        return 0
    elif indexPath not in list(df.iloc[:, INDEX_STOCKER_PATH_COL]):
        return 1
    else:
        df.iloc[list(df.iloc[:, INDEX_STOCKER_PATH_COL]).index(indexPath), INDEX_STOCKER_ID_COL] = id
        df.to_csv(index_stocker_path)
        return df


def set_last_updated_datetime_of_this_index(indexPath: str, date_time):
    df = get_index_stocker()
    if indexPath == "":
        return 0
    elif indexPath not in list(df.iloc[:, INDEX_STOCKER_PATH_COL]):
        return 1
    else:
        df.iloc[list(df.iloc[:, INDEX_STOCKER_PATH_COL]).index(indexPath), INDEX_STOCKER_LAST_UPDATED_COL] = date_time
        df.to_csv(index_stocker_path)
        return df


def get_last_update_stocker(indexPath: str):
    df = get_index_stocker()
    if indexPath == "":
        return 0
    elif indexPath not in list(df.iloc[:, INDEX_STOCKER_PATH_COL]):
        return 1
    else:
        return df.iloc[list(df.iloc[:, INDEX_STOCKER_PATH_COL]).index(indexPath), INDEX_STOCKER_LAST_UPDATED_COL]


def get_path_of_this_index(indexPath: str):
    df = get_index_stocker()
    if indexPath == "":
        return 0
    elif indexPath not in list(df.iloc[:, INDEX_STOCKER_PATH_COL]):
        return 1
    else:
        return df.iloc[list(df.iloc[:, INDEX_STOCKER_PATH_COL]).index(indexPath), INDEX_STOCKER_PATH_COL]


def get_creation_date(path_to_file, as_date: bool = True):
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
    
    if as_date:
        return dt.strptime(str(dt.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
    else:
        return str(dt.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S"))


def get_modification_date(path_to_file, as_date: bool = True):
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
    if as_date:
        return dt.strptime(str(dt.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
    else:
        return str(dt.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S"))


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
    patternized_indexes = df[df.iloc[:, INDEX_STOCKER_PATTERNIZED_COL] == True]
    for lu in range(len(list(patternized_indexes.iloc[:, INDEX_STOCKER_LAST_UPDATED_COL]))):
        # Getting the last modification date as registered in index_stocker.csv
        stocker_index_date = patternized_indexes.iloc[lu, INDEX_STOCKER_LAST_UPDATED_COL]
        
        if "." in stocker_index_date:
            stocker_index_date = dt.strptime(stocker_index_date.split(".")[0], "%Y-%m-%d %H:%M:%S")

        # Getting the real last modification date of that same index
        fresh_index_date   = get_modification_date(patternized_indexes.iloc[lu, INDEX_STOCKER_PATH_COL])
        #print("1111111111111111")
        #print(stocker_index_date)
        #print(type(stocker_index_date))
        #print("1111111111111111111")

        # Checking if our indexes have been updated
        if stocker_index_date < fresh_index_date:
            # Setting the patternized status to False for each index that is out of date. 
            # That way we label it ready to be patternized
            set_patternized_status_of_this_index(patternized_indexes.iloc[lu, INDEX_STOCKER_PATTERNIZED_COL], False)
            print("Index '", patternized_indexes.iloc[lu, INDEX_STOCKER_PATTERNIZED_COL].split("\\")[-1], "' is outdated. ")
            print("Its 'patternized' status was set to False. ")

    # Getting paths of un-patternized indexes
    patternized_slice = slice_df(get_index_stocker(), False, "Patternized")
    for j in list(patternized_slice["Path"]):
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
    """
    `atLeastLength` is the number of indexes to at least have per pattern
    """
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

    patternsDict = openPickle(patternsDictPath)
    patternsDF   = pickleToDF(patternsDict)
    patternsDF.to_csv(showcasePath + "allSortedPatterns.csv")

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


def slice_df(df: pd.DataFrame, value, column: str):
    """Filters a dataframe by a list of values"""
    return df.iloc[[i for i, x in enumerate(list(df[column])) if x == value], :]

#################################################################
####################### Country Filter ##########################
#################################################################
def countryFilter(index_PATTERNS_csv: pd.DataFrame, output_dir: str) -> None:
    for country in list(set(index_PATTERNS_csv["Pattern Country"])):
        print("++++++++++++++++")
        print(country)
        print("+++++++++++++")
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

        # Extracting the first and last years of the pattern index and match index years to have them in one dedicated column
        for row in range(len(dfTemp)):
            # Pattern Index: the years of the pattern for the pattern country
            pattern_index = dfTemp.iloc[row, COUNTRY_PATTERTNS_PATTERN_INDEX_COL]
            if isinstance(pattern_index, str):
                PattIndStart.append(int(ast.literal_eval(pattern_index)[0]))
                PattIndEnd.append(int(ast.literal_eval(pattern_index)[-1]))
            elif isinstance(pattern_index, list):
                PattIndStart.append(int(pattern_index[0]))
                PattIndEnd.append(int(pattern_index[-1]))
            
            # Match Index: the years of the pattern for the match country
            match_index = dfTemp.iloc[row, COUNTRY_PATTERNS_MATCH_INDEX_COL]
            if isinstance(match_index, str):
                MatchIndStart.append(int(ast.literal_eval(match_index)[0]))
                MatchIndEnd.append(int(ast.literal_eval(match_index)[-1]))
            elif isinstance(match_index, list):
                MatchIndStart.append(int(match_index[0]))
                MatchIndEnd.append(int(match_index[-1]))
            
        # Adding the new columns
        dfTemp["Pattern Index Start"] = PattIndStart
        dfTemp["Pattern Index End"]   = PattIndEnd
        dfTemp["Match Index Start"]   = MatchIndStart
        dfTemp["Match Index End"]     = MatchIndEnd

        if new:
            dfTemp.to_csv(output_dir + country + "_PATTERNS_DF.csv")
        else:
            oldDF                    = pd.read_csv(output_dir + country + "_PATTERNS_DF.csv").drop("Unnamed: 0", axis = 1)
            dfTemp                   = pd.concat([oldDF, dfTemp])
            list_valued_cols         = ["Pattern Values", "Pattern Index", "Match Values", "Match Index"]
            dfTemp[list_valued_cols] = dfTemp[list_valued_cols].applymap(str)
            dfTemp                   = dfTemp.drop_duplicates(keep = False)
            dfTemp[list_valued_cols] = dfTemp[list_valued_cols].applymap(eval)
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
        '/workspace/qgi\\trojan\\Numbeo\\Cost of Living\\Cost of Living Index.csv'
    and returns this: 
        '/workspace/qgi\\trojan\\Numbeo\\Cost of Living\\'
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
        if str(fixYears[1]) in str(df["Year"][i]):
            df = df.drop(index = i)
    for i in list(df.index):
        if str(fixYears[0]) in str(df["Year"][i]):
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