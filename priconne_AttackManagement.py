import discord
import datetime
import os

client = discord.Client()

token = os.environ['DISCORD_BOT_TOKEN']
channelid = os.environ['CHANNELID']

@client.event
async def on_ready():
    print('ログインしました。')

@client.event
async def on_message(message):
    # ".凸管理@数字"で起動
    if message.content.startswith(".凸管理"):

    channel = client.get_channel(message.channel_id)

        # チャンネル制御
        if channel == channelid:

            #global channel
            #channel = client.get_channel(channelid)

            # 最初の行の出力内容を加工
            daycount = int(message.content[5:len(message.content)])
            dt_now = datetime.datetime.now()
            ymd = dt_now.strftime('%Y年%m月%d日')
            text = "（{}日目）\n"
            whatday = text.format(daycount)
            todaymsg = '**__'+ ymd + whatday + '__**'

            reaction_member = [">>>"]

            msg = await message.channel.send(todaymsg)

            # メンバー取得
            user_count = sum(1 for member in message.guild.members if not member.bot)
            global memname
            memname = [member.name for member in message.guild.members if not member.bot]
            global membername
            membername = discord.Embed(color=0x00ff00)

            for i in range(user_count):
                a = i + 1
                b = str(a).zfill(2)
                membername.add_field(name=f'**{b} : {memname[i]}**', value="** **", inline=False)

            # 起動時処理回避フラグ
            global startupavoid
            startupavoid = 1

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

            # メンバー表示
            global members
            members = await message.channel.send(embed=membername)

            # 起動時処理回避フラグ解除
            startupavoid = 0

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
            if startupavoid != 1:
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
            if startupavoid != 1:
                membername.remove_field(indexnum)
                membername.insert_field_at(indexnum, name=f'**{printnum} : {memname[indexnum]}**', value="** **", inline=False)
                await members.edit(embed=membername)
                break

client.run(token)
