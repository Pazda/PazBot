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
		#admin check
		if not ctx.message.author.server_permissions.administrator:
			yield from self.bot.send_message( ctx.message.channel, "You must be an admin to use this command." )
			return
		
		try:
			amount = int(args[0])
		except IndexError:
			yield from self.bot.send_message( ctx.message.channel, "You need to tell me how many messages to erase." )
			return
			
		if amount > 100:
			yield from self.bot.send_message( ctx.message.channel, "Please keep this under 100." )
			return
		
		logs = yield from self.bot.logs_from(ctx.message.channel)
		i = 0
		for message in logs:
			if i <= amount:
				yield from self.bot.delete_message( message )
				i += 1
				
		yield from self.bot.send_message( ctx.message.channel, "Wiped " + amount + " messages." )
		
		
def setup(bot):
	bot.add_cog(Admin(bot))
