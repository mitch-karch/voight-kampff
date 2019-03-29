import http.client
import discord
import json

headers = {
    'cache-control': "no-cache",
}

def reddit_top3(request_subreddit):
    conn = http.client.HTTPSConnection("www.reddit.com")
    conn.request("GET", "/r/{stk}/top/.json?limit=3".format(stk=request_subreddit), headers=headers)
    json_response = json.loads(conn.getresponse().read().decode("utf-8"))
    
    tops = json_response["data"]["children"]
    constructedString = ("__Top 3 posts: ***r/{full}***__\n"
                        "\n"
                        "1.{t0} <{t0u}>\n"
                        "2.{t1} <{t1u}>\n"
                        "3.{t2} <{t2u}>\n"
                        )
    em = discord.Embed(title="Top posts",
                        description= \
                            "1. ["+tops[0]['data']['title']+"]("+tops[0]['data']['url']+") | [comments](https://www.reddit.com"+tops[0]['data']['permalink']+")\n" + \
                            "2. ["+tops[1]['data']['title']+"]("+tops[1]['data']['url']+") | [comments](https://www.reddit.com"+tops[0]['data']['permalink']+")\n" + \
                            "3. ["+tops[2]['data']['title']+"]("+tops[2]['data']['url']+") | [comments](https://www.reddit.com"+tops[0]['data']['permalink']+")\n",
                        colour=0x0000FF)
    return em
    """
    em.set_author(name="Top 3 subreddit posts: r/", url="www.reddit.com/r/",icon_url="https://cdn.discordapp.com/embed/avatars/0.png") 
    em.set_author(name="Top 3 subreddit posts: r/"+tops[0]["data"]["subreddit"], url="www.reddit.com/r/"+tops[0]["data"]["subreddit"],icon_url=client.user.default_avatar_url) 
    await client.say(constructedString.format(
                        full=tops[0]["data"]["subreddit"], 
                        t0=tops[0]["data"]["title"],
                        t1=tops[1]["data"]["title"],
                        t2=tops[2]["data"]["title"],
                        t0u=tops[0]["data"]["url"],
                        t1u=tops[1]["data"]["url"],
                        t2u=tops[2]["data"]["url"]
                        )
                    )
    """

