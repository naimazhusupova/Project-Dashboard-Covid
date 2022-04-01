# Project-Dashboard-Covid

This project repo contains the description, tools and instructions to replicate our dashboard with information about Covid-19. 

For this dashboard we use Streamlit for the vizualization based on a dataset [COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19) of Johns Hopkins University. 

Our dashboard is interactive and allows the user to:
1. Select which countries to display (among a pre-defined list).
2. Select which time period to display (i.e. user could choose start and finish dates).
3. Select which variable(s) to display: number / cumulated number / 7-day rolling average of confirmed cases / deaths / (recovered).

# Installing Dependencies

Instead of installing every package manually we created a requirements.txt file and by running it once, all the necessary packages will be installed.

Follow the next steps in order to install all required dependencies (Python, Pandas, Matplotlib, Jupyter Lab, Streamlit...):

Part 1
1. If you do not have Anaconda, install it on your computer in accordance with your operating system
2. You can find the instructions [here]( https://docs.anaconda.com/anaconda/install/) based on your operating system

Part 2
1. Open Anaconda Navigator
2. Create new environment based on the settings:
    - Click on Environments
    - Click on 'Create'
    - Name an environment
    - Choose Python version 3.8.12
    - Click 'Create'
3. Click on the created environment
4. Choose 'Open Terminal'
5. Go to the Terminal
6. Write `pip install -r requirements.txt` (this .txt file is provided in this repo)

Note:
In the 'requirements.txt' pip, python and pandas are not included, because they are installed by default when you create a new environment. In any case you can check if they are installed properly:
1. Go to Anaconda Navigator
2. Go to your environment
3. Choose in the drop-down menu 'Installed'
4. Search for the required packages
