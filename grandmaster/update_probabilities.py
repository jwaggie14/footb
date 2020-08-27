import requests
from bs4 import BeautifulSoup
import pandas as pd

def p2f(x):
    return float(x.strip('%'))/100

def create_prob_pickle(teams, outputname, mapping_path, outputpath=""):
    score='standard' # other options to be added
    
    url = r"https://fantasyfootballcalculator.com/scenario-calculator"
    params = lambda x,teams,scoring: {'format':scoring,
              'num_teams':teams,
              'draft_pick':x}

    probabilities = {}
    html = {}
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
    dfs[['Name','Pos','Team','Bye','%','pick','espnid']].to_pickle(path+name)
    pass