import grandmaster.draft_scrape as ds
import grandmaster.draft_logic as dl
from .update_probabilities import *
from .process_and_map_projections import *

def tell_me_what_to_do(players,prob,draft):
    players = draft.filter_picks(players)
    players = draft.map_empty_positions(players)
    np1, np2 = dl.next_picks(draft.pick_order,draft.myteam, draft.current_pick+1)
    px = dl.adj_probs(players,prob,np1,np2)
    return px