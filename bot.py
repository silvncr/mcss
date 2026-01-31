import datetime
import hashlib
import os
from pathlib import Path

import nextcord
from dotenv import load_dotenv
from mcstatus import JavaServer
from nextcord.ext import tasks

load_dotenv()

CHANNEL_ID = int(os.environ['CHANNEL_ID'])
MESSAGE_ID = int(os.environ['MESSAGE_ID'] or 0) or None
SERVER_IP = os.environ['SERVER_IP']
SERVER_NAME = os.environ['SERVER_NAME'] or 'Minecraft Server'
TIMEZONE_OFFSET = int(os.environ['TIMEZONE_OFFSET'] or 0)
TOKEN = os.environ['TOKEN']

ICON_FILE = 'server-icon.png'


intents = nextcord.Intents.default()
client = nextcord.Client(intents=intents)

status_message = None
last_status_data = (
    None
    # 0 status_type,
    # 1 players_online,
    # 2 players_max,
    # 3 player_names_tuple,
    # 4 icon_md5,
    # 5 unix_timestamp,
)


def file_hash(path: str) -> str:
    'Get MD5 hash of a file'
    hasher = hashlib.md5()  # noqa: S324
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


async def get_timestamp() -> datetime.datetime:
    'Get current timestamp'
    return nextcord.utils.utcnow()


async def get_status() -> tuple:
    'Get server status and stats'

    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print('⚠️  Channel not found. Check CHANNEL_ID.')
        return None

    players_online = 0
    players_max = 0
    player_names = []
    icon_md5 = file_hash(ICON_FILE) if Path(ICON_FILE).exists() else None

    try:
        server = JavaServer.lookup(SERVER_IP)

        try:
            query = server.query()
            player_names = query.players.names
            players_online = query.players.online
            players_max = query.players.max
        except Exception:  # noqa: BLE001
            status = server.status()
            players_online = status.players.online
            players_max = status.players.max
            player_names = []
            if players_online > 0 and status.players.sample:
                player_names = [p.name for p in status.players.sample]

        status_type = 'active' if players_online > 0 else 'empty'

    except Exception:  # noqa: BLE001
        status_type = 'offline'

    unix_timestamp = int(
        str(datetime.datetime.now(datetime.UTC).timestamp()).split('.')[0],
    )

    return (
        status_type,
        players_online,
        players_max,
        tuple(sorted(player_names, key=lambda x: x.lower())),
        icon_md5,
        unix_timestamp,
    )


async def create_status_embed(
    status_type: str,
    players_online: int = 0,
    players_max: int = 0,
    player_names: tuple | None = None,
    icon_url: str | None = None,  # noqa: ARG001
    unix_timestamp: str | None = None,
) -> nextcord.Embed:
    'Create status embed'
    timestamp_str = datetime.datetime.fromtimestamp(
        unix_timestamp, tz=datetime.timezone(datetime.timedelta(hours=TIMEZONE_OFFSET)),
    )
    print(f'[{timestamp_str}]', end=' ')
    if status_type == 'offline':
        print('🔴 Offline')
        await client.change_presence(
            activity=nextcord.CustomActivity(name='🔴 Offline'),
            status=nextcord.Status.do_not_disturb,
        )
        embed = nextcord.Embed(
            title=f'{SERVER_NAME}', description='🔴 Offline', color=0xFF0000,
        )
    elif status_type == 'empty':
        print(f'🟣 {players_online}/{players_max}')
        await client.change_presence(
            activity=nextcord.CustomActivity(
                name=f'🟣 Online ({players_online}/{players_max})',
            ),
            status=nextcord.Status.idle,
        )
        embed = nextcord.Embed(
            title=f'{SERVER_NAME}',
            description=f'🟣 Online ({players_online}/{players_max})',
            color=0x800080,
        )
    elif status_type == 'active':
        print(f'🟢 {players_online}/{players_max}', end='')
        await client.change_presence(
            activity=nextcord.CustomActivity(
                name=f'🟢 Online ({players_online}/{players_max})',
            ),
            status=nextcord.Status.online,
        )
        embed = nextcord.Embed(
            title=f'{SERVER_NAME}',
            description=f'🟢 Online ({players_online}/{players_max})',
            color=0x00FF00,
        )
        if player_names:
            print(f' - {", ".join(player_names)}')
            embed.add_field(
                name='Players',
                value=f'- {', '.join(player_names)}',
                inline=False,
            )
        else:
            print()

    embed.add_field(name='Last updated', value=f'<t:{unix_timestamp}:R>')

    # embed.set_footer(text='Last updated')
    # embed.timestamp = timestamp

    # if icon_url:
    #     embed.set_thumbnail(url=icon_url)

    return embed


# def exit_handler() -> None:
#     'Update status on exit'
#     channel = client.get_channel(CHANNEL_ID)
#     msg = channel.fetch_message(MESSAGE_ID)
#     msg.edit('Bot is offline.')


@client.event
async def on_ready() -> None:
    'On-ready function'
    global status_message, MESSAGE_ID

    print(f'✅ Logged in as {client.user} ({client.user.id}).')

    await client.change_presence(
        activity=nextcord.CustomActivity(name='⚙️ Starting up...'),
        status=nextcord.Status.do_not_disturb,
    )

    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print('⚠️  Channel not found. Check CHANNEL_ID.')
        return

    if MESSAGE_ID:
        try:
            status_message = await channel.fetch_message(MESSAGE_ID)
            print('⚙️  Found existing message, will update it.')
        except nextcord.NotFound:
            status_message = None

    if status_message is None:
        embed = await create_status_embed('offline', icon_url='attachment://icon.png')
        # icon_file = (
        #     nextcord.File(ICON_FILE, filename='icon.png')
        #     if Path(ICON_FILE).exists()
        #     else None
        # )
        msg = await channel.send(
            embed=embed,
            # file=icon_file,
        )
        status_message = msg
        MESSAGE_ID = msg.id
        print(f'🚨 Created new status message. (MESSAGE_ID: {MESSAGE_ID})')

    update_status.start()


@client.slash_command(name='server-status', description='See server status')
async def status(interaction: nextcord.Interaction) -> None:
    'Status command'
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(embed=await create_status_embed(*last_status_data))


@tasks.loop(seconds=30)
async def update_status() -> None:
    'Update loop for server message'
    global last_status_data

    # icon_url = 'attachment://icon.png'
    # icon_file = (
    #     nextcord.File(ICON_FILE, filename='icon.png')
    #     if Path(ICON_FILE).exists()
    #     else None
    # )

    current_status_data = await get_status()

    # if current_status_data == last_status_data:
    #     return

    last_status_data = current_status_data

    if status_message:
        channel = client.get_channel(CHANNEL_ID)
        msg = await channel.fetch_message(MESSAGE_ID)
        await msg.edit(
            embed=await create_status_embed(*current_status_data),
            # attachments=[icon_file] if icon_file else [],
        )


# atexit.register(exit_handler)
client.run(TOKEN)
