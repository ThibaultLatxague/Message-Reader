import discord
from config import TOKEN, PRIVATE_CHANNEL_ID
from discord.ext import commands

# Configure le bot avec les intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Nécessaire pour lire les contenus des messages
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)
USER_ID = 661239854197112835


@bot.event
async def on_ready():
	print(f"Bot connecté en tant que {bot.user}")


async def envoyer_mp(user_id: int, message: str, channel):
	"""Commande pour envoyer un MP à un utilisateur spécifique."""
	try:
		user = await bot.fetch_user(user_id)  # Récupère l'utilisateur par son ID
		await user.send(message)  # Envoie un MP
		await channel.send(
		    f"Message envoyé à {user.name}#{user.discriminator} avec succès !")
	except Exception as e:
		await channel.send(f"Erreur : {e}")


@bot.event
async def on_message(message):
	if message.guild and message.author != bot.user:
		channel = bot.get_channel(PRIVATE_CHANNEL_ID)
		if message.attachments and channel:  # Vérifie si le message contient des fichiers attachés
			for attachment in message.attachments:
				if attachment.content_type.startswith(
				    "image/"):  # Vérifie si c'est une image
					await channel.send(
					    f"Message de {message.author} : {message.content}")
					await attachment.save(attachment.filename
					                      )  # Sauvegarde l'image localement
					await message.channel.send(
					    f"Image de {message.author} : {attachment.filename} sauvegardée !"
					)
					await channel.send(f"Image relayée depuis {message.author} :",
					                   file=await attachment.to_file())
					await message.delete()  # Supprime le message original
					await envoyer_mp(USER_ID, "Message sauvegardé avec succès !",
					                 channel)
		elif channel:
			await channel.send(f"Message de {message.author} : {message.content}")
			await message.delete()
			await envoyer_mp(USER_ID, "Message sauvegardé avec succès !", channel)


bot.run(TOKEN)
