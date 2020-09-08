from selenium import webdriver 
import pandas as pd 
import numpy as np

oc_mult = dict(zip(['QB','RB','WR','TE','K','DST'],[.3,.5,.5,.3,.15,.15]))

flex_positions = ['RB','WR','TE']

class draft_monitor:
    def __init__(self, team_name, driver='firefox', driver_path=None):
        """
        initializing the draft monitor will open a selenium window and define
        most of the parameters for your draft.
        
        Log into your ESPN account and open the draft lobby using the selenium
        window. 
        
        Parameters
        ----------
        team_name : STRING
            team_name needs to match your ESPN draft name. Unless you've changed
            your team name, it defaults to "Team Your-Last-Name"
        driver : STRING, optional
            Used to indicate which driver used by Selenium. The default is 'firefox'.
            Valid entries are:
                'firefox'
                'chrome'
                'edge'
                'safari'
            All other entries will raise an exception.

        Returns
        -------
        draft_monitor class object.

        """
        self.team_name = team_name.upper()
        ddriver = driver.lower().strip()
        if driver_path is None:
            if ddriver == 'firefox':
                self.driver = webdriver.Firefox()
            elif ddriver == 'chrome':
                self.driver = webdriver.Chrome()
            elif ddriver == 'edge':
                self.driver = webdriver.Edge()
            elif ddriver == 'safari':
                self.driver = webdriver.Safari()
            else:
                raise NotImplementedError(f"driver '{driver}' does not match any Selenium drivers.")
        else:
            if ddriver == 'firefox':
                self.driver = webdriver.Firefox(executable_path=driver_path)
            elif ddriver == 'chrome':
                self.driver = webdriver.Chrome(executable_path=driver_path)
            elif ddriver == 'edge':
                self.driver = webdriver.Edge(executable_path=driver_path)
            elif ddriver == 'safari':
                self.driver = webdriver.Safari(executable_path=driver_path)
            else:
                raise NotImplementedError(f"driver '{driver}' does not match any Selenium drivers.")
    
        self.driver.get(r'https://www.espn.com')
        self.rosters = {}
        self.team_map = {}
        pass
    
    def configure_draft(self):
        """
        Do not run this function until your draft room is up.
        
        This function will:
            populate the initial rosters for each team (with nans b/c theyre empty)
            figure out the number of teams
            figure out your draft picks
            figure out what positions are required for your league
        
        """
        self.update_rosters()
        self.teams = len(self.team_map)
        self.myteam = list(self.team_map.keys())[list(self.team_map.values()).index(self.team_name)]
        self.mypick = list(self.team_map.values()).index(self.team_name) + 1
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
        """
        This function scrapes the current team and rosters to keep track of 
        who has drafted who.
        
        If you only want to update 1 team (like yours), use the optional arg.
        "specific_team" which accepts an integer and correspond to the team's
        index within self.teams.
        """
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
            st = specific_team
            t = teams[st]
            t.click()
            tnum = int(t.get_property('value'))
            team_ele = self.driver.find_elements_by_xpath("/html/body/div[1]/div[1]/section/div/div[2]/main/div/div/div[3]/div[1]/div[1]/div[2]/div[2]/div/section/div/div/div[2]/table/tbody/tr")
            team = pd.DataFrame([r.text.splitlines() for r in team_ele])[[0,1]].rename(columns={0:'position',1:'player'})
            team['player'] = team['player'].replace('Empty', np.nan)
            self.rosters[tnum] = team
            self.team_map[tnum] = t.text
        pass
    
    def open_positions(self):
        """
        Finds and counts your unfilled starting roster positions.
        """
        self.empty_positions = self.rosters[self.myteam][self.open_mask()]['position'].value_counts().rename({'D/ST':'DST'})
        if 'FLEX' in self.empty_positions.index:
            self.need_flex = True
        else:
            self.need_flex = False
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
        return f"/html/body/div[1]/div[1]/section/div/div[2]/main/div/div/div[3]/div[2]/div/div/div/div[2]/div/div[2]/div{f'[{r}]' if first_r else ''}/div[2]/div/div[1]/div/div/div[3]/div[{p}]/div/div/div[2]/div/div[2]/div/div/div/div/div/div[1]/img[1]"
    
    def rpick_name(self,first_r, r, p):
        return f"/html/body/div[1]/div[1]/section/div/div[2]/main/div/div/div[3]/div[2]/div/div/div/div[2]/div/div[2]/div{f'[{r}]' if first_r else ''}/div[2]/div/div[1]/div/div/div[3]/div[{p}]/div/div/div[2]/div/div[2]/div/div/div/div/div/div[2]/div[1]/span/span/a"

    def do_pick_id(self,r, p):
        return f"/html/body/div[1]/div[1]/section/div/div[2]/main/div/div/div[3]/div[2]/div/div/div/div[2]/div/div[2]/div[{r}]/div[2]/div/div[1]/div/div/div[3]/div[{p}]/div/div/div[2]/div/div[2]/div/div/div/div/div/div[1]/img[1]"
    
      
    def do_pick_name(self,r, p):
        return f"/html/body/div[1]/div[1]/section/div/div[2]/main/div/div/div[3]/div[2]/div/div/div/div[2]/div/div[2]/div[{r}]/div[2]/div/div[1]/div/div/div[3]/div[{p}]/div/div/div[2]/div/div[2]/div/div/div/div/div/div[2]/div[1]/span/span/a"

    def update(self):
        """
        Scrapes the pick history to get a complete record of the drafting.
        
        Collects the entire draft history on every call to prevent errors in the
        history.        
        """
        self.get_current_pick(exception=1)
        if self.current_pick <0:
            self.avail_players()
            self.pickids = []
            return
        else:
            self.pick_history()
        #     current_pick = 128
            self.update_rosters(self.myteam)
            self.open_positions()
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
        "scrapes draft picks by id that matches the 'espn_id' column"
        pick = self.pick_()
        first_round = pick > self.teams
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
        "scrapes the current pick number"
        
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
    
    def map_empty_positions(self,df):
        self.open_positions()
        df['bench_mult'] = df['position'].map(oc_mult)
        df['needs'] = df['position'].map(self.empty_positions)
        df['needs'] = df['needs'].fillna(0)
        if self.need_flex:
            df['needs'] += np.where(df['position'].isin(flex_positions), 1, 0)
        
        df['oc_adj'] = np.where(df['needs'] <= 0,
                                df['bench_mult'],
                                1)
        return df
    
    
    def filter_picks(self,df):
        dfp = self.process_update()
        df['picked'] = df['espn_id'].isin(dfp.index.astype(str))
        df['round'] = df['espn_id'].map(dfp['round'])
        df['rpick'] = df['espn_id'].map(dfp['pick'])
        return df

