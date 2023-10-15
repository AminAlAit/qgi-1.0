from datetime import datetime as dt
from pathlib  import Path
import pandas as pd
import numpy  as np
import uuid
import glob
import os 
import sys
if "FIFADash" in str(Path(os.path.dirname(os.getcwd()))):
    sys.path.insert(1, "\\".join(str(Path(os.path.dirname(os.getcwd()))).split("\\")[:-2]) + "\\Projects\\FIFADash\\trojan\\data engine")
else:
    sys.path.insert(1, "\\".join(str(Path(os.path.dirname(os.getcwd()))).split("\\")[:-1]) + "\\trojan\\trojan\\data engine")
import dataPrep as dp


INDEX_STOCKER_FILE_NAME_COL        = 0
INDEX_STOCKER_INDEX_COL            = 1
INDEX_STOCKER_ID_COL               = 2
INDEX_STOCKER_ORG_COL              = 3
INDEX_STOCKER_PATTERNIZED_COL      = 4
INDEX_STOCKER_LAST_UPDATED_COL     = 5
INDEX_STOCKER_MAIN_PATH_COL        = 6
INDEX_STOCKER_PATH_COL             = 7
INDEX_STOCKER_EXEC_DURATION_COL    = 8

MAINs_STOCKER_ID_COL               = 0
MAINs_STOCKER_MAIN_INDEX_NAME_COL  = 1
MAINs_STOCKER_ORG_COL              = 2
MAINs_STOCKER_CUTTED_COL           = 3
MAINs_STOCKER_MAIN_PATH_COL        = 4
MAINs_STOCKER_SINGLE_SUBS_PATH_COL = 5
MAINs_STOCKER_SUBS_COUNT_COL       = 6
MAINs_STOCKER_STOCKED_DATE_COL     = 7

IDs_GROUP_ID                       = 0
IDs_GROUP_INDEX                    = 1
IDs_GROUP_ORG                      = 2
IDs_GROUP_MAIN_NAME                = 3
IDs_GROUP_MAIN_PATH                = 4
IDs_GROUP_SUB_PATH                 = 5


### Reading MAINs_stocker
dp.update_MAINs_stocker_SUBs_count()

MAINs_stocker = dp.get_MAINs_stocker()

### Adding new MAINs, Updating MAINs Stocker and configuring "Cutted"
## First we check if any of our MAINs were never registered in the MAINs stocker. 
## If so, these fresh new MAINs are added to the stocker with their 'Cutted' status set to 'False'
## The code then checks if the MAIN is in the stocker then does two checks on them: 
## Is the last modification date greater (newer) then the stocking date, and also checks if
## If the MAIN has 0 SUBs. If any of these checks is 'True', the MAIN's 'Cutted' status is set 
## to 'False', and their stocking date is updated. 
for MAIN in dp.get_MAINs_to_cut():
    ## MAIN is not in the stocker, add it and by default the 'Cutted' status is set to 'False'
    if MAIN not in list(MAINs_stocker["MAIN Path"]):
        dp.add_MAIN_to_stocker(MAIN)
    
    ## It IS in the stocker, but is it outdated? 
    else:
        # Get its index number 
        index_number                   = list(MAINs_stocker["MAIN Path"]).index(MAIN)
        # Get last modification date of this MAIN
        last_modification_date_of_MAIN = dp.get_modification_date(MAIN)
        # Get date when this MAIN has been last stocked
        stocked_date_of_MAIN           = dt.strptime(MAINs_stocker["Stocked Date"][index_number], "%Y-%m-%d %H:%M:%S")
        
        ## Check if the last modification of this MAIN is beyond its stocked date, then this MAIN is outdated
        if last_modification_date_of_MAIN > stocked_date_of_MAIN:
            # so we first set its 'cutted' status to False
            dp.set_cutted_status_of_this_MAIN(MAIN, False)
            # Then we update its 'Stocked Date'
            dp.update_MAIN_stocking_date(MAIN)
        
        # Let's also check if these MAINs have some SUBs
        elif dp.get_SUBs_Count_of_this_MAIN(MAIN) == 0:
            # If not, then we first set its 'cutted' status to False
            dp.set_cutted_status_of_this_MAIN(MAIN, False)
            # Then we update its 'Stocked Date'
            dp.update_MAIN_stocking_date(MAIN)

