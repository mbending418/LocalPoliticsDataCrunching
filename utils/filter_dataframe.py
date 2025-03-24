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
