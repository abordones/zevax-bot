import discord
from discord.ext import commands
import logging
import os
import webserver
from dotenv import load_dotenv
from datetime import datetime
import random
from textacos import APOCALYPSE_TEXT

load_dotenv()

#imprimir todas las variables de entorno para debuggear
print("Environment Variables:")
for key, value in os.environ.items():
    print(f"{key}: {value}")

token = os.getenv("BOT_TOKEN")
forec_event_id = os.getenv("FOREC_EVENT_ID")

image_path = os.getenv("FOREC_IMAGE")

test_event_id = os.getenv("TEST_EVENT_ID")
test_user_id = os.getenv("TEST_ID_USER")    

handlers = logging.FileHandler(filename='zevaxt-bot.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.guild_scheduled_events = True
intents.members = True

bot = commands.Bot(command_prefix='z!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

    
@bot.command()
async def ping(ctx):
    await ctx.send(f'toy aca')

@bot.command()
async def tictac(ctx):
    await ctx.send(f'ommmmmmm :person_in_lotus_position:')

@bot.command()
async def cocobug(ctx):
    await ctx.send(f'env variables')
    print("=" * 50)
    for key, value in os.environ.items():
        if key == "BOT_TOKEN":
            censored_token = value[:3] + '*' * (len(value) - 6) + value[-3:] if len(value) > 6 else '*' * len(value)
            print(f"{key}: {censored_token}")
        else:
            print(f"{key}: {value}")
    print("=" * 50)



@bot.command()
async def listevents(ctx):
    events = ctx.guild.scheduled_events
    
    if not events:
        await ctx.send("No scheduled events found on this server.")
        return
    
    event_list = []
    for event in events:
        event_list.append(f"**{event.name}** - ID: `{event.id}`")
    
    await ctx.send("\n".join(event_list))
    
    # Also print to console
    print("=" * 50)
    print("Scheduled Events on Server:")
    for event in events:
        print(f"{event.name}: {event.id}")
    print("=" * 50)


@bot.command()
async def df(ctx):

    if not forec_event_id :
        await ctx.send("El id no esta en el env, pibe")
        print(f"{forec_event_id} is not set in the environment variables.")
        return
    
    try:
        event_id = int(forec_event_id)
        events = ctx.guild.scheduled_events
        target_event = None

        for event in events:
            if event.id == event_id:
                target_event = event
                break
        

        if target_event is None:
            await ctx.send(f"el evento no existe, pije")
            print(f"Event with ID {event_id} not found in the guild's scheduled events.")
            return
        
        if not target_event.start_time:
            await ctx.send("ese evento no tiene hora, hijito")
            return
        
        now = datetime.now(target_event.start_time.tzinfo)
        time_diff = target_event.start_time - now

        # weas para ver si el tiempo esta bien
        print(f"Time difference: {time_diff}")
        print(f"{time_diff.total_seconds()=} Seconds")
        print(f"{time_diff.total_seconds() / 60=} Minutes")
        print(f"{time_diff.total_seconds() / 3600=} Hours")
        print(f"{time_diff.total_seconds() / 86400=} Days")

        if time_diff.total_seconds() <= 0:
            embed = discord.Embed(
                title=f" ",
                description=" ",
                color=0xff6b35
            ) 

            if image_path and os.path.exists(image_path):
                file = discord.File(image_path, filename="eshoy.png")
                embed.set_image(url="attachment://eshoy.png")
                await ctx.send(file=file, embed=embed)
            else:
                await ctx.send(embed=embed)

        else: # mas de 1 dia
            longahh = APOCALYPSE_TEXT
            full_text = "\n\n".join(longahh)
            
            embed = discord.Embed(
                title=f"**{time_diff.total_seconds() / 86400:.0f} Días**",
                description=full_text,
                color=0x000000
            )

            if image_path and os.path.exists(image_path):
                file = discord.File(image_path, filename="event_image.png")
                embed.set_image(url="attachment://event_image.png")
                await ctx.send(file=file, embed=embed)
            else:
                await ctx.send(embed=embed)


    except ValueError:
        await ctx.send("Invalid test event ID format in environment file.")
    except Exception as e:
        print(f"Error fetching event: {str(e)}")
        await ctx.send(f"An error occurred while fetching test event information: {str(e)}")

@bot.command()
async def targetevent(ctx):
    if not forec_event_id:
        await ctx.send("El id no esta en el env")
        print(f"{forec_event_id} is not set in the environment variables.")
        return
    
    try:
        event_id = int(forec_event_id)
        events = ctx.guild.scheduled_events
        target_event = None

        for event in events:
            if event.id == event_id:
                target_event = event
                break
        
        if target_event is None:
            await ctx.send(f"el evento no existe, pije")
            print(f"Event with ID {event_id} not found in the guild's scheduled events.")
            return
        
        await ctx.send(f"Targeted event: **{target_event.name}** - ID: `{target_event.id}`")

    except ValueError:
        await ctx.send("Invalid test event ID format in environment file.")
    except Exception as e:
        print(f"Error fetching event: {str(e)}")
        await ctx.send(f"An error occurred while fetching test event information: {str(e)}")

if __name__ == "__main__":
    webserver.keep_alive()
    
    print("Starting Discord bot...")
    bot.run(token, log_handler=handlers, log_level=logging.DEBUG)
