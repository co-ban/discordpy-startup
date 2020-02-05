import discord
import datetime

client = discord.Client()

@client.event
async def on_ready():
    print('ログインしました。')

@client.event
async def on_message(message):
    # ".凸管理@数字"で起動
    if message.content.startswith(".凸管理"):

        # 最初の行の出力内容を加工
        daycount = int(message.content[5:len(message.content)])
        dt_now = datetime.datetime.now()
        ymd = dt_now.strftime('%Y年%m月%d日')
        text = "（{}日目）\n"
        whatday = text.format(daycount)
        todaymsg = '**__'+ ymd + whatday + '__**'
        
        reaction_member = [">>>"]
        
        # 凸管理チャンネルのID取得
        # 後でチャンネル制御を実装予定（一番上に処理を移動する）
        #channel_ID = 627778785051279360
        global channel_ID
        channel_ID = 666298362437304342
        global channel
        channel = client.get_channel(channel_ID)
        #channel = message.channel

        msg = await message.channel.send(todaymsg)

        # メンバー
        user_count = sum(1 for member in message.guild.members if not member.bot)
        global memname
        memname = [member.name for member in message.guild.members if not member.bot]
        global membername
        membername = discord.Embed(color=0x00ff00)

        for i in range(user_count):
            a = i + 1
            b = str(a).zfill(2)
            membername.add_field(name=f'**{b} : {memname[i]}**', value="** **", inline=False)

        # embed削除処理回避フラグ
        global notdeleteembed
        notdeleteembed = 1

        # 凸回数
        atk = await message.channel.send("ポチリンピック凸会場")
        await atk.add_reaction('\U0001f947')
        await atk.add_reaction('\U0001f948')
        await atk.add_reaction('\U0001f949')

        # 持ち越し
        carryover = await message.channel.send('持ち越し')

        cnt = 5
        emojis = ["1⃣","2⃣","3⃣","4⃣","5⃣"]

        for i in range(cnt):
            await carryover.add_reaction(emojis[i])

        global members
        members = await message.channel.send(embed=membername)
        
        # embed削除処理回避フラグ解除
        notdeleteembed = 0

@client.event
async def on_reaction_add(reaction, user):

    for i in range(len(memname)):
        str_name = memname[i]
        if str_name.startswith(user.name):
            indexnum = i
            printnum = str(indexnum+1).zfill(2)

            memname[indexnum] = memname[indexnum] + " " + str(reaction)
            
            # メンバー情報再表示
            global members
            if notdeleteembed != 1:
                membername.remove_field(indexnum)
                membername.insert_field_at(indexnum, name=f'**{printnum} : {memname[indexnum]}**', value="** **", inline=False)
                await members.edit(embed=membername)
                break

@client.event
async def on_reaction_remove(reaction, user):

    for i in range(len(memname)):
        str_name = memname[i]
        if str_name.startswith(user.name):
            indexnum = i
            printnum = str(indexnum+1).zfill(2)
            memname[indexnum] = str(memname[indexnum]).replace(" " + str(reaction),"",1)

            # メンバー情報再表示
            global members
            if notdeleteembed != 1:
                membername.remove_field(indexnum)
                membername.insert_field_at(indexnum, name=f'**{printnum} : {memname[indexnum]}**', value="** **", inline=False)
                await members.edit(embed=membername)
                break

client.run("NjY2Mjk3NzY1MjY1MTQ1ODk2.XhyILQ.-00gC3Xm1xHycISOQLd0VmpKcKc")