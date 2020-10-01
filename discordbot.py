from discord.ext import commands
import os
import discord
import traceback
import psycopg2
import re
token = os.environ['DISCORD_BOT_TOKEN']
path=os.environ['DATABASE_URL']
con = psycopg2.connect(path,sslmode='require')
client = discord.Client()
cursor = con.cursor()

#チャンネルID
ch_bot=706713526873620500
ch_kan=667380995242328078
ch_CR=667404424007647272
ch_WR=669536277502099471
ch_RR=677771772212412459

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

#season定義
season='4'

#全登録プレーヤー数
cursor.execute("select * from PLdata order by ID")
allPlayer=int(len(cursor.fetchall()))

#season試合数
s1match=2726
s2match=887
s3match=993

#レート計算関数

#抽出関数 DBに汎用性を持たせる
    
    

@client.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

# 起動時に動作する処理
@client.event
#再起動通知
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    channel=client.get_channel(ch_bot)#実装時に(ch_kan)に変更
    await channel.send('業務を開始します')

@client.event #新規メンバー用
async def on_member_join(member):
    channel=667380995242328078
    await channel.send("はじめまして、どうぶつタワーバトル闘技場、DTB闘技場の運営をしているYatasweeと申します。"\
                        +"\n闘技場に参加するにはまず登録コマンド「regist\n名前」を打って新規登録をしてください"\
                        +"\nこのサーバーでは、そこで発行されるIDが重要ですので、自分のIDをニックネーム変更から名前の後ろに付けていただけるとありがたいです。"\
                        +"\nまずは部屋説明から一読することをお勧めします。")

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    try:
        # メッセージ送信者がBotだった場合は無視する
        if message.author.bot:
            return
        # 「neko」と発言したら「正論」が返る処理
        if message.content == 'neko':
            await message.channel.send('私は猫ではないです...')


#プレーヤーデータベース作成コマンド(10項目)
        if 'make_PLdata' == message.content:#プレーヤーデータの作成
            cursor.execute("DROP TABLE IF EXISTS PLdata")
            cursor.execute("create table PLdata(name text,ID integer,CR integer,Ctotal integer,Cwin integer,Close integer,WR integer,Wtotal integer,Wwin integer,Wlose integer)")
            cursor.execute("insert into PLdata values('Yataswee',0,1500,0,0,0,1500,0,0,0)")
            con.commit()
            await message.channel.send('作成完了です')

#SeasonhistoryDB作成
        if 'make_history4' == message.content:#試合履歴DBの作成
            cursor.execute("DROP TABLE IF EXISTS history4")
            cursor.execute("create table history4(MID integer,Wname text,WinID integer,Lname text,LoseID integer,Wcount integer,Lcount integer)")
            cursor.execute("insert into history4 values(0,'Yataswee',0,'Soraneko',71,0,0)")
            con.commit()
            await message.channel.send('作成完了です')
            
#s3代理試合記録DB
        if 'make_s3history' == message.content:#試合履歴DBの作成
            cursor.execute("DROP TABLE IF EXISTS s3history")
            cursor.execute("create table s3history(MID integer,Wname text,WinID integer,Lname text,LoseID integer,Wcount integer,Lcount integer)")
            cursor.execute("insert into s3history values(0,'Yataswee',0,'Soraneko',71,0,0)")
            for i in range(606):
                cursor.execute("SELECT * FROM history3 order by MID")#name
                MID=cursor.fetchall()[i+1][0]
                cursor.execute("SELECT * FROM history3 order by MID")#name
                Wname=cursor.fetchall()[i+1][1]
                cursor.execute("SELECT * FROM history3 order by MID")#name
                WinID=cursor.fetchall()[i+1][2]
                cursor.execute("SELECT * FROM history3 order by MID")#name
                Lname=cursor.fetchall()[i+1][3]
                cursor.execute("SELECT * FROM history3 order by MID")#name
                LoseID=cursor.fetchall()[i+1][4]
                cursor.execute("SELECT * FROM history3 order by MID")#name
                Wcount=cursor.fetchall()[i+1][5]
                cursor.execute("SELECT * FROM history3 order by MID")#name
                Lcount=cursor.fetchall()[i+1][6]
                cursor.execute("select * from history4 where Wname=(%s)",(Wname,))
                cursor.execute("select * from history4")
                Num=(len(cursor.fetchall())-1)
                
                cursor.execute("insert into s3history values ((%s),(%s),(%s),(%s),(%s),(%s),(%s))",(MID,Wname,WinID,Lname,LoseID,Wcount,Lcount,))
            con.commit()
            await message.channel.send('作成完了です')
            
        
        if 'plus' in message.content:#新規登録
            res001=re.split('[\n]',message.content)
            await message.channel.send(res001)
            try:
                test00=res001[3]
            except IndexError:
                res2=res001[1]
                res3=res001[2]
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
                            await message.channel.send('構文エラーです。\n情報同一エラー')
                        else:
                            WID=int(res4[0])#勝者データ
                            WG=int(res5[0])
                            LID=int(res4[1])#敗者データ
                            LG=int(res5[1])
            else:
                await message.channel.send('構文エラーです。\n情報過多エラー')
            
            cursor.execute("SELECT * FROM PLdata order by ID")
            Wname=cursor.fetchall()[WID][0]
            cursor.execute("SELECT * FROM PLdata order by ID")
            Lname=cursor.fetchall()[LID][0]

            #試合記録
            cursor.execute("select * from s3history")
            Num=(len(cursor.fetchall())-1)
            cursor.execute("insert into s3history values ((%s),(%s),(%s),(%s),(%s),(%s),(%s))",(Num+1,Wname,WID,Lname,LID,WG,LG))
            con.commit()
            #ソート
            cursor.execute("SELECT * FROM PLdata order by ID")
            con.commit()
            await message.channel.send('試合ID：'+str(Num+1)+'\n出力終了です')
            
#天庭戦データベース作成コマンド            
        if 'make_TTQual' == message.content:#天庭戦関連DBの作成
            cursor.execute("DROP TABLE IF EXISTS TTQual")
            cursor.execute("create table TTQual(PLID integer,CRmax integer,WRmax integer,Qual text,Wnow integer,Rank integer)")
            cursor.execute("insert into TTQual values(0,1500,1500,'特になし',0,999)")
            
            cursor.execute("select * from PLdata order by ID")
            allPL=cursor.fetchall()
            for i in range(len(allPL)-1):
                cursor.execute("insert into TTQual values ((%s),(%s),(%s),(%s),(%s),(%s))",(i+1,1500,1500,'特になし',0,999,))
            con.commit()
            await message.channel.send('作成完了です')

#PLdataデータベース確認コマンド
#定数変更済
        if 'check_PLdata' == message.content:#PLdataを見る
            if message.author.guild_permissions.administrator:
                for j in range(0,allPlayer,10):
                    cursor.execute("select * from PLdata order by ID")
                    allPL=cursor.fetchall()
                    if j!=allPlayer-allPlayer%10:
                        await message.channel.send(str(allPL[j])+'\n'+str(allPL[j+1])+'\n'+str(allPL[j+2])\
                                                   +'\n'+str(allPL[j+3])+'\n'+str(allPL[j+4])+'\n'+str(allPL[j+5])+'\n'+str(allPL[j+6])+'\n'+str(allPL[j+7])+'\n'+str(allPL[j+8])+'\n'+str(allPL[j+9]))
                    else:
                        for i in range(allPlayer-(allPlayer%10),allPlayer):
                            await message.channel.send(str(allPL[i]))
                await message.channel.send("全員出力完了！")

