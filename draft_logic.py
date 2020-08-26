import pandas as pd
import numpy as np
from scipy.stats import poisson
import statsmodels.api as sm

def predonadp(x):
    X = x['adp']
    X = sm.add_constant(X)
    y = x['points']
    mod = sm.OLS(y,X)
    res = mod.fit()
    pred = res.predict(X)
    return pred

def regonadp(x):
    X = x['adp']
    X = sm.add_constant(X)
    y = x['points']
    mod = sm.OLS(y,X)
    res = mod.fit()
    return res

# df = pd.read_csv(r'C:\Users\james.whiting\OneDrive - Shell\Documents\ffa_customrankings2020-0.csv')

pos_mask = df['position'].isin(['RB','QB','WR','TE','K','DL'])

df = df.dropna(subset=['adp']).sort_values('adp')

regressions = {pos:regonadp(df[df['position']==pos]) for pos in df.position.unique()}

df['adp_points'] = df.dropna(subset=['adp']).groupby('position').apply(predonadp).reset_index(level=0, drop=True)
df['blend'] = (df['points'] + df['adp_points']) / 2

PROJ = 'blend'

df = df[pos_mask]

df = df.reset_index(drop=True)

df['position'] = df['position'].replace('DL','D/ST')
oc_mult = dict(zip(['QB','RB','WR','TE','K','D/ST'],[.3,.5,.5,.3,.15,.15]))
df['bench_mult'] = df['position'].map(oc_mult)

df['blacklist'] = False

df['bench_adj'] = df['position'].map(oc_mult)

df = df.reset_index(drop=True)

teams = 12
rounds = 16
mypick = 6
pick_order = (list(range(1,teams+1)) + list(range(teams,0,-1))) * (rounds//2)

mypick = 5
this_pick = 35 # 1 indexed
next_pick = pick_order.index(mypick,this_pick) + 1
next_pick2 = pick_order.index(mypick,next_pick) + 1

next_pick, next_pick2

df['picked'] = df.index < this_pick

positions = ['QB','RB','WR','TE','K','D/ST']

roster_needs = ['RB','TE','K','D/ST']
need_flex = False

df['flex_position'] = df['position'].isin(['RB','WR','TE'])

fdf = df[~df['picked'] & ~df['blacklist']].copy()
fdf['need_pos'] = fdf['position'].isin(roster_needs) | (fdf['flex_position'] & need_flex)

fdf['multiplier'] = ~fdf['need_pos'] * fdf['bench_mult'] + fdf['need_pos']

fdf['prob_picked1'] = (fdf.apply(lambda x: poisson.cdf(next_pick, x['adp']), axis=1).fillna(0))
fdf['prob_picked2'] = (fdf.apply(lambda x: poisson.cdf(next_pick2, x['adp']), axis=1).fillna(0))
fdf['include1'] = fdf['prob_picked1'] > 0.01
fdf['include2'] = fdf['prob_picked2'] > 0.01
fdf['prob_avail1'] = (1 - fdf['prob_picked1']) * fdf['include1']
fdf['prob_avail2'] = (1 - fdf['prob_picked2']) * fdf['include2']

fdf['points_picked1'] = fdf['prob_picked1'] * fdf[PROJ]
fdf['points_picked2'] = fdf['prob_picked2'] * fdf[PROJ]
fdf['points_avail1'] = fdf['prob_avail1'] * fdf[PROJ]
fdf['points_avail2'] = fdf['prob_avail2'] * fdf[PROJ]

oc1cols = ['prob_picked1','prob_avail1','points_picked1','points_avail1']
oc2cols = ['prob_picked2','prob_avail2','points_picked2','points_avail2']

oc1 = fdf.groupby('position')[oc1cols].sum()
oc1['points_picked1'] = oc1['points_picked1'] / oc1['prob_picked1']
oc1['points_avail1'] = oc1['points_avail1'] / oc1['prob_avail1']

oc1['oc'] = oc1['points_picked1'] - oc1['points_avail1']
oc1['adj_oc'] = oc1['oc']

oc1.round(2)

oc2 = fdf.groupby('position')[oc2cols].sum()
oc2['points_picked2'] = oc2['points_picked2'] / oc2['prob_picked2']
oc2['points_avail2'] = oc2['points_avail2'] / oc2['prob_avail2']

oc2['oc'] = oc2['points_picked2'] - oc2['points_avail2']

oc2.round(2)




