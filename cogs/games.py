#!/user/bin/env python
import discord
from discord.ext import commands
import asyncio
from random import randint

rouletteStarted, triviaStarted = False, False
bulletPos, chamberPos, triviaQuestion = 0, 0, 0
questions = [
"What do you cancel to get a boost grab in Smash Ultimate?",
"Who was the first Smash 4 DLC character?",
"What language is this bot coded in?",
"Where is this bot's creator from?"
]
answers = [
"roll",
"mewtwo",
"python",
"belgium"
]

class Games():
	def __init__(self, bot):
		self.bot = bot	
		
	#[-----Trivia-----]
	#Checking for answer
	def check_answer( self, answer ):
		return answers[triviaQuestion] in answer.content.lower()
	
	#Main trivia
	@commands.command(pass_context=True)
	@asyncio.coroutine
	def trivia( self, ctx, *args ):
		"""Starts a game of trivia!"""
		#Ensure no duplicate trivia games
		global triviaStarted
		if triviaStarted:
			yield from self.bot.send_message( ctx.message.channel, "Trivia already in session!" )
			return False
		triviaStarted = True
		
		#pick a question (not optimized but small scale enough)
		global triviaQuestion
		triviaQuestion = randint(0,len(questions)-1)
		yield from self.bot.send_message( ctx.message.channel, "[TRIVIA] " + questions[triviaQuestion] )
		
		#Wait for answer
		message = yield from self.bot.wait_for_message( check=self.check_answer, timeout=13 )
		if message is None:
			yield from self.bot.send_message( ctx.message.channel, "[TRIVIA] Nobody got the question right." )
		else:
			yield from self.bot.send_message( ctx.message.channel, "[TRIVIA] " + message.author.name + " got the correct answer!" )
		
		triviaStarted = False
		
		
	#[-----Russian Roulette-----]
	@commands.command(pass_context=True)
	@asyncio.coroutine
	def roulette( self, ctx, *args ):
		"""Starts a game of Russian roulette!"""
		global rouletteStarted, chamberPos, bulletPos
		#Initialize game
		if not rouletteStarted:
			yield from self.bot.send_message( ctx.message.channel, "Starting a new game of Russian Roulette!" )
			rouletteStarted = True
			bulletPos = randint(1,6)
			chamberPos = randint(1,6)

		#They lost
		if chamberPos == bulletPos:
			yield from self.bot.send_message( ctx.message.channel, ":boom: :gun: BAM! " +  ctx.message.author.name + " lost in Russian Roulette!" )
			rouletteStarted = False
		#They won
		else:
			if chamberPos == 6:
				chamberPos = 1
			else:
				chamberPos = chamberPos + 1
			yield from self.bot.send_message( ctx.message.channel, ctx.message.author.name + " lived... this time. "  )	
		
def setup(bot):
	bot.add_cog(Games(bot))
