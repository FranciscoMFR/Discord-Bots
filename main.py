import os
import discord
from discord.ext.commands import Bot
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


#Client = discord.Client()
Client = Bot(command_prefix='!')

sad_words = ["triste", "deprimido", "deprimida", "infeliz", "chateado", "chateada", "deprimente"]

riddle_question = "O que tem de ser partido antes de o puderes usar?"
riddle_answer = ["Ovo", "ovo"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person!"
]

if "tts" not in db.keys():
  db["tts"] = True

if "responding" not in db.keys():
  db["responding"] = True 

if "wip" not in db.keys():
  db["wip"] = False

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return quote

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

#def see_encouragements():

@Client.event
async def on_ready():
  print('We have logged in as {0.user} v2.0'.format(Client))

@Client.command()
async def wip(ctx):
  db["wip"] = True
  db["responding"] = False
  print(db["wip"])
  await ctx.send('A entrar em manutenção! Até já! @everyone')

@Client.command()
async def work(ctx):
  db["wip"] = False
  db["responding"] = True
  print(db["wip"])
  await ctx.send('Estou de volta ao ativo!Bota trabalhar! @everyone')

@Client.command()
async def wipstatus(ctx):
  if db["wip"]:
    await ctx.send('Encontro-me em manutenção!')
  else:
    await ctx.send('Estou on the work!')

@Client.command()
async def shutup(ctx):
  db["tts"] = False
  await ctx.send("Ok ok já me vou calar!")

@Client.command()
async def speak(ctx):
  db["tts"] = True
  await ctx.send("Yey já posso falar!")

@Client.command()
async def ttsstatus(ctx):
  if db["tts"]:
    await ctx.send('Estou habilitado a parlar com vocês!')
  else:
    await ctx.send('*Gri Gri Gri*')

if db["wip"] == False:
  @Client.command()
  async def hello(ctx):
    await ctx.send('Sup {0}!'.format(ctx.author.mention))

  @Client.command()
  async def sad(ctx):
    quote = get_quote()
    await ctx.channel.send(quote)

  @Client.command()
  async def new(ctx, arg):
    encouraging_message = arg
    update_encouragements(encouraging_message)
    await ctx.send("Nova mensagem adicionada.")

  @Client.command()
  async def delete(ctx, arg):
    #encouragements = []
    if "encouragements" in db.keys():
      aux = db["encouragements"][int(arg)]
      delete_encouragement(int(arg))
      #encouragements = db["encouragements"]
    await ctx.send("A frase [" + aux + "] foi eliminada")
    #await ctx.send(list(encouragements))

  @Client.command()
  async def see(ctx):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await ctx.send(list(encouragements))

  @Client.command()
  async def tts(ctx, arg):
    await ctx.send(arg, tts=db["tts"])

  @Client.command()
  async def local(ctx):
    await ctx.send(file=discord.File("mapa.PNG"))

  @Client.command()
  async def riddle(ctx):
    await ctx.send(riddle_question, tts=db["tts"])

  @Client.command()
  async def answer(ctx, arg):
    if any(word in arg for word in riddle_answer):
      await ctx.send(file=discord.File("mapa.PNG"))

  #@Client.command()

keep_alive()
Client.run(os.environ['TOKEN'])
