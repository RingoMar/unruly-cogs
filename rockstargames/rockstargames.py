import aiohttp
import discord
from discord.ext import commands

try: 
    from bs4 import BeautifulSoup
    soupAvailable = True
except:
    soupAvailable = False


class Rockstargames:
    """The Rockstargames cog that finds information from websites"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context = True)
    async def r(self, ctx):
        """Returns various rockstar commands"""
        
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @r.command(name = 'events', pass_context = True)
    async def events(self, ctx):
        """The Current GTA Online Bonuses live now"""
        # This will remove the commmand when you call it
        if ctx.message.server.me.bot:
            try:
                await self.bot.delete_message(ctx.message)
            except:
                await self.bot.send_message(ctx.message.author, 'Could not delete your message on ' + ctx.message.server.name)

        url = "https://socialclub.rockstargames.com/" 
        # Beautiful Soup getting the website(url) and web scraping found with soupObject.find 
        async with aiohttp.get(url) as response:
            soupObject = BeautifulSoup(await response.text(), "html.parser")

        try:    
            # Stuff to just make  it look cool
            avi = "https://i.imgur.com/s5O1yD2.png"
            img = "https://i.imgur.com/0Gu4sSK.png"
            rm = "[Read More](https://socialclub.rockstargames.com/events)"
            # Soup FInd  text and image
            bonus1 = soupObject.find(class_='bonuses').find('ul').get_text()
            evpic = soupObject.find(class_='eventThumb').find('img').get('data-src') #Checking the website, Rockstar doesn't use the src tag in their images 
                                                                                     #because it is handled by some internal JS
                                                                                     #So to fix, you would need to change .get('src') to a .get('data-src')
            # EMBED
            # colour is any hex value with "0x" in front of it
            data = discord.Embed(title='GTA Online Bonuses', description='The Current GTA Online Bonuses', colour=0xE4BA22)
            data.set_author(name='Rockstar Games', icon_url=avi)
            data.add_field(name="This week: \n", value=bonus1)
            data.add_field(name="--------", value=rm)
            data.set_image(url=evpic)
            data.set_thumbnail(url=img)
            # sends everything in the data value
            await self.bot.say(embed=data)

        # if it doesn't work it will just say this:
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission to send this OR error")


    @r.command(name = 'newswire', pass_context = True)
    async def newswire(self, ctx):
        """Latest rockstar newswire"""

        if ctx.message.server.me.bot:
            try:
                await self.bot.delete_message(ctx.message)
            except:
                await self.bot.send_message(ctx.message.author, 'Could not delete your message on ' + ctx.message.server.name)

        url = "https://socialclub.rockstargames.com/" 

        async with aiohttp.get(url) as response:
	        soupObject = BeautifulSoup(await response.text(), "html.parser")

        try:
            # Soup Find
            Tittle = soupObject.find(class_='articleContainer').find('h3').find('a').get_text()
            news = soupObject.find(class_='articleContainer').find('h3').find('a')
            img = soupObject.find(class_='articlePictureContainer').find('a').find('img').get('data-src')
            link =  ' https://socialclub.rockstargames.com' + news.get('href')
            # Other stuff
            avi = "https://i.imgur.com/s5O1yD2.png"
            rm = "[See More](https://socialclub.rockstargames.com/news)"
            # Embed
            data = discord.Embed(title=Tittle, description='---------', colour=0xE4BA22)
            data.set_author(name='R* L' , icon_url=avi)
            data.add_field(name= 'Read More:', value=link)
            data.set_image(url=img)
            await self.bot.say(embed=data)


        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission to send this OR error")

    @r.command(name = 'players', pass_context = True)
    async def players(self, ctx):
        """Amount of players on steam"""

        url = "https://steamdb.info/app/271590/graphs/" 

        async with aiohttp.get(url) as response:
	        soupObject = BeautifulSoup(await response.text(), "html.parser")

        try:
            # Find the number
            online = soupObject.find(class_='span6').find('li').find('strong').get_text()
            await self.bot.say(online + ' players are playing this game at the moment')
        except:
            await self.bot.say("Couldn't load amount of players. No one is playing this game anymore or there's an error.")

    @r.command(name = 'servers', pass_context = True)
    async def servers(self, ctx):
        """Grand Theft Auto sever status"""
       
        try:
            img = "https://i.imgur.com/rnZwn44.png"
            arw = "\U0001f199"
            avi = "https://i.imgur.com/s5O1yD2.png"
            link = "[See More!](https://support.rockstargames.com/hc/articles/200426246)"
            #EMBED
            data = discord.Embed(title='GTA Online Server Status -- Latest Updates', description='Stay tuned for the latest GTA Online server status updates.', colour=0xE4BA22)
            data.set_author(name='Rockstar Games', icon_url=avi)
            data.add_field(name='**Ps3** \u2014', value=arw)
            data.add_field(name='**Ps4** \u2014', value=arw)
            data.add_field(name='**Xbox One** \u2014', value=arw)
            data.add_field(name='**Xbox 360** \u2014', value=arw)
            data.add_field(name='**PC** \u2014', value=arw)
            data.add_field(name='**Social Club** \u2014', value=arw)
            data.add_field(name='--------' , value=link)
            data.set_thumbnail(url=img)
            await self.bot.say(embed=data)
            # If it doesn't work
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission to send this OR error")

    
def setup(bot):
    if soupAvailable:
        bot.add_cog(Rockstargames(bot))
    else:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")
