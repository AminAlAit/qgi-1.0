from datetime import datetime, time, date
import matplotlib.pyplot as plt
#import plotly.express    as px
import pandas            as pd
import numpy             as np
import dataPrep          as dp
#import pycountry
import requests
import time
import json

def countriesInit():
    dictt      = json.loads(requests.get("https://raw.githubusercontent.com/flyingcircusio/pycountry/main/src/pycountry/databases/iso3166-1.json").text)
    name       = []
    alpha2     = []
    alpha3     = []
    num        = []
    name2      = []
    name3      = []
    name4      = []
    name5      = []
    name6      = []
    name7      = []
    name8      = []
    name9      = []
    name10     = []
    cols       = [ name,   name2,    name3,    name4,    name5,    name6,    name7,    name8,    name9,    name10,    alpha2,    alpha3,    num]
    colNames   = ["Name", "Name 2", "Name 3", "Name 4", "Name 5", "Name 6", "Name 7", "Name 8", "Name 9", "Name 10", "Alpha 2", "Alpha 3", "Numeric"]
    for country in dictt["3166-1"]:
        alpha2.append(country["alpha_2"])
        alpha3.append(country["alpha_3"])
        num.append(country["numeric"])
        if "common_name" in country and "official_name" in country and "name" in country:
            name.append(country["common_name"])
            name2.append(country["name"])
            name3.append(country["official_name"])
        elif "official_name" in country and "name" in country:
            name.append(country["name"])
            name2.append(country["official_name"])
            name3.append(np.nan)
        elif "name" in country:
            name.append(country["name"])
            name2.append(np.nan)
            name3.append(np.nan)
        else:
            name.append(np.nan)
            name2.append(np.nan)
            name3.append(np.nan)
        name4.append(np.nan)
        name5.append(np.nan)
        name6.append(np.nan)
        name7.append(np.nan)
        name8.append(np.nan)
        name9.append(np.nan)
        name10.append(np.nan)

    countries = pd.DataFrame(cols, colNames).T
    temp      = []
    goodnames = ["South Korea", "North Korea", "Taiwan", "Palestine", "Laos", "Iran", "Russia", "Bolivia", "Syria", "Venezuela", "Tanzania", "Vietnam", "Vatican City",
                "Congo", "Brunei", "Ivory Coast", "Moldova", "Micronesia",  "Myanmar"]
    badnames  = ["Korea, Republic of", "Korea, Democratic People's Republic of", "Taiwan, Province of China", "Palestine, State of", "Lao People's Democratic Republic", 
                "Iran, Islamic Republic of", "Russian Federation", "Bolivia, Plurinational State of", "Syrian Arab Republic", "Venezuela, Bolivarian Republic of", 
                "Tanzania, United Republic of", "Viet Nam", "Holy See (Vatican City State)", "Congo, The Democratic Republic of the", "Brunei Darussalam", "Côte d'Ivoire",
                "Moldova, Republic of", "Micronesia, Federated States of", "Burma"]
    for j in range(len(goodnames)):
        for i in range(len(countries.index)):
            if countries.iloc[i, 0] == badnames[j]:
                if str(countries.iloc[i, 1]) == "nan":
                    countries.iloc[i, 1] = badnames[j]
                elif str(countries.iloc[i, 2]) == "nan":
                    countries.iloc[i, 1] = badnames[j]
                elif str(countries.iloc[i, 3]) == "nan":
                    countries.iloc[i, 1] = badnames[j]
                elif str(countries.iloc[i, 4]) == "nan":
                    countries.iloc[i, 1] = badnames[j]
                elif str(countries.iloc[i, 5]) == "nan":
                    countries.iloc[i, 1] = badnames[j]
                elif str(countries.iloc[i, 6]) == "nan":
                    countries.iloc[i, 1] = badnames[j]
                elif str(countries.iloc[i, 7]) == "nan":
                    countries.iloc[i, 1] = badnames[j]
                elif str(countries.iloc[i, 8]) == "nan":
                    countries.iloc[i, 1] = badnames[j]
                elif str(countries.iloc[i, 9]) == "nan":
                    countries.iloc[i, 1] = badnames[j]
                else:
                    temp.append(countries.iloc[i, 0])
                countries.iloc[i, 0] = goodnames[j]

    # Duplicates turn to np.nan
    for i in range(len(countries.index)):
        if countries.iloc[i, 1] == countries.iloc[i, 2]:
            countries.iloc[i, 2] = np.nan

    # Manual additions and alterations
    refCol     = ["Name",    "Name",                 "Name",            "Name",            "Name",          "Name",                    "Name 2",                "Name",                  "Name",                  "Name",                  "Name 2",                                "Name",                                 "Name",                                  "Name",                             "Name",             "Name",     "Name",           "Name",    "Name",               "Name",                        "Name",                       "Name",                      "Name",                 "Name",           "Name",          "Name",          "Name",      "Name",                             "Name",                  "Name",                                "Name",                          "Name",                               "Name",                               "Name",                             "Name",                "Name",                       "Name",            "Name",                   "Name"]
    indexName  = ["Réunion", "Virgin Islands, U.S.", "North Macedonia", "Myanmar",         "Ivory Coast",   "Palestine",               "Republic of the Congo", "Republic of the Congo", "Republic of the Congo", "Republic of the Congo", "Congo, The Democratic Republic of the", "Congo",                                "Congo",                                 "Congo",                            "Congo",            "Congo",    "American Samoa", "Curaçao", "Dominican Republic", "Falkland Islands (Malvinas)", "Saint Martin (French part)", "Sint Maarten (Dutch part)", "United Arab Emirates", "United Kingdom", "United States", "United States", "Eswatini",  "Micronesia",                       "Moldova",               "North Korea",                         "Tanzania",                      "Venezuela",                          "Congo",                              "Bolivia",                          "South Korea",         "Iran",                       "Ivory Coast",     "Eswatini",               "Hong Kong"]
    newColName = ["Name 2",  "Name 3",               "Name 3",          "Name 3",          "Name 3",        "Name 3",                  "Name",                  "Name 2",                "Name 3",                "Name 4",                "Name",                                  "Name 2",                               "Name 3",                                "Name 4",                           "Name 5",           "Name 6",   "Name 2",         "Name 3",  "Name 2",             "Name 2",                      "Name 2",                     "Name 3",                    "Name 2",               "Name 3",         "Name 3",        "Name 4",        "Name 3",    "Name 3",                           "Name 4",                "Name 4",                              "Name 4",                        "Name 4",                             "Name 7",                             "Name 4",                           "Name 3",              "Name 3",                     "Name 4",          "Name 4",                 "Name 3"]
    newName    = ["Reunion", "Us Virgin Islands",    "Macedonia",       "Myanmar (Burma)", "Côte d’Ivoire", "Palestinian Territories", "Republic of the Congo", np.nan,                  "Congo - Brazzaville",   "Brazzaville",           "Congo",                                 "The Democratic Republic of the Congo", "Congo, The Democratic Republic of the", "République démocratique du Congo", "Congo - Kinshasa", "Kinshasa", "Samoa",          "Curacao", "Dominican",          "Malvinas",                    "Saint Martin",               "Sint Maarten",              "UAE",                  "UK",             "USA",           "US",            "Swaziland", "Micronesia (Federated States of)", "Moldova (Republic of)", "Korea (Democratic People's Rep. of)", "Tanzania (United Republic of)", "Venezuela (Bolivarian Republic of)", "Congo (Democratic Republic of the)", "Bolivia (Plurinational State of)", "Korea (Republic of)", "Iran (Islamic Republic of)", "C��te d'Ivoire", "Eswatini (Kingdom of)",  "Hong Kong, China (SAR)"] 

    for i in range(len(indexName)):
        countries.at[countries[refCol[i]][countries[refCol[i]] == indexName[i]].index[0], newColName[i]] = newName[i]

    countries = addCountry(countries, "Kosovo",              "Kosovo (Disputed Territory)", np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, "XK", "XXK", np.nan)
    countries = addCountry(countries, "Netherlands Antilles", np.nan,                       np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, "AN", "ANT", np.nan)

    countries = countries.sort_values(by = ["Name"], ascending = True).reset_index(drop = True)
    countries.to_csv("countries.csv")

