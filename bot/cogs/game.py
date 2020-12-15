from data.genshin.models import Character, Food
from data.monabot.models import GameCharacter, GameProfile
from data.db import session_scope
from bot.utils.users import mention_by_id
from discord.ext import commands
from datetime import datetime, timedelta
from  sqlalchemy.sql.expression import func
import discord
import random
import asyncio

class Game(commands.Cog, name='DiscordFun'):

    EXP_MULTIPLIER = 100
    HP_MULTIPLIER = 1500
    STAMINA_INCREMENT = 20
    REGEN_RATE = 3600  # Seconds
    STAMINA_REGEN = 7
    HEALTH_REGEN = 50
    MAX_DMG_MULTIPLIER = 750
    CRIT_CHANCE = 18
    TRIP_CHANCE = 5
    TRIP_DAMAGE = 25
    RESPAWN_TIME = 3  # Hours
    PRIMO_CLAIM_RATE = 24  # Hours
    PRIMO_CLAIM_VALUE = 300
    PRIMO_BONUS_CHANCE = 10
    PRIMO_BONUS_MULTIPLIER = 10
    STEAL_CHANCE = 20
    STEAL_CAUGHT_CHANCE = 5
    MAX_HEAL_CHANCE = 35
    HEAL_MULTIPLIER = 750
    WEATHER_MULTIPLIER = 1.5
    WEATHER_SPECIAL_CHANCE = 20
    WEATHER_CHANGE_RATE = 14400  # Seconds
    WEATHER = {
        'Pyro': 'Scorching day, not a single cloud in the sky! Pyro characters enjoy a boost!',
        'Cryo': 'It is freezing today! Cryo characters enjoy a boost!',
        'Geo': 'There seems to be occasional tremors today! Geo characters enjoy a boost!',
        'Hydro': 'Heavy rain! Hydro characters enjoy a boost!',
        'Anemo': 'It seems the winds are strong today! Anemo characters enjoy a boost!',
        'Electro': 'Careful! Looks like there is a dry thunderstorm today! Electro characters enjoy a boost!',
        'Normal': 'Nothing out of the ordinary today'
    }

    def __init__(self, bot):
        self.bot = bot
        self.todays_weather = 'Normal'
        self._enable_weather = True

    @commands.Cog.listener()
    async def on_ready(self):
        print('Warming up Game Server...')
        self.bot.loop.create_task(self.weather_engine())

    async def weather_engine(self):
        print('Starting the Weather Engine!')
        while self._enable_weather:
            n = random.randint(0, 100)
            if n <= self.WEATHER_SPECIAL_CHANCE:
                #Special weather
                weathers = ['Pyro', 'Cryo', 'Geo', 'Hydro', 'Anemo','Electro']
                w = random.randint(0, len(weathers)-1)
                self._todays_weather = weathers[w]
            else:
                self._todays_weather = 'Normal'
            await asyncio.sleep(self.WEATHER_CHANGE_RATE)  # wait 6 hours

    @commands.command()
    async def startadventure(self, ctx, character:str=''):
        """Start your discord genshin minigame adventure!"""
        with session_scope() as s:
            user = s.query(GameProfile).filter_by(discord_id=ctx.author.id).first()
            if user:
                await ctx.send(f"You've already started your adventure\nType m!help DiscordFun for game commands")
                return
            else:
                if not character:
                    await ctx.send(f"{mention_by_id(ctx.author.id)} you are about to embark on your discord adventure!\nChoose a starting character from tevyat\nType m!startadventure <character name>")
                    return
                name = character.capitalize()
                char = s.query(Character).filter_by(name=name).first()
                if not char:
                    await ctx.send(f'"{name}" is not a know Tevyat character\nTry again with m!startadventure')
                    return
                user = GameProfile(
                    discord_id=ctx.author.id,
                    primogems=8000,
                    stamina=80,
                    max_stamina=80,
                    last_check=datetime.utcnow(),
                    last_claim=None,
                    health=1500,
                    max_health=1500,
                    level=1,
                    exp=0,
                    max_exp=100,
                    deathtime=None,
                    pity=0
                )
                gamechar = GameCharacter(
                    active=True,
                    constellation=1
                )
                gamechar.character=char
                user.characters.append(gamechar)
                s.add(user)
        
        await self.send_user_profile(ctx)

    @commands.command()
    async def profile(self, ctx, member: discord.Member=None):
        """Check player profile"""
        if not member:
            member = ctx.author

        check = await self.check_member_is_mona(ctx, member)
        if check:
            return

        with session_scope() as s:
            user = s.query(GameProfile).filter_by(discord_id=member.id).first()
            if not user:
                await self.no_profile(ctx, member)
                return
            await self.send_user_profile(ctx, member)

    @commands.command()
    async def checkweather(self, ctx):
        """Check current game weather"""
        embed=discord.Embed(title='Weather Report')
        flair = self.bot.get_cog("Flair")
        desc = ''
        if self._todays_weather != 'Normal':
            desc += f'{flair.get_emoji(self._todays_weather)} '
        desc += self.WEATHER[self._todays_weather]

        embed.description = desc
        embed.color = flair.get_element_color(self._todays_weather)
        await ctx.send(embed=embed)

    @commands.command()
    async def wish(self, ctx, n:int=1):
        """Make a wish!"""

        if n < 1:
            await ctx.send('Invalid wish')
        cost = n*160
        msg=''

        with session_scope() as s:
            user = s.query(GameProfile).filter_by(discord_id=ctx.author.id).first()
            if not user:
                await self.no_profile(ctx)
                return
            flair = self.bot.get_cog("Flair")
            if user.primogems < cost:
                await ctx.send(f'You do not have enough primogems. Current {flair.get_emoji("Primogem")} {user.primogems}')
                return

            char_n = 0
            food_n = 0
            for i in range(n):
                roll = random.randint(0, 100)
                if user.pity==10 or roll >= 92:
                    user.pity=0
                    char_n +=1
                else:
                    food_n +=1
                    user.pity+=1
            if char_n:
                msg += '\nCharacters Wished:'
                lvl_ups = {}
                for i in range(char_n):
                    new_char = s.query(Character).order_by(func.random()).limit(1).first()
                    game_char = s.query(GameCharacter).filter_by(profile_id=user.id, character_id=new_char.id).first()
                    if game_char:
                        game_char.constellation += 1
                        if game_char.character.name in lvl_ups.keys():
                            lvl_ups[new_char.name] += 1
                        else:
                            lvl_ups[new_char.name] = 1
                    else:
                        game_char = GameCharacter(
                            active=False,
                            constellation=1
                        )
                        game_char.character=new_char
                        user.characters.append(game_char)
                        msg += f'\n{flair.get_emoji(new_char.name)} {new_char.name} joins your party!'
                for k, i in lvl_ups.items():
                    msg += f'\n\u2022 {flair.get_emoji(k)} {k} constellation up-ed! x{i}'

            if food_n:
                msg += '\n\nFoods Wished:'
                food_drops = {}
                for i in range(food_n):
                    f = s.query(Food).order_by(func.random()).limit(1).first()
                    if f.name in food_drops.keys():
                        food_drops[f.name] += 1
                    else:
                        food_drops[f.name] = 1
                for k, i in food_drops.items():
                    msg += f'\n\u2022 {k} x{i}'
                msg += '\n\nUnfortunately... Sara stepped in a puddle of water and the food went to waste!'
            
            user.primogems -= cost

            msg+= f'\n\n{flair.get_emoji("Primogem")} Remaining: {user.primogems}'
    
        embed = discord.Embed(title=f"{ctx.author.display_name} wished... ",
        description = msg.strip(),
        color = discord.Colour.purple())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def attack(self, ctx, target: discord.Member):
        """Attack a player! Stamina Cost: 15"""
        cost = 15
        if ctx.guild:
            server_region = ctx.guild.region.name
        else:
            server_region = 'GMT'

        check = await self.check_member_is_mona(ctx, target)
        if check:
            return
        
        with session_scope() as s:
            user = s.query(GameProfile).filter_by(discord_id=ctx.author.id).first()
            target_user = s.query(GameProfile).filter_by(discord_id=target.id).first()
            if not user:
                await self.no_profile(ctx)
                return
            if not target_user:
                await ctx.send(f'{target.display_name.title()} does not seem to have started their adventure')
                return
            user = self.check_user_status(user)
            target_user = self.check_user_status(target_user)
            if user.deathtime:
                await ctx.send(f'You are currently respawning!')
                return
            if target_user.deathtime:
                await ctx.send(f'{target.display_name} is currently still respawning!')
                return
            if user.stamina < cost:
                await ctx.send(f'Sorry you do not have enough stamina. Go take a nap and come back later')
                return
            user.stamina -= cost
            # Calculate Damage
            crit = random.randint(0, 100)
            dmg = int(random.randint(50*user.level,user.level*self.MAX_DMG_MULTIPLIER)*self.bonus_rate(user))
            msg = ''
            # Unfortunate chance
            if crit <=self.TRIP_CHANCE:
                # Rex Lapis chance
                if (user.level-target_user.level) > 3:
                    user.health = 0
                    msg += 'Morax did not take kindly to you picking on the weak. You have been struck by earth from above!'
                # Trip chance
                else:
                    self_dmg = user.level*self.TRIP_DAMAGE
                    user.health -= self_dmg
                    msg += f'Oops! {ctx.author.display_name} tripped on a Cor Lapis and took {user.level*self.TRIP_DAMAGE} damage'
                user = self.check_death(user)
                if not user.health:
                    respawn_time = self.get_respawn_time(ctx, user)
                    msg += f'\n{user.display_name} died. Respawning at {respawn_time}'
                msg += f'\n{target.display_name} laughed and got away unscathed'
                await ctx.send(msg.strip())
                return
            
            msg = ''
            if crit <= self.CRIT_CHANCE:
                dmg = dmg*2
                msg += '\nA Critical Hit!'
            if (target_user.level-user.level) > 3:
                dmg = dmg*(user.level+1)
                msg += '\nYou seem to have found his weak point! Insane Damage!'
            target_user.health -= dmg
            msg += f'\n{ctx.author.display_name} dealt {dmg} damage to {target.display_name}!'
            target_user = self.check_death(target_user)
            if not target_user.health:
                exp_gain = 50*target_user.level
                user.exp += exp_gain
                respawn_time = self.get_respawn_time(ctx, target_user)
                msg += f'\n{ctx.author.display_name} defeated {target.display_name} and gained {exp_gain} exp!\n{target.display_name} will respawn at {respawn_time}'
                if user.exp >= user.max_exp:
                    msg += f'\n{ctx.author.display_name} Leveled up!'
            user = self.check_user_status(user)
            await ctx.send(msg.strip())

    @commands.command()
    async def claimdaily(self, ctx):
        """Claim daily primogems"""
        now = datetime.utcnow()

        with session_scope() as s:
            user = s.query(GameProfile).filter_by(discord_id=ctx.author.id).first()
            if not user:
                await self.no_profile(ctx)
                return
            if not user.last_claim or user.last_claim+timedelta(hours=self.PRIMO_CLAIM_RATE) < now:
                msg = ''
                luck = random.randint(0, 100)
                primo = self.PRIMO_CLAIM_VALUE
                if luck <= self.PRIMO_BONUS_CHANCE:
                    primo=primo*self.PRIMO_BONUS_MULTIPLIER
                    msg += "It's your lucky day! You found a precious chest!"
                user.primogems += primo
                user.last_claim = now
                msg += f'\nYou have claimed {primo} primogems!'
                await ctx.send(msg.strip())
            else:
                await ctx.send(f"Don't be greedy! Only one claim every {self.PRIMO_CLAIM_RATE} hours")
                return

    @commands.command()
    async def mug(self, ctx, target:discord.Member):
        """Attempt to steal primogems from another player. Stamina Cost: 15"""
        cost = 15
        flair = self.bot.get_cog("Flair")

        check = await self.check_member_is_mona(ctx, target)
        if check:
            return

        with session_scope() as s:
            user = s.query(GameProfile).filter_by(discord_id=ctx.author.id).first()
            target_user = s.query(GameProfile).filter_by(discord_id=target.id).first()
            if not user:
                await self.no_profile(ctx)
                return
            if not target_user:
                await ctx.send(f'{target.display_name.title()} does not seem to have started their adventure')
                return
            user = self.check_user_status(user)
            if user.deathtime:
                await ctx.send(f'You are currently respawning!')
                return
            if user.stamina < cost:
                await ctx.send(f'Sorry you do not have enough stamina. Go take a nap and come back later')
                return
            user.stamina -= cost
            # Calculate steal chance
            chance = random.randint(0, 100)
            if chance <= self.STEAL_CAUGHT_CHANCE:
                await ctx.send(f'{ctx.author.display_name} was caught stealing by Morax.\
                \nAs punishment for breaking moral contract, {ctx.author.display_name} gave {target.display_name} all his primogems.\
                \n{target.display_name} recieved {flair.get_emoji("Primogem")} {user.primogems}')
                target_user.primogems = user.primogems
                user.primogems = 0
                return
            if chance <= self.STEAL_CHANCE*self.bonus_rate(user):
                steal_amount = random.randint(500, 1000)
                if target_user.primogems > steal_amount:
                    target_user.primogems -= steal_amount
                    user.primogems += steal_amount
                    stole = f'{flair.get_emoji("Primogem")} {steal_amount}'
                else:
                    stole = f'{flair.get_emoji("Primogem")} {target_user.primogems}'
                    user.primogems += target_user.primogems
                    target_user.primogems = 0
                await ctx.send(f'{ctx.author.display_name} stole {stole} from {target.display_name}!')
                return
        
        await ctx.send(f'{ctx.author.display_name} failed to steal from {target.display_name}')
                
    @commands.command()
    async def primolvlup(self, ctx):
        """Spend 3000 primogems for an instant lvlup"""
        cost = 3000
        flair = self.bot.get_cog("Flair")
        with session_scope() as s:
            user = s.query(GameProfile).filter_by(discord_id=ctx.author.id).first()
            if not user:
                await self.no_profile(ctx)
                return
            user = self.check_user_status(user)
            if user.deathtime:
                await ctx.send(f'You are currently respawning!')
                return
            if user.primogems < cost:
                await ctx.send(f'You do not have enough primogems. {flair.get_emoji("Primogem")} {cost} needed for instant lvlup')
                return
            user.primogems -= cost
            user.exp = user.max_exp
            user = self.check_user_status(user)
            await ctx.send(f'{ctx.author.display_name} spent {flair.get_emoji("Primogem")} {cost} and leveled up!')
            return

    @commands.command()
    async def heal(self, ctx):
        """Heal yourself. Stamina Cost: 10"""
        cost = 10
        with session_scope() as s:
            user = s.query(GameProfile).filter_by(discord_id=ctx.author.id).first()
            if not user:
                await self.no_profile(ctx)
                return
            user = self.check_user_status(user)
            if user.deathtime:
                await ctx.send(f'You are currently respawning!')
                return
            if user.stamina < cost:
                await ctx.send(f'Sorry you do not have enough stamina. Go take a nap and come back later')
                return
            if user.health == user.max_health:
                await ctx.send('Your health is already full!')
                return
            user.stamina -= cost
            chance = random.randint(0, 100)
            if chance <= self.MAX_HEAL_CHANCE*self.bonus_rate(user):
                user.health = user.max_health
                await ctx.send(f'{ctx.author.display_name} were blessed by Barbatos! Healed to full!')
                return
            heal = random.randint(10, user.level*self.HEAL_MULTIPLIER)
            user.health += heal
            if user.health > user.max_health:
                user.health=user.max_health
            await ctx.send(f'{ctx.author.display_name} healed for {heal}!')

    @commands.command()
    async def switchactive(self, ctx, name:str):
        """Switch active character"""
        flair = self.bot.get_cog("Flair")
        name = name.title()
        with session_scope() as s:
            user = s.query(GameProfile).filter_by(discord_id=ctx.author.id).first()
            if not user:
                await self.no_profile(ctx)
                return
            current_active = s.query(GameCharacter).filter_by(active=True, profile_id=user.id).first()
            if current_active.character.name == name:
                await ctx.send(f'{flair.get_emoji(name)} {name} is already your active character!')
                return
            char = s.query(Character).filter_by(name=name).first()
            if not char:
                await ctx.send(f'{name} is not a known character in Tevyat')
                return
            new_active = s.query(GameCharacter).filter_by(character_id=char.id, profile_id=user.id).first()
            if not new_active:
                await ctx.send(f'{name} is not in your party')
                return
            new_active.active = True
            current_active.active = False
            await ctx.send(f'{flair.get_emoji(name)} {name} is now your active character!')

    @commands.command()
    async def explore(self, ctx):
        """You never know what you might find. Stamina Cost: 10"""
        if ctx.guild:
            server_region = ctx.guild.region.name
        else:
            server_region = 'GMT'

        cost = 10
        with session_scope() as s:
            user = s.query(GameProfile).filter_by(discord_id=ctx.author.id).first()
            if not user:
                await self.no_profile(ctx)
                return
            user = self.check_user_status(user)
            if user.deathtime:
                await ctx.send(f'You are currently respawning!')
                return
            if user.stamina < cost:
                await ctx.send(f'Sorry you do not have enough stamina. Go take a nap and come back later')
                return
            user.stamina -= cost
            flair = self.bot.get_cog("Flair")
            random_event = random.randint(1, 1000)
            # Trigger random event
            if random_event == 999:
                random_char = s.query(GameCharacter).filter_by(profile_id=user.id).order_by(func.random()).first()
                random_char.constellation += 1
                await ctx.send(f'While exploring Stormterror {ctx.author.display_name} stumbled upon a strange meteor.\n{flair.get_emoji(random_char.character.name)} {random_char.character.name} touched the rock and was imbued with mysterious energy. {random_char.character.name} constellation up-ed!')
                return
            elif random_event >= 989:
                user.stamina == 0
                await ctx.send(f'{ctx.author.display_name} did not pay attention while collecting crabs at Yangguang Shoal.\n {ctx.author.display_name} was frozen by an Ice Slime and lost all stamina')
                return
            elif random_event >= 979:
                user.primogems += 1000
                await ctx.send(f'Wow, {ctx.author.display_name} found a precious chest! {flair.get_emoji("Primogem")} 1000')
                return
            elif random_event >= 969:
                if user.primogems < 500:
                    stolen = user.primogems
                else:
                    stolen = 500
                user.primogems -= stolen
                await ctx.send(f'{ctx.author.display_name} was investigation Dunyu Ruins when an invisible Fatui agent snuck up and snatched his purse!\nLost {flair.get_emoji("Primogem")} {stolen}!')
                return
            elif random_event >= 959:
                dmg = user.level*750
                user.health -= dmg
                user = self.check_death(user)
                msg = f'{ctx.author.display_name} stepped on a buried bomb. Kaboom! {ctx.author.display_name} took {dmg} damage'
                if user.deathtime:
                    respawn_time = self.get_respawn_time(ctx, user)
                    msg += f'\n{ctx.author.display_name} perished. Respawning at {respawn_time}'
                await ctx.send(msg)
                return
            elif random_event >= 759:
                random_exp = random.randint(1, 50)
                user.exp += random_exp
                user = self.check_user_status(user)
                await ctx.send(f'{ctx.author.display_name} found some hilichurls and took them out. Gained {random_exp} exp')
                return
            elif random_event >= 559:
                random_gems = random.randint(50, 100)
                user.primogems += random_gems
                await ctx.send(f'{ctx.author.display_name} stumbled on a buried common chest. {flair.get_emoji("Primogem")} {random_gems}')
                return
            elif random_event >= 549:
                user.health = user.max_health
                await ctx.send(f'{ctx.author.display_name} passed a Statue of the Seven. Fully healed!')
                return
            elif random_event >= 539:
                dmg = int(user.health/2)+1
                await ctx.send(f'{ctx.author.display_name} slipped and fell while climbing Mount Hulao\n{ctx.author.display_name} took {dmg} damage!')
                return
            elif random_event >= 529:
                stamina_increase = user.level*5
                user.stamina += stamina_increase
                if user.stamina > user.max_stamina:
                    user.stamina = user.max_stamina
                await ctx.send(f'{ctx.author.display_name} found a relaxing spot and took a nap. Regained {stamina_increase} stamina')
                return
            else:
                await ctx.send(f'{ctx.author.display_name} did not find anything particularly interesting')
                return

    async def no_profile(self, ctx, member=None):
        if member is None:
            await ctx.send(f'You have not started your discord adventure\nRun m!startadventure to start your game')
        else:
            await ctx.send(f'{member.display_name} has not started their discord adventure')

    async def send_user_profile(self, ctx, member=None):
        if ctx.guild:
            server_region = ctx.guild.region.name
        else:
            server_region = 'GMT'

        with session_scope() as s:
            if not member:
                member = ctx.author
            user = s.query(GameProfile).filter_by(discord_id=member.id).first()
            if not user:
                await self.no_profile(ctx, member)
                return
            user = self.check_user_status(user)
            desc = f"\nLevel: {user.level}"
            desc += f"\nHealth: {user.health}/{user.max_health}"
            desc += f"\nStamina: {user.stamina}/{user.max_stamina}"
            desc += f"\nExp: {user.exp}/{user.max_exp}"
            if user.deathtime:
                respawn = self.get_respawn_time(ctx, user)
                desc+= f"\nRespawn Time: {respawn}"
            active_char = s.query(GameCharacter).filter_by(profile_id=user.id,active=True).first()
            bench_char = s.query(GameCharacter).filter_by(profile_id=user.id,active=False).all()
            flair = self.bot.get_cog("Flair")
            embed = discord.Embed(title=f"{member.display_name.title()}'s profile",
            description=desc,
            color=flair.get_element_color(active_char.character.element)
            )
            embed.add_field(name=f'{flair.get_emoji("Primogem")} Primogems', value=user.primogems)
            embed.add_field(name='Active Character', value=f'{flair.get_emoji(active_char.character.name)} {active_char.character.name} C{active_char.constellation}')
            embed.add_field(name='\u200b', value='\u200b')
            if bench_char:
                bench1 = ''
                bench2 = ''
                bench3 = ''
                i = 1
                for c in bench_char:
                    if i ==1:
                        bench1 += f'\n{flair.get_emoji(c.character.name)} {c.character.name} C{c.constellation}'
                    if i ==2:
                        bench2 += f'\n{flair.get_emoji(c.character.name)} {c.character.name} C{c.constellation}'
                    if i ==3:
                        bench3 += f'\n{flair.get_emoji(c.character.name)} {c.character.name} C{c.constellation}'
                    i = i%3+1
                embed.add_field(name='Bench Characters', value=bench1.strip(), inline=True)
                embed.add_field(name='\u200b', value=bench2.strip(), inline=True)
                embed.add_field(name='\u200b', value=bench3.strip(), inline=True)
            embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    def convert_from_utc(self, time, server_region):
        reminder_cog = self.bot.get_cog('Reminders')
        return reminder_cog.convert_from_utc(time, server_region)

    def check_user_status(self, user):
        now = datetime.utcnow()
        # check if dead
        user = self.check_death(user)
        if user.deathtime:
            return user
        # check stamina
        if user.last_check+timedelta(seconds=self.REGEN_RATE) <= now:
            stamina_gain = int(((now-user.last_check).seconds/self.REGEN_RATE*self.STAMINA_REGEN)+user.level)
            user.stamina += stamina_gain
            health_gain = int((now-user.last_check).seconds/self.REGEN_RATE*self.HEALTH_REGEN*user.level)
            user.health += health_gain
            if user.stamina >= user.max_stamina:
                user.stamina = user.max_stamina
            if user.health >= user.max_health:
                user.health = user.max_health
            user.last_check=now
        # check level up
        while user.exp >= user.max_exp:
            user.level += 1
            user.exp = user.exp-user.max_exp
            user.max_exp=user.level*self.EXP_MULTIPLIER
            user.max_health=user.level*self.HP_MULTIPLIER
            user.max_stamina+= self.STAMINA_INCREMENT
            user.health=user.max_health
            user.deathtime=None
        return user

    def check_death(self, user):
        now = datetime.utcnow()
        if user.deathtime is not None and user.deathtime+timedelta(hours=self.RESPAWN_TIME) < now:
            user.health = user.max_health
            user.stamina = user.max_stamina
            user.deathtime = None
            return user
        if user.deathtime:
            return user
        if user.health <= 0:
            user.deathtime=datetime.utcnow()
            user.stamina = 0
            user.health = 0
            user.exp = int(user.exp/2)
        return user

    def get_respawn_time(self, ctx, user):
        if ctx.guild:
            server_region = ctx.guild.region.name
        else:
            server_region = 'GMT'
        if user.deathtime:
            respawn_time = user.deathtime + timedelta(hours=self.RESPAWN_TIME)
            return self.convert_from_utc(respawn_time, server_region).strftime("%I:%M %p, %d %b %Y")
        return ''

    def bonus_rate(self, user):
        element = 'Normal'
        constellation = 1
        for c in user.characters:
            if c.active:
                element=c.character.element
                constellation = c.constellation
                break
        constellation_bonus = (1-constellation)*0.3
        if element.lower() == self._todays_weather.lower():
            return self.WEATHER_MULTIPLIER+constellation_bonus
        else:
            return 1+constellation_bonus

    async def check_member_is_mona(self, ctx, member):
        if member == self.bot.user:
            await ctx.send('Do you think I have time for your silly games? Go bother someone else!')
            return True