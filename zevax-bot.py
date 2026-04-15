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
