import pandas as pd


def merge_metrics(overlap, origin_dfs):
    res_lists = []
    for key, value in overlap.items():
        df = pd.DataFrame(list(value), columns=["Accession"])
        for idx in key:
            suffix = f"_{idx}" if len(key) > 1 else ""
            df = pd.merge(df, origin_dfs[idx], on="Accession", how="left", suffixes=("", suffix))
        res_lists.append(df)
    return res_lists


def filter_metrics(df_list):
    keywords = ['Accession', 'Abundance Ratio', 'P-Value']

    filter_list = []
    for df in df_list:
        filter_list.append(df.filter(regex = '|'.join(keywords)))

    return filter_list