from discord.ext import commands
import os
import discord
import traceback
import psycopg2
token = os.environ['DISCORD_BOT_TOKEN']
path=os.environ['DATABASE_URL']
con = psycopg2.connect(path,sslmode='require')
client = discord.Client()
cursor = con.cursor()
import re

#チャンネルID
ch_bot=706713526873620500
ch_kan=667380995242328078
ch_CR=667404424007647272
ch_WR=669536277502099471
ch_RR=677771772212412459

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

@client.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

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
    if message.content == 'neko':
        await message.channel.send('私は猫ではないです...')
    #「/who」botの説明
    if message.content == 'who':
        await message.channel.send('私はDTB闘技場の管理人、ヤタスィです。\n24時間稼働に対応しました。\nSeason2から正式に業務を開始します。よろしくお願いします。')
    #「進捗どうですか？」
    if message.content =='進捗どうですか？':
        await message.channel.send('ついに24時間稼働に成功しました')

    if 'make_PLdata' == message.content:#プレーヤーデータの作成
        cursor.execute("DROP TABLE IF EXISTS PLdata")
        cursor.execute("create table PLdata(name,ID,CR,Ctotal,Cwin,Close,WR,Wtotal,Wwin,Wlose)")
        cursor.execute("insert into PLdata values('Yataswee',0,1500,0,0,0,1500,0,0,0)")
        con.commit()
    if 'check_PLdata' == message.content:#PLdataを見る
        if message.author.guild_permissions.administrator:
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
            cursor.execute("select * from PLdata where name=(%s)",(PLname,))
            delet=cursor.fetchall()
            if len(delet)==0:
                cursor.execute("select * from PLdata")
                num=(len(cursor.fetchall())-1)
                cursor.execute("insert into PLdata values ((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))",(PLname,num+1,1500,0,0,0,1500,0,0,0))
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
                cursor.execute("update PLdata set name=(%s) where name=(%s)",(Newname,Defname))
                con.commit()
                await message.channel.send("名前を変更しました")
    if 'myID' in message.content:#指定した人のIDを表示
            member_name=re.split('[\n]',message.content)[1]
            cursor.execute("select * from PLdata where name=(%s)",(member_name,))
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
            
    #試合処理系統
    if 'result'in message.content:#試合処理
#前処理
        res1=re.split('[\n]',message.content)
        try:
            test0=res1[3]
        except IndexError:
            res2=res1[1]
            res3=res1[2]
            res4=res2.split('/')
            res5=res3.split('-')
            try:
                res4[0]=='' or res4[1]=='' or res5[0]=='' or res5[1]==''#エラー検出（記号ミス)
            except IndexError:
                await message.channel.send('構文エラーです\n記号ミスエラー')
            else:
                try:
                    test4=int(res4[0])
                    test5=int(res4[1])
                    test6=int(res5[0])
                    test7=int(res5[1])
                except ValueError:
                    await message.channel.send('構文エラーです。\n情報欠損エラー')
                else:
                    try:
                        test8=1/int(int(res5[0])-int(res5[1]))
                        test9=1/int(int(res4[0])-int(res4[1]))
                    except ZeroDivisionError:
                        await message.channel.send('構文エラーです。\情報同一エラー')
                    else:
                        WID=int(res4[0])#勝者データ
                        WG=int(res5[0])
                        LID=int(res4[1])#敗者データ
                        LG=int(res5[1])
        else:
            await message.channel.send('構文エラーです。\n情報過多エラー')
#レート処理
        cursor.execute("SELECT * FROM PLdata")
        Wname=cursor.fetchall()[WID][0]
        cursor.execute("SELECT * FROM PLdata")
        Lname=cursor.fetchall()[LID][0]
        cursor.execute("SELECT * FROM PLdata")
        WCR=cursor.fetchall()[WID][2]
        cursor.execute("SELECT * FROM PLdata")
        LCR=cursor.fetchall()[LID][2]
        cursor.execute("SELECT * FROM PLdata")
        WWR=cursor.fetchall()[WID][6]
        cursor.execute("SELECT * FROM PLdata")
        LWR=cursor.fetchall()[LID][6]

        match=int(WG+LG)
        await message.channel.send('結果出力が終わるまでコマンドは打たないでください')
        await message.channel.send(Wname+"さん"+' 対 '+Lname+"さん の試合結果です")
        await message.channel.send('試合前レート')
        await message.channel.send("闘技場："+str(WCR)+"-"+str(LCR))
        await message.channel.send("勝敗："+str(WWR)+"-"+str(LWR))
