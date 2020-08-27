# DraftMaster
# *Super preliminary alpha*
## Contributors welcomed!

Draftmaster gives you live drafting recommendations to start your season with your best foot forward.

Right now, I can only promise that it *mostly* works with Python 3, ESPN, windows 10, and the firefox/gecko webdriver.

I highly recommend creating a new environment to work in.

# What it does

DraftMaster maximizes your draft by suggesting you pick from the players with the highest opportunity cost with every pick.  DM tracks which players have been picked, what positions you need to fill, and when you get to pick.

Step 1 - calculate each positions' expected best pick given at your next pick.

If this the draft is a 10 person league, first round, 6th pick, then draftmaster calculates the expected points of the players available at the 15th and 26th picks.

Step 2 - Calculate the difference between each players projected points and their positions future expected max points and multiply by the probability that the player will be available at your next pick. If you don't have a starting spot available for a position, DM adjusts the projections for the expected number of games that a bench player will be needed for a given position.

<img src="https://render.githubusercontent.com/render/math?math=E(Max) = \sum(p(available) * points * p(player is best available))">

Step 3 - Make recommendations. Sort the players by opportunity cost from highest to lowest. Higher opportunity cost picks are suggested over lower opportunity cost.


