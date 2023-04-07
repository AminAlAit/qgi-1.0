import pandas       as pd
import subprocess
import pickle
import sys

patternCountries         = r"/workspace/qgi\trojan\showcase\patternCountries.csv"
matchCountries           = r"/workspace/qgi\trojan\showcase\matchCountries.csv"
patternCountriesShowcase = r"/workspace/qgi\trojan\showcase\patternCountriesShowcase.csv"
matchCountriesShowcase   = r"/workspace/qgi\trojan\showcase\matchCountriesShowcase.csv"

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