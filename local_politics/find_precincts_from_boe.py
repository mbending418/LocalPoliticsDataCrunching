from utils.filter_dataframe import filter_by_column_value
import os
import pandas as pd

# standardized column headers from board of elections
CITY = "city"
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
    # narrow down the search to cleveland heights
    ch_df = filter_by_column_value(boe_df, column=CITY, value="CLEVELAND HTS")

    merged_df = voter_df.merge(ch_df[[NAME_LAST, NAME_FIRST, WARD, PRECINCT]], how='left',
                               left_on=[NAME_LAST, NAME_FIRST],
                               right_on=[NAME_LAST, NAME_FIRST])

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
    # narrow down the search to cleveland heights
    ch_df = filter_by_column_value(boe_df, column=CITY, value="CLEVELAND HTS")

    # merge columns with address info into one column
    ch_df[FULL_ADDRESS] = (ch_df[HOUSE_NUMBER].astype(str) + " " + ch_df[PREFIX_DIRECTION].fillna("") + " "
                           + ch_df[STREET]).replace("  ", " ", regex=True)

    merged_df = voter_df.merge(ch_df[[FULL_ADDRESS, WARD, PRECINCT]], how='left',
                               left_on=[FULL_ADDRESS],
                               right_on=[FULL_ADDRESS])

    merged_df[[NAME_LAST_VOTER_CSV, NAME_FIRST_VOTER_CSV, ADDRESS_CSV, WARD, PRECINCT]].to_csv(
        f"{file_base}"f"_added_precinct_by_address.csv")
