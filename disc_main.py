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
    players_matches = await rankCommand.get_accs_data()
    match_dto = await rankCommand.get_accs_matches_info(players_matches)
    players_points = await rankCommand.point_processing(match_dto)
    print(players_points)


client.run('')