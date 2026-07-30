import pandas as pd
from itertools import combinations

def generate_sets(df_list : list[pd.DataFrame]):

    df_sets = [set(x['Accession']) for x in df_list]

    return df_sets


def find_intersection(set_list: list[set]):

    n = len(set_list)

    all_indices = set(range(n))

    regions = {}


    for k in range(n, 0, -1):
        for indices in combinations(range(n), k):
            overlap = set.intersection(*(set_list[i] for i in indices))

            for i in all_indices - set(indices):
                overlap -= set_list[i]

            regions[indices] = overlap
    return regions
