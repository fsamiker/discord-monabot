from discord.ext import commands
import discord

class Core(commands.Cog):
    def __init__(self, bot, image_processor):
        self.bot = bot
        self.im_p = image_processor

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')
        await self.bot.change_presence(activity=discord.Game(name="Genshin Impact"))

        print(f'Pre-Generating Images...')
        info_cog = self.bot.get_cog('Info')
        for _, c in info_cog.characters.items():
            info_cog.generate_basic_info(c)
        print(f'Image Generation Complete')


    