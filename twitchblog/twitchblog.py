import aiohttp
import discord
from discord.ext import commands
try: 
    from bs4 import BeautifulSoup
    soupAvailable = True
except:
    soupAvailable = False


class Twitchblog:
    """Twitch cog!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context = True)
    async def twitch(self, ctx):
        """Returns various Twitch commands"""
        
        if ctx.invoked_subcommand is None:
            await self.bot.say("Type `[p]help Twitch` for info.")
            
    @twitch.command(name = 'top', pass_context = True)
    async def top(self, ctx):
        """The top stroy pinned to the top of the twitch blog page"""
        if ctx.message.server.me.bot:
            try:
                await self.bot.delete_message(ctx.message)
            except:
                await self.bot.send_message(ctx.message.author, 'Could not delete your message on ' + ctx.message.server.name)

        url = "https://blog.twitch.tv/" 

        async with aiohttp.get(url) as response:
            soupObject = BeautifulSoup(await response.text(), "html.parser")
        try:
            Ttltle = soupObject.find(class_='col u-xs-marginBottom10 u-paddingLeft9 u-paddingRight12 u-paddingTop0 u-sm-paddingTop20 u-paddingBottom25 u-size4of12 u-xs-size12of12 u-marginBottom30').find('h3').get_text()
            tlink = soupObject.find(class_='u-lineHeightBase postItem u-marginRight3').find('a')
            tre_t = tlink.get('href')
            tavi = soupObject.find(class_='postMetaInline-avatar u-flex0').find('a').find('img')
            tavi_r = tavi.get('src')
            tname = soupObject.find(class_='postMetaInline postMetaInline-authorLockup u-flex1 u-noWrapWithEllipsis').find('a').get_text()
            tdate = soupObject.find(class_='u-fontSize12 u-baseColor--textNormal u-textColorNormal js-postMetaInlineSupplemental').find('time').get_text()
            # img = soupObject.find(class_='u-lineHeightBase postItem u-marginRight3').find('a')
            # img_r = img.get('style')['url']
            rm = "[See More](https://blog.twitch.tv/)"
			#embed time
            data = discord.Embed(title=Ttltle, colour=0x6441A4)
            data.set_author(name= tname, icon_url=tavi_r)
            data.add_field(name='--------', value=tre_t)
            data.add_field(name='--------', value=tdate)
            data.add_field(name='--------', value=rm)
            await self.bot.say(embed=data)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission to send this OR error")
            
    @twitch.command(name = 'blog', pass_context = True)
    async def blog(self, ctx):
        """The most recent blog of twitch.tv"""
        if ctx.message.server.me.bot:
            try:
                await self.bot.delete_message(ctx.message)
            except:
                await self.bot.send_message(ctx.message.author, 'Could not delete your message on ' + ctx.message.server.name)

        url = "https://blog.twitch.tv/" 

        async with aiohttp.get(url) as response:
            soupObject = BeautifulSoup(await response.text(), "html.parser")

        try:
            title = soupObject.find(class_='u-lineHeightBase postItem').find('a').get_text()
            tlink = soupObject.find(class_='u-lineHeightBase postItem').find('a')
            therf = tlink.get('href')
            tdate = soupObject.find(class_='u-fontSize12 u-baseColor--textNormal u-textColorNormal js-postMetaInlineSupplemental').find('time').get_text()
            tavi = soupObject.find(class_='postMetaInline-avatar u-flex0').find('a').find('img')
            avi_r = tavi.get('src')
            tname = soupObject.find(class_='postMetaInline postMetaInline-authorLockup u-flex1 u-noWrapWithEllipsis').find('a').get_text()
            # timg = soupObject.find(class_='u-lineHeightBase postItem').find('a').find('img')
            # img_r = timg.get('url')
            rm = "[See More](https://blog.twitch.tv/)"
			#embed Starts here
            data = discord.Embed(title=title , colour=0x6441A4)
            data.set_author(name= tname, icon_url=avi_r)
            data.add_field(name='--------', value=therf)
            data.add_field(name="--------", value=rm)
            # sends everything in the data value
            await self.bot.say(embed=data)

        # if it doesn't work it will just say this
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission to send this OR error")

			

def setup(bot):
    if soupAvailable:
        bot.add_cog(Twitchblog(bot))
    else:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")
