import sys
sys.path.insert(1, r"/workspace/qgi\trojan\data engine")
import dataPrep  as dp
import trojan    as tr
tr.install(["yfinance", "streamlit"])
import pandas    as pd
import streamlit as st
import yfinance  as yf
import numpy     as np
import re

### cd trojan-streamlit
### python -m streamlit run main.py

patternsPath         = r"/workspace/qgi\trojan\countries patterns\allSortedPatterns.pickle"
patternsShowcasePath = r"/workspace/qgi\trojan\showcase\allSortedPatternsDiffShowcase.pkl"

st.write("""# Trojan Geopolitics""")

patterns                 = tr.openPickle(patternsPath)
patternsShowcase         = tr.openPickle(patternsShowcasePath) #dp.filterSortedPatternDict(sortedPatternsDict = patterns, corrScore = 0.9, pattLength = 6, onlyDifferentPattIndexStarts = True)
lists                    = tr.getShowcaseCountryNamesLists()
patternCountriesShowcase = lists["patternCountriesShowcase"]
#matchCountriesShowcase   = lists["matchCountriesShowcase"]


## Pattern Country Dropdown
patternCountry = st.selectbox("Select country A", tuple(patternCountriesShowcase))


## Pattern Length Slider
patternLengths         = []
for stitchName in patternsShowcase.keys():
    if stitchName.startswith(patternCountry):
        patternLengths.append(int(stitchName.split("-")[1]))
patternLengths = list(set(patternLengths))
patternLength  = st.slider("Select Pattern Length", min(patternLengths), max(patternLengths), min(patternLengths))


## Match Country Dropdown
matchCountriesShowcase = []
for stitchName in patternsShowcase.keys():
    if stitchName.startswith(patternCountry):
        if int(stitchName.split("-")[1]) == patternLength:
            matchCountriesShowcase.append(tr.removeNumbersFromString(stitchName.split("-")[-1]))
matchCountry = st.selectbox("Select country B", tuple(matchCountriesShowcase))

## Pattern Country Index Start
patternCountryIndexStarts = []
for stitchName in patternsShowcase.keys():
    if stitchName.startswith("Singapore"):
        if int(stitchName.split("-")[1]) == patternLength:
            if tr.removeNumbersFromString(stitchName.split("-")[-1]) == matchCountry:
                patternCountryIndexStarts.append(re.sub("[^0-9]", "", stitchName.split("-")[0]))
patternCountryIndexStart = st.selectbox("Please select when do you want your pattern to start for country A: ", tuple(patternCountryIndexStarts))


## Match Country Index Start
matchCountryIndexStarts = []
for stitchName in patternsShowcase.keys():
    if stitchName.startswith("Singapore"):
        if int(stitchName.split("-")[1]) == patternLength:
            if tr.removeNumbersFromString(stitchName.split("-")[-1]) == matchCountry:
                if re.sub("[^0-9]", "", stitchName.split("-")[0]) == patternCountryIndexStart:
                    matchCountryIndexStarts.append(re.sub("[^0-9]", "", stitchName.split("-")[-1]))
matchCountryIndexStart = st.selectbox("Please select when do you want your pattern to start for country B: ", tuple(matchCountryIndexStarts))

stitchName = patternCountry + patternCountryIndexStart + "-" + str(patternLength) + "-" + matchCountry + matchCountryIndexStart

st.write("""### Raw Dataframe""")
df = patternsShowcase[stitchName]
st.dataframe(df)

st.write("""### Plots Dataframe""")
dfViz = dp.patternVsMatcheDF(df)
st.dataframe(dfViz)