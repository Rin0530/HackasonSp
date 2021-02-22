import discord

# exitを使うため
import sys

# csvReader と csvWriter をインポート
import csvReader
import csvWriter


# Bot Commands Frameworkをインポート
from discord.ext import commands

bot = commands.Bot(command_prefix='-')
bot.remove_command('help')


# bot token
TOKEN = ''


reader = csvReader.csvReader()
writer = csvWriter.csvWriter()



@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

    # 起動時にメッセージの送信
    channel = bot.get_channel(799188941760233482)
    await channel.send('botを起動しました')
    


# テスト用
@bot.command(aliases=['te'])
async def test(ctx, *arg: str):
    if len(arg) <= 0:
        await ctx.send('コマンドが間違っています\n-test str')
    else:
        await ctx.send('```markdown\nok test\n```')
        await ctx.send(arg)
        await writer.ttp()


    

# 一応終了するコマンドも用意しておく
@bot.command()
async def exit(ctx):
    await ctx.send('終了します')
    sys.exit()



# 書き込み部分 csvWriter

# addFavorite コマンド
@bot.command(aliases=['adF'])
async def addFavorite(ctx, url: str, *tags):
    x = await writer.addFavorite(url, tags)
    await ctx.send(x)

# addFavorite error
@addFavorite.error
async def addFavorite_error(ctx, error):
    await ctx.send(error)
    await ctx.send('コマンドが間違っています\n-adF url tags')


# deleteFavorite コマンド
@bot.command(aliases=['delF'])
async def deleteFavorite(ctx, num: int):
    x = await writer.deleteFavorite(num)
    await ctx.send(x)

# deleteFavorite error
@deleteFavorite.error
async def deleteFavorite_error(ctx, error):
    await ctx.send(error)
    await ctx.send('コマンドが間違っています\n-delF num')


# addTag コマンド
@bot.command(aliases=['adT'])
async def addTag(ctx, num: int, tag: str):
    x = await writer.addTag(num, tag)
    await ctx.send(x)

# addTag error
@addTag.error
async def addTag_error(ctx, error):
    await ctx.send(error)
    await ctx.send('コマンドが間違っています\n-adT num tag')


# deleteTag コマンド
@bot.command(aliases=['delT'])
async def deleteTag(ctx, num: int, tag: str):
    x = await writer.deleteTag(num, tag)
    await ctx.send(x)

# deleteTag error
@deleteTag.error
async def deleteTag_error(ctx, error):
    await ctx.send(error)
    await ctx.send('コマンドが間違っています\n-delT num tag')


# clear コマンド 
@bot.command(aliases=['c'])
async def clear(ctx):
    x = await writer.clear()
    await ctx.send(x)

# clear error
@clear.error
async def clear_error(ctx, error):
    await ctx.send(error)
    await ctx.send('コマンドが間違っています\n-c')


# clearFavoriteTags コマンド 
@bot.command(aliases=['cFTs'])
async def clearFavoriteTags(ctx, num: int):
    x = await writer.clearFavoriteTags(num)
    await ctx.send(x)

# clearFavoriteTags error
@clearFavoriteTags.error
async def clearFavoriteTags_error(ctx, error):
    await ctx.send(error)
    await ctx.send('コマンドが間違っています\n-cFTs num')


# replaceTags コマンド
@bot.command(aliases=['repTs'])
async def replaceTags(ctx,num: int, delTag: str, newTag: str):
    x = await writer.replaceTags(num, delTag, newTag)
    await ctx.send(x)

# replaceTags error
@replaceTags.error
async def replaceTags_error(ctx, error):
    await ctx.send(error)
    await ctx.send('コマンドが間違っています\n-repTs num delTag newTag')


# show コマンド
#@bot.command()
#async def show(ctx):
#    await ctx.send('ok test')
#    x = await writer.show()
#    await ctx.send(x)

# show error
#@show.error
#async def show_error(ctx, error):
#    await ctx.send(error)
#    await ctx.send('コマンドが間違っています\n-show')


