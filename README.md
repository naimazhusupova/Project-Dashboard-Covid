# Project-Dashboard-Covid

Software Heritage Repository:

[![SWH](https://archive.softwareheritage.org/badge/swh:1:dir:4344038aa64c26473fefb27c4dd8cca0c4748fc3/)](https://archive.softwareheritage.org/swh:1:dir:4344038aa64c26473fefb27c4dd8cca0c4748fc3;origin=https://github.com/naimazhusupova/Project-Dashboard-Covid;visit=swh:1:snp:2f48c1ea827e9550fc13ff660892cbac08d5a9a4;anchor=swh:1:rev:e9ceed24df5c4a852c30a152e7a741dbfdad9efc)

This project repository contains the description, tools and instructions to replicate our dashboard with information about Covid-19. You can check the deployed dashboard [here](https://share.streamlit.io/naimazhusupova/project-dashboard-covid/main/plot_data.py) (Streamlit Cloud).

For this dashboard we use Streamlit for the vizualization based on a dataset [COVID-19 Dataset by Our World in Data](https://github.com/owid/covid-19-data/blob/master/public/data/README.md) 

Our dashboard is interactive and allows the user to:
1. Select which countries to display (among a pre-defined list).
2. Select which time period to display (i.e. user could choose start and finish dates).
3. Select which variable(s) to display: number / cumulated number / 7-day rolling average of confirmed cases / deaths / (recovered).
4. Select to show the peak when cumulated number was chossen.

## Installing Dependencies

Instead of installing every package manually we created a requirements.txt file and by running it once, all the necessary packages will be installed.

Follow the next steps in order to install all required dependencies (e.g. Pandas, Matplotlib, Streamlit, ...):

Part 1
1. If you do not have Anaconda, install it on your computer in accordance with your operating system
2. You can find the instructions [here]( https://docs.anaconda.com/anaconda/install/) based on your operating system

Part 2
1. Open Anaconda Navigator
2. Create new environment based on the settings:
    - Click on Environments
    - Click on 'Create'
    - Name an environment (for example: My_Environment)
    - Choose Python version 3.8.12
    - Click 'Create'
3. Click on the created environment
4. Choose 'Open Terminal'
5. Go to the Terminal
6. Move to the directory where you want to clone theis repo. So, write in the terminal: `cd /<any_folder>/`
7. Clone the respository using the following command in the terminal: `git clone git@github.com:naimazhusupova/Project-Dashboard-Covid.git`
8. Move to the folder of the cloned repo `cd /.../Project-Dashboard-Covid` (where you cloned this repo) command, e.g. `cd /Users/nazgul/Desktop/Project-Dashboard-Covid`
9. Write in the Terminal: `pip install -r requirements.txt` (this .txt file is provided in this repo)

Note:
In the 'requirements.txt' pip, pandas among others are not included, because they are installed by default when you create a new environment using Anaconda. In any case you can check if they are installed properly:
1. Go to Anaconda Navigator
2. Go to your environment
3. Choose in the drop-down menu 'Installed'
4. Search for the required packages

## How to run the dashboard locally?
1. Open Anaconda Navigator
2. Choose a created environment
3. Open the terminal in your created environment (click on the play-icon button and choose "Open Terminal")
4. Move to your directory using `cd your_directory` (where you cloned this repo) command, for example `cd /Users/nazgul/Desktop/Project-Dashboard-Covid`
5. Write the following command `streamlit run plot_data.py`
6. Then, the dashboard will be automatically displayed in your default browser
