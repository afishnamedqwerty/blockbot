# Twitter Keyword Blocker

## Project Overview
This Python project utilizes Tweepy, a Python library for accessing the Twitter API v2, to automatically block users who reply or quote tweets with specific keywords or phrases. It's designed to filter out unwanted interactions based on predefined criteria.

## Features
- Stream tweets in real-time that are replies or quotes to a specific Twitter account.
- Automatically block users who use certain red flag keywords or yellow flag phrases in their tweets.

## Requirements
- Python 3.x
- Tweepy library

## Installation
1. Ensure Python is installed on your system.
2. Install Tweepy using pip:
   ```bash
   pip install tweepy

## Configuration
1. Obtain a Twitter API Bearer Token from Twitter Developer Portal
2. Replace `'YOUR_BEARER_TOKEN'` in the script with your actual Bearer Token

## Usage 
1. Set the `BEARER_TOKEN` with your Twitter API Bearer Token
2. Define the target Twitter account in the `rule` variable.
3. Customize `red_keywords` and `yellow_phrases` lists with your criteria for blocking.
4. Run the script to start monitoring and blocking as per the defined rules.

`BEARER_TOKEN = 'YOUR_BEARER_TOKEN'  # Replace with your Bearer Token`
`red_keywords = ['keyword1', 'keyword2']  # Add red flag keywords`
`yellow_phrases = ['phrase one', 'phrase two']  # Add yellow flag phrases`

### Execute the script:
`python twitter_keyword_blocker.py`

### Disclaimer
I'm probably underestimating the rate limiter so stay tuned