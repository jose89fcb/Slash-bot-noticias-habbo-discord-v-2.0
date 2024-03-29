import discord
from discord.ext import commands
import requests
import json
import html
import time
import locale
import requests
locale.setlocale(locale.LC_TIME, "es_ES")
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash import SlashCommand, SlashContext
 

with open("config.json") as f:
    config = json.load(f) 
 
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config["comando"], description="ayuda bot") #Comando
bot.remove_command("help") # Borra el comando por defecto !help
slash = SlashCommand(bot, sync_commands=True)
@slash.slash(
    name="noticias", description="Noticias Habbo Hotel",
    options=[
                
                 create_option(
                  name="hotel",
                  description="Elige él hotel",
                  option_type=3,
                  required=True,
                  choices=[
                      create_choice(
                          name="ES - Hotel España",
                          value="es"
                      ),
                      create_choice(
                          name="BR - Hotel Brasil",
                          value="com.br"
                      ),
                      create_choice(
                          name="COM - Hotel Estados unidos",
                          value="com"
                      ),
                      create_choice(
                          name="DE - Hotel Aleman",
                          value="de"
                      ),
                      create_choice(
                          name="FR - Hotel Frances",
                          value="fr"
                      ),
                      create_choice(
                          name="FI - Hotel Finalandia",
                          value="fi"
                      ),
                      create_choice(
                          name="IT - Hotel Italiano",
                          value="it"
                      ),
                      create_choice(
                          name="TR - Hotel Turquia",
                          value="com.tr"
                      ),
                      create_choice(
                          name="NL - Hotel Holandés",
                          value="nl"
                      )
                  ]
                
               
                  
                )
             ])
             
            
             

    


async def _noticias(ctx:SlashContext, hotel:str):
    await ctx.defer()

    bandera_dict = {
    "es": "https://i.imgur.com/IplIfNP.png",
    "com.br":  "https://i.imgur.com/YGQlPor.png",
    "nl":"https://i.imgur.com/fC8eIvR.png",
    "de":"https://i.imgur.com/vUgY11U.png",
    "fr":"https://i.imgur.com/CoLWbjf.png",
    "it":"https://i.imgur.com/va1X4j6.png",
    "com":"https://i.imgur.com/D6vwN9n.png",
    "com.tr":"https://i.imgur.com/wtiow4R.png",
    "fi":"https://i.imgur.com/BpQCpVi.png"
    }
    bandera = bandera_dict[str(hotel)]
    ####
    HotelNoticia_dict = {
    "es": "es",
    "com.br":  "pt",
    "nl":"nl",
    "de":"de",
    "fr":"fr",
    "it":"it",
    "com":"en",
    "com.tr":"tr",
    "fi":"fi"
    }
    HotelNoticia = HotelNoticia_dict[str(hotel)]

    url = f"https://images.habbo.com/habbo-web-news/{HotelNoticia}/production/front.json"
    response = requests.get(url)
    news_data = response.json()

    # Find the latest news dynamically
    latest_news = max(news_data, key=lambda x: x.get("published", 0), default=None)

    if latest_news:
        title = html.unescape(latest_news.get('title', 'No Title'))
        summary = html.unescape(latest_news.get('summary', 'No Summary'))
        published_time = int(latest_news.get('published', 0) / 1000)
        formatted_time = time.strftime("%A, %#d de %B del %Y  Hora: %H:%M:%S", time.localtime(published_time))
        path = latest_news.get('path', '')
        image = latest_news.get('featured', '')
        thumbnail = latest_news.get('thumbnail', '')

        embed = discord.Embed(
            title=f"{title}",
            description=f"{summary}\n\n[Ver Noticia en Habbo.{hotel}]({f'https://habbo.{hotel}{path}'})",
            color=discord.Colour.random()
        )
        embed.set_image(url=f"{image}")
        embed.set_author(name=f"Habbo [{HotelNoticia}]", icon_url=f"{bandera}")
        embed.set_footer(text=f"habbo [{HotelNoticia}] - {formatted_time}", icon_url="https://i.imgur.com/6ePWlHz.png")
        embed.set_thumbnail(url=f"{thumbnail}")

        await ctx.send(embed=embed)
    else:
        await ctx.send("No se encontraron noticias recientes.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('El comando no existe 🤷🏼‍♂️🔍')

@bot.event
async def on_ready():
    print("BOT listo!")

bot.run(config["token_discord"])
