# Reddit Bot Main Script
# Note that all comments reference the line/lines directly below them.

# importing praw: 'python reddit api wrapper', allows you to login to and access reddit through python
import praw

# Importing a script that I have made myself which contains mostly database interactions for the bot
import BotFunctions as bf

reddit = praw.Reddit(client_id='ZFDI3RdjTq9BJQ',
                     client_secret='Kw-rM_L_M-STr6K-DNTNHuUj1pc',
                     username='example_bot',
                     password='examplebot_CompSci_5338',
                     user_agent='python:com.examplebot:v1.0 (by u/sealgram)'
                     )

activesubreddit = reddit.subreddit('BotTraining')

botkeyphrase = '!!keyphrase '


def maininstance(subreddit, keyphrase):
    # defining repliedcomments for later use using a function from my other script
    repliedcomments = bf.listoflines('ExampleBotDatabase/ForbiddenComments.txt')
    # Infinite loop to make sure nothing breaks
    while True:
        # Running a loop of the code for each new comment in the subreddit's comment stream
        for comment in subreddit.stream.comments():
            # each comment has a specific ID, and the program records the id of any comment it has already responded
            # to- this makes sure that the comment it is analyzing has not already been analyzed by cross-checking it
            # with a database.
            if comment.id not in repliedcomments:
                # Appending the comment id of the comment it will now respond to into the database of replied comments
                bf.databaseappend('ExampleBotDatabase/ForbiddenComments.txt', comment.id)
                if keyphrase in comment.body:
                    print("replying to a summon.")
                    bf.uponesummon('ExampleBotDatabase/BotSummons.txt')
                    with open('ExampleBotDatabase/BotSummons.txt', 'r') as botsummons:
                        summons = botsummons.read().strip()
                    reply = f"" \
                            f"\n\nThis bot has been summoned {summons} times!"
                    comment.reply(reply)
                    print("Replied to a summon")


maininstance(activesubreddit, botkeyphrase)