#season2historyデータベース確認コマンド
        if 's2_history' == message.content:#historyを見る
            if message.author.guild_permissions.administrator:
                cursor.execute("SELECT * FROM history order by MID")
                allhis=cursor.fetchall()
                for j in range(0,len(allhis),5):
                    if j!=len(allhis)-len(allhis)%5:
                        await message.channel.send(str(allhis[j])+'\n'+str(allhis[j+1])+'\n'+str(allhis[j+2])\
                                                   +'\n'+str(allhis[j+3])+'\n'+str(allhis[j+4]))
                    else:
                        for i in range(len(allhis)-(len(allhis)%5),len(allhis)):
                            await message.channel.send(str(allhis[i]))
                await message.channel.send("全試合出力完了！")

        if 'check_history3' == message.content:#history3を見る
            if message.author.guild_permissions.administrator:
                cursor.execute("SELECT * FROM history3 order by MID")
                allhis=cursor.fetchall()
                for j in range(0,len(allhis),10):
                    if j!=len(allhis)-len(allhis)%10:
                        await message.channel.send(str(allhis[j])+'\n'+str(allhis[j+1])+'\n'+str(allhis[j+2])\
                                                   +'\n'+str(allhis[j+3])+'\n'+str(allhis[j+4])+'\n'+str(allhis[j+5])+'\n'+str(allhis[j+6])+'\n'+str(allhis[j+7])\
                                                   +'\n'+str(allhis[j+8])+'\n'+str(allhis[j+9]))
                    else:
                        for i in range(len(allhis)-(len(allhis)%10),len(allhis)):
                            await message.channel.send(str(allhis[i]))
                await message.channel.send("全試合出力完了！")
                
                
        if 'check_s3history' == message.content:#history4を見る
            if message.author.guild_permissions.administrator:
                cursor.execute("SELECT * FROM s3history order by MID")
                allhis=cursor.fetchall()
                for j in range(0,len(allhis),10):
                    if j!=len(allhis)-len(allhis)%10:
                        await message.channel.send(str(allhis[j])+'\n'+str(allhis[j+1])+'\n'+str(allhis[j+2])\
                                                   +'\n'+str(allhis[j+3])+'\n'+str(allhis[j+4])+'\n'+str(allhis[j+5])+'\n'+str(allhis[j+6])+'\n'+str(allhis[j+7])\
                                                   +'\n'+str(allhis[j+8])+'\n'+str(allhis[j+9]))
                    else:
                        for i in range(len(allhis)-(len(allhis)%10),len(allhis)):
                            await message.channel.send(str(allhis[i]))
                await message.channel.send("全試合出力完了！")
                
        if 'check_history4' == message.content:#history4を見る
            if message.author.guild_permissions.administrator:
                cursor.execute("SELECT * FROM history4 order by MID")
                allhis=cursor.fetchall()
                for j in range(0,len(allhis),10):
                    if j!=len(allhis)-len(allhis)%10:
                        await message.channel.send(str(allhis[j])+'\n'+str(allhis[j+1])+'\n'+str(allhis[j+2])\
                                                   +'\n'+str(allhis[j+3])+'\n'+str(allhis[j+4])+'\n'+str(allhis[j+5])+'\n'+str(allhis[j+6])+'\n'+str(allhis[j+7])\
                                                   +'\n'+str(allhis[j+8])+'\n'+str(allhis[j+9]))
                    else:
                        for i in range(len(allhis)-(len(allhis)%10),len(allhis)):
                            await message.channel.send(str(allhis[i]))
                await message.channel.send("全試合出力完了！")
                
        if 'check_TTQual' == message.content:#TTQualを見る
            if message.author.guild_permissions.administrator:
                cursor.execute("SELECT * FROM TTQual order by PLID")
                allQ=cursor.fetchall()
                for j in range(0,len(allQ),5):
                    if j!=len(allQ)-len(allQ)%5:
                        await message.channel.send(str(allQ[j])+'\n'+str(allQ[j+1])+'\n'+str(allQ[j+2])\
                                                   +'\n'+str(allQ[j+3])+'\n'+str(allQ[j+4]))
                    else:
                        for i in range(len(allQ)-(len(allQ)%5),len(allQ)):
                            await message.channel.send(str(allQ[i]))
                await message.channel.send("全員出力完了！")

#闘技場登録コマンド
        if 'regist' in message.content:#新規登録
            PLname=re.split('[\n]',message.content)[1]
            #名称利用可能/不可能判定
            if ',' in PLname or ' ' in PLname or '/' in PLname or '-' in PLname or '(' in PLname or ')' in PLname or'\u3000' in PLname:
                await message.channel.send(', - / ( ) 全角/半角スペースは名前に使用することができません')
            else:
                #新規登録処理
                cursor.execute("select * from PLdata where name=(%s)",(PLname,))
                delet=cursor.fetchall()
                if len(delet)==0:
                    cursor.execute("select * from PLdata order by ID")
                    num=(len(cursor.fetchall())-1)
                    cursor.execute("insert into PLdata values ((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))",(PLname,num+1,1500,0,0,0,1500,0,0,0))
                    con.commit()
                    #発行ID出力
                    await message.channel.send("新規登録完了です\nIDは"+str(num+1)+"です")
                    #同一名存在時
                else:
                    await message.channel.send("同じ名前が既に使用されています\nほかの名前を使ってください")

#プレーヤー名称変更コマンド
        if 'Nupdate' in message.content:
            Defname=re.split('[\n]',message.content)[1]
            Newname=re.split('[\n]',message.content)[2]
            #名称利用可能/不可能判定
            if ',' in Newname or ')' in Newname or '(' in Newname or '-' in Newname or '\u3000' in Newname:
                await message.channel.send(', - / ( ) 全角/半角スペースは名前に使用することができません')
            else:
                #名称変更処理
                cursor.execute("update PLdata set name=(%s) where name=(%s)",(Newname,Defname))
                con.commit()
                await message.channel.send("名前を変更しました")

#ID確認コマンド
        if 'myID' in message.content:#指定した人のIDを表示
            member_name=re.split('[\n]',message.content)[1]
            cursor.execute("select * from PLdata where name=(%s)",(member_name,))
            await message.channel.send(cursor.fetchall()[0][1])
        
