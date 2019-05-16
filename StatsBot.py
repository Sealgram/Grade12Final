# Reddit Bot Main Script
# Note that all comments reference the line/lines directly below them.

# importing praw: 'python reddit api wrapper', allows you to login to and access reddit through python
import praw

# Importing a script that I have made myself which contains mostly database interactions for the bot
import BotFunctions as bf
# importing time to be used in the code
import time

# initializing the Reddit class, which is the way that PRAW interacts with the reddit API through a reddit account.
reddit = praw.Reddit(client_id='bPOXVTpIkZ77Gw',
                     client_secret='3oxD-2mUiDPX7bjtoAsKvPAT5P0',
                     username='User_Stats_Bot',
                     password='userstatsbot_CompSci_5338',
                     user_agent='python:com.statsbot:v1.0 (by u/sealgram)'
                     )

# limiting the bot to one Subreddit
activesubreddit = reddit.subreddit('BotTraining')

# defining the bot's keyphrase (how users will summon it)
botkeyphrase = '!!stats '

'''
The following function contains the main loop, and with it, all the inner workings of my reddit bot. This is a user
stats bot, and it replies to specific commands on comments on the subreddit r/BotTraining on reddit. It can provide
a user with a breakdown of their Karma, Find out how many trophies a user has and display a random trophy from the
user's display case, and find out how many times a user has commented, and provide that user with their most commonly
used phrase.
'''


def maininstance(subreddit, keyphrase):
    # defining repliedcomments for later use using a function from my other script
    repliedcomments = bf.listoflines('StatsBotDatabase/ForbiddenComments.txt')
    # Infinite loop to make sure nothing breaks
    while True:
        # Running a loop of the code for each new comment in the subreddit's comment stream
        for comment in subreddit.stream.comments():
            # each comment has a specific ID, and the program records the id of any comment it has already responded
            # to- this makes sure that the comment it is analyzing has not already been analyzed by cross-checking it
            # with a database.
            if comment.id not in repliedcomments:
                # Appending the comment id of the comment it will now respond to into the database of replied comments
                bf.databaseappend('StatsBotDatabase/ForbiddenComments.txt', comment.id)
                if keyphrase in comment.body:
                    # removing every part of the command except the word after the keyphrase
                    command = comment.body.replace(keyphrase, '')
                    # responding to !!stats help
                    if command == 'Help':
                        print("Responding to !!stats Help...")
                        # using another of my functions from the other script to record that the bot has been summoned
                        bf.uponesummon('StatsBotDatabase/BotSummons.txt')
                        # getting the amount of summons from the database
                        with open('StatsBotDatabase/BotSummons.txt', 'r') as botsummons:
                            summons = botsummons.read().strip()
                        # finding the redditor who made the comment
                        redditor = comment.author
                        # formulating the reply
                        reply = f"Some commands you can give me:" \
                                f"\n\n !!stats Karma: A detailed Karma Breakdown" \
                                f"\n\n !!stats Trophies: The amount of trophies a user has, as well as one random" \
                                f"trophy feature, and if the user has reddit premium." \
                                f"\n\n !!stats Comments: Shows the number of comments the user has made, as well as" \
                                f" the user's most commonly used phrase"\
                                f"\n\n\n Summoned By: u/{redditor}" \
                                f"\n\n this bot has been summoned {summons} times!"
                        # replying to the comment
                        comment.reply(reply)
                        print('Responded to !!stats Help')
                    # responding to !!stats Karma
                    elif command == 'Karma':
                        print("Responding to !!stats Karma...")
                        # the next 4 lines are identical to the ones in the last if statement
                        bf.uponesummon('StatsBotDatabase/BotSummons.txt')
                        with open('StatsBotDatabase/BotSummons.txt', 'r') as botsummons:
                            summons = botsummons.read().strip()
                        redditor = comment.author
                        # finding the redditor's total karma
                        karma = redditor.link_karma + redditor.comment_karma
                        # formulating the reply
                        reply = f"Comment Karma: {redditor.comment_karma}" \
                                f"\n\nPost Karma: {redditor.link_karma}" \
                                f"\n\nTotal Karma: {karma}" \
                                f"\n\nSummoned By: u/{redditor}" \
                                f"\n\nThis bot has been summoned {summons} times!"
                        # replying to the comment
                        comment.reply(reply)
                        print('Responded to !!stats Karma')
                    # responding to !!stats Comments
                    elif command == 'Comments':
                        print("Responding to !!stats Comments...")
                        # the next 4 lines are identical to the ones in the first if statement
                        bf.uponesummon('StatsBotDatabase/BotSummons.txt')
                        with open('StatsBotDatabase/BotSummons.txt', 'r') as botsummons:
                            summons = botsummons.read().strip()
                        redditor = comment.author
                        # wiping the comment database
                        bf.databasewipe('StatsBotDatabase/CommentDatabase.txt')
                        # recording all of the comments the redditor who summoned the bot has ever made into a database.
                        for comments in redditor.comments.new(limit=None):
                            text = comments.body.split('\n', 1)[0][:100]
                            bf.databaseappend('StatsBotDatabase/CommentDatabase.txt', text)
                        # letting the database sit for 2 seconds so it doesn't get accessed too fast
                        time.sleep(2)
                        # making a list of every comment the redditor has ever made
                        listofcomments = bf.listoflines('StatsBotDatabase/CommentDatabase.txt')
                        # finding the redditor's most used phrase and how many times they have used it.
                        mostused = bf.mostused(listofcomments)
                        # formulating the reply
                        reply = f"Total Comments Posted: {len(listofcomments)}" \
                                f"\n\nYou have used the phrase '{mostused[0]}' {mostused[1]} times" \
                                f"\n\nSummoned by: u/{redditor}" \
                                f"\n\nThis bot has been summoned {summons} times!"
                        # replying to the comment
                        comment.reply(reply)
                        print('Responded to !!stats Comments')
                    # responding to !!stats Trophies
                    elif command == 'Trophies':
                        print("Responding to !!stats Trophies...")
                        # the next 4 lines are identical to the ones in the first if statement
                        bf.uponesummon('StatsBotDatabase/BotSummons.txt')
                        with open('StatsBotDatabase/BotSummons.txt', 'r') as botsummons:
                            summons = botsummons.read().strip()
                        redditor = comment.author
                        # wiping the trophy database before it is used again
                        bf.databasewipe('StatsBotDatabase/TrophyDatabase.txt')
                        # storing all the trophies the user has in their account's trophy case to a database
                        for trophy in redditor.trophies():
                            bf.databaseappend('StatsBotDatabase/TrophyDatabase.txt', trophy.name)
                        # making a list of all the trophies and removing the last item in the list (it will be blank)
                        trophies = bf.listoflines('StatsBotDatabase/TrophyDatabase.txt')
                        trophies.pop()
                        # formulating the response
                        reply = f"Total Trophies: {len(trophies)}" \
                                f"\n\n Congrats on your {bf.randompick(trophies)} trophy!" \
                                f"\n\nSummoned By: u/{redditor}" \
                                f"\n\nThis bot has been summoned {summons} times!"
                        # replying to the comment
                        comment.reply(reply)
                        print("Responded to !!stats Trophies")
            # formatting for my own sanity
            else:
                continue


# calling the main function
maininstance(activesubreddit, botkeyphrase)
