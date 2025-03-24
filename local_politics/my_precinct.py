from utils.filter_dataframe import filter_by_mapping
from typing import Literal
import os
import pandas as pd

CapitalLetter = Literal["A", "B", "C", "D", "E", "F", "G",
                        "H", "I", "J", "K", "L", "M", "N",
                        "O", "P", "Q", "R", "S", "T", "U",
                        "V", "W", "X", "Y", "Z"]

PARTY = "party"
CITY = "city"
WARD = "ward"
PRECINCT = "pct"


def search_precinct_for_dems(df, city: str, ward: int, precinct: CapitalLetter):
    """
    searches a Pandas DataFrame representing voters for
    all voters in a particular ward/precinct in a particular city.

    (cities are divided up into wards which are divided up into precincts)

    :param df: Pandas DataFrame of voters
    :param city: city to search
    :param ward: ward to search
    :param precinct: precinct to search
    :return:
    """
    voter_filter = {
        PARTY: "DEM",
        CITY: city,
        WARD: ward,
        PRECINCT: precinct
    }
    return filter_by_mapping(df, voter_filter)


def find_dems_in_my_precinct(boe_voter_csv):
    """
    find all dems in my precinct

    :param boe_voter_csv: board of elections csv file
    :return:
    """

    file_base = os.path.splitext(boe_voter_csv)[0]

    boe_df = pd.read_csv(boe_voter_csv)
    my_precinct_df = search_precinct_for_dems(boe_df, city="CLEVELAND HTS", ward=3, precinct="D")
    my_precinct_df.to_csv(f"{file_base}_CH3D.csv")