def addCountry(df, name1, name2, name3, name4, name5, name6, name7, name8, name9, name10, alpha2, alpha3, numeric):
    df.loc[-1] = [name1, name2, name3, name4, name5, name6, name7, name8, name9, name10, alpha2, alpha3, numeric]  # adding a row
    df.index   = df.index + 1  # shifting index
    df         = df.sort_index()  # sorting by index
    return df

def correctCountryName(country):
    """
    Recieves a 'country' name, checks if this name is the first, second or third 
    option of all 'countries', if so, it returns the first option, otherwise 
    returns 0, so try to catch the 0s to see which countries/territories are not 
    registered yet.
    """
    countries = pd.read_csv(r"/workspace/qgi Geopolitics\data engine\Trojan Geopolitics\Indexes\Numbeo\countries.csv")
    country   = country.replace(" AND ", " and").replace(" And ", " and ").replace(" & ", " and ")
    country   = country.replace(" THE ", " the ").replace(" The ", " the ")
    country   = country.replace(" OF ", " of ").replace(" Of ", " of ")
    
    if country in list(countries["Name"]):
        return countries["Name"][list(countries["Name"]).index(country)]
    elif country in list(countries["Name 2"]):
        return countries["Name 2"][list(countries["Name 2"]).index(country)]
    elif country in list(countries["Name 3"]):
        return countries["Name 3"][list(countries["Name 3"]).index(country)]
    elif country in list(countries["Name 4"]):
        return countries["Name 4"][list(countries["Name 4"]).index(country)]
    elif country in list(countries["Name 5"]):
        return countries["Name 5"][list(countries["Name 5"]).index(country)]
    elif country in list(countries["Name 6"]):
        return countries["Name 6"][list(countries["Name 6"]).index(country)]
    elif country in list(countries["Name 7"]):
        return countries["Name 7"][list(countries["Name 7"]).index(country)]
    elif country in list(countries["Name 8"]):
        return countries["Name 8"][list(countries["Name 8"]).index(country)]
    elif country in list(countries["Name 9"]):
        return countries["Name 9"][list(countries["Name 9"]).index(country)]
    elif country in list(countries["Name 10"]):
        return countries["Name 10"][list(countries["Name 10"]).index(country)]
    else:
        return 0

