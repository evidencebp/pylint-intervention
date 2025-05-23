import asyncio
import discord
import os
from   datetime import datetime
from   operator import itemgetter
from   discord.ext import commands

# This is the Debugging module. It keeps track of how long the bot's been up

class Debugging:

	# Init with the bot reference, and a reference to the settings var
	def __init__(self, bot, settings, debug = False):
		self.bot = bot
		self.settings = settings
		self.debug = debug

	async def oncommand(self, command, ctx):
		if self.debug:
			# We're Debugging
			timeStamp = datetime.today().strftime("%Y-%m-%d %H.%M")
			msg = '{}{}:\n"{}"\nRun at {}\nBy {}\nOn {}'.format(ctx.prefix, command, ctx.message.content, timeStamp, ctx.message.author.name, ctx.message.server.name)
			if os.path.exists('debug.txt'):
				# Exists - let's append
				msg = "\n\n" + msg
				with open("debug.txt", "a") as myfile:
					myfile.write(msg)
			else:
				with open("debug.txt", "w") as myfile:
					myfile.write(msg)

	@commands.command(pass_context=True)
	async def setdebug(self, ctx, *, debug = None):
		"""Turns on/off debugging (owner only - always off by default)."""

		author  = ctx.message.author
		server  = ctx.message.server
		channel = ctx.message.channel

		try:
			owner = self.settings.serverDict['Owner']
		except KeyError:
			owner = None

		if owner == None:
			# No previous owner, let's set them
			msg = 'I cannot adjust debugging until I have an owner.'
			await self.bot.send_message(channel, msg)
			return
		if not author.id == owner:
			# Not the owner
			msg = 'You are not the *true* owner of me.  Only the rightful owner can change this setting.'
			await self.bot.send_message(channel, msg)
			return

		if debug == None:
			# Swap
			if self.debug == False:
				debug = True
			else:
				debug = False
		elif debug.lower() == "yes" or debug.lower() == "on":
			debug = True
		elif debug.lower() == "no" or debug.lower() == "off":
			debug = False
		else:
			debug = None

		if debug == True:
			if self.debug == True:
				msg = 'Debugging remains enabled.'
			else:
				msg = 'Debugging now enabled.'
		else:
			if self.debug == False:
				msg = 'Debugging remains disabled.'
			else:
				msg = 'Debugging now disabled.'
		self.debug = debug
		
		await self.bot.send_message(ctx.message.channel, msg)