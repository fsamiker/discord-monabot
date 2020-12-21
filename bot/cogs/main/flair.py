from discord.ext import commands
import discord

class Flair(commands.Cog):

    element_colors = {
        'Pyro': discord.Colour.red(),
        'Cryo': discord.Colour.greyple(),
        'Anemo': discord.Colour.teal(),
        'Hydro': discord.Colour.blue(),
        'Electro': discord.Colour.purple(),
        'Geo': discord.Colour.gold()
    }

    def __init__(self, bot):
        self.bot = bot
        self.emojis = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print('Retrieving Emojis')
        self.emojis['Mora'] = self.bot.get_emoji(786073743155396685)
        self.emojis['Resin'] = self.bot.get_emoji(786187951200665600)
        self.emojis['Primogem'] = self.bot.get_emoji(787307965027057684)
        self.emojis['Star'] = self.bot.get_emoji(786073815062937610)
        self.emojis['Hydro'] = self.bot.get_emoji(786073653879373895)
        self.emojis['Pyro'] = self.bot.get_emoji(786073580629655612)
        self.emojis['Geo'] = self.bot.get_emoji(786073540251222037)
        self.emojis['Electro'] = self.bot.get_emoji(787707576640733224)
        self.emojis['Cryo'] = self.bot.get_emoji(786073446730694696)
        self.emojis['Anemo'] = self.bot.get_emoji(786072181384937502)
        self.emojis['Tartaglia'] = self.bot.get_emoji(786074538835705857)
        self.emojis['Sucrose'] = self.bot.get_emoji(786074517285634060)
        self.emojis['Razor'] = self.bot.get_emoji(786074495018205185)
        self.emojis['Qiqi'] = self.bot.get_emoji(786074475513774101)
        self.emojis['Noelle'] = self.bot.get_emoji(786074457449037835)
        self.emojis['Ningguang'] = self.bot.get_emoji(786074437807112233)
        self.emojis['Mona'] = self.bot.get_emoji(786074417397760060)
        self.emojis['Lisa'] = self.bot.get_emoji(786074398360076308)
        self.emojis['Klee'] = self.bot.get_emoji(786074378223878148)
        self.emojis['Keqing'] = self.bot.get_emoji(786074358673047582)
        self.emojis['Kaeya'] = self.bot.get_emoji(786074339094953984)
        self.emojis['Jean'] = self.bot.get_emoji(786074319146188881)
        self.emojis['Fischl'] = self.bot.get_emoji(786074301132439612)
        self.emojis['Diona'] = self.bot.get_emoji(786074279984234497)
        self.emojis['Diluc'] = self.bot.get_emoji(786074237555179560)
        self.emojis['Chongyun'] = self.bot.get_emoji(786074207439159316)
        self.emojis['Bennett'] = self.bot.get_emoji(786074183007207434)
        self.emojis['Beidou'] = self.bot.get_emoji(786074158739619851)
        self.emojis['Barbara'] = self.bot.get_emoji(786074128502489099)
        self.emojis['Amber'] = self.bot.get_emoji(786074070650322986)
        self.emojis['Zhongli'] = self.bot.get_emoji(787664573565501470)
        self.emojis['Xingqiu'] = self.bot.get_emoji(787664923818852352)
        self.emojis['Xiangling'] = self.bot.get_emoji(787664876675268618)
        self.emojis['Venti'] = self.bot.get_emoji(787664848380493834)
        self.emojis['FS'] = self.bot.get_emoji(789122991036432415)
        self.emojis['AR'] = self.bot.get_emoji(789122934248701992)
        self.emojis['Reminder'] = self.bot.get_emoji(789438946366324737)

    def get_element_color(self, element):
        return self.element_colors.get(element, discord.Colour.dark_theme())
    
    def get_emoji(self, emoji_name):
        return self.emojis.get(emoji_name, '')