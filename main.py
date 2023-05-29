# import pathlib
# import sys
# sys.path.insert(1, r"/workspace/qgi\trojan\data engine")
# import dataPrep  as dp
# tr.install(["streamlit"])
# import matplotlib.pyplot as plt
import streamlit         as st
import trojan            as tr
import pandas            as pd
import numpy             as np
import ast

### cd trojan-streamlit
### python -m streamlit run main.py

#### Title
st.write("""# Trojan Geopolitics""")


#### Data Prep
# patterns, patternsShowcase = tr.getPatternDFs()
patterns = tr.getPatternDFs()[1]


sorted_countries_A = np.sort(patterns['Pattern Country'].unique())
sorted_countries_B = np.sort(patterns['Match Country'].unique())
pattern_length_min = min(patterns["Pattern Length"])
pattern_length_max = max(patterns["Pattern Length"])


#### Sidebar filters
country_A_filter      = st.sidebar.selectbox("Country A", sorted_countries_A)
country_B_filter      = st.sidebar.selectbox("Country B", sorted_countries_B)
pattern_length_filter = st.sidebar.slider("Pattern Length", pattern_length_min, pattern_length_max, (int(pattern_length_max / 2), ))
correlation_filter    = st.sidebar.slider("Correlation threshold", 0.0, 1.0, 0.9, step = 0.05)


#### Filtering
# error booleans
filtered_bool       = True
country_b_bool      = True
pattern_length_bool = True
correlation_bool    = True

# filtering for Country A
filtered_df = patterns[patterns["Pattern Country"] == country_A_filter]

# filtering for Country B
if country_B_filter in list(set(filtered_df["Match Country"])):
    filtered_df = filtered_df[(filtered_df["Match Country"] == country_B_filter)]
else:
    filtered_bool  = False
    country_b_bool = False

## filtering for pattern length
if pattern_length_filter[0] in list(filtered_df["Pattern Length"]):
    filtered_df = filtered_df[filtered_df["Pattern Length"] == pattern_length_filter[0]]
else:
    filtered_bool       = False
    pattern_length_bool = False

## filtering for correlation threshold
if correlation_filter <= max(list(filtered_df["Correlation Score"])):
    filtered_df = filtered_df[filtered_df["Correlation Score"] >= correlation_filter]
else:
    filtered_bool    = False
    correlation_bool = False


#### Exceptions Handling
if len(filtered_df) != len(list(set(filtered_df["Index"]))):
    st.write("Exception reached with this df.")
else:
    pattern_strength = len(filtered_df)


#### Final touches & Data Prep
filtered_df        = filtered_df.drop(["Pattern ID"], axis = 1)
correlation_scores = list(filtered_df["Correlation Score"])


#### Viz Prep
df_viz       = tr.patternVsMatcheDF(filtered_df)
country1Cols = []
country2Cols = []
for col in list(df_viz):
    if country_A_filter in col:
        country1Cols.append(col)
    elif country_B_filter in col:
        country2Cols.append(col)


#### Main Display
if filtered_bool:
    ## Display original pattern dataframe
    #st.dataframe(filtered_df)
    ## Display vizable pattern dataframe
    #st.dataframe(tr.patternVsMatcheDF(filtered_df))

    st.write(country_A_filter + """ and """ + country_B_filter + """ have a pattern of length """ + str(pattern_length_filter[0]) + """ years and strength of """ + str(pattern_strength) + """indexes. """)

    col1, col2 = st.columns(2)
    j          = 0
    for i in range(len(country2Cols)):
        if j == 0:
            col1.header(country1Cols[i].split("-")[1].strip() + "\nCorrelation: " + str(correlation_scores[i] * 100) + "%")
            df_temp = pd.DataFrame()
            df_temp["Years"]          = df_viz.iloc[:, 0]
            df_temp[country_A_filter] = df_viz[country1Cols[i]]
            df_temp[country_B_filter] = df_viz[country2Cols[i]]
            col1.line_chart(data = df_temp, x = list(df_viz)[0], y = [country_A_filter, country_B_filter], use_container_width = True)
            j = 1
            continue
        elif j == 1:
            col2.header(country1Cols[i].split("-")[1].strip() + "\nCorrelation: " + str(correlation_scores[i] * 100) + "%")
            df_temp = pd.DataFrame()
            df_temp["Years"]          = df_viz.iloc[:, 0]
            df_temp[country_A_filter] = df_viz[country1Cols[i]]
            df_temp[country_B_filter] = df_viz[country2Cols[i]]
            col2.line_chart(data = df_temp, x = list(df_viz)[0], y = [country_A_filter, country_B_filter], use_container_width = True)
            j = 0
            continue
    

## Exceptions
else:
    st.write("""Report could not be produced. Please revise your inputs: """)
    
    if not country_b_bool:
        st.write(country_A_filter + """ does not have any pattern with """ + country_B_filter + """. """)
        st.write("""----Please select another pattern length. """)
    if not pattern_length_bool:
        if not country_b_bool:
            st.write(country_A_filter + """ does not have any pattern with length """ + str(pattern_length_filter[0])) 
            st.write("""----Please select another pattern length. """)
        else:
            st.write(country_A_filter + """ and """ + country_B_filter + """ do not have a pattern of length """ + str(pattern_length_filter[0]))
            st.write("""----Please select another pattern length. """)
    if not correlation_bool:
        st.write("""The pattern between """ + country_A_filter + """ and """ + country_B_filter + """ has no indexes pass the correlation threshold. """)