#全情報確認コマンド(現行シーズンのみ)
        if 'fulldata' in message.content:#プレーヤーデータfullの確認
            res10=re.split('[\n]',message.content)
            try:
                testID=int(res10[1])
            except ValueError:
                await message.channel.send("構文エラー\n自分のIDを入力してください")
            else:
                nameID=int(res10[1])
                cursor.execute("SELECT * FROM PLdata order by ID")#name
                Mname=cursor.fetchall()[nameID][0]
                cursor.execute("SELECT * FROM PLdata order by ID")#ID
                MID=cursor.fetchall()[nameID][1]
                cursor.execute("SELECT * FROM PLdata order by ID")#CR
                MCR=cursor.fetchall()[nameID][2]
                cursor.execute("SELECT * FROM PLdata order by ID")#Cwin
                MCw=cursor.fetchall()[nameID][4]
                cursor.execute("SELECT * FROM PLdata order by ID")#Close
                MCl=cursor.fetchall()[nameID][5]
                cursor.execute("SELECT * FROM PLdata order by ID")#WR
                MWR=cursor.fetchall()[nameID][6]
                cursor.execute("SELECT * FROM PLdata order by ID")#Wtotal
                MWt=cursor.fetchall()[nameID][7]
                cursor.execute("SELECT * FROM PLdata order by ID")#Wwin
                MWw=cursor.fetchall()[nameID][8]
                cursor.execute("SELECT * FROM PLdata order by ID")#Wlose
                MWl=cursor.fetchall()[nameID][9]
                cursor.execute("SELECT * FROM TTQual order by PLID")
                CRmax=cursor.fetchall()[nameID][1]
                cursor.execute("SELECT * FROM TTQual order by PLID")
                WRmax=cursor.fetchall()[nameID][2]
                cursor.execute("SELECT * FROM TTQual order by PLID")
                qual=cursor.fetchall()[nameID][3]
                cursor.execute("SELECT * FROM TTQual order by PLID")
                rank=cursor.fetchall()[nameID][5]
                await message.channel.send('名前：'+str(Mname)+'\nID：'+str(MID)+'\n'+str(MWt)+'試合'+str(MWw)+'勝'+str(MWl)+'敗'+'\n'+str(MCw)+'-'+str(MCl)\
                                           +'\n闘技場レート'+'：'+str(MCR)+'/'+str(CRmax)+'\n勝敗レート'+'：'+str(MWR)+'/'+str(WRmax)+'\n天庭戦'+'：'+str(qual)+'**'+str(rank)+'位**')

#簡略式情報確認コマンド
        if 'mydata' in message.content:
            res11=re.split('[\n]',message.content)
            try:
                testID=int(res11[1])
            except ValueError:
                await message.channel.send("構文エラー\n自分のIDを入力してください")
            else:
                nameID=int(res11[1])
                cursor.execute("SELECT * FROM PLdata order by ID")#name
                Mname=cursor.fetchall()[nameID][0]
                cursor.execute("SELECT * FROM PLdata order by ID")#ID
                MID=cursor.fetchall()[nameID][1]
                cursor.execute("SELECT * FROM PLdata order by ID")#CR
                MCR=cursor.fetchall()[nameID][2]
                cursor.execute("SELECT * FROM PLdata order by ID")#Wtotal
                MWt=cursor.fetchall()[nameID][7]
                cursor.execute("SELECT * FROM PLdata order by ID")#WR
                MWR=cursor.fetchall()[nameID][6]
                await message.channel.send('名前：'+str(Mname)+'\nID：'+str(MID)+'\n試合数：'+str(MWt)+'\n闘技場レート：'+str(MCR)+'\n勝敗レート：'+str(MWR))
    
#全闘技場登録プレーヤーID表示コマンド
        if 'IDlist'in message.content:
            if message.author.guild_permissions.administrator:
                IDlist=[]
                cursor.execute("SELECT * FROM PLdata order by ID")
                allPL=cursor.fetchall()
                for i in range(len(allPL)):
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    PLname=cursor.fetchall()[i][0]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    PLID=cursor.fetchall()[i][1]
                    IDlist.append([PLID,PLname])
                IDlist.sort(key=lambda x:x[0],reverse=False)#IDソート             
                for i in range(0,len(allPL),10):
                    if i!=len(allPL)-len(allPL)%10:
                        await message.channel.send(str(IDlist[i])+'\n'+str(IDlist[i+1])+'\n'+str(IDlist[i+2])+'\n'+str(IDlist[i+3])+'\n'+str(IDlist[i+4])+'\n'+str(IDlist[i+5])+'\n'+str(IDlist[i+6])+'\n'+str(IDlist[i+7])+'\n'+str(IDlist[i+8])+'\n'+str(IDlist[i+9]))
                    else:
                        for j in range(len(allPL)-(len(allPL)%10),len(allPL)):
                            await message.channel.send(str(IDlist[j]))
                await message.channel.send('出力完了です')
            else:
                await message.channel.send('管理技士専用コマンドです')
        #試合処理系統 result Rupdateコマンド
        if '/result'in message.content:#試合処理
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
                            await message.channel.send('構文エラーです。\n情報同一エラー')
                        else:
                            WID=int(res4[0])#勝者データ
                            WG=int(res5[0])
                            LID=int(res4[1])#敗者データ
                            LG=int(res5[1])
            else:
                await message.channel.send('構文エラーです。\n情報過多エラー')
    #レート処理
            cursor.execute("SELECT * FROM PLdata order by ID")
            Wname=cursor.fetchall()[WID][0]
            cursor.execute("SELECT * FROM PLdata order by ID")
            Lname=cursor.fetchall()[LID][0]
            cursor.execute("SELECT * FROM PLdata order by ID")
            WCR=cursor.fetchall()[WID][2]
            cursor.execute("SELECT * FROM PLdata order by ID")
            LCR=cursor.fetchall()[LID][2]
            cursor.execute("SELECT * FROM PLdata order by ID")
            WWR=cursor.fetchall()[WID][6]
            cursor.execute("SELECT * FROM PLdata order by ID")
            LWR=cursor.fetchall()[LID][6]

            match=int(WG+LG)
            await message.channel.send('結果出力が終わるまでコマンドは打たないでください'+'\n試合結果：'+Wname+"さん"+' 対 '+Lname+"さん"+'\n試合前レート'+'\n闘技場：'+str(WCR)+"-"+str(LCR)+"\n勝敗："+str(WWR)+"-"+str(LWR))
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
            NWWR=int(round(WWR+32*WBWper))
            NLWR=int(round(LWR-32*WBWper))
    #試合後の出力
            await message.channel.send('試合後レート'+"\n闘技場："+str(NWCR)+"-"+str(NLCR)+"\n勝敗："+str(NWWR)+"-"+str(NLWR))
    #データのアップデート
            #取得部分
            cursor.execute("SELECT * FROM PLdata order by ID")
            WCw=cursor.fetchall()[WID][4]
            cursor.execute("SELECT * FROM PLdata order by ID")
            WCl=cursor.fetchall()[WID][5]
            cursor.execute("SELECT * FROM PLdata order by ID")
            WWw=cursor.fetchall()[WID][8]
            cursor.execute("SELECT * FROM PLdata order by ID")
            WWl=cursor.fetchall()[WID][9]
            cursor.execute("SELECT * FROM PLdata order by ID")
            LCw=cursor.fetchall()[LID][4]
            cursor.execute("SELECT * FROM PLdata order by ID")
            LCl=cursor.fetchall()[LID][5]
            cursor.execute("SELECT * FROM PLdata order by ID")
            LWw=cursor.fetchall()[LID][8]
            cursor.execute("SELECT * FROM PLdata order by ID")
            LWl=cursor.fetchall()[LID][9]
            
            
            #勝利側
            WCw=WCw+WG
            WCl=+WCl+LG
            WCt=int(WCw)+int(WCl)
            WWw=int(WWw)+1
            WWt=int(WWw)+int(WWl)
            cursor.execute("update PLdata set CR=(%s) where ID=(%s)",(NWCR,WID))#CR
            cursor.execute("update PLdata set WR=(%s) where ID=(%s)",(NWWR,WID))#WR
            cursor.execute("update PLdata set Ctotal=(%s) where ID=(%s)",(WCt,WID))#Ctotal
            cursor.execute("update PLdata set Cwin=(%s) where ID=(%s)",(WCw,WID))#Cwin
            cursor.execute("update PLdata set Close=(%s) where ID=(%s)",(WCl,WID))#Close
            cursor.execute("update PLdata set Wtotal=(%s) where ID=(%s)",(WWt,WID))#Wtotal
            cursor.execute("update PLdata set Wwin=(%s) where ID=(%s)",(WWw,WID))#Wwin
            
            con.commit()
            #敗北側
            LCw=LCw+LG
            LCl=LCl+WG
            LCt=int(LCw)+int(LCl)
            LWl=int(LWl)+1
            LWt=int(LWl)+int(LWw)
            cursor.execute("update PLdata set CR=(%s) where ID=(%s)",(NLCR,LID))#CR
            cursor.execute("update PLdata set WR=(%s) where ID=(%s)",(NLWR,LID))#WR
            cursor.execute("update PLdata set Ctotal=(%s) where ID=(%s)",(LCt,LID))#Ctotal
            cursor.execute("update PLdata set Cwin=(%s) where ID=(%s)",(LCw,LID))#Cwin
            cursor.execute("update PLdata set Close=(%s) where ID=(%s)",(LCl,LID))#Close
            cursor.execute("update PLdata set Wtotal=(%s) where ID=(%s)",(LWt,LID))#Wtotal
            cursor.execute("update PLdata set Wlose=(%s) where ID=(%s)",(LWl,LID))#Wlose
            #試合記録
            cursor.execute("select * from history4 where Wname=(%s)",(Wname,))
            cursor.execute("select * from history4")
            Num=(len(cursor.fetchall())-1)
            cursor.execute("insert into history4 values ((%s),(%s),(%s),(%s),(%s),(%s),(%s))",(Num+1,Wname,WID,Lname,LID,WG,LG))
            con.commit()
            #ソート
            cursor.execute("SELECT * FROM PLdata order by ID")
            con.commit()
            await message.channel.send('試合ID：'+str(Num+1)+'\n出力終了です')
            
