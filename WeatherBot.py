# Reddit Bot Main Script
# Note that all comments reference the line/lines directly below them.

# importing praw: 'python reddit api wrapper', allows you to login to and access reddit through python
import praw
import prawcore

# Other Imports:
import BotFunctions as bf
import time

reddit = praw.Reddit(client_id='wfQSiDTeHjWEmQ',
                     client_secret='4XfhuuSEvmk3FWmnLfN2PtuAhJI',
                     username='weather_purveyor',
                     password='weatherbot_CompSci_5338',
                     user_agent='python:com.weatherbot:v1.0 (by u/sealgram)'
                     )

activesubreddit = reddit.subreddit('BotTraining')

botkeyphrase = '!!weather '