#dp.get_MAINs_stocker()
#dp.get_index_stocker()

### Selecting need-to-be `Cutted` MAINs
MAINs_stocker          = dp.get_MAINs_stocker()
MAINs_to_cut_No_SUBs   = [] # list will be filled with MAINs that have no recorded SUBs
MAINs_to_cut_with_SUBs = [] # list will be filled with MAINs that HAVE SUBs

## This loop will browse all registered MAINs and picks out only those with 'Cutted' status set to 'False',
## and stage them for cutting
for i in range(len(MAINs_stocker["MAIN Path"])):
    if MAINs_stocker.iloc[i, MAINs_STOCKER_SUBS_COUNT_COL] == 0:
        MAINs_to_cut_No_SUBs.append(i)
    elif MAINs_stocker.iloc[i, MAINs_STOCKER_SUBS_COUNT_COL] > 0:
        if not MAINs_stocker.iloc[i, MAINs_STOCKER_CUTTED_COL]:
            MAINs_to_cut_with_SUBs.append(i)

## Now we have a list of MAINs to cut
#MAINs_to_cut_with_SUBs
#MAINs_to_cut_No_SUBs

### Dealing with IDs
MAINs_IDs = []
for MAIN_index_number in MAINs_to_cut_with_SUBs:
    #IDs1 = []
    IDs2 = []
    
    ### Method 1
    ## That means we need to collect these SUBs' IDs
    # So we take a slice from the `index_stocker` such that the "MAIN Path" in `index_stocker` is equal to the MAIN path of the MAIN_index_number
    # that way we can isolate the SUBs and thus extract their IDs
    #index_stocker = dp.slice_df(dp.get_index_stocker(), MAINs_stocker.iloc[MAIN_index_number, MAINs_STOCKER_MAIN_PATH_COL], "MAIN Path")
    #
    # We then go over the column, extracting every ID substring from each value
    #for i in index_stocker["Index"]:
    #    IDs1.append(i.split("----")[INDEX_STOCKER_FILE_NAME_COL][:8])

    ### Method 2
    MAIN_Path = MAINs_stocker.iloc[MAIN_index_number, MAINs_STOCKER_MAIN_PATH_COL]
    MAIN_SINGLE_SUBs_Path = "\\".join(MAIN_Path.split("\\")[:-1]) + "\\SINGLE_SUBs\\"
    if os.path.exists(MAIN_SINGLE_SUBs_Path):
        Index_SINGLE_SUB_files = glob.glob(MAIN_SINGLE_SUBs_Path + "/*Index_SINGLE_SUB.csv")
        if len(Index_SINGLE_SUB_files) > 0:
            for SINGLE_SUB in Index_SINGLE_SUB_files:
                SINGLE_SUB = SINGLE_SUB.split("\\")[-1]
                IDs2.append(SINGLE_SUB.split("----")[1][:8])
    
    MAINs_IDs.append(IDs2)
#MAINs_IDs


### Cutting MAINs
IDs_index_names_stocker_from_MAINs = []

## Looping over MAINs (index numbers) that have SUBs, not creating new IDs
if len(MAINs_IDs) == len(MAINs_to_cut_with_SUBs):
    for i in range(len(MAINs_to_cut_with_SUBs)):
        ## Getting the MAIN's path
        MAIN_in_the_loop = MAINs_stocker.iloc[MAINs_to_cut_with_SUBs[i], 4]
        ## Cutting the MAIN while providing the IDs list, saving results in list
        IDs_index_names_stocker_from_MAINs.append(dp.MAINs_cutter(MAIN_in_the_loop, passed_IDs = MAINs_IDs[i]))
        ## Setting `Cutted` of this MAIN to True
        dp.set_cutted_status_of_this_MAIN(MAIN_in_the_loop, True)
else:
    print("Impossible Exception Reached")

## Looping over MAINs (index numbers) that have no SUBs (new MAINs), creating new IDs
for i in range(len(MAINs_to_cut_No_SUBs)):
    ## Getting the MAIN's path
    MAIN_in_the_loop = MAINs_stocker.iloc[MAINs_to_cut_No_SUBs[i], 4]
    ## Cutting the MAIN, saving results in list
    IDs_index_names_stocker_from_MAINs.append(dp.MAINs_cutter(MAIN_in_the_loop))
    ## Setting `Cutted` of this MAIN to True
    dp.set_cutted_status_of_this_MAIN(MAIN_in_the_loop, True)