#レート一覧表示 以下管理技士専用コマンド
        if 'Rupdate'in message.content:#レート更新
            if message.author.guild_permissions.administrator:
                Rup=re.split('[\n]',message.content)
                channel=client.get_channel(ch_kan)#更新告知　ch_kan
                await channel.send(str(Rup[1])+'\nレート一覧を更新します\n完了の表示が出るまでコマンドを使用しないでください\nこの処理は5分～10分程度を要する可能性があります')
                #レートリセット
                cursor.execute("SELECT * FROM PLdata order by ID")
                allPL=cursor.fetchall()
                cursor.execute("select * from history4 order by MID")
                alhis=cursor.fetchall()
                for i in range(len(allPL)-1):
                    cursor.execute("update PLdata set CR=(%s) where ID=(%s)",(1500,i+1))#CR
                    cursor.execute("update PLdata set WR=(%s) where ID=(%s)",(1500,i+1))#WR
                    cursor.execute("update PLdata set Ctotal=(%s) where ID=(%s)",(0,i+1))#Ctotal
                    cursor.execute("update PLdata set Cwin=(%s) where ID=(%s)",(0,i+1))#Cwin
                    cursor.execute("update PLdata set Close=(%s) where ID=(%s)",(0,i+1))#Close
                    cursor.execute("update PLdata set Wtotal=(%s) where ID=(%s)",(0,i+1))#Wtotal
                    cursor.execute("update PLdata set Wwin=(%s) where ID=(%s)",(0,i+1))#Wwin
                    cursor.execute("update PLdata set Wlose=(%s) where ID=(%s)",(0,i+1))#Wlose
                #レート計算

                for i in range(len(alhis)-1):
                    cursor.execute("SELECT * FROM history4 order by MID")
                    WID=cursor.fetchall()[i+1][2]
                    cursor.execute("SELECT * FROM history4 order by MID")
                    LID=cursor.fetchall()[i+1][4]
                    cursor.execute("SELECT * FROM history4 order by MID")
                    WG=cursor.fetchall()[i+1][5]
                    cursor.execute("SELECT * FROM history4 order by MID")
                    LG=cursor.fetchall()[i+1][6]

                    cursor.execute("SELECT * FROM PLdata order by ID")
                    WCR=cursor.fetchall()[WID][2]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    LCR=cursor.fetchall()[LID][2]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    WWR=cursor.fetchall()[WID][6]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    LWR=cursor.fetchall()[LID][6]

                    match=int(WG+LG)
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
                    NWWR=int(round(WWR+32*WBWper))
                    NLWR=int(round(LWR-32*WBWper))

    #データのアップデート
                    #取得部分
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    WCw=cursor.fetchall()[WID][4]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    WCl=cursor.fetchall()[WID][5]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    WWw=cursor.fetchall()[WID][8]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    WWl=cursor.fetchall()[WID][9]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    LCw=cursor.fetchall()[LID][4]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    LCl=cursor.fetchall()[LID][5]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    LWw=cursor.fetchall()[LID][8]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    LWl=cursor.fetchall()[LID][9]
                    #勝利側
                    WCw=WCw+WG
                    WCl=+WCl+LG
                    WCt=int(WCw)+int(WCl)
                    WWw=int(WWw)+1
                    WWt=int(WWw)+int(WWl)
                    cursor.execute("update PLdata set CR=(%s) where ID=(%s)",(NWCR,WID))#CR
                    cursor.execute("update PLdata set WR=(%s) where ID=(%s)",(NWWR,WID))#WR
                    cursor.execute("update PLdata set Ctotal=(%s) where ID=(%s)",(WCt,WID))#Ctotal
                    cursor.execute("update PLdata set Cwin=(%s) where ID=(%s)",(WCw,WID))#Cwin
                    cursor.execute("update PLdata set Close=(%s) where ID=(%s)",(WCl,WID))#Close
                    cursor.execute("update PLdata set Wtotal=(%s) where ID=(%s)",(WWt,WID))#Wtotal
                    cursor.execute("update PLdata set Wwin=(%s) where ID=(%s)",(WWw,WID))#Wwin
                    con.commit()
                    #敗北側
                    LCw=LCw+LG
                    LCl=LCl+WG
                    LCt=int(LCw)+int(LCl)
                    LWl=int(LWl)+1
                    LWt=int(LWl)+int(LWw)
                    cursor.execute("update PLdata set CR=(%s) where ID=(%s)",(NLCR,LID))#CR
                    cursor.execute("update PLdata set WR=(%s) where ID=(%s)",(NLWR,LID))#WR
                    cursor.execute("update PLdata set Ctotal=(%s) where ID=(%s)",(LCt,LID))#Ctotal
                    cursor.execute("update PLdata set Cwin=(%s) where ID=(%s)",(LCw,LID))#Cwin
                    cursor.execute("update PLdata set Close=(%s) where ID=(%s)",(LCl,LID))#Close
                    cursor.execute("update PLdata set Wtotal=(%s) where ID=(%s)",(LWt,LID))#Wtotal
                    cursor.execute("update PLdata set Wlose=(%s) where ID=(%s)",(LWl,LID))#Wlose
                    #ソート
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    cursor.execute("SELECT * FROM history4 order by MID")
                    con.commit()

                sort_CR=[]
                sort_WR=[]
                rank_CR=[]
                rank_WR=[]

                channel=client.get_channel(ch_CR)#ch_CRに変更
                #闘技場レート＆勝敗レート処理
                cursor.execute("SELECT * FROM PLdata order by ID")
                allPL=cursor.fetchall()
                for i in range(len(allPL)):
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    PLname=cursor.fetchall()[i][0]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    PLID=cursor.fetchall()[i][1]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    PLCR=cursor.fetchall()[i][2]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    PLWR=cursor.fetchall()[i][6]
                    sort_CR.append([PLID,PLname,PLCR])
                    sort_WR.append([PLID,PLname,PLWR])
                #闘技場レート出力機構
                await channel.send(str(Rup[1])+'現在\n闘技場レート')#闘技場レート更新
                sort_CR.sort(key=lambda x:x[0],reverse=False)#IDソート
                for j in range(0,len(allPL),5):
                    if j!=len(allPL)-len(allPL)%5:
                        await channel.send(str(sort_CR[j])+'\n'+str(sort_CR[j+1])+'\n'+str(sort_CR[j+2])\
                                       +'\n'+str(sort_CR[j+3])+'\n'+str(sort_CR[j+4]))
                else:
                    for i in range(len(allPL)-(len(allPL)%5),len(allPL)):
                        await channel.send(str(sort_CR[i]))
                await channel.send('出力完了です')
                #勝敗レート出力機構
                channel=client.get_channel(ch_WR)#ch_WRに変更
                await channel.send(str(Rup[1])+'現在\n勝敗レート')#勝敗レート更新
                sort_WR.sort(key=lambda x:x[0],reverse=False)#IDソート
                for j in range(0,len(allPL),5):
                    if j!=len(allPL)-len(allPL)%5:
                        await channel.send(str(sort_WR[j])+'\n'+str(sort_WR[j+1])+'\n'+str(sort_WR[j+2])\
                                       +'\n'+str(sort_WR[j+3])+'\n'+str(sort_WR[j+4]))
                else:
                    for i in range(len(allPL)-(len(allPL)%5),len(allPL)):
                        await channel.send(str(sort_WR[i]))
                await channel.send('出力完了です')
                #レートランキング出力機構
                channel=client.get_channel(ch_RR)#ch_RRに変更
                await channel.send(str(Rup[1])+'現在\nレートランキング')#レートランキング更新
                for k in range(len(allPL)):
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    PLname=cursor.fetchall()[k][0]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    PLCRr=cursor.fetchall()[k][2]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    PLWRr=cursor.fetchall()[k][6]
                    rank_CR.append([PLCRr,PLname])
                    rank_WR.append([PLWRr,PLname])
                rank_CR.sort(key=lambda x:x[0],reverse=True)#ソートCR
                rank_WR.sort(key=lambda x:x[0],reverse=True)#ソートWR
                channel=client.get_channel(ch_RR)#ch_RRに変更
                await channel.send('闘技場レートランキング')
                await channel.send(str(rank_CR[0])+'\n'+str(rank_CR[1])+'\n'+str(rank_CR[2])+'\n'+str(rank_CR[3])+'\n'+str(rank_CR[4])+'\n'+str(rank_CR[5])\
                                   +'\n'+str(rank_CR[6])+'\n'+str(rank_CR[7])+'\n'+str(rank_CR[8])+'\n'+str(rank_CR[9]))
                await channel.send('勝敗レートランキング')
                await channel.send(str(rank_WR[0])+'\n'+str(rank_WR[1])+'\n'+str(rank_WR[2])+'\n'+str(rank_WR[3])+'\n'+str(rank_WR[4])+'\n'+str(rank_WR[5])\
                                   +'\n'+str(rank_WR[6])+'\n'+str(rank_WR[7])+'\n'+str(rank_WR[8])+'\n'+str(rank_WR[9]))
                await channel.send('出力完了です')
                #終了告知
                channel=client.get_channel(ch_kan)#更新告知　ch_kan
                await channel.send(str(Rup[1])+'\nレート一覧を更新しました')
            else:
                await message.channel.send('管理技士専用コマンドです')

