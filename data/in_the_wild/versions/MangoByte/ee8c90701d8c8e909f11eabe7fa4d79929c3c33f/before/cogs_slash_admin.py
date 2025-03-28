import asyncio

import disnake
from disnake.ext import commands
from utils.command import botdatatypes, checks
from utils.tools.botdata import GuildInfo
from utils.tools.globals import botdata, logger
from utils.tools.helpers import *

from .mangocog import *


class Admin(MangoCog):
	"""Commands to help manage mangobyte on your server/guild
	
	Primarily used to stop people from ruining stuff, and to configure mangobyte to do different things.

	Only admins or people with the correct role can use these commands. To set a role as the 'Bot Admin' role, try `{cmdpfx}config botadmin`"""
	def __init__(self, bot):
		MangoCog.__init__(self, bot)
	
	def bot_check(self, ctx_inter: InterContext):
		"""Checks to make sure the user has permissions"""
		commandname = ""
		cog = None
		guildinfo = botdata.guildinfo(ctx_inter)
		if isinstance(ctx_inter, disnake.Interaction):
			if isinstance(ctx_inter, disnake.CommandInter):
				commandname = slash_command_name(ctx_inter)
			# check cogs
			cog = ctx_inter.application_command.cog
			if cog:
				if not cog.cog_check(ctx_inter):
					return False
		else:
			commandname = ctx_inter.command
			cog = ctx_inter.cog
		
		if guildinfo and ctx_inter.channel.type != disnake.ChannelType.private:
			if guildinfo.is_banned(ctx_inter.author):
				return False
			if guildinfo.is_disabled(commandname):
				return False
			if guildinfo.is_disabled(cog):
				return False
		return True

	def cog_check(self, ctx_inter: InterContext):
		"""Checks to make sure the user has admin privilages"""
		return checks.is_admin_check(ctx_inter)

	@commands.command()
	async def botban(self, ctx, user: disnake.Member):
		"""Bans the user from using commands"""
		if checks.is_owner_check(user):
			await ctx.send("Ya can't ban mah owner, man. 😠")
			return
		if checks.is_admin_check(ctx, user):
			if not checks.is_owner_check(ctx.message.author):
				await ctx.send("Ya can't ban other admins")
				return
		if user.id == self.bot.user.id:
			await ctx.send("Lol you can't ban me, silly")
			return
		botdata.guildinfo(ctx.message.guild).botban(user)
		await ctx.send("{} has henceforth been banned from using commands 😤".format(user.mention))

	@commands.command()
	async def botunban(self, ctx, user: disnake.Member):
		"""Unbans the user, allowing them to use commands"""
		if checks.is_owner_check(user) or user == self.bot.user:
			await ctx.send("Ha ha. Very funny.")
			return
		botdata.guildinfo(ctx.message.guild).botunban(user)
		await ctx.send("{} is free of their restraints and may once again use commands".format(user.mention))

	def get_command_or_cog(self, bot: commands.Bot, text):
		result = bot.cogs.get(text)
		if result is not None:
			return result
		result = bot.get_command(text)
		if result is not None:
			return result
		result = bot.get_slash_command(text)
		if result is not None:
			return result
		text = text.lower()
		for cog in bot.cogs:
			if text == cog.lower():
				return bot.cogs[cog]
		return None

	@commands.command()
	async def disablecommand(self, ctx, command: str):
		"""Disabled the specified command or command category

		**Examples:**
		`{cmdpfx}disablecommand wiki`
		`{cmdpfx}disablecommand Audio`"""
		guildinfo = botdata.guildinfo(ctx)
		if not guildinfo:
			raise UserError("This command must be called in a guild")

		cmd = self.get_command_or_cog(ctx.bot, command)
		if cmd is None:
			raise UserError("Couldn't find a command or command category by that name")

		secure_cogs = [ "Admin", "Owner" ]
		if isinstance(cmd, disnake.ext.commands.Command):
			if guildinfo.is_disabled(cmd.cog_name):
				raise UserError(f"The category this command belongs to ({cmd.cog_name}) is already disabled")
			if cmd.cog_name in secure_cogs:
				raise UserError("You can't disable a command in this category")
		else:
			if cmd.name in secure_cogs:
				raise UserError("You can't disable this category")

		if guildinfo.is_disabled(cmd.name):
			raise UserError("This has already been disabled")
		guildinfo.disable_command(cmd.name)
		await ctx.message.add_reaction("✅")

	@commands.command()
	async def enablecommand(self, ctx, command: str):
		"""Re-enables the specified command or command category

		Only works on commands that have already been disabled by the `{cmdpfx}disablecommand` command

		**Examples:**
		`{cmdpfx}enablecommand wiki`
		`{cmdpfx}enablecommand Audio`"""
		guildinfo = botdata.guildinfo(ctx)
		if not guildinfo:
			raise UserError("This command must be called in a guild")
		cmd = self.get_command_or_cog(ctx.bot, command)
		if cmd is None:
			raise UserError("Couldn't find a command or command category by that name")
		if not guildinfo.is_disabled(cmd.name):
			if guildinfo.is_disabled(cmd):
				raise UserError(f"This command is not disabled, but its category ({cmd.cog_name}) is")
			else:
				raise UserError("This is not currently disabled")
		guildinfo.enable_command(cmd.name)
		await ctx.message.add_reaction("✅")


	@commands.command()
	async def summon(self, ctx, channel : str = None):
		"""Summons the bot to the voice channel

		You can specify the specific voice channel that you would like to connect to. If no channel is specified, it will connect to whatever channel you are currently in.
		**Examples:**
		`{cmdpfx}summon`
		`{cmdpfx}summon General`"""
		if channel:
			actual_channel = None
			if ctx.message.guild:
				for ch in ctx.message.guild.voice_channels:
					if channel.lower() == ch.name.lower():
						actual_channel = ch
						break
				if not actual_channel:
					for ch in ctx.message.guild.voice_channels:
						if channel.lower() in ch.name.lower():
							actual_channel = ch
							break
			channel = actual_channel

		if not channel:
			if not ctx.message.guild:
				raise UserError("You have to say that in a server")
			if not ctx.message.author.voice:
				raise UserError("You are not currently in a voice channel")
			channel = ctx.message.author.voice.channel
			if channel.guild != ctx.message.guild:
				raise UserError("You are not currently in a voice channel on this server/guild")

		audio = self.bot.get_cog("Audio")
		if not audio:
			raise UserError("You must have the Audio cog enabled to do this")
		try:
			await audio.connect_voice(channel)
			botdata.guildinfo(channel.guild.id).voicechannel = channel.id
		except asyncio.TimeoutError:
			cmdpfx = botdata.command_prefix(ctx)
			raise UserError(f"There was a timeout when attempting to do the `{cmdpfx}summon`")
		await ctx.message.add_reaction("✅")


	@commands.command()
	async def unsummon(self, ctx):
		"""Removes the bot from the voice channel"""
		audio = self.bot.get_cog("Audio")
		if not audio:
			raise UserError("You must have the Audio cog enabled to do this")
		if not ctx.message.guild:
			raise UserError("You have to say that in a server")
		await audio.disconnect(ctx.message.guild)
		botdata.guildinfo(ctx.message.guild.id).voicechannel = None
		await ctx.message.add_reaction("✅")


	@commands.command()
	async def resummon(self, ctx):
		"""Re-summons the bot to the voice channel

		This command is useful if you are having issues with mangobyte not being responsive"""
		audio = self.bot.get_cog("Audio")
		if not audio:
			raise UserError("You must have the Audio cog enabled to do this")
		if not ctx.message.guild:
			raise UserError("You have to be in a server to use this command")

		guildinfo = botdata.guildinfo(ctx.message.guild.id)

		save_channel = False
		channel = None
		if ctx.message.guild.me.voice:
			channel = ctx.message.guild.me.voice.channel
		elif ctx.message.author.voice:
			channel = ctx.message.author.voice.channel
		elif guildinfo.voicechannel is not None:
			channel = self.bot.get_channel(guildinfo.voicechannel)
		else:
			raise UserError("I'm not sure where you want me to resummon to. I'm not in any channel currently.")

		await audio.disconnect(ctx.message.guild)

		await asyncio.sleep(1)

		try:
			await audio.connect_voice(channel)
			guildinfo.voicechannel = channel.id
		except asyncio.TimeoutError:
			cmdpfx = botdata.command_prefix(ctx)
			raise UserError(f"There was a timeout when attempting to do the `{cmdpfx}summon`")

		await ctx.message.add_reaction("✅")

	@commands.slash_command()
	async def config(self, inter: disnake.CmdInter, setting: commands.option_enum(GuildInfo.keys_list()), value: str):
		"""Configures the bot's settings for this server/guild

		Parameters
		----------
		setting: The setting you'd like to show/change
		value: The value you'd like to set for this setting, or 'show' to see the current value and more info
		"""
		if inter.guild is None:
			await inter.send("You must be in a server/guild to use this command")
			return
		if value == "show":
			value = None
		var = next((v for v in GuildInfo.variables if v["key"] == setting), None)
		
		currentvalue = botdata.guildinfo(inter.guild)[var["key"]]
		if not value: # We are just getting a value
			await inter.send(embed=await botdatatypes.localize_embed(inter, var, currentvalue, f"/config"))
		else: # We are setting a value
			value = await botdatatypes.parse(inter, var, value, currentvalue)
			botdata.guildinfo(inter.guild)[var["key"]] = value
			await inter.send(f"✅ {setting} has been set!")


def setup(bot):
	bot.add_cog(Admin(bot))
