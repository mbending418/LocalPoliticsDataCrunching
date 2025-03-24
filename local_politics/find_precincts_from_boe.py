from typing import Optional, Literal, Union, List, Any
import os
import pandas as pd

PartyType = Literal["DEM", "REP", "NOPTY"]

# standardized column headers from board of elections
CITY = "city"
PARTY = "party"
NAME_LAST = "name_last"
NAME_FIRST = "name_first"
WARD = "ward"
PRECINCT = "pct"
HOUSE_NUMBER = "house_no"
PREFIX_DIRECTION = "pre_dir"  # N, S, E, W, etc
STREET = "street"

# augmented column headers for combined columns from the board of elections
FULL_ADDRESS = "full_address"

# column headers from voter_csv
NAME_LAST_VOTER_CSV = "Last Name"
NAME_FIRST_VOTER_CSV = "First Name"
ADDRESS_CSV = "Address"


def add_precincts_to_voter_df(voter_df, boe_df, match_on: Union[Any, List[Any]],
                              city: Optional[str] = None,
                              party: Optional[PartyType] = None):
    """

    :param voter_df: df of voter data
    :param boe_df:  df of voter data from boe (that includes precinct information)
    :param match_on: which columns to use to match voters from the boe_df to the voter_df
    :param city: optionally restrict boe search to a given city
    :param party: optionally restrict boe search to a particular politics party
    :return:
    """
    if city is not None:
        boe_df = boe_df[boe_df[CITY] == city]
    if party is not None:
        boe_df = boe_df[boe_df[PARTY] == party]

    if not isinstance(match_on, list):
        match_on = [match_on]
    boe_slice = match_on + [WARD, PRECINCT]

    return voter_df.merge(boe_df[boe_slice], how='left',
                          left_on=match_on,
                          right_on=match_on)


def add_precincts_by_name(voter_csv, boe_voter_csv):
    """
    For each voter in the voter_csv
    look them up in the boe_voter_csv
    and add their precinct and ward
    matches on voter name

    :param voter_csv: csv of voters
    :param boe_voter_csv: board of election csv of voter information
    :return: 
    """""

    file_base = os.path.splitext(voter_csv)[0]

    # load voter df and set names to upper case
    voter_df = pd.read_csv(voter_csv)
    voter_df[NAME_LAST] = voter_df[NAME_LAST_VOTER_CSV].astype(str).str.upper()
    voter_df[NAME_FIRST] = voter_df[NAME_FIRST_VOTER_CSV].astype(str).str.upper()

    boe_df = pd.read_csv(boe_voter_csv)

    merged_df = add_precincts_to_voter_df(voter_df=voter_df,
                                          boe_df=boe_df,
                                          match_on=[NAME_LAST, NAME_FIRST],
                                          city="CLEVELAND HTS")

    merged_df[[NAME_LAST_VOTER_CSV, NAME_FIRST_VOTER_CSV, ADDRESS_CSV, WARD, PRECINCT]].to_csv(
        f"{file_base}"f"_added_precinct_by_name.csv")


def add_precincts_by_address(voter_csv, boe_voter_csv):
    """
    For each voter in the voter_csv
    look them up in the boe_voter_csv
    and add their precinct and ward
    matches on street address

    :param voter_csv: csv of voters
    :param boe_voter_csv: board of election csv of voter information
    :return: 
    """""

    file_base = os.path.splitext(voter_csv)[0]

    # load voter df and set names to upper case
    voter_df = pd.read_csv(voter_csv)
    voter_df[FULL_ADDRESS] = voter_df[ADDRESS_CSV].astype(str).str.upper()

    boe_df = pd.read_csv(boe_voter_csv)

    # merge columns with address info into one column
    boe_df[FULL_ADDRESS] = (boe_df[HOUSE_NUMBER].astype(str) + " " + boe_df[PREFIX_DIRECTION].fillna("") + " "
                            + boe_df[STREET]).replace("  ", " ", regex=True)

    merged_df = add_precincts_to_voter_df(voter_df=voter_df,
                                          boe_df=boe_df,
                                          match_on=FULL_ADDRESS,
                                          city="CLEVELAND HTS")

    merged_df[[NAME_LAST_VOTER_CSV, NAME_FIRST_VOTER_CSV, ADDRESS_CSV, WARD, PRECINCT]].to_csv(
        f"{file_base}"f"_added_precinct_by_address.csv")
