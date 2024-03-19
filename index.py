import os
import discord
import aiohttp  # Add this line
from discord.ext import commands

intents = discord.Intents.all()  # Enable all intents

class MyClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='#', intents=intents)

    async def on_ready(self):
        print('Logged in as {0.user}'.format(self))

    async def on_presence_update(self, before, after):  # Change to on_presence_update
        # Check if the user is being tracked
        for tracker in trackerList:
            if after == tracker['tracked']:
                await self.send_tracked_info(tracker, before, after)

    async def send_tracked_info(self, tracker, before, after):
        user = tracker['tracked']  # Access the member directly
        author = tracker['author']

        # Prepare the message content with stylish formatting
        message_content = f"**Tracked user:** {user.name}#{user.discriminator}\n\n"
        message_content += f"**Before:** {before.status}\n"
        message_content += f"**After:** {after.status}\n"

        # Send the message to the tracker's author
        user_id = 138273340476358656  # Your user ID
        owner = self.get_user(user_id)
        if owner:
            # Create an embed for the message
            embed = discord.Embed(
                title="Presence Update",
                description=message_content,
                color=discord.Color.blue()
            )
            # Set the user's avatar as thumbnail if available
            if user.avatar:
                avatar_url = user.avatar.url
            else:
                # Use default avatar if no custom avatar is available
                avatar_url = discord.Embed.Empty
            embed.set_thumbnail(url=avatar_url)
            await owner.send(embed=embed)
        else:
            print("Failed to find owner user.")

client = MyClient()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

trackerList = []

@client.command()
async def track(ctx, member: discord.Member, mention_author=False):
    tracker = {
                "tracked": member,
                "author": ctx.author,
                "channel" : ctx.channel,
                "mention_author" : True if mention_author else mention_author,
                "guild" : ctx.guild,
                }
    await ctx.send("Tracking!")
    trackerList.append(tracker)

@client.command()
async def untrack(ctx, member: discord.Member):
    global trackerList
    for tracker in trackerList:
        if tracker['tracked'] == member:
            trackerList.remove(tracker)
            await ctx.send(f"Stopped tracking {member.display_name}")
            return
    await ctx.send(f"{member.display_name} is not being tracked.")    

client.run("MTIxOTQ2MzA1MjU5NzEzMzM0NA.GEdd06.vlnYrHZjZj9mKblqCoVMtEZrYcxsxPRrz3gU0k")
