import discord
from discord.ext import commands
import logging
import os
import webserver
from dotenv import load_dotenv
from datetime import datetime
import random

load_dotenv()
token = os.getenv("BOT_TOKEN")
test_event_id = os.getenv("TEST_EVENT_ID")
image_path = os.getenv("MAIN_IMAGE")
zevax_user_id = os.getenv("ZEVAX_USER_ID")

handlers = logging.FileHandler(filename='zevaxt-bot.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='z!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if zevax_user_id:
        recent_user_id = str(message.author.id)
        if recent_user_id == zevax_user_id:
            print(f"   Usuario: {message.author.display_name}")
            print(f"   ID: {recent_user_id}")
            print(f"   Contenido: {message.content[:50]}{'...' if len(message.content) > 50 else ''}")
        else:
            print(f"   Usuario: {message.author.display_name}")
            print(f"   ID: {recent_user_id}")
            print(f"   ID Objetivo: {zevax_user_id}")
            print(f"   Contenido: {message.content[:50]}{'...' if len(message.content) > 50 else ''}")

    if zevax_user_id and str(message.author.id) == zevax_user_id:
        random_roll = random.randint(1, 15) # 1 out of 15 chance

        if (random_roll == 1):
            if (message.content.startswith('z!')):
                return
            else:
                responses = [
                    "**NEGRO IMPURO ¿QUE COJONES HACES, ZEVAXTIANS? TIENES POCO TIEMPO PARA ESCRIBIR Y PIERDES TU TIEMPO CON LAS CARNALIDES DEL MUNDO**",
                    "**LA FURIA DEL SEOL CAERA SOBRE TI, ZEVAXTIANS, SI SIGUES PROCASTINANDO COMO UN PUTO FRACASADO**",
                    "**TUVOS Y VIDRIOS A ESTE PERDEDOR... TUVOS Y VIDRIOS SI NO TERMINAS LA ESCRITURA CALENDARIZADA PARA EL 8 DE SEPTIEMBRE DE 2025 A LAS 3 DE LA TARDE, ZEVAXTIANS**"
                ]
                
                selected_response = random.choice(responses)
                
                embed = discord.Embed(
                    title=f"⏰🐇",
                    description=selected_response,
                    color=0xff6b35
                )
                
                if image_path and os.path.exists(image_path):
                    file = discord.File(image_path, filename="event_image.png")
                    embed.set_image(url="attachment://event_image.png")
                    await message.reply(file=file, embed=embed)
                    print("Respuesta enviada con imagen")
                else:
                    await message.reply(embed=embed)
                    print("Respuesta enviada sin imagen")

    await bot.process_commands(message)
    
@bot.command()
async def ping(ctx):
    await ctx.send(f'toy aca')


@bot.command()
async def cuanto(ctx):

    if not test_event_id:
        await ctx.send("El el id no esta en el env, pibe")
        return
    
    try:
        event_id = int(test_event_id)
        
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
        

        if time_diff.total_seconds() <= 0:
            time_left_str = "**LA HORA DE MORIR HA LLEGADO**"
        else:
            days = time_diff.days
            hours, remainder = divmod(time_diff.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            time_parts = []
            if days > 0:
                time_parts.append(f"{days} DIA{'S' if days != 1 else ''}")
            if hours > 0:
                time_parts.append(f"{hours} HORA{'S' if hours != 1 else ''}")
            if minutes > 0:
                time_parts.append(f"{minutes} MINUTO{'S' if minutes != 1 else ''}")

            if not time_parts:
                time_left_str = "⏰🐇 **EL AZZOTH YA VIENE**"
            else:
                time_left_str = f"# ⏰🐇 **QUEDAN {', '.join(time_parts)} PARA LA NARCOEJECUCION DEL MARRONAZO DE ZEVAX**"
        
        embed = discord.Embed(
            title=f"📅 {target_event.name}",
            description=time_left_str,
            color=0xff6b35
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
        await ctx.send(f"An error occurred while fetching test event information: {str(e)}")

webserver.keep_alive()
bot.run(token, log_handler=handlers, log_level=logging.DEBUG)