#闘技場レート計算
        CsaA=LCR-WCR
        CsaB=int(CsaA)*-1
        AWper=round(1/(10**((CsaA)/400)+1),2)
        BWper=round(1/(10**((CsaB)/400)+1),2)
        NWCR=round(WCR+16*(WG-match*AWper))
        NLCR=round(LCR+16*(LG-match*BWper))
#勝敗レート計算
        WsaA=LWR-WWR
        WsaB=int(WsaA*-1)
        WBWper=round(1/(10**((WsaB)/400)+1),2)
        NWWR=int(WWR+32*WBWper)
        NLWR=int(LWR-32*WBWper)
#試合後の出力
        await message.channel.send('試合後レート')
        await message.channel.send("闘技場："+str(NWCR)+"-"+str(NLCR))
        await message.channel.send("勝敗："+str(NWWR)+"-"+str(NLWR))
        await message.channel.send('出力終了です')
#データのアップデート
        #勝利側
        cursor.execute("SELECT * FROM PLdata")
        WCw=cursor.fetchall()[WID][4]
        cursor.execute("SELECT * FROM PLdata")
        WCl=cursor.fetchall()[WID][5]
        cursor.execute("SELECT * FROM PLdata")
        WWw=cursor.fetchall()[WID][8]
        cursor.execute("SELECT * FROM PLdata")
        WWl=cursor.fetchall()[WID][9]
        WCw=WCw+WG
        WCl=WCl+LG
        WCt=int(WCw)+int(WCl)
        WWw=WWw+1
        WWt=int(WWw)+WWl
        cursor.execute("update PLdata set CR=(%s) where ID=(%s)",(NWCR,WID))#CR
        cursor.execute("update PLdata set WR=(%s) where ID=(%s)",(NWWR,WID))#WR
        cursor.execute("update PLdata set Ctotal=(%s) where ID=(%s)",(WCt,WID))#Ctotal
        cursor.execute("update PLdata set Cwin=(%s) where ID=(%s)",(WCw,WID))#Cwin
        cursor.execute("update PLdata set Close=(%s) where ID=(%s)",(WCl,WID))#Close
        cursor.execute("update PLdata set Wtotal=(%s) where ID=(%s)",(WWt,WID))#Wtotal
        cursor.execute("update PLdata set Wwin=(%s) where ID=(%s)",(WWw,WID))#Wwin
        #敗北側
        cursor.execute("SELECT * FROM PLdata")
        LCw=cursor.fetchall()[LID][4]
        cursor.execute("SELECT * FROM PLdata")
        LCl=cursor.fetchall()[LID][5]
        cursor.execute("SELECT * FROM PLdata")
        LWw=cursor.fetchall()[LID][8]
        cursor.execute("SELECT * FROM PLdata")
        LWl=cursor.fetchall()[LID][9]
        LCw=LCw+LG
        LCl=LCl+WG
        LCt=int(LCw)+int(LCl)
        LWl=LWl+1
        LWt=int(LWl)+LWw
        cursor.execute("update PLdata set CR=(%s) where ID=(%s)",(NLCR,LID))#CR
        cursor.execute("update PLdata set WR=(%s) where ID=(%s)",(NLWR,LID))#CR
        cursor.execute("update PLdata set Ctotal=(%s) where ID=(%s)",(LCt,LID))#Ctotal
        cursor.execute("update PLdata set Cwin=(%s) where ID=(%s)",(LCw,LID))#Cwin
        cursor.execute("update PLdata set Close=(%s) where ID=(%s)",(LCl,LID))#Close
        cursor.execute("update PLdata set Wtotal=(%s) where ID=(%s)",(LWt,LID))#Wtotal
        cursor.execute("update PLdata set Wlose=(%s) where ID=(%s)",(LWl,LID))#Wlose
        con.commit()

