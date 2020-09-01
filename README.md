# GrandMaster
# *Super preliminary alpha*
## Contributors welcomed!

GrandMaster gives you live drafting recommendations to start your season with your best foot forward.

Right now, I can only promise that it *mostly* works with Python 3, ESPN, windows 10, and the firefox/gecko webdriver.

I highly recommend creating a new environment to work in.

# What it does

GrandMaster maximizes your draft by suggesting you pick from the players with the highest opportunity cost with every pick.  GM tracks which players have been picked, what positions you need to fill, and when you get to pick.

1. calculate each positions' expected best pick given at your next pick.

If this the draft is a 10 person league, first round, 6th pick, then draftmaster calculates the expected points of the players available at the 15th and 26th picks.

2. Calculate the difference between each players projected points and their positions future expected max points and multiply by the probability that the player will be available at your next pick. If you don't have a starting spot available for a position, GM adjusts the projections for the expected number of games that a bench player will be needed for a given position.

<img src="https://render.githubusercontent.com/render/math?math=E(Max) = \sum(p(available) * points * p(player is best available))">

3. Make recommendations. Sort the players by opportunity cost from highest to lowest. Higher opportunity cost picks are suggested over lower opportunity cost.


# How to Use it
I'm going to polish this over time. But at the moment, the best way to get this working is:
1. Copy this repo to a local folder
2. Create a python 3 conda environment with the anaconda package ```conda create --name NAME python=3 anaconda```
3. Install the selenium package and the gecko webdriver. see https://selenium-python.readthedocs.io/installation.html for detailed instructions
4. Install the ipython widgets. See https://ipywidgets.readthedocs.io/en/latest/user_install.html for instructions
3. Run the "Grandmaster.ipynb" notebook.
4. Draft your team from the web driver window.



# To do list (no particular order)
- turn this into a legit package
  - create a requirements.txt file for package management.
- Add support for other web drivers
- Add support for other hosts (sleeper, nfl, etc.)
- Add support for other score settings
- Create a GUI
- figure out a method for wider accessibility, (web-based, .exe, ???)

