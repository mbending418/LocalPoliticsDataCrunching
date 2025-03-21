from utils.filter_dataframe import filter_by_mapping
import os
import pandas as pd

BIRTH_YEAR = "birth_date"
PARTY = "party"
CITY = "city"


def find_young_dems(boe_voter_csv):
    """
    Find all dems in Cleveland Heights under a certain age

    :param boe_voter_csv: board of elections csv file
    :return:
    """

    file_base = os.path.splitext(boe_voter_csv)[0]

    boe_df = pd.read_csv(boe_voter_csv)
    voter_filter = {
        PARTY: "DEM",
        CITY: "CLEVELAND HTS",
    }
    ch_dems_df = filter_by_mapping(boe_df, voter_filter)

    under_35_ch_dems = ch_dems_df[ch_dems_df[BIRTH_YEAR] > 1989]
    under_35_ch_dems.to_csv(f"{file_base}_under_35_dems.csv")

    under_25_ch_dems = ch_dems_df[ch_dems_df[BIRTH_YEAR] > 1999]
    under_25_ch_dems.to_csv(f"{file_base}_under_25_dems.csv")