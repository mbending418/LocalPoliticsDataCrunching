from typing import Optional, Literal
import os
import pandas as pd
import click

PartyType = Literal["DEM", "REP", "NOPTY"]  # Dem means Democrat. Rep means Republican. NOPTY mean No Party

BIRTH_YEAR = "birth_date"
PARTY = "party"
CITY = "city"


def find_voters_born_after_target_year(df, year: int, city: Optional[str], party: Optional[PartyType] = None):
    """
    searches a Pandas DataFrame representing voters for
    all democratic voters born after a target year
    Optionally restricting the search to a given city

    :param df: Pandas DataFrame of voters
    :param year: target birth year
    :param city: city to narrow the search to
    :param party: what political party to optionally narrow the search to
    :return:
    """
    if city is not None:
        df = df[df[CITY] == city]
    if party is not None:
        df = df[df[PARTY] == party]
    return df[df[BIRTH_YEAR] > year]


def find_ch_young_dems(boe_voter_csv):
    """
    Find all dems in Cleveland Heights under a certain age

    :param boe_voter_csv: board of elections csv file
    :return:
    """

    file_base = os.path.splitext(boe_voter_csv)[0]

    boe_df = pd.read_csv(boe_voter_csv)

    under_35_ch_dems = find_voters_born_after_target_year(boe_df, year=1989, city="CLEVELAND HTS", party="DEM")
    under_35_ch_dems.to_csv(f"{file_base}_under_35_dems.csv")

    under_25_ch_dems = find_voters_born_after_target_year(boe_df, year=1999, city="CLEVELAND HTS", party="DEM")
    under_25_ch_dems.to_csv(f"{file_base}_under_25_dems.csv")


@click.command()
@click.argument('filename', type=str)
def run_find_ch_young_dems(filename):
    print(filename)
    find_ch_young_dems(filename)


if __name__ == '__main__':
    run_find_ch_young_dems()