#レート一覧表示 以下管理技士専用コマンド
    if 'Rupdate'in message.content:#レート更新
        if message.author.guild_permissions.administrator:
            rank_CR=[]
            rank_WR=[]
            Rup=re.split('[\n]',message.content)
            channel=client.get_channel(ch_kan)#更新告知　ch_kan
            await channel.send(str(Rup[1])+'\nレート一覧を更新します\n完了の表示が出るまでコマンドを使用しないでください\nこの処理は5分～10分程度を要する可能性があります')
            channel=client.get_channel(ch_CR)#ch_CRに変更
            #闘技場レート出力機構
            await channel.send(str(Rup[1])+'現在\n闘技場レート')#闘技場レート更新
            cursor.execute("SELECT * FROM PLdata")
            allPL=cursor.fetchall()
            for i in range(len(allPL)):
                cursor.execute("SELECT * FROM PLdata")
                PLname=cursor.fetchall()[i][0]
                cursor.execute("SELECT * FROM PLdata")
                PLCR=cursor.fetchall()[i][2]
                await channel.send(str(PLname)+' '+str(PLCR))
            await channel.send('出力完了です')
            #勝敗レート出力機構
            channel=client.get_channel(ch_WR)#ch_WRに変更
            await channel.send(str(Rup[1])+'現在\n勝敗レート')#勝敗レート更新
            for j in range(len(allPL)):
                cursor.execute("SELECT * FROM PLdata")
                PLname=cursor.fetchall()[j][0]
                cursor.execute("SELECT * FROM PLdata")
                PLWR=cursor.fetchall()[j][6]
            await channel.send(str(PLname)+' '+str(PLWR))
            await channel.send('出力完了です')
            #レートランキング出力機構
            channel=client.get_channel(ch_RR)#ch_RRに変更
            await channel.send(str(Rup[1])+'現在\nレートランキング')#レートランキング更新
            for k in range(len(allPL)):
                cursor.execute("SELECT * FROM PLdata")
                PLname=cursor.fetchall()[k][0]
                cursor.execute("SELECT * FROM PLdata")
                PLCRr=cursor.fetchall()[k][2]
                cursor.execute("SELECT * FROM PLdata")
                PLWRr=cursor.fetchall()[k][6]
                rank_CR.append([PLCRr,PLname])
                rank_WR.append([PLWRr,PLname])
            rank_CR.sort(key=lambda x:x[0],reverse=True)#ソートCR
            rank_WR.sort(key=lambda x:x[0],reverse=True)#ソートWR
            await channel.send('闘技場レートランキング')
            for i in range(10):
                await channel.send(rank_CR[i])
            await channel.send('勝敗レートランキング')
            for j in range(10):
                await channel.send(rank_WR[j])
            await channel.send('出力完了です')
            #終了告知
            channel=client.get_channel(ch_kan)#更新告知　ch_kan
            await channel.send(str(Rup[1])+'\nレート一覧を更新しました')
        else:
            await message.channel.send('管理技士専用コマンドです')

#ミス修正コマンド
    if 'edit' in message.content:#PLdataの値変更
        if message.author.guild_permissions.administrator:
            retsu=re.split('[\n]',message.content)[1]
            nani=re.split('[\n]',message.content)[2]
            cursor2.execute("select * PLdata")
            await message.channel.send('変更前'+str(cursor2.fetchall()))
            cursor2.execute("update info set{0}=(%s)"%retsu,(int(nani),))
            cursor2.execute("select * PLdata")
            await message.channel.send('変更後'+str(cursor2.fetchall()))
            con.commit()
        else:
                await message.channel.send('管理技士専用コマンドです')
    
        
#通称リセットコマンド
    if 'reset' in message.content:#指定した何かの指定した列を変更する（シーズンリセット時に使用）
            if message.author.guild_permissions.administrator:
                nani2=re.split('[\n]',message.content)[1]#変更前値
                namae=re.split('[\n]',message.content)[2]#name
                nani1=re.split('[\n]',message.content)[3]#変更後値
                retsu=re.split('[\n]',message.content)[4]#DBの場所
                typ=re.split('[\n]',message.content)[5]
                try:
                    sori=int(namae)
                    namae=sori
                except:
                    pass
                cursor.execute("select * from PLdata where{0}=(%s)"%nani2,(namae,))
                try:
                    await message.channel.send('変更前　'+str(cursor.fetchall()))
                except:
                    await message.channel.send('文字数オーバーで変更前を表示できません')
                if typ=='str':
                    cursor.execute("update PLdata set{0}=(%s) where{0}=(%s)"%(nani1,nani2),(retsu,namae))
                elif typ=='int':
                    cursor.execute("update PLdata set{0}=(%s) where{0}=(%s)"%(nani1,nani2),(int(retsu),namae))
                cursor.execute("select * from PLdata where{0}=(%s)"%nani2,(namae,))
                try:
                    await message.channel.send('変更後　'+str(cursor.fetchall()))
                except:
                    await message.channel.send('文字数オーバーで変更後を表示できません')
                con.commit()
                await message.channel.send("変更完了です")
            else:
                await message.channel.send('管理技士専用コマンドです')
# Botの起動とDiscordサーバーへの接続
client.run(token)