# 読み込み部分 csvReader

# readFavorite コマンド
@bot.command(aliases=['readF'])
async def readFavorite(ctx, num: int):
    x = await reader.readFavorite(num)
    await ctx.send(x)

# readFavorite error
@readFavorite.error
async def readFavorite_error(ctx, error):
    await ctx.send(error)
    await ctx.send('コマンドが間違っています\n-readF num')


# searchTag コマンド
@bot.command(aliases=['sT'])
async def searchTag(ctx, tag: str):
    x = await reader.searchTag(tag)
    await ctx.send(x)

# searchTag error
@searchTag.error
async def searchTag_error(ctx, error):
    await ctx.send(error)
    await ctx.send('コマンドが間違っています\n-sT tag')


# searchTags コマンド
@bot.command(aliases=['sTs'])
async def searchTags(ctx, *tags: str):
    if len(tags) <= 0:
        await ctx.send('コマンドが間違っています\n-sTs tags')
    else:
        await ctx.send(tags)
        x = await reader.searchTags(tags)
        await ctx.send(x)


# showFavList コマンド 
@bot.command(aliases=['showFL'])
async def showFavList(ctx):
    x = await reader.showFavList()
    await ctx.send(x)


# showFavList error
@showFavList.error
async def showFavList_error(ctx, error):
    await ctx.send(error)
    await ctx.send('コマンドが間違っています\n-showFL')


# showFavoriteAll コマンド 
@bot.command(aliases=['showFAll'])
async def showFavoriteAll(ctx, num: int):
    x = await reader.showFavAll(num)
    await ctx.send(x)


# showFavoriteAll error
@showFavoriteAll.error
async def showFavoriteAll_error(ctx, error):
    await ctx.send(error)
    await ctx.send('コマンドが間違っています\n-showFAll num')



# showAllTags コマンド
@bot.command(aliases=['showAllTs'])
async def showAllTags(ctx):
    x = await reader.showAllTag()
    await ctx.send(x)

# showAllTags error
@showAllTags.error
async def showAllTags_error(ctx, error):
    await ctx.send(error)
    await ctx.send('コマンドが間違っています\n-showAllTs')



# help コマンド
@bot.command(pass_context=True)
async def help(ctx):
    
    embed = discord.Embed(
        colour = discord.Color.orange()
    )

    embed.set_author(name='Help')
    embed.add_field(name='-readF num', value='指定した番号のブックマークを呼び出す。',inline=False)

    #embed.add_field(name='-show', value='全ての番号、ブックマーク、タグを表示する。',inline=False)
    embed.add_field(name='-sT tag', value='タグを一つ検索する。',inline=False)
    embed.add_field(name='-sTs tags', value='タグを複数検索する。',inline=False)
    embed.add_field(name='-showFL', value='全てのブックマークの番号とタイトルを表示する。',inline=False)
    embed.add_field(name='-showFAll num', value='指定した番号のブックマークの内容を全て表示させる。',inline=False)
    embed.add_field(name='-showAllTs', value='現存する全てのタグを表示する。',inline=False)

    embed.add_field(name='-adF url tags', value='URLと関連付けるタグを用いてブックマークを追加する。',inline=False)
    embed.add_field(name='-delF num', value='指定した番号のブックマークを削除する。',inline=False)
    embed.add_field(name='-adT num tag', value='指定した番号にタグを追加する。',inline=False)
    embed.add_field(name='-delT num tag', value='指定した番号のタグを削除する。',inline=False)
    embed.add_field(name='-c', value='保存したブックマークを全て削除する。',inline=False)
    embed.add_field(name='-cFTs num', value='指定した番号のブックマークに関連付けられているタグを削除する。',inline=False)
    embed.add_field(name='-repTs num delTag newTag', value='指定した番号のブックマークに関連付けられているタグを変更する。',inline=False)
    
    

    await ctx.send(embed=embed)






# Botの起動とDiscordサーバーへの接続
bot.run(TOKEN)