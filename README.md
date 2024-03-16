# tiktok_billboard_virality
Code for the data collection and analysis of the correlation between viral Tiktok songs and their Billboard Hot 100 rankings. (COGS_9 Final Project)

# How to Use

Clone this repository  
`git clone https://github.com/CarterT27/tiktok_billboard_virality`

Install dependencies  
`cd tiktok_billboard_virality`  
`pip install -r requirements.txt`

Add personally identifying information to environment (for ethical reasons)  
`export NAME='Your Name'`  
`export EMAIL='insert_email_here@gmail.com'`

Add [Kaggle API Key](https://www.kaggle.com/docs/api#getting-started-installation-&-authentication) to Use Kaggle CLI Tool

Run scripts to collect data  
`cd scripts`  
`chmod +x ./download_kaggle.sh`  
`./download_kaggle.sh`  
`python tokchart.py`  