def dateCountryNamesStandardizer(df, dateCol, countryCol, dateFix = "", format = "%Y.%m.%d", dateOrTime = "date", NAN = "nan"):
    countries         = pd.read_csv(r"/workspace/qgi Geopolitics\data engine\Trojan Geopolitics\Indexes\Numbeo\countries.csv")
    df                = dp.dashToNAN(df)
    correctedNames    = []
    notCorrectedNames = []
    allCountryNames   = []

    for j in range(len(countries.index)):
        allCountryNames.append(countries.iloc[j, 0])
        allCountryNames.append(countries.iloc[j, 1])
        allCountryNames.append(countries.iloc[j, 2])
        allCountryNames.append(countries.iloc[j, 3])
        allCountryNames.append(countries.iloc[j, 4])
        allCountryNames.append(countries.iloc[j, 5])
        allCountryNames.append(countries.iloc[j, 6])
        allCountryNames.append(countries.iloc[j, 7])
        allCountryNames.append(countries.iloc[j, 8])
        allCountryNames.append(countries.iloc[j, 9])

    for i in range(len(df)):
        df.iloc[i, dateCol] = dp.strToDateTime(str(df.iloc[i, dateCol]) + dateFix, format, dateOrTime, NAN)
        countryName         = correctCountryName(df.iloc[i, countryCol])
        if (countryName != 0):
            df.iloc[i, countryCol] = countryName
            correctedNames.append(df.iloc[i, countryCol])
        else:
            if df.iloc[i, countryCol] not in set(allCountryNames):
                notCorrectedNames.append(df.iloc[i, countryCol])
    return [df, list(set(correctedNames)), list(set(notCorrectedNames))]