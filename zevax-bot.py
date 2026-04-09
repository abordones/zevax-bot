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
token = os.getenv("BOT_TOKEN")
zevax_event_id = os.getenv("ZEVAX_EVENT_ID")
forec_event_id = os.getenv("FOREC_EVENT_ID")

image_path = os.getenv("FOREC_IMAGE")
final_image_path = os.getenv("FINAL_IMAGE")
end_image_path = os.getenv("END_IMAGE")

zevax_user_id = os.getenv("ZEVAX_USER_ID")
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

''' 
respuesta aleatoria

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
        
    if zevax_user_id and str(message.author.id) == zevax_user_id:
        random_roll = random.randint(1, 5) # 1 out of 5 chance

        if (random_roll == 1):
            if (message.content.startswith('z!')):
                return
            else:
                responses = [
                    "## MEMENTO MORI"
                ]
                
                selected_response = random.choice(responses)
                
                embed = discord.Embed(
                    title=f"⏰🐇",
                    description=selected_response,
                    color=0x36060b
                )
                
                if image_path and os.path.exists(image_path):
                    file = discord.File(image_path, filename="3meses.png")
                    embed.set_image(url="attachment://3meses.png")
                    await message.reply(file=file, embed=embed)
                else:
                    await message.reply(embed=embed)

    await bot.process_commands(message)
'''
    
@bot.command()
async def ping(ctx):
    await ctx.send(f'toy aca')

@bot.command()
async def tictac(ctx):
    await ctx.send(f'ommmmmmm :person_in_lotus_position:')


@bot.command()
async def df(ctx):

    if not forec_event_id :
        await ctx.send("El id no esta en el env, pibe")
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

            if end_image_path and os.path.exists(end_image_path):
                file = discord.File(end_image_path, filename="eshoy.png")
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

if __name__ == "__main__":
    webserver.keep_alive()
    
    print("Starting Discord bot...")
    bot.run(token, log_handler=handlers, log_level=logging.DEBUG)
