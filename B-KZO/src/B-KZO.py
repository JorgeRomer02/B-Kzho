import asyncio
from unicodedata import category
import discord
from discord.ext import commands
import datetime
import aiohttp
from discord.utils import get
from urllib import parse, request
import re
from matplotlib.pyplot import title
from webserver import keep_alive
import os

# ESTABLECIMIENTO DEL PREFIJO ---------------------------------------------------------------------------------------------------------------------
bot = commands.Bot(command_prefix='+', description="El magnifico B-KZO no sirve para absolutamente nada :D")

# ELIMINACION DEL COMANDO "HELP" POR DEFECTO ------------------------------------------------------------------------------------------------------
bot.remove_command('help')

# COMANDOS DEL BOT --------------------------------------------------------------------------------------------------------------------------------
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Commandos del bot", description="primero que nada, todo se usa con el prefijo \"+\"", color=discord.Color.blue())
    embed.add_field(name="**help**", value="Te manda este mensaje")
    embed.add_field(name="admin", value="Te muestra una lista con los administradores")
    embed.add_field(name="ping", value="Es simplemente para ver si el bot esta jalando o si tiene delay")
    embed.add_field(name="sum", value="Por si estudiaste en un cetis, como su servilleta, suma")
    embed.add_field(name="res", value="Por si estudiaste en un cebatis, resta")
    embed.add_field(name="realm", value="Te da los datos de realm de minecraft del servidor")
    embed.add_field(name="info", value="Te hecha los datillos del server (owner, creacion,etc.)")
    embed.add_field(name="yt", value="Solo busca videos en youtube y te da el link")
    embed.add_field(name="clean", value="Sirve para borrar una cantidad de mensajes deseada")
    embed.add_field(name="create_c", value="Crea un canal permanente")
    embed.add_field(name="temp_c", value="Te genera un canal temporal")
    embed.add_field(name="del_c", value="Elimina un canal ya existente (pemanente)")
    embed.set_thumbnail(url="https://yt3.ggpht.com/FNtm76qzyhrIO0ryxNjs3hvnLpJuy3gZf7Jfyn7oesz8UaLRXJzcoiJqz7vIgZx6MviOFIIDMQ=s900-c-k-c0x00ffffff-no-rj")
    await ctx.send(embed=embed)

@bot.command()
async def admin(ctx):
    await ctx.send('Nomas hay 2 personas bro, que esperas')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def sum(ctx, numOne: int, numTwo: int):
    await ctx.send(numOne + numTwo)

@bot.command()
async def res(ctx, numOne: int, numTwo: int):
    await ctx.send(numOne - numTwo)

@bot.command()
async def realm(ctx):
    embed = discord.Embed(title="REALM DE MINECRAFT", description="tengo un realm de minecraft, porque no vienes con nosotros :D", color=discord.Color.blue())
    embed.add_field(name="Plataforma:\n", value="Bedrock")
    embed.add_field(name="Version:\n", value="latest")
    embed.add_field(name="Link:\n", value="https://realms.gg/3VtpDzbfCng")
    embed.set_thumbnail(url="https://seeklogo.com/images/M/minecraft-logo-5EAD3A1535-seeklogo.com.png")

    await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Ahí le bailan unos datillos del server", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    # embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/3309/3309960.png")

    await ctx.send(embed=embed)

@bot.command()
async def yt(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    # print(html_content.read().decode())
    search_results=re.findall('watch\?v=(.{11})',html_content.read().decode('utf-8'))
    #print(search_results)
    # I will put just the first result, you can loop the response to show more results
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])

#--# COMANDOS ADMINISTRATIVOS -------------------------------------------------------------------------------------------------------------------
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clean(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.send('{} Barrio el chat '.format(ctx.author.mention))
        await ctx.message.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def create_c(ctx, channel_name):
	guild = ctx.guild
	channel = await guild.create_text_channel(channel_name)

@bot.command()
@commands.has_role("VIP")
async def temp_c(ctx,time:int,*,ChannelName):
    mbed=discord.Embed(title='Succes!',description=f'Este canal se eliminara en {time} minutos!')
    cat = discord.utils.get(ctx.guild.categories, name="VIP")
    await ctx.guild.create_text_channel(name = ChannelName,category=cat)
    channel = get(ctx.guild.channels, name = ChannelName)
    await ctx.send(embed = mbed)
    await asyncio.sleep(60*time)
    await channel.delete()

@bot.command()
async def del_c(ctx, channel: discord.TextChannel, time: int):
 if ctx.author.guild_permission.manage_channels:
  await ctx.send(f'Este canal ya existente se eliminara en {time} minutos.')
  await asyncio.sleep(60*time)
  await channel.delete()

# EVENTOS/ERRORES ---------------------------------------------------------------------------------------------------------------------------
@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Oilo, ni que fueras admin, que pues")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="The Legend Of Kaizho",url='https://www.youtube.com/watch?v=lLSu0UHNZhU'))
    print('Bot en linea')

keep_alive()
bot.run('OTk0ODExMjY2NTU4MzM3MDI0.GPER-U.6n2myoLlrU7CU93mDbwqwmNzjw_jXy0Pgfx9xk')
