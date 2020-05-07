#!/usr/bin/env python
#from difflib import SequenceMatcher
import discord
import numpy as np
from joblib import dump, load
import sys
import math


helpText = "Tell me the sizes of two of your gems and i will calculate the optimal size of the third gem based on the current ritual bonus. If running a ritual with a bigger third gem will still yield a maximum sized gem (2,999,997). You can also change the bonus to use or get the current bonus used for calculations.\n"
helpText = helpText + "Type \"!max SIZE1,SIZE2\" where SIZE1 and SIZE2 are numeric values, the sizes of your first and second gem respectively. Type !bonus [set=VAL] to get or set the current ritual bonus.\n"

	
def calculate(text):
	text = text.split(",")
	if len(text) != 2:
		return helpText

	val = [-1,-1]
	for i in range(2):
		try:
			val[i] = int(text[i].replace(" ",""))
		except ValueError:
			return "Could not parse value \"" + text[i] + "\". Must be an integer value, check your input and try again!"
	
	bonus = load('bonus.joblib')
	target = math.ceil(2999997/bonus) - val[0] - val[1]
	if 0 < target <= 999999:
		return "Optimal 3rd gem size is " + str(target) + ". Absolute bonus will be " + str(2999997 - val[0] - val[1] - target) + "."
	elif not 0 < val[0] <= 999999 or not 0 < val[1] <= 999999:
		return "Whoops, something went wrong with your input values... valid gems have a positive value below 1,000,000. Your input values where \"" + text[0] + "\" and \"" + text[1] + "\". Check your input and try again!"
	else:
		return "Optimal 3rd gem size would be " + str(target) + ". Try bigger 1st and 2nd gem for a maximum gem ritual."

def bonus(text):
	text = text.split("=")
	if len(text) != 2 or text[0].lower().replace(" ","") != "set":
		return "Current ritual bonus is " + str(load('bonus.joblib'))
	try:
		val = float(text[1].replace(" ",""))
	except ValueError:
		return "Could not parse value \"" + text[i] + "\". Must be a floating point value, check your input and try again!"

	dump(val,'bonus.joblib')
	return "Bonus set to " + str(val) +"."

TOKEN = sys.argv[1]

client = discord.Client()	
@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if message.content.startswith('!max'):
		msg = calculate(message.content[4:])
		msg = msg.format(message)
		await message.channel.send(msg)
	elif message.content.startswith('!bonus'):
		msg = bonus(message.content[6:])
		msg = msg.format(message)
		await message.channel.send(msg)
		
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	
client.run(TOKEN)

