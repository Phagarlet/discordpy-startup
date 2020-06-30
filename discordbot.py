import os
import discord
import traceback
import psycopg2
token = os.environ['DISCORD_BOT_TOKEN']
path=os.environ['DATABASE_URL']
con = psycopg2.connect(path,sslmode='require')
client = discord.Client()
cursor = con.cursor()
channel_debug=706713526873620500

@client.event
async def on_ready():
    CHANNEL_ID = channel_debug
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('起きたよー')

@client.event
async def on_message(message):
    try:
        if message.author.bot:#botの文章を無視する
            return
        if 'neko' == message.content:#にゃんにゃんと返す
            await message.channel.send("ねこ")
    except:
        cursor.execute("ROLLBACK")#エラー時にその操作を無かったことにする
        await message.channel.send('エラー')
        
client.run(token)
