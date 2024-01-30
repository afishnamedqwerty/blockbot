# X keyword & phrase Blockbot

## Project Overview
This Python project utilizes Tweepy, a Python library for accessing the Twitter API v2, to automatically block users who reply or quote tweets with specific keywords or phrases. It's designed to filter out unwanted interactions based on predefined criteria.

## Features
- Stream tweets in real-time that are replies or quotes to a specific Twitter account.
- Automatically block users who use certain red flag keywords or yellow flag phrases in their tweets.

## Requirements
- Python >=3.8
- Tweepy library
- Twitter Developer token and OPENAI API access

## Installation
1. Ensure Python is installed on your system `python --version`.
2. Download the blockbot project to a local repo: `git clone https://github.com/afishnamedqwerty/blockbot.git`
3. Install Tweepy using pip:
   ```bash
   pip install tweepy, numpy 

## Configuration
1. Obtain a Twitter API Bearer Token from Twitter Developer Portal
2. Replace `'YOUR_BEARER_TOKEN'` in the script with your actual Bearer Token
3. Replace `'OPENAI_API_KEY'` in the script with your OPENAI api key
4. Add your `red_words` and `yellow_phrases` to their respective `.txt` files
5. (Optional) ~Requires sklearn import~ Tune `semantic_cosine_simlarity()` sensitivity using the `threshold=` parameter to switch to a more sensitive block detector based on cosine similarity correlation to each phrase in the `yellow_phrases.txt` file. This function must replace `is_semantically_similar()` in the `handle_tweet` function to utilize cosine similarity instead of boolean response (a zero shot prompt comparing semantic similarity which can be customized).

## Usage 
1. Set the `BEARER_TOKEN` with your Twitter API Bearer Token
2. Define the target Twitter account in the `rule` variable.
3. Customize `red_words` and `yellow_phrases` lists in their designated `.txt` files with your criteria for blocking.
4. Run the script to start monitoring and blocking as per the defined rules.
5. `blocked_users_log.txt` maintains a running log of all blocked users and offending tweets.

`BEARER_TOKEN = 'YOUR_BEARER_TOKEN'  # Replace with your Bearer Token`
`red_words = ['keyword1', 'keyword2']  # Add red flag keywords`
`yellow_phrases = ['phrase one', 'phrase two']  # Add yellow flag phrases`

### Execute the script:
`python blockbot.py`

### Disclaimer
I'm probably underestimating the rate limiter so stay tuned