#レート再計算コマンド
        if 'recal'in message.content:#レート更新
            if message.author.guild_permissions.administrator:
                #レートリセット
                cursor.execute("SELECT * FROM PLdata order by ID")
                allPL=cursor.fetchall()
                cursor.execute("select * from history4 order by MID")
                alhis=cursor.fetchall()
                for i in range(len(allPL)):
                    cursor.execute("update PLdata set CR=(%s) where ID=(%s)",(1500,i))#CR
                    cursor.execute("update PLdata set WR=(%s) where ID=(%s)",(1500,i))#WR
                    cursor.execute("update PLdata set Ctotal=(%s) where ID=(%s)",(0,i))#Ctotal
                    cursor.execute("update PLdata set Cwin=(%s) where ID=(%s)",(0,i))#Cwin
                    cursor.execute("update PLdata set Close=(%s) where ID=(%s)",(0,i))#Close
                    cursor.execute("update PLdata set Wtotal=(%s) where ID=(%s)",(0,i))#Wtotal
                    cursor.execute("update PLdata set Wwin=(%s) where ID=(%s)",(0,i))#Wwin
                    cursor.execute("update PLdata set Wlose=(%s) where ID=(%s)",(0,i))#Wlose

                await message.channel.send('レリセ完了')

                #レート計算
                for i in range(len(alhis)-1):
                    cursor.execute("SELECT * FROM history4 order by MID")
                    WID=cursor.fetchall()[i+1][2]
                    cursor.execute("SELECT * FROM history4 order by MID")
                    LID=cursor.fetchall()[i+1][4]
                    cursor.execute("SELECT * FROM history4 order by MID")
                    WG=cursor.fetchall()[i+1][5]
                    cursor.execute("SELECT * FROM history4 order by MID")
                    LG=cursor.fetchall()[i+1][6]

                    cursor.execute("SELECT * FROM PLdata order by ID")
                    WCR=cursor.fetchall()[WID][2]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    LCR=cursor.fetchall()[LID][2]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    WWR=cursor.fetchall()[WID][6]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    LWR=cursor.fetchall()[LID][6]

                    match=int(WG+LG)
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
                    NWWR=int(round(WWR+32*WBWper))
                    NLWR=int(round(LWR-32*WBWper))

    #データのアップデート
                    #取得部分
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    WCw=cursor.fetchall()[WID][4]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    WCl=cursor.fetchall()[WID][5]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    WWw=cursor.fetchall()[WID][8]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    WWl=cursor.fetchall()[WID][9]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    LCw=cursor.fetchall()[LID][4]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    LCl=cursor.fetchall()[LID][5]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    LWw=cursor.fetchall()[LID][8]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    LWl=cursor.fetchall()[LID][9]
                    
                    cursor.execute("SELECT * FROM TTQual order by PLID")
                    WCmax=cursor.fetchall()[WID][1]
                    cursor.execute("SELECT * FROM TTQual order by PLID")
                    LCmax=cursor.fetchall()[LID][1]
                    cursor.execute("SELECT * FROM TTQual order by PLID")
                    WRmax=cursor.fetchall()[WID][2]
                    #勝利側
                    WCw=WCw+WG
                    WCl=+WCl+LG
                    WCt=int(WCw)+int(WCl)
                    WWw=int(WWw)+1
                    WWt=int(WWw)+int(WWl)
                    cursor.execute("update PLdata set CR=(%s) where ID=(%s)",(NWCR,WID))#CR
                    cursor.execute("update PLdata set WR=(%s) where ID=(%s)",(NWWR,WID))#WR
                    cursor.execute("update PLdata set Ctotal=(%s) where ID=(%s)",(WCt,WID))#Ctotal
                    cursor.execute("update PLdata set Cwin=(%s) where ID=(%s)",(WCw,WID))#Cwin
                    cursor.execute("update PLdata set Close=(%s) where ID=(%s)",(WCl,WID))#Close
                    cursor.execute("update PLdata set Wtotal=(%s) where ID=(%s)",(WWt,WID))#Wtotal
                    cursor.execute("update PLdata set Wwin=(%s) where ID=(%s)",(WWw,WID))#Wwin
                    cursor.execute("update TTQual set Wnow=(%s) where PLID=(%s)",(NWWR,WID))#WR
                    if int(NWCR)>int(WCmax):
                        cursor.execute("update TTQual set CRmax=(%s) where PLID=(%s)",(NWCR,WID))#WCmax
                    if int(NWWR)>int(WRmax):
                        cursor.execute("update TTQual set WRmax=(%s) where PLID=(%s)",(NWWR,WID))#WRmax
                    con.commit()
                    #敗北側
                    LCw=LCw+LG
                    LCl=LCl+WG
                    LCt=int(LCw)+int(LCl)
                    LWl=int(LWl)+1
                    LWt=int(LWl)+int(LWw)
                    cursor.execute("update PLdata set CR=(%s) where ID=(%s)",(NLCR,LID))#CR
                    cursor.execute("update PLdata set WR=(%s) where ID=(%s)",(NLWR,LID))#WR
                    cursor.execute("update PLdata set Ctotal=(%s) where ID=(%s)",(LCt,LID))#Ctotal
                    cursor.execute("update PLdata set Cwin=(%s) where ID=(%s)",(LCw,LID))#Cwin
                    cursor.execute("update PLdata set Close=(%s) where ID=(%s)",(LCl,LID))#Close
                    cursor.execute("update PLdata set Wtotal=(%s) where ID=(%s)",(LWt,LID))#Wtotal
                    cursor.execute("update PLdata set Wlose=(%s) where ID=(%s)",(LWl,LID))#Wlose
                    cursor.execute("update TTQual set Wnow=(%s) where PLID=(%s)",(NLWR,LID))#WR
                    if int(NLCR)>int(LCmax):
                        cursor.execute("update TTQual set CRmax=(%s) where PLID=(%s)",(NLCR,LID))#LCmax
                    #ソート
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    cursor.execute("SELECT * FROM history4 order by MID")
                    cursor.execute("SELECT * FROM TTQual order by PLID")
                    con.commit()
                await message.channel.send('完了です')

            else:
                await message.channel.send('管理技士専用コマンドです')

                
