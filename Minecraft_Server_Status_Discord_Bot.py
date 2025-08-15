'''
Created by: Ayan Khan
Email: ayankhantnp786@gmail.com
Version: 15.08.2025-1
'''


import discord
from discord.ext import tasks
from mcstatus import JavaServer
import os, hashlib

with open("TOKEN",'r') as tokenfile:
    TOKEN=tokenfile.read()
with open("MC_SERVER_IP",'r') as mc_server_ip_file:
    MC_SERVER_IP=mc_server_ip_file.read()
with open("CHANNEL_ID",'r') as channel_id_file:
    CHANNEL_ID=int(channel_id_file.read())
with open("MESSAGE_ID",'r') as message_id_file:
    MESSAGE_ID=int(message_id_file.read())
ICON_FILE = "server-icon.png"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

status_message = None
last_status_data = None  # (status_type, players_online, players_max, player_names_tuple, icon_md5)


def file_hash(path):
    """Returns MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def create_status_embed(status_type, players_online=0, players_max=0, player_names=None, icon_url=None):
    if status_type == "offline":
        embed = discord.Embed(title="Minecraft Server Status", description="🔴 Server is Offline!", color=0xFF0000)
    elif status_type == "empty":
        embed = discord.Embed(title="Minecraft Server Status", description="🟣 Server is Online", color=0x800080)
        embed.add_field(name="Players", value=f"{players_online}/{players_max}", inline=True)
    elif status_type == "active":
        embed = discord.Embed(title="Minecraft Server Status", description="🟢 Server is Online!", color=0x00FF00)
        embed.add_field(name="Players", value=f"{players_online}/{players_max}", inline=True)
        if player_names:
            embed.add_field(name="Online Players", value=", ".join(player_names), inline=False)

    embed.set_footer(text="Last updated")
    embed.timestamp = discord.utils.utcnow()

    if icon_url:
        embed.set_thumbnail(url=icon_url)
    return embed


@client.event
async def on_ready():
    global status_message, MESSAGE_ID
    print(f"✅ Logged in as {client.user}")
    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        print("⚠ Channel not found. Check CHANNEL_ID.")
        return

    if MESSAGE_ID:
        try:
            status_message = await channel.fetch_message(MESSAGE_ID)
            print("ℹ Found existing message, will update it.")
        except discord.NotFound:
            status_message = None
    if status_message is None:
        embed = create_status_embed("offline", icon_url="attachment://icon.png")
        icon_file = discord.File(ICON_FILE, filename="icon.png") if os.path.exists(ICON_FILE) else None
        msg = await channel.send(embed=embed, file=icon_file)
        status_message = msg
        MESSAGE_ID = msg.id
        print(f"🆕 Created new status message. Save this MESSAGE_ID: {MESSAGE_ID}")

    update_status.start()


@tasks.loop(seconds=30)
async def update_status():
    global status_message, last_status_data

    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print("⚠ Channel not found. Check CHANNEL_ID.")
        return

    players_online = 0
    players_max = 0
    player_names = []
    icon_url = "attachment://icon.png"
    icon_file = discord.File(ICON_FILE, filename="icon.png") if os.path.exists(ICON_FILE) else None
    icon_md5 = file_hash(ICON_FILE) if os.path.exists(ICON_FILE) else None

    try:
        server = JavaServer.lookup(MC_SERVER_IP)

        try:
            query = server.query()
            player_names = query.players.names
            players_online = query.players.online
            players_max = query.players.max
        except Exception:
            status = server.status()
            players_online = status.players.online
            players_max = status.players.max
            player_names = []
            if players_online > 0 and status.players.sample:
                player_names = [p.name for p in status.players.sample]

        if players_online > 0:
            status_type = "active"
        else:
            status_type = "empty"

    except Exception:
        status_type = "offline"

    current_status_data = (status_type, players_online, players_max, tuple(player_names), icon_md5)

    if current_status_data == last_status_data:
        return

    last_status_data = current_status_data
    embed = create_status_embed(status_type, players_online, players_max, player_names, icon_url)

    if status_message:
        await status_message.edit(embed=embed, attachments=[icon_file] if icon_file else [])

client.run(TOKEN)
