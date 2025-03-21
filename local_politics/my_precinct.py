from utils.filter_dataframe import filter_by_mapping
import os
import pandas as pd

PARTY = "party"
CITY = "city"
WARD = "ward"
PRECINCT = "pct"

def find_dems_in_my_precinct(boe_voter_csv):
    """
    find all dems in my precinct

    :param boe_voter_csv: board of elections csv file
    :return:
    """

    file_base = os.path.splitext(boe_voter_csv)[0]

    boe_df = pd.read_csv(boe_voter_csv)
    voter_filter = {
        PARTY: "DEM",
        CITY: "CLEVELAND HTS",
        WARD: 3,
        PRECINCT: "D"
    }
    my_precinct_df = filter_by_mapping(boe_df, voter_filter)
    my_precinct_df.to_csv(f"{file_base}_CH3D.csv")
