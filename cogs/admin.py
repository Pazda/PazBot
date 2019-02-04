#!/user/bin/env python
import discord
from discord.ext import commands
import asyncio

class Admin():
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command(pass_context=True)
	@asyncio.coroutine
	def wipe( self, ctx, *args ):
		"""Wipes the last X messages"""
		#admin check
		if not ctx.message.author.server_permissions.administrator:
			yield from self.bot.send_message( ctx.message.channel, "You must be an admin to use this command." )
			return
		
		#Make sure we got an argument
		try:
			amount = int(args[0])
		except IndexError:
			yield from self.bot.send_message( ctx.message.channel, "You need to tell me how many messages to erase." )
			return
			
		#Not above 100 plz
		if amount > 100:
			yield from self.bot.send_message( ctx.message.channel, "Please keep this under 100." )
			return
		
		#Actually do it
		logs = yield from self.bot.logs_from(ctx.message.channel)
		i = 0
		for message in logs:
			if i <= amount: #1 extra for the new message
				yield from self.bot.delete_message( message )
				i += 1

		
def setup(bot):
	bot.add_cog(Admin(bot))
