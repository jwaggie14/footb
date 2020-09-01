import requests
from bs4 import BeautifulSoup
import pandas as pd

def p2f(x):
    return float(x.strip('%'))/100

def create_prob_pickle(teams, scoring, outputname, mapping_path):
    """
    teams: int, number of teams in league
    outputname: string, filename for the output probability pickle
    mapping_path: string, filepath for the mapping file. 
    scoring: string, valid entries are "standard", "ppr", "half-ppr", or "2qb"
    """
    
    
    score=scoring
    
    url = r"https://fantasyfootballcalculator.com/scenario-calculator"
    params = lambda x,teams,scoring: {'format':scoring,
              'num_teams':teams,
              'draft_pick':x}

    probabilities = {}
    html = {}
    print('1 of 4: scraping picks - this will take a minute')
    for i in range(1,201):
        test = requests.get(url,params(i,teams,score))
        if test.status_code == 200:
            soup = BeautifulSoup(test.text, 'html.parser')
            html[i] = test
            probabilities[i] = soup.select("table")
        else:
            print(f"{i} failed")
            print(test.status_code)

    df = pd.read_html(str(soup.find_all('table')[0]))
    print('2 of 4: scraping done - starting processing')
    dfs = None
    for k, table in probabilities.items():
        df = pd.read_html(str(table[0]))[0]
        df['pick'] = k
        if dfs is None:
            dfs = df
        else:
            dfs = dfs.append(df)
    
    mapping = pd.read_csv('probmap.csv')
    dfs = dfs.merge(mapping, how='left', left_on='Name', right_on='probname')
    dfs['%'] = dfs['%'].apply(p2f)
    dfs['espnid'] = dfs['espnid'].astype(str)
    dfs[['Name','Pos','Team','Bye','%','pick','espnid']].to_pickle(outputname)
    print(f'3 of 4: probabilities updated')
    print(f'4 of 4: pickle saved as {outputname}')
    pass


