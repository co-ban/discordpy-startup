import discord
import datetime
import os

client = discord.Client()

token = os.environ['DISCORD_BOT_TOKEN']
channelid = os.environ['CHANNELID']
dividelistnum = os.environ['DIVIDE_LIST_NUM']

@client.event
async def on_ready():
    print('ログインしました。')

@client.event
async def on_message(message):
    # ".凸管理@数字"で起動
    if message.content.startswith(".凸管理"):

        # チャンネル制御
        if message.channel.id == int(channelid):

            # 最初の出力内容
            daycount = int(message.content[5:len(message.content)])
            dt_now = datetime.datetime.now()
            ymd = dt_now.strftime('%Y年%m月%d日')
            text = "（{}日目）\n"
            whatday = text.format(daycount)
            todaymsg = '**__'+ ymd + whatday + '__**'

            reaction_member = [">>>"]

            msg = await message.channel.send(todaymsg)

            # メンバー取得
            global memname
            user_count = sum(1 for member in message.guild.members if not member.bot)
            memname = [member.name for member in message.guild.members if not member.bot]
            
            # メンバーリスト
            global memberlist
            global memberlist2
            memberlist = discord.Embed(color=0x00ff00)
            memberlist2 = discord.Embed(color=0x00ff00)
            
            # 2段目リスト表示フラグ
            global displaymemberlist2
            displaymemberlist2 = 0

            # メンバーリスト作成処理
            for i in range(user_count):
                indexnum = i + 1
                printnum = str(indexnum).zfill(2)

                # リスト分岐処理
                # Embedのフィールド数の最大が25のため2段目のリストを用意
                if i < int(dividelistnum):
                    memberlist.add_field(name=f'**{printnum} : {memname[i]}**', value="** **", inline=False)
                else:
                    memberlist2.add_field(name=f'**{printnum} : {memname[i]}**', value="** **", inline=False)
                    displaymemberlist2 = 1

            # 起動時リアクション処理回避フラグON
            global startupavoid
            startupavoid = 1

            # メダル
            global medalemojis
            medalemojis = ["\U0001f947","\U0001f948","\U0001f949"]

            # 凸回数メッセージ出力
            atk = await message.channel.send("ポチリンピック凸会場")

            for i in range(len(medalemojis)):
                await atk.add_reaction(medalemojis[i])

            # 凸数メッセージのIDを取得
            global atkmsgid
            atkmsgid = atk.id

            # 四角数字
            global numemojis
            numemojis = ["1⃣","2⃣","3⃣","4⃣","5⃣"]

            # 持ち越しメッセージ出力
            global carryover
            carryover = await message.channel.send('持ち越し')

            for i in range(len(numemojis)):
                await carryover.add_reaction(numemojis[i])
            
            # 持ち越しメッセージのIDを取得
            global carryovermsgid
            carryovermsgid = carryover.id

            # メンバーリスト出力
            global members
            members = await message.channel.send(embed=memberlist)
            
            # 2段目メンバーリスト出力
            if displaymemberlist2 == 1:
                global members2
                members2 = await message.channel.send(embed=memberlist2)

            # 起動時処理回避フラグOFF
            startupavoid = 0

@client.event
async def on_reaction_add(reaction, user):

    # 起動時処理回避判定
    #if startupavoid == 1:
    #   return
    medalemojis = ["\U0001f947","\U0001f948","\U0001f949"]
    global atkmsgid
    numemojis = ["1⃣","2⃣","3⃣","4⃣","5⃣"]
    global carryovermsgid
    
    # 凸管理botに対するリアクションかどうか判定
    if (reaction.emoji in medalemojis and reaction.message.id == atkmsgid or
        reaction.emoji in numemojis and reaction.message.id == carryovermsgid):

        # 対象者の取得
        for i in range(len(memname)):
            str_name = memname[i]

            # リアクション追加処理
            if str_name.startswith(user.name):
                indexnum = i + 1
                printnum = str(indexnum).zfill(2)
                memname[i] = memname[i] + " " + str(reaction)

                # メンバー情報再表示
                if i < int(dividelistnum):
                    memberlist.remove_field(i)
                    memberlist.insert_field_at(i, name=f'**{printnum} : {memname[i]}**', value="** **", inline=False)
                    await members.edit(embed=memberlist)
                    break
                else:
                    indexnum = i - int(dividelistnum)
                    memberlist2.remove_field(indexnum)
                    memberlist2.insert_field_at(indexnum, name=f'**{printnum} : {memname[i]}**', value="** **", inline=False)
                    await members2.edit(embed=memberlist2)
                    break

@client.event
async def on_reaction_remove(reaction, user):

    medalemojis = ["\U0001f947","\U0001f948","\U0001f949"]
    global atkmsgid
    numemojis = ["1⃣","2⃣","3⃣","4⃣","5⃣"]
    global carryovermsgid
    
    # 凸管理botに対するリアクションかどうか判定
    if (reaction.emoji in medalemojis and reaction.message.id == atkmsgid or
        reaction.emoji in numemojis and reaction.message.id == carryovermsgid):

        # 対象者の取得
        for i in range(len(memname)):
            str_name = memname[i]

            # リアクション削除処理
            if str_name.startswith(user.name):
                indexnum = i + 1
                printnum = str(indexnum).zfill(2)
                memname[i] = str(memname[i]).replace(" " + str(reaction),"",1)

                # メンバー情報再表示
                if i < int(dividelistnum):
                    memberlist.remove_field(i)
                    memberlist.insert_field_at(i, name=f'**{printnum} : {memname[i]}**', value="** **", inline=False)
                    await members.edit(embed=memberlist)
                    break
                else:
                    indexnum = i - int(dividelistnum)
                    memberlist2.remove_field(indexnum)
                    memberlist2.insert_field_at(indexnum, name=f'**{printnum} : {memname[i]}**', value="** **", inline=False)
                    await members2.edit(embed=memberlist2)
                    break

client.run(token)
