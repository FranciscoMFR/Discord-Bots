import os
import discord
from discord.ext.commands import Bot
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

Client = Bot(command_prefix='!')

sad_words = [
    "triste", "deprimido", "deprimida", "infeliz", "chateado", "chateada",
    "deprimente"
]

riddle_question = [
    "O que tem de ser partido antes de o puderes usar?",
    "O que é que está sempre à tua frente, mas não consegues ver?"
]
riddle_answer = [["Toalha", "toalha"], ["Ovo", "ovo"], ["Futuro", "futuro"]]
maps = ["mapa_pt1.PNG", "mapa_pt2.PNG"]

starter_encouragements = [
    "Cheer up!", "Hang in there.", "You are a great person!"
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

@Client.command(brief='WIP mode ON/OFF', description='Turn ON or OFF the mode where the BOT is in maintenance.')
async def wipSwitch(ctx):
  db["wip"] = not db["wip"]
  if db["wip"]:
    await ctx.send('A entrar em manutenção! Até já! @everyone')
    print(db["wip"])
  else:
    await ctx.send('Estou de volta ao ativo!Bota trabalhar! @everyone')
    print(db["wip"])

@Client.command(brief='Show the BOT status', description='Says to you if the BOT are in maintenance or not.')
async def wipStatus(ctx):
    if db["wip"]:
        await ctx.send('Encontro-me em manutenção!')
    else:
        await ctx.send('Estou on the work!')

@Client.command(brief='Show the tts status', description='Says to you if the BOT can use tts or not.')
async def ttsStatus(ctx):
    if db["tts"]:
        await ctx.send('Estou habilitado a parlar com vocês!')
    else:
        await ctx.send('*Gri Gri Gri*')

@Client.command(brief='Show the riddle status', description='Says to you if the riddle game is available.')
async def riddleStatus(ctx):
    if db["riddleStatus"]:
        await ctx.send("Estou apto a desafiar-te!")
    else:
        await ctx.send("Estou cansado de desafios! Espera até mais logo!")

@Client.command(brief='tts mode ON/OFF', description='Turn ON or OFF the mode where the BOT can send message in text to speech.')
async def ttsSwitch(ctx):
  db["tts"] = not db["tts"]
  if db["tts"]:
    await ctx.send("Yey já posso falar!")
  else:
    await ctx.send("Ok ok já me vou calar!")

@Client.command(brief='Riddle mode ON/OFF', description='Turn ON or OFF the riddle game. This command influence other commands.')
async def riddleSwitch(ctx):
    db["riddleStatus"] = not db["riddleStatus"]
    if db["riddleStatus"]:
        await ctx.send(
            "Malta está na hora das adivinhas! Juntem-se todos aqui à minha voltinha!",
            tts=db["tts"])
    else:
        await ctx.send(
            "Quem foi ao mar perdeu o lugar! Por isso se foste à ria ficaste sem adivinha!",
            tts=db["tts"])
    await ctx.send("@everyone")

@Client.command(brief='BOT congratz you', description='BOT will say hello to you.Just for fun.')
async def hello(ctx):
  if not db["wip"]:
    await ctx.send('Sup {0}!'.format(ctx.author.mention), tts=db["tts"])
  else:
    await ctx.send("Faz-me o favor de não me chateares **ENQUANTO ESTOU A LEVAR UPGRADE!**{0}".format(ctx.author.mention))

@Client.command(brief='BOT send an encouragement message', description='This command will send a random encouragement message from a random API.')
async def sad(ctx):
  if not db["wip"]:
    quote = get_quote()
    await ctx.channel.send(quote)
  else:
    await ctx.send("Faz-me o favor de não me chateares **ENQUANTO ESTOU A LEVAR UPGRADE!**{0}".format(ctx.author.mention))

@Client.command()
async def new(ctx, arg):
  if not db["wip"]:
    encouraging_message = arg
    update_encouragements(encouraging_message)
    await ctx.send("Nova mensagem adicionada.")
  else:
    await ctx.send("Faz-me o favor de não me chateares **ENQUANTO ESTOU A LEVAR UPGRADE!**{0}".format(ctx.author.mention))

@Client.command()
async def newRiddle(ctx, arg):
  if not db["wip"]:
    riddle = arg
    update_riddles(riddle)
    await ctx.send("Nova riddle adicionada.")
  else:
    await ctx.send("Faz-me o favor de não me chateares **ENQUANTO ESTOU A LEVAR UPGRADE!**{0}".format(ctx.author.mention))

@Client.command()
async def delete(ctx, arg):
  if not db["wip"]:
    if "encouragements" in db.keys():
      aux = db["encouragements"][int(arg)]
      delete_encouragement(int(arg))
      await ctx.send("A frase [" + aux + "] foi eliminada")
  else:
    await ctx.send("Faz-me o favor de não me chateares **ENQUANTO ESTOU A LEVAR UPGRADE!**{0}".format(ctx.author.mention))

@Client.command()
async def deleteRiddle(ctx, arg):
  if not db["wip"]:
    if "riddles" in db.keys():
      aux = db["riddles"][int(arg)]
      delete_riddles(int(arg))
      await ctx.send("A riddle [" + aux + "] foi eliminada")
  else:
    await ctx.send("Faz-me o favor de não me chateares **ENQUANTO ESTOU A LEVAR UPGRADE!**{0}".format(ctx.author.mention))

@Client.command(brief='Show the riddle or encouragements lists', description='This command shows the riddle list if you use "riddles" in <arg> and shows the encouragements list if you use "encouragements" in <arg>.')
async def see(ctx, arg):
  if not db["wip"]:
    lst = []
    if arg in db.keys():
      lst = db[arg]
      await ctx.send(list(lst))
  else:
    await ctx.send("Faz-me o favor de não me chateares **ENQUANTO ESTOU A LEVAR UPGRADE!**{0}".format(ctx.author.mention))

@Client.command(brief='BOT send a message', description='This command send a text to spech messado to the channel if the tts mode is ON.')
async def tts(ctx, arg):
  if not db["wip"]:
    await ctx.send(arg, tts=db["tts"])
  else:
    await ctx.send("Faz-me o favor de não me chateares **ENQUANTO ESTOU A LEVAR UPGRADE!**{0}".format(ctx.author.mention))

@Client.command(brief='Map location', description='This command sends a special image.')
async def local(ctx):
  if not db["wip"]:
    await ctx.send(file=discord.File("mapa.PNG"))
  else:
    await ctx.send("Faz-me o favor de não me chateares **ENQUANTO ESTOU A LEVAR UPGRADE!**{0}".format(ctx.author.mention))


@Client.command(brief='Show one riddle by number', description='Show a riddle that whould be chosed by the number, default number is 0.')
async def riddle(ctx, num=0):
  if not db["wip"]:
    if db["riddleStatus"]:
      await ctx.send(db["riddles"][int(num)], tts=db["tts"])
    else:
      await ctx.send(
                      "Não há adivinhas para ninguém! Muito menos para ti {0}!".
                      format(ctx.author.mention))
  else:
    await ctx.send("Faz-me o favor de não me chateares **ENQUANTO ESTOU A LEVAR UPGRADE!**{0}".format(ctx.author.mention))

@Client.command(brief='Answer a specific riddle by number', description='With this command you can answer a specific riddle by the number, if you answer correctly BOT send to you a DM with a congratx message and the prize.')
async def answer(ctx, num, arg):
  if not db["wip"]:
    if db["riddleStatus"]:
      if any(word in arg for word in riddle_answer[int(num)]):
        await ctx.author.send(
                          "Parabéns acertaste! Toma lá um biscoito!")
        await ctx.author.send(file=discord.File(maps[int(num)]))
      else:
        await ctx.author.send(
                          "Erraste! Não mereces ser empreendedor!")
    else:
      await ctx.send(
                      "Não aceito a tua resposta! Estou em modo PISTOLA!{0}".
                      format(ctx.author.mention))
  else:
    await ctx.send("Faz-me o favor de não me chateares ENQUANTO ESTOU A LEVAR UPGRADE!{0}".format(ctx.author.mention))

@Client.command(brief='Clear message from channel', description='Clear a certain number of messagem from the chat, by default is 5 messages.')
async def clear(ctx, amount=5):
  await ctx.channel.purge(limit=amount)

@Client.command(brief='BOT send a DM to specific user', description='With this command you can send a DM to someone in this discord channel using his tag.')
async def dm(ctx, user: discord.User, *, msg=None):
  if not db["wip"]:
    msg = msg or 'Oi gustosuh!!'
    await user.send(msg)
  else:
    await ctx.send("Faz-me o favor de não me chateares ENQUANTO ESTOU A LEVAR UPGRADE!{0}".format(ctx.author.mention))

keep_alive()
Client.run(os.environ['TOKEN'])
