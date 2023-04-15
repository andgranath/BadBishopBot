import os
import discord
from dotenv import load_dotenv
import requests

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")


intents = discord.Intents(messages=True, message_content=True)

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f"{client.user} is connected to the guild:\n"
        f"{guild.name} (id: {guild.id})"
    )

#Hämtar bild-url om ett schackproblem postas och sparar filen.
imagefiles = ['bmp','jpeg','jpg','png']

@client.event

async def on_message(message):


    if message.content.startswith("Svart"):
        move = "b"
    elif message.content.startswith("svart"):
        move ="b"
    elif message.content.startswith("Vit"):
        move = "w"
    elif message.content.startswith("vit"):
        move="w"
        print("whiter")
    else:
        move =""
    print(move)
    attachments = message.attachments
    if len(attachments) > 0:
        url = message.attachments[0].url
        if url[-3:] in imagefiles:
            ending = url[-3:] #filändelsen.
            r = requests.get(url, allow_redirects=True)
            
            open("image."+ending, "wb").write(r.content)

            os.system("python3 recognize.py image."+ending)
            os.remove("image."+ending) #raderar filen av utrymmesskäl.

#FEN är nu sparad i txt-filen "fentext.txt".
            with open("fentext.txt", "r") as file:
                fen = file.read()
                analysis_url = "https://www.lichess.org/analysis/"+fen+"%20"+move

            await message.channel.send("Analysera ställningen här: " + analysis_url)

#Nu ska den genererade FEN-strängen ska skickas till Lichess API. På något sätt ska
#vi också ange om svart eller vit är vid draget.


client.run(TOKEN)