def filter_by_column_value(df, column, value, keep: bool = True):
    """
    filter a dataframe and only keep/discard entries with a 'column' entry equal to 'value'

    eg. filter_by_column_value(df, 'city', 'boston', bool=True) will return a dataframe
    of all entries where the 'city' column has value 'boston'

    :param df: pandas dataframe
    :param column: column header/index
    :param value: value at the header/key
    :param keep: Set to true to keep matches, false to discard them
    :return: filtered pandas dataframe
    """
    if keep:
        return df[df[column] == value]
    else:
        return df[df[column] != value]


def filter_by_mapping(df, mapping):
    """
    use a key value mapping to filter out
    entries in a dataframe
    use None in the mapping for NaN

    eg. mapping={'city' : 'boston', 'age', '15'}
    will grab all entries where the 'city' column is 'boston'
    and the 'age' column is '15'

    :param df: pandas dataframe
    :param mapping: a dictionary mapping columns to values
    :return: filtered pandas dataframe
    """
    for key, value in mapping.items():
        if value is None:
            df = df[df[key].isna()]
        else:
            df = df[df[key] == value]
    return df
