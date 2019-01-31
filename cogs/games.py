#!/user/bin/env python
import discord
from discord.ext import commands
import asyncio
from random import randint, choice

finp = open( "trivia.txt", "r" )

rouletteStarted, triviaStarted = {}, {}
bulletPos, chamberPos, triviaQuestion = 0, 0, 0
questions = eval( finp.read() )
finp.close()

class Games():
	def __init__(self, bot):
		self.bot = bot
		
	#[------Spin the Bottle-----]
	@commands.command(pass_context=True)
	@asyncio.coroutine
	def spin( self, ctx, *args ):
		"""Spin the bottle :flushed:"""
		potentials = []
		for user in ctx.message.server.members:
			if user.status != discord.Status.offline:
				potentials.append( user.name )
		yield from self.bot.send_message( ctx.message.channel, ctx.message.author.name + " has to kiss " + choice( potentials ) + "! :kiss:" )
		
	#[-----Trivia-----]
	#Checking for answer
	def check_answer( self, answer ):
		return questions[triviaQuestion] in answer.content.lower()
	
	#Main trivia
	@commands.command(pass_context=True)
	@asyncio.coroutine
	def trivia( self, ctx, *args ):
		"""Starts a game of trivia!"""
		#Ensure no duplicate trivia games
		global triviaStarted
		try:
			if triviaStarted[ctx.message.server.id]:
				yield from self.bot.send_message( ctx.message.channel, "Trivia already in session!" )
				return False
			triviaStarted[ctx.message.server.id] = True
		except KeyError:
			triviaStarted[ctx.message.server.id] = True
		
		#pick a question (not optimized but small scale enough)
		global triviaQuestion
		triviaQuestion = choice( list( questions.keys() ) )
		yield from self.bot.send_message( ctx.message.channel, "[TRIVIA] " + triviaQuestion )
		
		#Wait for answer
		message = yield from self.bot.wait_for_message( check=self.check_answer, timeout=18 )
		if message is None:
			yield from self.bot.send_message( ctx.message.channel, "[TRIVIA] Nobody got the question right." )
		else:
			yield from self.bot.send_message( ctx.message.channel, "[TRIVIA] " + message.author.name + " got the correct answer!" )
		
		triviaStarted[ctx.message.server.id] = False
		
		
	#[-----Russian Roulette-----]
	@commands.command(pass_context=True)
	@asyncio.coroutine
	def roulette( self, ctx, *args ):
		"""Starts a game of Russian roulette!"""
		global rouletteStarted, chamberPos, bulletPos

		#Initialize game
		try:
			if not rouletteStarted[ctx.message.server.id]:
				yield from self.bot.send_message( ctx.message.channel, "Starting a new game of Russian Roulette!" )
				rouletteStarted[ctx.message.server.id] = True
				bulletPos = randint(1,6)
				chamberPos = randint(1,6)
		except KeyError:
			yield from self.bot.send_message( ctx.message.channel, "Starting a new game of Russian Roulette!" )
			rouletteStarted[ctx.message.server.id] = True
			bulletPos = randint(1,6)
			chamberPos = randint(1,6)
			

		#They lost
		if chamberPos == bulletPos:
			yield from self.bot.send_message( ctx.message.channel, ":boom: :gun: BAM! " +  ctx.message.author.name + " lost in Russian Roulette!" )
			rouletteStarted[ctx.message.server.id] = False
		#They won
		else:
			if chamberPos == 6:
				chamberPos = 1
			else:
				chamberPos = chamberPos + 1
			yield from self.bot.send_message( ctx.message.channel, ctx.message.author.name + " lived... this time. "  )	
		
def setup(bot):
	bot.add_cog(Games(bot))
