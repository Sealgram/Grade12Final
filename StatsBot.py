# Reddit Bot Main Script
# Note that all comments reference the line/lines directly below them.

# importing praw: 'python reddit api wrapper', allows you to login to and access reddit through python
import praw
import prawcore

# Other Imports:
import BotFunctions as bf
import time

reddit = praw.Reddit(client_id='bPOXVTpIkZ77Gw',
                     client_secret='3oxD-2mUiDPX7bjtoAsKvPAT5P0',
                     username='User_Stats_Bot',
                     password='userstatsbot_CompSci_5338',
                     user_agent='python:com.statsbot:v1.0 (by u/sealgram)'
                     )

activesubreddit = reddit.subreddit('BotTraining')

botkeyphrase = '!!stats '


def maininstance(subreddit, keyphrase):
    repliedcomments = bf.listoflines('StatsBotDatabase/ForbiddenComments.txt')
    while True:
        for comment in subreddit.stream.comments():
            if comment.id not in repliedcomments:
                bf.databaseappend('StatsBotDatabase/ForbiddenComments.txt', comment.id)
                if keyphrase in comment.body:
                    command = comment.body.replace(keyphrase, '')
                    if command == 'Help':
                        print("Responding to !!stats Help...")
                        redditor = comment.author
                        reply = f"Some commands you can give me:" \
                                f"\n\n !!stats Karma: A detailed Karma Breakdown" \
                                f"\n\n !!stats Trophies: The amount of trophies a user has, as well as one random" \
                                f"trophy feature, and if the user has reddit premium." \
                                f"\n\n !!stats Comments: Shows the number of comments the user has made, as well as" \
                                f" the user's most commonly used phrase"\
                                f"\n\n\n Summoned By: u/{redditor}"
                        comment.reply(reply)
                        print('Responded to !!stats Help')
                    elif command == 'Karma':
                        print("Responding to !!stats Karma")
                        redditor = comment.author
                        karma = redditor.link_karma + redditor.comment_karma
                        reply = f"Comment Karma: {redditor.comment_karma}" \
                                f"\n\nPost Karma: {redditor.link_karma}" \
                                f"\n\nTotal Karma: {karma}" \
                                f"\n\nSummoned By: u/{redditor}"
                        comment.reply(reply)
                        print('Responded to !!stats Karma...')
                    elif command == 'Upvotes':
                        print("Responding to !!stats Upvotes")
                        try:
                            redditor = comment.author
                            upvoteditems = []
                            for upvoted_item in redditor.upvoted():
                                upvoteditems.append(upvoted_item)
                            print(len(upvoteditems))
                        except prawcore.Forbidden:
                            print('Unable to complete !!stats Upvotes')
                    elif command == 'Comments':
                        print("Responding to !!stats Comments...")
                        redditor = comment.author
                        bf.databasewipe('StatsBotDatabase/CommentDatabase.txt')
                        for comments in redditor.comments.new(limit=None):
                            text = comments.body.split('\n', 1)[0][:100]
                            bf.databaseappend('StatsBotDatabase/CommentDatabase.txt', text)
                        time.sleep(2)
                        listofcomments = bf.listoflines('StatsBotDatabase/CommentDatabase.txt')
                        mostused = bf.mostused(listofcomments)
                        reply = f"Total Comments Posted: {len(listofcomments)}" \
                                f"\n\nYou have used the phrase '{mostused[0]}' {mostused[1]} times" \
                                f"\n\nSummoned by: u/{redditor}"
                        comment.reply(reply)
                        print('Responded to !!stats Comments')
                    elif command == 'Trophies':
                        print("Responding to !!stats Trophies...")
                        redditor = comment.author
                        bf.databasewipe('StatsBotDatabase/TrophyDatabase.txt')
                        for trophy in redditor.trophies():
                            bf.databaseappend('StatsBotDatabase/TrophyDatabase.txt', trophy.name)
                        trophies = bf.listoflines('StatsBotDatabase/TrophyDatabase.txt')
                        trophies.pop()
                        reply = f"Total Trophies: {len(trophies)}" \
                                f"\n\n Congrats on your {bf.randompick(trophies)} trophy!" \
                                f"\n\nSummoned By: u/{redditor}"
                        comment.reply(reply)
                        print("Responded to !!stats Trophies")
            else:
                continue


maininstance(activesubreddit, botkeyphrase)