### Updating Index Stocker
for IDs_group in IDs_index_names_stocker_from_MAINs:
    MAIN_in_the_loop = list(set(IDs_group["MAIN Path"]))[0]
    
    ## Checking if MAIN is in to index_stocker
    # if so, that means it has SUBs in the index_stocker
    if MAIN_in_the_loop in list(dp.get_index_stocker().iloc[:, INDEX_STOCKER_MAIN_PATH_COL]):
        ## filtering index_stocker to get the slice about the MAIN we are dealing with
        MAIN_sliced_index_stocker = dp.slice_df(dp.get_index_stocker(), MAIN_in_the_loop, "MAIN Path")
        
        ## We only keep the newly cut indexes and edit their info (Index, ID, Org, MAIN Path), and discard the rest
        discard_these_file_names = []
        IDs                      = []
        file_names               = []

        for sub in IDs_group["ID"]:
            i = 0
            for full in MAIN_sliced_index_stocker.iloc[:, INDEX_STOCKER_FILE_NAME_COL]:
                
                if sub in full:
                    IDs.append(sub)
                    file_names.append(full)
                    break
                i += 1

            if i == len(MAIN_sliced_index_stocker.iloc[:, INDEX_STOCKER_FILE_NAME_COL]):
                discard_these_file_names.append(full)

        ## edit info for this row
        for i in range(len(IDs)):
            index_index_number = list(dp.get_index_stocker().iloc[:, INDEX_STOCKER_FILE_NAME_COL]).index(file_names[i])
            index_path         = dp.get_index_stocker().iloc[index_index_number, INDEX_STOCKER_PATH_COL]
            org_name           = IDs_group.iloc[list(IDs_group["ID"]).index(IDs[i]), IDs_GROUP_ORG]
            index_name         = IDs_group.iloc[list(IDs_group["ID"]).index(IDs[i]), IDs_GROUP_INDEX]
            MAIN_Path          = list(set(IDs_group["MAIN Path"]))[0]

            dp.set_ID_of_this_index(index_path, IDs[i])
            dp.set_org_name_of_this_index(index_path, org_name)
            dp.set_Index_name_of_this_index(index_path, index_name)
            dp.set_MAIN_Path_of_this_index(index_path, MAIN_Path)
        
        discard_these_indexes = []
        ## discard these duplicated indexes
        for file_name in discard_these_file_names:
            print("----")
            print("REMOVING:")
            print(file_name)
            print(dp.get_index_stocker().iloc[list(dp.get_index_stocker().iloc[:, INDEX_STOCKER_FILE_NAME_COL]).index(file_name), INDEX_STOCKER_INDEX_COL])
            discard_these_indexes.append(list(dp.get_index_stocker().iloc[:, INDEX_STOCKER_FILE_NAME_COL]).index(file_name))
        dp.delete_list_indexes_from_index_stocker(list(set(discard_these_indexes)))
    
    # Otherwise, we are dealing with MAINs that are not in the index stocker, so we need to add the MAINs' SUBs into it
    else:
        for i in range(len(IDs_group)):
            SUB_index_path  = IDs_group.iloc[i, IDs_GROUP_SUB_PATH]
            index_ID        = IDs_group.iloc[i, IDs_GROUP_ID]
            index_Org       = IDs_group.iloc[i, IDs_GROUP_ORG]
            index_MAIN_path = IDs_group.iloc[i, IDs_GROUP_MAIN_PATH]
            index_name      = IDs_group.iloc[i, IDs_GROUP_INDEX]
            index_MAIN_name = IDs_group.iloc[i, IDs_GROUP_MAIN_NAME]

            dp.add_index_to_stocker(SUB_index_path)
            dp.set_ID_of_this_index(SUB_index_path, index_ID)
            dp.set_org_name_of_this_index(SUB_index_path, index_Org)
            dp.set_Index_name_of_this_index(SUB_index_path, index_name)
            dp.set_MAIN_Path_of_this_index(SUB_index_path, index_MAIN_path)

#dp.get_index_stocker()