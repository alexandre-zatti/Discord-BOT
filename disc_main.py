import discord
import join as joinCommand
import rank as rankCommand
from discord.ext import commands

client = commands.Bot(command_prefix= '!')


@client.event
async def on_ready():
    print('ready!')

@client.command()
async def hello(ctx):
    await ctx.reply('Opa garotão!')

@client.command()
async def join(ctx,arg1,arg2):
    await joinCommand.join_acc(ctx,arg1,arg2)

@client.command()
async def rank(ctx):
    await rankCommand.say(ctx)


client.run('Nzk5Mzk1OTI2MTYxNDg5OTYw.YAC9eA.xckf971SxLlJ6mQM6UJHXtQOpf0')