import discord
from discord.ext import commands

import os

TOKEN = os.getenv("TOKEN")
ROLE_ID = 1519879162289066164  # ID dyal Role Minecraft

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

reaction_message_id = None


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
@commands.has_permissions(administrator=True)
async def minecraft(ctx):
    global reaction_message_id

    embed = discord.Embed(
        title="⛏️ Minecraft Role",
        description="Dir react b ✅ bach takhod Role Minecraft.",
        color=discord.Color.green()
    )

    msg = await ctx.send(embed=embed)
    await msg.add_reaction("✅")

    reaction_message_id = msg.id


@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    if payload.message_id != reaction_message_id:
        return

    if str(payload.emoji) != "✅":
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    member = guild.get_member(payload.user_id)
    if member is None:
        member = await guild.fetch_member(payload.user_id)

    role = guild.get_role(ROLE_ID)
    if role:
        await member.add_roles(role)
        print(f"Role added to {member}")


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != reaction_message_id:
        return

    if str(payload.emoji) != "✅":
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    member = guild.get_member(payload.user_id)
    if member is None:
        member = await guild.fetch_member(payload.user_id)

    role = guild.get_role(ROLE_ID)
    if role:
        await member.remove_roles(role)
        print(f"Role removed from {member}")


bot.run(TOKEN)