#試合結果修正コマンド
        if 'edit' in message.content:
            res100=re.split('[\n/-]',message.content)#分割
            try:
                test0=res100[10]
            except IndexError:
                try:
                    MID=int(res100[1])
                    DWID=int(res100[2])
                    DLID=int(res100[3])
                    NWID=int(res100[6])
                    NLID=int(res100[7])
                    DWres=int(res100[4])
                    DLles=int(res100[5])
                    NWres=int(res100[8])
                    NLres=int(res100[9])
                except ValueError:
                    await message.channel.send('構文エラーです\n記号ミスエラー')
                else:
                    try:
                        test101=1/int(int(NWID)-int(NLID))
                        test102=1/int(int(NWres)-int(NLres))
                    except ZeroDivisionError:
                        await message.channel.send('構文エラーです。\n情報同一エラー')
                    else:
                        pass
            else:
                await message.channel.send('構文エラーです。\n情報過多エラー')

            MID=int(res100[1])
            DWID=int(res100[2])
            DLID=int(res100[3])
            NWID=int(res100[6])
            NLID=int(res100[7])
            DWres=int(res100[4])
            DLres=int(res100[5])
            NWres=int(res100[8])
            NLres=int(res100[9])
        
            #history4から抽出
            cursor.execute("SELECT * FROM history4 order by MID")#試合ID
            Match=cursor.fetchall()[MID][0]
            cursor.execute("SELECT * FROM history4 order by MID")#WID
            WinID=cursor.fetchall()[MID][2]
            cursor.execute("SELECT * FROM history4 order by MID")#LID
            LoseID=cursor.fetchall()[MID][4]
            cursor.execute("SELECT * FROM history4 order by MID")#Wcount
            Wcount=cursor.fetchall()[MID][5]
            cursor.execute("SELECT * FROM history4 order by MID")#Lcount
            Lcount=cursor.fetchall()[MID][6]
            
            try:
                test110=1/int(int(DWID)-int(WinID))
                test111=1/int(int(DLID)-int(LoseID))
                test112=1/int(int(DWres)-int(Wcount))
                test13=1/int(int(DLres)-int(Lcount))
            except ZeroDivisionError:

                cursor.execute("SELECT * FROM PLdata order by ID")#勝者名前取得
                Wname=cursor.fetchall()[WinID][0]
                cursor.execute("SELECT * FROM PLdata order by ID")#敗者名前取得
                Lname=cursor.fetchall()[LoseID][0]

                #修正上書き
                cursor.execute("update history4 set Wname=(%s) where MID=(%s)",(Wname,MID))#Wname
                cursor.execute("update history4 set WinID=(%s) where MID=(%s)",(NWID,MID))#WinID
                cursor.execute("update history4 set Lname=(%s) where MID=(%s)",(Lname,MID))#Lname
                cursor.execute("update history4 set LoseID=(%s) where MID=(%s)",(NLID,MID))#LoseID
                cursor.execute("update history4 set Wcount=(%s) where MID=(%s)",(NWres,MID))#Wcount
                cursor.execute("update history4 set Lcount=(%s) where MID=(%s)",(NLres,MID))#Lcount
                cursor.execute("SELECT * FROM history4 order by MID")
                con.commit()
                await message.channel.send('修正完了です')

            else:
                await message.channel.send('構文エラーです。\n情報不一致エラー')

                
                
