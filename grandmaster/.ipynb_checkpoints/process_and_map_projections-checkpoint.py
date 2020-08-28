import pandas as pd
import numpy as np

def process_projections(projection_path,idmap_path,output_path):
    proj = pd.read_csv(projection_path)
    proj = proj[proj['position'].isin(['RB','QB','WR','TE','K','DST'])]

    espnidmap = pd.read_excel(idmap_path)

    proj = proj.merge(espnidmap, how='left', on='player')
    proj = proj.dropna(subset=['adp'])
    proj = proj.drop_duplicates(subset=['playerId'])
    proj['picked'] = False
    proj['blacklist'] = False
    proj.to_pickle(output_path)
    pass