from utils.filter_dataframe import filter_by_mapping
from typing import Optional
import os
import click
import pandas as pd

NAME_LAST = "name_last"
NAME_FIRST = "name_first"
CITY = "city"


def find_voter_by_name(df, name_last: str, name_first: Optional[str] = None, city: Optional[str] = None):
    """
    searches a Pandas DataFrame representing voters for
    all voters with a particular name optionally narrowing down by city.

    :param df: Pandas DataFrame of voter info
    :param name_last: voters last name
    :param name_first: voters first name
    :param city: optionally the city to narrow it down
    :return:
    """
    voter_filter = {
        NAME_LAST: name_last,
    }
    if name_first is not None:
        voter_filter[NAME_FIRST] = name_first
    if city is not None:
        voter_filter[CITY] = city
    return filter_by_mapping(df, voter_filter)


def look_up_voters_by_name(boe_voter_csv,
                           name_last: str,
                           name_first: Optional[str] = None,
                           city: Optional[str] = None):
    """
    Find all voters at a given address from the Board of Elections CSV File

    :param boe_voter_csv: board of elections csv file
    :param name_last: voters last name
    :param name_first: voters first name
    :param city: optionally the city to narrow it down
    :return:
    """

    file_base = os.path.splitext(boe_voter_csv)[0]

    boe_df = pd.read_csv(boe_voter_csv)

    filtered_df = find_voter_by_name(boe_df, name_last, name_first, city)
    filtered_df.to_csv(f"{file_base}_name_search.csv")


@click.command
@click.argument("filename", type=str)
@click.argument("last_name", type=str)
@click.option("-n", "--first_name", default=None, help="optionally use the voters first name")
@click.option("-c", "--city", default=None, help="optional city to narrow the search down to")
def run_look_up_voters_by_name(filename, last_name, first_name, city):
    look_up_voters_by_name(filename, last_name, first_name, city)


if __name__ == '__main__':
    run_look_up_voters_by_name()
