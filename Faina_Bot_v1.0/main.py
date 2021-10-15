import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client = discord.Client()

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

@client.event
async def on_ready():
  print('We have logged in as {0.user} v1.0'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user: return
  msg = message.content
  if msg.startswith('!hello'):
    #await message.channel.send('/tts Oi tudo bem?', tts=True)
    await message.channel.send('Sup {0}!'.format(message.author.mention))
  if msg.startswith('!sad'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      #options = options + db["encouragements"]
      options.extend(db["encouragements"])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("!new"):
    encouraging_message = msg.split("!new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("Nova mensagem adicionada.")

  if msg.startswith("!del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("!del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(list(encouragements))

  if msg.startswith("!see"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(list(encouragements))

  if msg.startswith("!shutup"):
    db["responding"] = False
    db["tts"] = False
    await message.channel.send("Ok ok já me vou calar!")
  
  if msg.startswith("!speak"):
    db["responding"] = True
    db["tts"] = True
    await message.channel.send("De volta ao ativo!")
  
  if db["tts"]:
    if msg.startswith("!tts"):
      mensagem = msg.split("!tts",1)[1]
      await message.channel.send(mensagem, tts=True)
  
  if msg.startswith("!local"):
    await message.channel.send(file=discord.File("mapa.PNG"))

  if msg.startswith("!riddle"):
    await message.channel.send(riddle_question, tts=db["tts"])

  if any(word in msg for word in riddle_answer):
    await message.channel.send(file=discord.File("mapa.PNG"))

  if msg.startswith("!wip"):
    await message.channel.send("A entrar em manutenção! Até já!")

keep_alive()
client.run(os.environ['TOKEN'])
