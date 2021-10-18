import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()


bad_words = [
    "mc", "bc", "kutta", "bahinchod", "madarchod", "chut", "lawda", "lund",
    "maa", "behen", "gand", "bsdk", "bhadwe", "bhadwa", "lawde", "baap",
    "chutiya", "chutiye", "fuck", "motherfucker", "dick", "pussy", "gandu",
    "paagal", "pagal", "bkl", "tatta", "tatto", "nunnu", "kutte", "kameene", "gandu"
]

reply_bad_words = [
    "Ja na bsdk", "Apne baap ko bolna yeh",
    "Ek aur baar kuch bol aur teri gand leleni hai meko", "abe chuth marike",
    "Abe o do baap ke", "Aisa marenge do kan ke niche naam bhul jaoge",
    "Khada hota hai tera?", "Abe o cuckold", "Fuck u and ur thoughts",
    "No body loves u bro", "Ever thought of killing yourself?", "Abe o rand",
    "O gand ke andhe", "bsdk guda hai tere mei?",
    "Char chourahe mei char lund leke chod dunga chikhe pura maholla sunega bc",
    "Kash tere baap ne choda na hota teri maa ko", "Mu mei le le mera", "bkl"
]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


def update_badWords(badWords):
    if "slang" in db.keys():
        slang = db["slang"]
        slang.append(badWords)
        db["slang"] = slang
    else:
        db["slang"] = [badWords]


def delete_badWords(index):
    slang = db["slang"]
    if len(slang) > int(index):
        del slang[int(index)]
        db["slang"] = slang


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith("$slang"):
        await message.channel.send(random.choice(reply_bad_words))
    if msg.startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        options = reply_bad_words

        if "slang" in db.keys():
            options = options + list(db["slang"])

        if any(word in msg for word in bad_words):
            await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
        badWords = msg.split("$new ", 1)[1]
        update_badWords(badWords)
        await message.channel.send("New gali added!!")

    if msg.startswith("$delete"):
        slang = []
        if "slang" in db.keys():
            index = msg.split("$delete", 1)[1]
            delete_badWords(index)
            slang = db["slang"]
        await message.channel.send(slang)

    if msg.startswith("$list"):
        slang = []
        if "slang" in db.keys():
            slang = db["slang"]
        await message.channel.send(slang)

    if msg.startswith("$responding"):
        value = msg.split("$responding ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv('TOKEN'))
