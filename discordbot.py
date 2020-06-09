from discord.ext import commands
import os
import traceback
import discord
import sqlite3
import re
import sys

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

# 接続に必要なオブジェクトを生成
client = discord.Client()
con = sqlite3.connect("DTBCdata.db")
cursor = con.cursor()



@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


#@bot.command()
#async def ping(ctx):
#    await ctx.send('pong')

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    channel=client.get_channel(ch_kan)#実装時に(ch_kan)に変更
    await channel.send('業務を開始します')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('私は猫ではないです...')
    #「/who」botの説明
    if message.content == '/who':
        await message.channel.send('私はDTB闘技場の管理人、ヤタスィです。\n24時間は動けませんが、必須そうな処理は覚えたので、実際に運営をする日も近いかもしれません。')
    #「進捗どうですか？」
    if message.content =='進捗どうですか？':
        await message.channel.send('24時間稼働"には"対応しました')

    if 'make_PLdata' == message.content:#プレーヤーデータの作成
        cursor.execute("DROP TABLE IF EXISTS PLdata")
        cursor.execute("create table PLdata(name,ID,CR,Ctotal,Cwin,Close,WR,Wtotal,Wwin,Wlose)")
        cursor.execute("insert into PLdata values('Yataswee',0,1500,0,0,0,1500,0,0,0)")
        con.commit()
    if 'check_PLdata' == message.content:#PLdataを見る
        cursor.execute("select * from PLdata")
        allPL=cursor.fetchall()
        for j in range(0,len(allPL),5):
            if j!=len(allPL)-len(allPL)%5:
                await message.channel.send(str(allPL[j])+'\n'+str(allPL[j+1])+'\n'+str(allPL[j+2])\
                                           +'\n'+str(allPL[j+3])+'\n'+str(allPL[j+4]))
            else:
                for i in range(len(allPL)-(len(allPL)%5),len(allPL)):
                    await message.channel.send(str(allPL[i]))
        await message.channel.send("全員出力完了！")
    if 'regist' in message.content:#新規登録
        PLname=re.split('[\n]',message.content)[1]
        if ',' in PLname or ' ' in PLname or '/' in PLname or '-' in PLname or '(' in PLname or ')' in PLname or'\u3000' in PLname:
            await message.channel.send(', - / ( ) 全角/半角スペースは名前に使用することができません')
        else:
            cursor.execute("select * from PLdata where name=?",(PLname,))
            delet=cursor.fetchall()
            if len(delet)==0:
                cursor.execute("select * from PLdata")
                num=(len(cursor.fetchall())-1)
                cursor.execute("insert into PLdata values (?,?,?,?,?,?,?,?,?,?)",(PLname,num+1,1500,0,0,0,1500,0,0,0))
                con.commit()
                await message.channel.send("新規登録完了です\nIDは"+str(num+1)+"です")
            else:
                await message.channel.send("同じ名前が既に使用されています\nほかの名前を使ってください")
    if 'Nupdate' in message.content:#プレーヤーの名前を変更する
            Defname=re.split('[\n]',message.content)[1]
            Newname=re.split('[\n]',message.content)[2]
            if ',' in Newname or ')' in Newname or '(' in Newname or '-' in Newname or '\u3000' in Newname:
                await message.channel.send(', - / ( ) 全角/半角スペースは名前に使用することができません')
            else:
                cursor.execute("update PLdata set name=? where name=?",(Newname,Defname))
                con.commit()
                await message.channel.send("名前を変更しました")
    if 'myID' in message.content:#指定した人のIDを表示
            member_name=re.split('[\n]',message.content)[1]
            cursor.execute("select * from PLdata where name=?",(member_name,))
            await message.channel.send(cursor.fetchall()[0][1])
        
    if 'fulldata' in message.content:#プレーヤーデータfullの確認
        res10=re.split('[\n]',message.content)
        try:
            testID=int(res10[1])
        except ValueError:
            await message.channel.send("構文エラー\n自分のIDを入力してください")
        else:
            nameID=int(res10[1])
            cursor.execute("SELECT * FROM PLdata")#name
            Mname=cursor.fetchall()[nameID][0]
            cursor.execute("SELECT * FROM PLdata")#ID
            MID=cursor.fetchall()[nameID][1]
            cursor.execute("SELECT * FROM PLdata")#CR
            MCR=cursor.fetchall()[nameID][2]
            cursor.execute("SELECT * FROM PLdata")#Cwin
            MCw=cursor.fetchall()[nameID][4]
            cursor.execute("SELECT * FROM PLdata")#Close
            MCl=cursor.fetchall()[nameID][5]
            cursor.execute("SELECT * FROM PLdata")#WR
            MWR=cursor.fetchall()[nameID][6]
            cursor.execute("SELECT * FROM PLdata")#Wtotal
            MWt=cursor.fetchall()[nameID][7]
            cursor.execute("SELECT * FROM PLdata")#Wwin
            MWw=cursor.fetchall()[nameID][8]
            cursor.execute("SELECT * FROM PLdata")#Wlose
            MWl=cursor.fetchall()[nameID][9]
            await message.channel.send('名前：'+str(Mname)+'\nID：'+str(MID)+'\n'+str(MWt)+'試合'+str(MWw)+'勝'+str(MWl)+'敗'+'\n'+str(MCw)+'-'+str(MCl)+'\n闘技場レート'+str(MCR)+'\n勝敗レート'+str(MWR))
    if 'mydata' in message.content:#プレーヤーデータの確認
        res11=re.split('[\n]',message.content)
        try:
            testID=int(res11[1])
        except ValueError:
            await message.channel.send("構文エラー\n自分のIDを入力してください")
        else:
            nameID=int(res11[1])
            cursor.execute("SELECT * FROM PLdata")#name
            Mname=cursor.fetchall()[nameID][0]
            cursor.execute("SELECT * FROM PLdata")#ID
            MID=cursor.fetchall()[nameID][1]
            cursor.execute("SELECT * FROM PLdata")#CR
            MCR=cursor.fetchall()[nameID][2]
            cursor.execute("SELECT * FROM PLdata")#Wtotal
            MWt=cursor.fetchall()[nameID][7]
            cursor.execute("SELECT * FROM PLdata")#WR
            MWR=cursor.fetchall()[nameID][6]
            await message.channel.send('名前：'+str(Mname)+'\nID：'+str(MID)+'\n試合数：'+str(MWt)+'\n闘技場レート'+str(MCR)+'\n勝敗レート'+str(MWR))
# Botの起動とDiscordサーバーへの接続
client.run(token)

    
