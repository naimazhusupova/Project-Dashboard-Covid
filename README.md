# Project-Dashboard-Covid

This project repo contains a dashboard with the information about Covid-19. It gives you a visualization of the Covid cases over time. 
For this dashboard we use Streamlit and a dataset from Johns Hopkins University. 

Our dashboard is interactive and allows the user to:
1. Select which countries to display (among a pre-defined list).
2. Select which time period to display (i.e. user could choose start and finish dates).
3. Select which variable(s) to display: number / cumulated number / 7-day rolling average of confirmed cases / deaths / (recovered).

# Installing Dependencies

Instead of installing every package mannualy we created a requirements.txt file and by running once all the necessary packages will be installed at once.
Check this [tutorial](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/app-dependencies)

How to install all required dependencies?

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
