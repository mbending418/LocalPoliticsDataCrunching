from utils.filter_dataframe import filter_by_mapping
from typing import Optional
import os
import pandas as pd


BIRTH_YEAR = "birth_date"
PARTY = "party"
CITY = "city"


def find_dems_born_after_target_year(df, year: int, city: Optional[str]):
    """
    searches a Pandas DataFrame representing voters for
    all democratic voters born after a target year
    Optionally restricting the search to a given city

    :param df: Pandas DataFrame of voters
    :param year: target birth year
    :param city: city to narrow the search to
    :return:
    """
    voter_filter = {
        PARTY: "DEM",
        CITY: city,
    }
    filtered_df = filter_by_mapping(df, voter_filter)
    return filtered_df[filtered_df[BIRTH_YEAR] > year]


def find_young_dems(boe_voter_csv):
    """
    Find all dems in Cleveland Heights under a certain age

    :param boe_voter_csv: board of elections csv file
    :return:
    """

    file_base = os.path.splitext(boe_voter_csv)[0]

    boe_df = pd.read_csv(boe_voter_csv)

    under_35_ch_dems = find_dems_born_after_target_year(boe_df, year=1989, city="CLEVELAND HTS")
    under_35_ch_dems.to_csv(f"{file_base}_under_35_dems.csv")

    under_25_ch_dems = find_dems_born_after_target_year(boe_df, year=1999, city="CLEVELAND HTS")
    under_25_ch_dems.to_csv(f"{file_base}_under_25_dems.csv")
