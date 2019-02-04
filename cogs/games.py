#!/user/bin/env python
import discord
from discord.ext import commands
import asyncio
from random import randint, choice

finp = open( "trivia.txt", "r" )
storyLoader = open( "stories.txt", "r" )

rouletteStarted, triviaStarted, stories = {}, {}, {}
bulletPos, chamberPos, triviaQuestion = 0, 0, 0
questions = eval( finp.read() )
stories = eval( storyLoader.read() ) #reading a dict of strings so shouldn't have holes
finp.close()
storyLoader.close()

storySaver = open( "stories.txt", "w" )

class Games():
	def __init__(self, bot):
		self.bot = bot
		
	#[------Storytime------]
	#TODO: move to a text file so it's not deleted when bot goes offline
	@commands.command(pass_context=True)
	@asyncio.coroutine
	def story( self, ctx, *args ):
		"""Write a story with your friends."""
		global stories
		
		#Generating new story if none exists
		try:
			story = stories[ctx.message.server.id]
		except KeyError:
			yield from self.bot.send_message( ctx.message.channel, "No story detected. Generating a blank one." )
			stories[ctx.message.server.id] = ""
			return
		
		#Getting an argument, helping if none
		try:
			command = args[0]
		except IndexError: #if just !story
			yield from self.bot.send_message( ctx.message.channel, "No arguments provided. Try 'read', 'add', or 'clear'." )
			return
			
		#Read argument
		if command == 'read':
			yield from self.bot.send_message( ctx.message.channel, "Story:\n" + stories[ctx.message.server.id] )
			return
		#Add argument
		elif command == 'add':
			#combine the rest of the arguments (probably a better way somewhere)
			added = ""
			for i in range( len(args) ):
				if i == 0:
					continue
				added += args[i] + " "
				
			added = added[:-1]
			#Punctuation
			if not added.endswith('.') and not added.endswith('?') and not added.endswith('!'):
				added += "."
			added += " "
				
			stories[ctx.message.server.id] += ( added )
			yield from self.bot.send_message( ctx.message.channel, "Added to story. \n\n" + stories[ctx.message.server.id] )
			storySaver.seek(0)
			storySaver.truncate()
			storySaver.write( str( stories ) )
			return
		#Clear the story
		elif command == 'clear':
			stories[ctx.message.server.id] = ""
			yield from self.bot.send_message( ctx.message.channel, "Cleared the story." )
			storySaver.seek(0)
			storySaver.truncate()
			storySaver.write( str( stories ) )
			return
		else:
			yield from self.bot.send_message( ctx.message.channel, "Invalid argument. Try 'read', 'add', or 'clear'." )
				
		
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
		if answer.author.name is 'PazBot':
			return False
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
