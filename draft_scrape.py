from selenium import webdriver 
import pandas as pd 
import numpy as np


class draft_monitor:
    def __init__(self, team_name):
        self.team_name = team_name.upper()
        self.driver = webdriver.Firefox()
        self.driver.get(r'https://www.espn.com')
        self.rosters = {}
        self.team_map = {}
        pass
    
    def configure_draft(self):
        self.update_rosters()
        self.teams = len(self.team_map)
        self.myteam = list(self.team_map.keys())[list(self.team_map.values()).index(self.team_name)]
        self.open_positions()
        self.rounds = self.empty_positions.sum()
        self.pick_order = (list(range(1,self.teams+1)) + list(range(self.teams,0,-1))) * (self.rounds // 2)
        if self.rounds % 2 == 1:
            self.pick_order += list(range(1,self.teams+1))
        self.current_pick = 1
        pass

    def round_(self):
        return self.current_pick - 1 // self.teams + 1
    
    def pick_(self):
        return self.current_pick - 1 % self.teams + 1
    
    def update_rosters(self,specific_team=None):
        teams = self.driver.find_elements_by_xpath("/html/body/div[1]/div[1]/section/div/div[2]/main/div/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/select/option")
        if specific_team is None:
            for t in teams:
                t.click()
                tnum = int(t.get_property('value'))
                team_ele = self.driver.find_elements_by_xpath("/html/body/div[1]/div[1]/section/div/div[2]/main/div/div/div[3]/div[1]/div[1]/div[2]/div[2]/div/section/div/div/div[2]/table/tbody/tr")
                team = pd.DataFrame([r.text.splitlines() for r in team_ele])[[0,1]].rename(columns={0:'position',1:'player'})
                team['player'] = team['player'].replace('Empty', np.nan)
                self.rosters[tnum] = team
                self.team_map[tnum] = t.text
        else:
            t = teams[specific_team]
            t.click()
            tnum = int(t.get_property('value'))
            team_ele = self.driver.find_elements_by_xpath("/html/body/div[1]/div[1]/section/div/div[2]/main/div/div/div[3]/div[1]/div[1]/div[2]/div[2]/div/section/div/div/div[2]/table/tbody/tr")
            team = pd.DataFrame([r.text.splitlines() for r in team_ele])[[0,1]].rename(columns={0:'position',1:'player'})
            team['player'] = team['player'].replace('Empty', np.nan)
            self.rosters[tnum] = team
            self.team_map[tnum] = t.text
        pass
    
    def open_positions(self):
        self.empty_positions = self.rosters[self.myteam][self.open_mask()]['position'].value_counts()
        pass
    
    def open_mask(self):
        return self.rosters[self.myteam]['player'].isna()
    

    def pick_history(self):
        self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/section/div/div[2]/main/div/div/div[3]/div[2]/div[2]/div/nav/ul/li[2]/button').click()
        pass

    def avail_players(self):
        self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/section/div/div[2]/main/div/div/div[3]/div[2]/div[2]/div/nav/ul/li[1]/button').click()
        pass

    def rpick_id(self,first_r, r, p):
        return f"/html/body/div[1]/div[1]/section/div/div[2]/main/div/div/div[3]/div[2]/div[2]/div/div/div[2]/div/div[2]/div{f'[{r}]' if first_r else ''}/div[2]/div/div[1]/div/div/div[3]/div[{p}]/div/div/div[2]/div/div[2]/div/div/div/div/div/div[1]/img[1]"
    
    def rpick_name(self,first_r, r, p):
        return f"/html/body/div[1]/div[1]/section/div/div[2]/main/div/div/div[3]/div[2]/div[2]/div/div/div[2]/div/div[2]/div{f'[{r}]' if first_r else ''}/div[2]/div/div[1]/div/div/div[3]/div[{p}]/div/div/div[2]/div/div[2]/div/div/div/div/div/div[2]/div[1]/span/span/a"

    def do_pick_id(self,r, p):
        return f"/html/body/div[1]/div[1]/section/div/div[2]/main/div/div/div[3]/div[2]/div[2]/div/div/div[2]/div/div[2]/div[{r}]/div[2]/div/div[1]/div/div/div[3]/div[{p}]/div/div/div[2]/div/div[2]/div/div/div/div/div/div[1]/img[1]"
    
    def do_pick_name(self,r, p):
        return f"/html/body/div[1]/div[1]/section/div/div[2]/main/div/div/div[3]/div[2]/div[2]/div/div/div[2]/div/div[2]/div[{r}]/div[2]/div/div[1]/div/div/div[3]/div[{p}]/div/div/div[2]/div/div[2]/div/div/div/div/div/div[2]/div[1]/span/span/a"

    def update(self):
        self.get_current_pick()
        self.pick_history()
    #     current_pick = 128
        cR = (self.current_pick-1) // self.teams + 1
        cP = (self.current_pick-1) % self.teams + 1
        picks_list = [(r,p) for r in range(1,cR) for p in range(1,self.teams+1)]
        picks_list = picks_list + [(cR, p) for p in range(1, cP+1)]
        pickids = [self.scrape_pick_ids(r,p) for r,p in picks_list]
        1+1
        self.avail_players()
        self.pickids = pickids
        pass

    def scrape_pick_ids(self, r,p):
        pick = self.pick_()
        first_round = pick <= self.teams
        if pick != self.teams * self.rounds:
            string = self.rpick_id(first_round,r,p)
            ns = self.rpick_name(first_round,r,p)
        else:
            string = self.do_pick_id(r,p)
            ns = self.do_pick_name(r,p)

        element = self.driver.find_element_by_xpath(string)
        imgref = element.get_property('src')
        beg = imgref.find('full') + 5
        end = imgref.find('.png')

        if beg == 4:
            beg = imgref.find('nfl/500/') + 8
            pid = imgref[beg:end]
        else:
            pid = int(imgref[beg:end])

        ne = self.driver.find_element_by_xpath(ns)
        name = ne.text
        return r,p,pid,name

    def get_current_pick(self, exception=None):
        if exception is None:
            exception = self.teams * self.rounds
            
        try:
            cpe = self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/section/div/div[2]/main/div/div/div[2]/div/div[2]/div/div[2]')
            picktxt = cpe.text
            beg = picktxt.find('PICK') + 5
            self.current_pick = int(picktxt[beg:]) - 1 
        except:
            self.current_pick = exception
        pass


    
    def process_update(self):
        self.update()
        dfpids = pd.DataFrame(self.pickids)
        dfpids.columns = ['round','pick','espn_id','espn_name']
        dfpids = dfpids.set_index('espn_id')
        return dfpids
    
    def filter_picks(self,df):
        dfp = self.process_update()
        df['picked'] = df['espn_id'].isin(dfp.index)
        df['round'] = df['espn_id'].map(dfp['round'])
        df['rpick'] = df['espn_id'].map(dfp['pick'])
        return df