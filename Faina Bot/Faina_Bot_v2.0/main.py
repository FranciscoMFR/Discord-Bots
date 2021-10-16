import os
import discord
from discord.ext.commands import Bot
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


Client = Bot(command_prefix='!')

sad_words = ["triste", "deprimido", "deprimida", "infeliz", "chateado", "chateada", "deprimente"]

riddle_question = ["O que tem de ser partido antes de o puderes usar?", "O que é que está sempre à tua frente, mas não consegues ver?"]
riddle_answer = [["Toalha", "toalha"], ["Ovo", "ovo"], ["Futuro", "futuro"]]
maps = ["mapa_pt1.PNG", "mapa_pt2.PNG"]

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

if "riddleStatus" not in db.keys():
  db["riddleStatus"] = False

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

def update_riddles(riddle):
  if "riddles" in db.keys():
    riddles = db["riddles"]
    riddles.append(riddle)
    db["riddles"] = riddles
  else:
    db["riddles"] = riddle

def delete_riddles(index):
  riddles = db["riddles"]
  if len(riddles) > index:
    del riddles[index]
    db["riddles"] = riddles

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

@Client.command()
async def riddleStatus(ctx):
  db["riddleStatus"] = not db["riddleStatus"]

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
  async def newRiddle(ctx, arg):
    riddle = arg
    update_riddles(riddle)
    await ctx.send("Nova riddle adicionada.")

  @Client.command()
  async def delete(ctx, arg):
    if "encouragements" in db.keys():
      aux = db["encouragements"][int(arg)]
      delete_encouragement(int(arg))
    await ctx.send("A frase [" + aux + "] foi eliminada")

  @Client.command()
  async def deleteRiddle(ctx, arg):
    if "riddles" in db.keys():
      aux = db["riddles"][int(arg)]
      delete_riddles(int(arg))
    await ctx.send("A riddle [" + aux + "] foi eliminada")

  @Client.command()
  async def see(ctx, arg):
    lst = []
    if arg in db.keys():
      lst = db[arg]
    await ctx.send(list(lst))

  @Client.command()
  async def tts(ctx, arg):
    await ctx.send(arg, tts=db["tts"])

  @Client.command()
  async def local(ctx):
    await ctx.send(file=discord.File("mapa.PNG"))

  if db["riddleStatus"]:
    @Client.command()
    async def riddle(ctx, num=0):
      await ctx.send(db["riddles"][int(num)], tts=db["tts"])

    @Client.command()
    async def answer(ctx, num, arg):
      if any(word in arg for word in riddle_answer[int(num)]):
        await ctx.author.send("O espertinho {0} acertou! Verifica as mensagens privadas!".format(ctx.author.mention), tts=db["tts"])
        await ctx.author.send(file=discord.File(maps[int(num)]))
      else:
        await ctx.author.send("Erraste! Não mereces ser empreendedor!")

  @Client.command()
  async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit=amount)

  @Client.command()
  async def dm(ctx, user: discord.User, *, msg=None):
    msg = msg or 'Oi gustosuh!!'
    await user.send(msg)


keep_alive()
Client.run(os.environ['TOKEN'])
