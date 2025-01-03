import discord
from config import TOKEN, PRIVATE_CHANNEL_ID
from discord.ext import commands

# Configure le bot avec les intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Nécessaire pour lire les contenus des messages
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
  print(f"Bot connecté en tant que {bot.user}")


@bot.event
async def on_message(message):
  # Vérifie que le message provient d'un DM et qu'il ne vient pas du bot lui-même
  if message.guild is None:
    # Relaye le message dans le canal spécifié
    channel = bot.get_channel(PRIVATE_CHANNEL_ID)
    if channel:
      await channel.send(f"DM de {message.author} : {message.content}")

  if message.guild and message.author != bot.user:
    channel = bot.get_channel(PRIVATE_CHANNEL_ID)
    if message.attachments and channel:  # Vérifie si le message contient des fichiers attachés
      for attachment in message.attachments:
        if attachment.content_type.startswith(
            "image/"):  # Vérifie si c'est une image
          await channel.send(f"Message de {message.author} : {message.content}"
                             )
          await attachment.save(attachment.filename
                                )  # Sauvegarde l'image localement
          await message.channel.send(
              f"Image reçue : {attachment.filename} sauvegardée !")
          await channel.send(f"Image relayée depuis {message.author} :",
                             file=await attachment.to_file())
          await message.delete()  # Supprime le message original

    elif channel:
      await channel.send(f"Message de {message.author} : {message.content}")
      await message.delete()


bot.run(TOKEN)