#天庭戦資格アップデートコマンド
        if 'Tupdate'in message.content:#資格関連更新
            if message.author.guild_permissions.administrator:
                cursor.execute("select * from PLdata order by ID")
                allPL=cursor.fetchall()
                for i in range(len(allPL)):
                    cursor.execute("SELECT * FROM TTQual order by PLID")
                    WRmax=cursor.fetchall()[i][2]
                    cursor.execute("SELECT * FROM TTQual order by PLID")
                    qual=cursor.fetchall()[i][3]
                    cursor.execute("SELECT * FROM TTQual order by PLID")
                    rank=cursor.fetchall()[i][4]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    NWR=cursor.fetchall()[i][6]
                    cursor.execute("SELECT * FROM PLdata order by ID")
                    game=cursor.fetchall()[i][7]
                    if int(game)>=20 and int(WRmax)>=1550:
                        if int(game)>=25 and int(WRmax)>=1600:
                            qual='資格保持'
                        else:
                            qual='次点保持'
                    #上書き
                    cursor.execute("update TTQual set Qual=(%s) where PLID=(%s)",(qual,i))#Qual
                    cursor.execute("SELECT * FROM history4 order by MID")
                    con.commit
                cursor.execute("SELECT * FROM TTQual where Qual=(%s) order by Wnow desc",('資格保持',) )
                FQ=cursor.fetchall()
                for i in range(len(FQ)):
                    FQID=FQ[i][0]
                    cursor.execute("update TTQual set Rank=(%s) where PLID=(%s)",(i+1,FQID))#順位更新
                    if i+1>=9:
                        cursor.execute("update TTQual set Qual=(%s) where PLID=(%s)",('資格補欠',FQID))#資格変更
                        cursor.execute("update TTQual set Rank=(%s) where PLID=(%s)",(i+3,FQID))#順位更新
                    con.commit()    
                    await message.channel.send(FQ[i])
                cursor.execute("SELECT * FROM TTQual where Qual=(%s) order by Wnow desc",('次点保持',))
                SQ=cursor.fetchall()
                for i in range(len(SQ)):
                    SQID=SQ[i][0]
                    cursor.execute("update TTQual set Rank=(%s) where PLID=(%s)",(i+101,SQID))#順位更新
                    con.commit()
                    await message.channel.send(SQ[i])
                cursor.execute("SELECT * FROM history4 order by MID")
                con.commit()
            else:
                await message.channel.send('管理技士専用コマンドです')
                
        if 'make_s2PLD' == message.content:#S2PLdata DB作成
            cursor.execute("DROP TABLE IF EXISTS s2PLD")
            cursor.execute("create table s2PLD(name text,ID integer,CR integer,Ctotal integer,Cwin integer,Close integer,WR integer,Wtotal integer,Wwin integer,Wlose integer)")
            cursor.execute("insert into s2PLD values('Yataswee',0,1500,0,0,0,1500,0,0,0)")
            
            cursor.execute("select * from PLdata order by ID")
            allPL=cursor.fetchall()
            for i in range(len(allPL)-1):
                cursor.execute("insert into s2PLD values ((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))",('仮',i+1,1500,0,0,0,1500,0,0,0))
            con.commit()
            await message.channel.send('作成完了です')
            
        if 'check_s2PLD' == message.content:#s2PLDを見る
            if message.author.guild_permissions.administrator:
                cursor.execute("select * from s2PLD order by ID")
                allPL=cursor.fetchall()
                for j in range(0,len(allPL),5):
                    if j!=len(allPL)-len(allPL)%5:
                        await message.channel.send(str(allPL[j])+'\n'+str(allPL[j+1])+'\n'+str(allPL[j+2])\
                                                   +'\n'+str(allPL[j+3])+'\n'+str(allPL[j+4]))
                    else:
                        for i in range(len(allPL)-(len(allPL)%5),len(allPL)):
                            await message.channel.send(str(allPL[i]))
                await message.channel.send("全員出力完了！")
                
        if 'make_s2TTQ' == message.content:#天庭戦関連DBの作成
            cursor.execute("DROP TABLE IF EXISTS s2TTQ")
            cursor.execute("create table s2TTQ(PLID integer,CRmax integer,WRmax integer,Qual text, Rank integer)")
            cursor.execute("insert into s2TTQ values(0,1500,1500,'特になし',999)")
            
            cursor.execute("select * from s2PLD order by ID")
            allPL=cursor.fetchall()
            for i in range(len(allPL)-1):
                cursor.execute("insert into s2TTQ values ((%s),(%s),(%s),(%s),(%s))",(i+1,1500,1500,'特になし',999,))
            con.commit()
            await message.channel.send('作成完了です')

        if 'check_s2TTQ' == message.content:#s2TTQを見る
            if message.author.guild_permissions.administrator:
                cursor.execute("SELECT * FROM s2TTQ order by PLID")
                allQ=cursor.fetchall()
                for j in range(0,len(allQ),5):
                    if j!=len(allQ)-len(allQ)%5:
                        await message.channel.send(str(allQ[j])+'\n'+str(allQ[j+1])+'\n'+str(allQ[j+2])\
                                                   +'\n'+str(allQ[j+3])+'\n'+str(allQ[j+4]))
                    else:
                        for i in range(len(allQ)-(len(allQ)%5),len(allQ)):
                            await message.channel.send(str(allQ[i]))
                await message.channel.send("全員出力完了！")
                
        if 's2RCL'in message.content:#レート更新
            if message.author.guild_permissions.administrator:
                #レートリセット
                cursor.execute("SELECT * FROM s2PLD order by ID")
                allPL=cursor.fetchall()
                cursor.execute("select * from history order by MID")
                alhis=cursor.fetchall()
                for i in range(len(allPL)):
                    cursor.execute("update s2PLD set CR=(%s) where ID=(%s)",(1500,i))#CR
                    cursor.execute("update s2PLD set WR=(%s) where ID=(%s)",(1500,i))#WR
                    cursor.execute("update s2PLD set Ctotal=(%s) where ID=(%s)",(0,i))#Ctotal
                    cursor.execute("update s2PLD set Cwin=(%s) where ID=(%s)",(0,i))#Cwin
                    cursor.execute("update s2PLD set Close=(%s) where ID=(%s)",(0,i))#Close
                    cursor.execute("update s2PLD set Wtotal=(%s) where ID=(%s)",(0,i))#Wtotal
                    cursor.execute("update s2PLD set Wwin=(%s) where ID=(%s)",(0,i))#Wwin
                    cursor.execute("update s2PLD set Wlose=(%s) where ID=(%s)",(0,i))#Wlose

                await message.channel.send('レリセ完了')

                #レート計算
                for i in range(len(alhis)-1):
                    if i%5==2:
                        await message.channel.send(i+1)
                    cursor.execute("SELECT * FROM history order by MID")
                    WID=cursor.fetchall()[i+1][2]
                    cursor.execute("SELECT * FROM history order by MID")
                    LID=cursor.fetchall()[i+1][4]
                    cursor.execute("SELECT * FROM history order by MID")
                    WG=cursor.fetchall()[i+1][5]
                    cursor.execute("SELECT * FROM history order by MID")
                    LG=cursor.fetchall()[i+1][6]

                    cursor.execute("SELECT * FROM s2PLD order by ID")
                    WCR=cursor.fetchall()[WID][2]
                    cursor.execute("SELECT * FROM s2PLD order by ID")
                    LCR=cursor.fetchall()[LID][2]
                    cursor.execute("SELECT * FROM s2PLD order by ID")
                    WWR=cursor.fetchall()[WID][6]
                    cursor.execute("SELECT * FROM s2PLD order by ID")
                    LWR=cursor.fetchall()[LID][6]

                    match=int(WG+LG)
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

    #データのアップデート
                    #取得部分
                    cursor.execute("SELECT * FROM s2PLD order by ID")
                    WCw=cursor.fetchall()[WID][4]
                    cursor.execute("SELECT * FROM s2PLD order by ID")
                    WCl=cursor.fetchall()[WID][5]
                    cursor.execute("SELECT * FROM s2PLD order by ID")
                    WWw=cursor.fetchall()[WID][8]
                    cursor.execute("SELECT * FROM s2PLD order by ID")
                    WWl=cursor.fetchall()[WID][9]
                    cursor.execute("SELECT * FROM s2PLD order by ID")
                    LCw=cursor.fetchall()[LID][4]
                    cursor.execute("SELECT * FROM s2PLD order by ID")
                    LCl=cursor.fetchall()[LID][5]
                    cursor.execute("SELECT * FROM s2PLD order by ID")
                    LWw=cursor.fetchall()[LID][8]
                    cursor.execute("SELECT * FROM s2PLD order by ID")
                    LWl=cursor.fetchall()[LID][9]
                    
                    cursor.execute("SELECT * FROM s2TTQ order by PLID")
                    WCmax=cursor.fetchall()[WID][1]
                    cursor.execute("SELECT * FROM s2TTQ order by PLID")
                    LCmax=cursor.fetchall()[LID][1]
                    cursor.execute("SELECT * FROM s2TTQ order by PLID")
                    WRmax=cursor.fetchall()[WID][2]
                    #勝利側
                    WCw=WCw+WG
                    WCl=+WCl+LG
                    WCt=int(WCw)+int(WCl)
                    WWw=int(WWw)+1
                    WWt=int(WWw)+int(WWl)
                    cursor.execute("update s2PLD set CR=(%s) where ID=(%s)",(NWCR,WID))#CR
                    cursor.execute("update s2PLD set WR=(%s) where ID=(%s)",(NWWR,WID))#WR
                    cursor.execute("update s2PLD set Ctotal=(%s) where ID=(%s)",(WCt,WID))#Ctotal
                    cursor.execute("update s2PLD set Cwin=(%s) where ID=(%s)",(WCw,WID))#Cwin
                    cursor.execute("update s2PLD set Close=(%s) where ID=(%s)",(WCl,WID))#Close
                    cursor.execute("update s2PLD set Wtotal=(%s) where ID=(%s)",(WWt,WID))#Wtotal
                    cursor.execute("update s2PLD set Wwin=(%s) where ID=(%s)",(WWw,WID))#Wwin
                    if int(NWCR)>int(WCmax):
                        cursor.execute("update s2TTQ set CRmax=(%s) where PLID=(%s)",(NWCR,WID))#WCmax
                    if int(NWWR)>int(WRmax):
                        cursor.execute("update s2TTQ set WRmax=(%s) where PLID=(%s)",(NWWR,WID))#WRmax
                    con.commit()
                    #敗北側
                    LCw=LCw+LG
                    LCl=LCl+WG
                    LCt=int(LCw)+int(LCl)
                    LWl=int(LWl)+1
                    LWt=int(LWl)+int(LWw)
                    cursor.execute("update s2PLD set CR=(%s) where ID=(%s)",(NLCR,LID))#CR
                    cursor.execute("update s2PLD set WR=(%s) where ID=(%s)",(NLWR,LID))#WR
                    cursor.execute("update s2PLD set Ctotal=(%s) where ID=(%s)",(LCt,LID))#Ctotal
                    cursor.execute("update s2PLD set Cwin=(%s) where ID=(%s)",(LCw,LID))#Cwin
                    cursor.execute("update s2PLD set Close=(%s) where ID=(%s)",(LCl,LID))#Close
                    cursor.execute("update s2PLD set Wtotal=(%s) where ID=(%s)",(LWt,LID))#Wtotal
                    cursor.execute("update s2PLD set Wlose=(%s) where ID=(%s)",(LWl,LID))#Wlose
                    if int(NLCR)>int(LCmax):
                        cursor.execute("update s2TTQ set CRmax=(%s) where PLID=(%s)",(NLCR,LID))#LCmax
                    #ソート
                    cursor.execute("SELECT * FROM s2PLD order by ID")
                    cursor.execute("SELECT * FROM history order by MID")
                    cursor.execute("SELECT * FROM s2TTQ order by PLID")
                    con.commit()
                await message.channel.send('完了です')

            else:
                await message.channel.send('管理技士専用コマンドです')
                
        if 's2TUD'in message.content:#資格関連更新
            if message.author.guild_permissions.administrator:
                cursor.execute("select * from s2PLD order by ID")
                allPL=cursor.fetchall()
                for i in range(len(allPL)):
                    cursor.execute("SELECT * FROM s2TTQ order by PLID")
                    WRmax=cursor.fetchall()[i][2]
                    cursor.execute("SELECT * FROM s2TTQ order by PLID")
                    qual=cursor.fetchall()[i][3]
                    cursor.execute("SELECT * FROM s2TTQ order by PLID")
                    rank=cursor.fetchall()[i][4]
                    cursor.execute("SELECT * FROM s2PLD order by ID")
                    NWR=cursor.fetchall()[i][6]
                    cursor.execute("SELECT * FROM s2PLD order by ID")
                    game=cursor.fetchall()[i][7]
                    if int(game)>=20 and int(WRmax)>=1550:
                        if int(game)>=25 and int(WRmax)>=1600:
                            qual='資格保持'
                        else:
                            qual='次点保持'
                    #上書き
                    cursor.execute("update s2TTQ set Qual=(%s) where PLID=(%s)",(qual,i))#Qual
                    cursor.execute("SELECT * FROM history order by MID")
                    con.commit
                    
                cursor.execute("SELECT * FROM s2TTQ where Qual=(%s)",('資格保持',))
                FQ=cursor.fetchall()
                for i in range(len(FQ)):
                    await message.channel.send(FQ[i])
                cursor.execute("SELECT * FROM s2TTQ where Qual=(%s)",('次点保持',))
                SQ=cursor.fetchall()
                for i in range(len(SQ)):
                    await message.channel.send(SQ[i])
                cursor.execute("SELECT * FROM history order by MID")
                con.commit
            else:
                await message.channel.send('管理技士専用コマンドです')

        if 'Rcheck'in message.content:#資格関連更新
            TCR=0
            TWR=0
            for i in range(allPlayer):
                cursor.execute("SELECT * FROM PLdata order by ID")#CR
                CR=cursor.fetchall()[i][2]
                cursor.execute("SELECT * FROM PLdata order by ID")#Cwin
                WR=cursor.fetchall()[i][6]
                TCR+=CR
                TWR+=WR
                Ave_CR=TCR/allPlayer
                Ave_WR=TWR/allPlayer
            await message.channel.send(str(Ave_CR)+'　'+str(Ave_WR))


    except:
        traceback.print_exc()
        cursor.execute("ROLLBACK")
        await message.channel.send('どこかでエラーが検出されました')
# Botの起動とDiscordサーバーへの接続
client.run(token)
