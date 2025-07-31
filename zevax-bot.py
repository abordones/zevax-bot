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
zevax_event_id = os.getenv("ZEVAX_EVENT_ID")
image_path = os.getenv("MAIN_IMAGE")
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


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if zevax_user_id:
        recent_user_id = str(message.author.id)
        if recent_user_id == zevax_user_id:
            print(f"   user: {message.author.display_name}")
            print(f"   ID: {recent_user_id}")
            print(f"   content: {message.content[:50]}{'...' if len(message.content) > 50 else ''}")
        else:
            print(f"   user: {message.author.display_name}")
            print(f"   ID: {recent_user_id}")
            print(f"   target ID: {zevax_user_id}")
            print(f"   content: {message.content[:50]}{'...' if len(message.content) > 50 else ''}")

    if zevax_user_id and str(message.author.id) == zevax_user_id:
        random_roll = random.randint(1, 15) # 1 out of 15 chance

        if (random_roll == 1):
            if (message.content.startswith('z!')):
                return
            else:
                responses = [
                    "**NEGRO IMPURO ¿QUE COJONES HACES, ZEVAXTIANS? TIENES POCO TIEMPO PARA ESCRIBIR Y PIERDES TU TIEMPO CON LAS CARNALIDES DEL MUNDO**",
                    "**LA FURIA DEL SEOL CAERA SOBRE TI, ZEVAXTIANS, SI SIGUES PROCASTINANDO COMO UN PUTO FRACASADO**",
                    "**TUBOS Y VIDRIOS A ESTE PERDEDOR... TUBOS Y VIDRIOS SI NO TERMINAS LA ESCRITURA CALENDARIZADA PARA EL 8 DE SEPTIEMBRE DE 2025 A LAS 3 DE LA TARDE, ZEVAXTIANS**"
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
                else:
                    await message.reply(embed=embed)

    if test_user_id and str(message.author.id) == test_user_id:
        random_roll = random.randint(1, 3) # 1 out of 3 chance

        if (random_roll == 1):
            if (message.content.startswith('z!')):
                return
            else:
                response = "**TESTING**"

                embed = discord.Embed(
                    title=f"⏰🐇",
                    description=response,
                    color=0xff6b35
                )
                
                if image_path and os.path.exists(image_path):
                    file = discord.File(image_path, filename="event_image.png")
                    embed.set_image(url="attachment://event_image.png")
                    await message.reply(file=file, embed=embed)
                else:
                    await message.reply(embed=embed)

    await bot.process_commands(message)
    
@bot.command()
async def ping(ctx):
    await ctx.send(f'toy aca')


@bot.command()
async def tictac(ctx):

    if not zevax_event_id:
        await ctx.send("El id no esta en el env, pibe")
        return
    
    try:
        event_id = int(zevax_event_id)
        
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
            time_left_str = "**YA LLEGO TU HORA PUTO FRACASADO**"
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

@bot.command()
async def test_event(ctx):

    if not test_event_id:
        await ctx.send("El id no esta en el env, pibe")
        return

    if not test_user_id:
        await ctx.send("El id de usuario no esta en el env, pibe")
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
        
        embed = discord.Embed(
            title=f"📅 {target_event.name}",
            description=target_event.description or "No description provided",
            color=0x00ff00
        )
        
        if target_event.start_time:
            start_time_str = target_event.start_time.strftime("%Y-%m-%d at %H:%M UTC")
            embed.add_field(name="Start Time", value=start_time_str, inline=False)
        
        if target_event.end_time:
            end_time_str = target_event.end_time.strftime("%Y-%m-%d at %H:%M UTC")
            embed.add_field(name="End Time", value=end_time_str, inline=False)
        
        if hasattr(target_event, 'location') and target_event.location:
            embed.add_field(name="Location", value=target_event.location, inline=False)
        
        embed.add_field(name="Interested Users", value=str(target_event.user_count), inline=True)
        
        # event status
        status_emoji = {
            discord.EventStatus.scheduled: "⏰",
            discord.EventStatus.active: "🔴",
            discord.EventStatus.completed: "✅",
            discord.EventStatus.cancelled: "❌"
        }
        status_text = target_event.status.name.capitalize()
        embed.add_field(name="Status", value=f"{status_emoji.get(target_event.status, '❓')} {status_text}", inline=True)
        
        embed.add_field(name="Event ID", value=str(target_event.id), inline=True)
        
        embed.set_footer(text=f"Test Event - Created by {target_event.creator.display_name if target_event.creator else 'Unknown'}")
        
        await ctx.send(embed=embed)

    except ValueError:
        await ctx.send("formato del ID invalido en el archivo de entorno, jaja ese perdedor")
    except Exception as e:
        await ctx.send(f"An error occurred while fetching test event information: {str(e)}")

if __name__ == "__main__":
    webserver.keep_alive()
    
    print("Starting Discord bot...")
    bot.run(token, log_handler=handlers, log_level=logging.DEBUG)
