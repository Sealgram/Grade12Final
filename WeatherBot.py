# Reddit Bot Main Script
# Note that all comments reference the line/lines directly below them.

# importing praw: 'python reddit api wrapper', allows you to login to and access reddit through python
import praw

# Importing a script that I have made myself which contains mostly database interactions for the bot
import BotFunctions as bf

# Importing requests to be used in the code.
import requests

reddit = praw.Reddit(client_id='wfQSiDTeHjWEmQ',
                     client_secret='4XfhuuSEvmk3FWmnLfN2PtuAhJI',
                     username='weather_purveyor',
                     password='weatherbot_CompSci_5338',
                     user_agent='python:com.weatherbot:v1.0 (by u/sealgram)'
                     )

activesubreddit = reddit.subreddit('BotTraining')

botkeyphrase = '!!weather '


def maininstance(subreddit, keyphrase):
    # defining repliedcomments for later use using a function from my other script
    repliedcomments = bf.listoflines('WeatherBotDatabase/ForbiddenComments.txt')
    # Infinite loop to make sure nothing breaks
    while True:
        # Running a loop of the code for each new comment in the subreddit's comment stream
        for comment in subreddit.stream.comments():
            # each comment has a specific ID, and the program records the id of any comment it has already responded
            # to- this makes sure that the comment it is analyzing has not already been analyzed by cross-checking it
            # with a database.
            if comment.id not in repliedcomments:
                # Appending the comment id of the comment it will now respond to into the database of replied comments
                bf.databaseappend('WeatherBotDatabase/ForbiddenComments.txt', comment.id)
                if keyphrase in comment.body:
                    print("replying to a summon.")
                    bf.uponesummon('WeatherBotDatabase/BotSummons.txt')
                    with open('WeatherBotDatabase/BotSummons.txt', 'r') as botsummons:
                        summons = botsummons.read().strip()
                    # removing every part of the command except the words after the keyphrase
                    city = comment.body.replace(keyphrase, '')
                    # finding the redditor who summoned the bot
                    redditor = comment.author
                    # the API key for accessing the weather api
                    api_key = "89ea3f323d661f91d8df1df3388a2163"
                    # defines the base URL function for simplicity
                    base_url = "http://api.openweathermap.org/data/2.5/weather?"
                    # builds the URL with the base URL, API key, and the city name specified by the reddit user
                    complete_url = base_url + "appid=" + api_key + "&q=" + city
                    # uses the requests module to get the return from the complete URL
                    response = requests.get(complete_url)
                    # defines the response using JSON, so that python can interpret it.
                    x = response.json()
                    # if it got a response, continues with the code
                    if x["cod"] != "404":
                        # defines y as the main return from the JSON
                        y = x["main"]
                        # gets the current temperature in kelvin from the main
                        current_temperature = y["temp"]
                        # converts the temperature to celsius from kelvin
                        celsius = current_temperature - 273.15
                        # defines z as everything from the 'weather' part of the JSON
                        z = x["weather"]
                        # defines z as everything from the 'weather' part of the JSON
                        weather_description = z[0]["description"]
                        # formulating the reply
                        reply = f"It is currently {weather_description} and {celsius:.2f} degrees celsius in {city}" \
                                f"\n\n\n Summoned by: u/{redditor}" \
                                f"\n\n This bot has been summoned {summons} times!"
                        # replying to the summon
                        comment.reply(reply)
                        print("replied to a summon with a successful cityname.")
                    # if the cityname was invalid, a different reply is warranted.
                    else:
                        # formulating the reply
                        reply = f"That is not a valid city name!" \
                                f"\n\n\n Summoned by: u/{redditor}"\
                                f"\n\n This bot has been summoned {summons} times!"
                        # replying to the summon
                        comment.reply(reply)
                        print("replied to a summon with an invalid cityname.")
            # formatting for my own sanity
            else:
                continue


maininstance(activesubreddit, botkeyphrase)
