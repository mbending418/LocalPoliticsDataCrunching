from utils.filter_dataframe import filter_by_column_value, filter_by_mapping
from typing import Literal, Optional, Dict
import pandas as pd
import os

SPRING_2024 = "P_03_19_2024"  # Partisan Primary
GENERAL_2023 = "G_11_07_2023"  # General Election (non partisan)
FALL_2023 = "S_08_08_2023"  # Special Election (non partisan)
GENERAL_2022 = "G_11_08_2022"  # General Election (non partisan)
FALL_2022 = "P_08_02_2022"  # Partisan Primary (special)
SPRING_2022 = "P_05_03_2022"  # Partisan Primary
GENERAL_2021 = "G_11_02_2021"  # General Election (non partisan)
SPECIAL_2021 = "P_09_14_2021"  # Non-Partisan Primary/Special
PRIMARY_2021 = "P_08_03_2021"  # Partisan Primary
GENERAL_2020 = "G_11_03_2020"  # General Election (non partisan)

HowVoted = Optional[Literal["Y", "D", "R"]]
# Y means "Yes" (used for non-partisan elections)
# D means "Democrat" (meaning they pulled a democratic ballot in a partisan primary)
# R means "Republican" (meaning they pulled a republican ballot in a partisan primary)
# None means they didn't vote in that election

FirstTimeFall2023 = {
    FALL_2023: "Y",
    GENERAL_2022: None,
    FALL_2022: None,
    SPRING_2022: None,
    GENERAL_2021: None,
    SPECIAL_2021: None,
    PRIMARY_2021: None,
    GENERAL_2020: None

}

FirstTimeGeneral2023 = {
    GENERAL_2023: "Y",
    FALL_2023: None,
    GENERAL_2022: None,
    FALL_2022: None,
    SPRING_2022: None,
    GENERAL_2021: None,
    SPECIAL_2021: None,
    PRIMARY_2021: None,
    GENERAL_2020: None
}

FirstTimeDemSpring2024 = {
    SPRING_2024: "D",
    GENERAL_2023: None,
    FALL_2023: None,
    GENERAL_2022: None,
    FALL_2022: None,
    SPRING_2022: None,
    GENERAL_2021: None,
    SPECIAL_2021: None,
    PRIMARY_2021: None,
    GENERAL_2020: None
}


def find_voters_by_history(df: pd.DataFrame, voting_history: Dict[str, HowVoted]):
    """
    find the voters in a voter database who voted with a particular voting history

    :param df: pandas dataframe for the voter database
    :param voting_history: dict mapping the election header to how they voted.
    :return: pandas dataframe of filtered voters
    """

    return filter_by_mapping(df, voting_history)


def find_new_voters(boe_voter_csv):
    """
    takes in a board of elections voter csv and filters out
    new democratic voters in cleveland heights

    :param boe_voter_csv:
    :return:
    """
    file_base = os.path.splitext(boe_voter_csv)[0]

    boe_df = pd.read_csv(boe_voter_csv)
    ch_df = filter_by_column_value(df=boe_df, column="city", value="CLEVELAND HTS")
    ch_dems_df = filter_by_column_value(df=ch_df, column="party", value="DEM")
    ch_dems_df.to_csv(f"{file_base}_ch_dems.csv")

    new_fall_2023_df = find_voters_by_history(ch_df, FirstTimeFall2023)
    new_fall_2023_df.to_csv(f"{file_base}_new_fall_2023.csv")

    new_dems_fall_2023_df = find_voters_by_history(ch_dems_df, FirstTimeFall2023)
    new_dems_fall_2023_df.to_csv(f"{file_base}_new_dems_fall_2023.csv")

    new_general_2023_df = find_voters_by_history(ch_df, FirstTimeGeneral2023)
    new_general_2023_df.to_csv(f"{file_base}_new_general_2023.csv")

    new_dems_general_2023_df = find_voters_by_history(ch_dems_df, FirstTimeGeneral2023)
    new_dems_general_2023_df.to_csv(f"{file_base}_new_dems_general_2023.csv")

    new_dems_spring_2024_df = find_voters_by_history(ch_dems_df, FirstTimeDemSpring2024)
    new_dems_spring_2024_df.to_csv(f"{file_base}_new_dems_spring_2024.csv")