import discord
from discord.ext import commands

# ボットの接頭辞とBotのインスタンスを作成
intents = discord.Intents.default()
intents.messages = True  # メッセージの読み取り権限を有効にする
bot = commands.Bot(command_prefix='!', intents=intents)

# チャンネルIDを保存するファイル
CHANNELS_FILE = 'channels.txt'
#botのトークンを入力
TOKEN = 'とーくん'

# チャンネルIDを保存する関数
def save_channel_id(channel_id):
    with open(CHANNELS_FILE, 'a') as file:
        file.write(f"{channel_id}\n")

# チャンネルIDを削除する関数
def remove_channel_id(channel_id):
    try:
        with open(CHANNELS_FILE, 'r') as file:
            lines = file.readlines()
        with open(CHANNELS_FILE, 'w') as file:
            for line in lines:
                if line.strip() != str(channel_id):
                    file.write(line)
    except FileNotFoundError:
        pass

# チャンネルIDを読み込む関数
def load_channel_ids():
    try:
        with open(CHANNELS_FILE, 'r') as file:
            return [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        return []

# イベント: ボットが起動したとき
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# イベント: メッセージが送信されたとき
@bot.event
async def on_message(message):

    # 保存されたチャンネルIDのリストを取得
    channel_ids = load_channel_ids()
    
    # メッセージが保存されたチャンネルIDに一致する場合、👍リアクションを追加 リアクションはなんでもいい
    if message.channel.id in channel_ids:
        await message.add_reaction('👍')

    # 他のコマンドも正しく動作させるためにon_message内で処理を行う
    await bot.process_commands(message)

# コマンド: チャンネルIDを追加する
@bot.command(name='addreaction')
async def addreaction(ctx):
    channel_id = ctx.channel.id
    channel_ids = load_channel_ids()

    if channel_id in channel_ids:
        await ctx.send("すでに追加されてます！")
    else:
        save_channel_id(channel_id)
        await ctx.send(f"このチャンネル({ctx.channel.name})のメッセージに自動でリアクションをつけるように設定しました！")

# コマンド: チャンネルIDを削除する
@bot.command(name='deletereaction')
async def deletereaction(ctx):
    channel_id = ctx.channel.id
    channel_ids = load_channel_ids()

    if channel_id not in channel_ids:
        await ctx.send("このチャンネルはまだ追加されていません！")
    else:
        remove_channel_id(channel_id)
        await ctx.send(f"このチャンネル({ctx.channel.name})のメッセージに対するリアクション設定を削除しました。")

# Botを起動する
bot.run(TOKEN)
