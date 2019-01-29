#!/user/bin/env python

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from tweetMaker import runTrain
import os, sys

fout = open( ".\print_data.txt", "w" )
newF = open( ".\print_data.txt", "r" )
fout.truncate(0)

TOKEN = ''

bot = commands.Bot( command_prefix = '!' )

generatorInUse = False

#NN command
@bot.command(pass_context=True)
@asyncio.coroutine
def twitNN( ctx, *args ):

	#Just don't do anything if it's already in use.. small scale application anyway
	global generatorInUse
	if generatorInUse:
		bot.send_message( ctx.message.channel, "Learner currently in use, please wait." )
		return
	generatorInUse = True

	wrongFormat = "Improper format: !twitNN <username> <max tweets (<3000)> <number of tweets to generate (<20)> <temperature (<4.0)> <epochs to train (<30)>"

	#Make sure they're all the right format
	try:
		maxTweets = int( args[1] )
		genAmount = int( args[2] )
		temp = float( args[3] )
		epochs = int( args[4] )
	except IndexError:
		yield from bot.send_message( ctx.message.channel, wrongFormat )
		generatorInUse = False
		return
	except ValueError:
		yield from bot.send_message( ctx.message.channel, wrongFormat )
		generatorInUse = False
		return

	#Make sure no out of bounds stuff
	if len(args) is not 5 or maxTweets > 3000 or maxTweets < 30 or genAmount < 1 or genAmount > 20 or temp > 4.0 or temp < 0.1 or epochs < 1 or epochs > 30:
		yield from bot.send_message( ctx.message.channel, wrongFormat )
		generatorInUse = False
		return

	yield from bot.send_message( ctx.message.channel, "Generating your tweets. This may take up to 15 minutes." )
	
	#Start new process so we can keep pinging Discord on main process 
	newpid = os.fork()
	if newpid == 0:
	#Get return value
		retVal = yield from runTrain( True, maxTweets, args[0], genAmount, temp, epochs )
		os._exit(0)
		
	generatorInUse = False

#Reuse existing model
#TODO: User checks; documentation for user
@bot.command(pass_context=True)
@asyncio.coroutine
def twitNNR( ctx, *args ):
	retVal = yield from runTrain( False, 0, "", int(args[0]), float(args[1]), 0 )
	#If it's empty, we can't sned it, so send a notice instead
	#yield from bot.send_message( ctx.message.channel, "[-------Your new tweets-------]" )
	printStr = ""
	printStr = printStr + "[-------Your new tweets-------]\n\n"
	for x in range( int(args[0]) ):
		if retVal[x] == '':
			retVal[x] = 'Learner notice: Empty tweet.'
		#yield from bot.send_message( ctx.message.channel, retVal[ x ] )
		printStr = printStr + retVal[x] + "\n\n"
	#yield from bot.send_message( ctx.message.channel, "[-----------------------------]" )
	printStr = printStr + "[-------------------------]"
	yield from bot.send_message( ctx.message.channel, printStr )


bot.run( TOKEN )
