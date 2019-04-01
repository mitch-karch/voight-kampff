import http.client
import discord
import json

headers = {
    'cache-control': "no-cache",
}


def shortStringBuild(title, url, com):
    return "["+title+"]("+url+") | [comments](https://www.reddit.com"+com+")\n"


def reddit_top3(request_subreddit):
    conn = http.client.HTTPSConnection("www.reddit.com")
    conn.request("GET", "/r/{s}/top/.json?limit=3".format(s=request_subreddit),
                 headers=headers)
    json_response = json.loads(conn.getresponse().read().decode("utf-8"))

    tops = json_response["data"]["children"]
    message = ""
    for i in range(0, 3):
        message += str(i+1) +'. '+ shortStringBuild(tops[i]['data']['title'],
                                    tops[i]['data']['url'],
                                    tops[i]['data']['permalink'])

    em = discord.Embed(title="Top posts",
                       description=message,
                       colour=0x0000FF)
    return em
