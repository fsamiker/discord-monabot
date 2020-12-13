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
    REGEN_RATE = 60  # Seconds
    STAMINA_REGEN = 7
    HEALTH_REGEN = 10
    MAX_DMG_MULTIPLIER = 750
    CRIT_CHANCE = 20
    TRIP_CHANCE = 5
    TRIP_DAMAGE = 25
    RESPAWN_TIME = 1  # Hours
    PRIMO_CLAIM_RATE = 24  # Hours
    PRIMO_CLAIM_VALUE = 300
    PRIMO_BONUS_CHANCE = 10
    PRIMO_BONUS_MULTIPLIER = 10
    STEAL_CHANCE = 20
    STEAL_CAUGHT_CHANCE = 5
    MAX_HEAL_CHANCE = 35
    HEAL_MULTIPLIER = 750
    WEAHTER_MULTIPLIER = 1.5
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
            if n <= 20:
                #Special weather
                weathers = ['Pyro', 'Cryo', 'Geo', 'Hydro', 'Anemo','Electro']
                w = random.randint(0, len(weathers)-1)
                self._todays_weather = weathers[w]
            else:
                self._todays_weather = 'Normal'
            await asyncio.sleep(21600)  # wait 6 hours

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

        with session_scope() as s:
            user = s.query(GameProfile).filter_by(discord_id=member.id).first()
            if not user:
                await self.no_profile(ctx, member)
                return
            await self.send_user_profile(ctx, member)

    @commands.command()
    async def weatherreport(self, ctx):
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
                if user.pity==10 or roll >= 95:
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
        """Attack a player! Stamina Cost: 20"""
        cost = 20
        if ctx.guild:
            server_region = ctx.guild.region.name
        else:
            server_region = 'GMT'
        
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
            if user.stamina < cost:
                await ctx.send(f'Sorry you do not have enough stamina. Go take a nap and come back later')
                return
            user.stamina -= cost
            # Calculate Damage
            crit = random.randint(0, 100)
            dmg = int(random.randint(10,user.level*self.MAX_DMG_MULTIPLIER)*self.bonus_rate(user))
            # Trip chance
            if crit <=self.TRIP_CHANCE:
                self_dmg = user.level*self.TRIP_DAMAGE
                user.health -= self_dmg
                msg = f'Oops! {ctx.author.display_name} tripped on a Cor Lapis and took {user.level*self.TRIP_DAMAGE} damage'
                user = self.check_death(user)
                if not user.health:
                    respawn_time = self.convert_from_utc(user.deathtime, server_region).strftime("%I:%M %p, %d %b %Y")
                    msg += f'\n{user.display_name} died. Respawning at {respawn_time}'
                msg += f'\n{target.display_name} laughed and got away unscathed'
                await ctx.send(msg.strip())
                return
            
            msg = ''
            if crit <= self.CRIT_CHANCE:
                dmg = user.level*self.MAX_DMG_MULTIPLIER*2
                msg += 'A Critical Hit!\n'
            target_user.health -= dmg
            msg += f'\n{ctx.author.display_name} dealt {dmg} damage to {target.display_name}!'
            target_user = self.check_death(target_user)
            if not target_user.health:
                user.exp += 100
                respawn_time = self.convert_from_utc(target.deathtime, server_region).strftime("%I:%M %p, %d %b %Y")
                msg += f'\n{ctx.author.display_name} defeated {target.display_name} and gained 100 exp!\n{target.display_name} will respawn at {respawn_time}'
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
        """Attempt to steal primogems from another player. Stamina Cost: 20"""
        cost = 20
        flair = self.bot.get_cog("Flair")

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
            if user.stamina < cost:
                await ctx.send(f'Sorry you do not have enough stamina. Go take a nap and come back later')
                return
            user.stamina -= cost
            # Calculate steal chance
            chance = random.randint(0, 100)
            if chance <= self.STEAL_CAUGHT_CHANCE:
                random_char = s.query(GameCharacter).filter_by(profile_id=user.id,active=False).order_by(func.random()).limit(1).all()
                if random_char:
                    c = random_char[0].character
                    await ctx.send(f"{ctx.author.display_name}'s {c.name} was caught while attempting to steal from {target.display_name}\n{flair.get_emoji(c.name)} {c.name} was lost from party...")
                    s.delete(random_char[0])
                    return
            if chance <= self.STEAL_CHANCE*self.bonus_rate(user):
                steal_amount = random.randint(500, 1000)
                if target_user.primogems > steal_amount:
                    target_user.primogems -= steal_amount
                    user.primogems += steal_amount
                    stole = f'{flair.get_emoji("Primogem")} 1000'
                else:
                    stole = f'{flair.get_emoji("Primogem")} {target_user.primogems}'
                    user.primogems += target_user.primogems
                    target_user.primogems = 0
                await ctx.send(f'{ctx.author.display_name} stole {stole} from {target.display_name}!')
                return
        
        await ctx.send(f'{ctx.author.display_name} failed to steal from {target.display_name}')
                
    @commands.command()
    async def primolvlup(self, ctx):
        """Spend 1000 primogems for an instant lvlup"""
        cost = 3000
        flair = self.bot.get_cog("Flair")
        with session_scope() as s:
            user = s.query(GameProfile).filter_by(discord_id=ctx.author.id).first()
            if not user:
                await self.no_profile(ctx)
                return
            if user.primogems < cost:
                await ctx.send(f'You do not have enough primogems. {flair.get_emoji("Primogem")} 1000 needed for instant lvlup')
                return
            user.primogems -= 1000
            user.exp = user.max_exp
            user = self.check_user_status(user)
            await ctx.send(f'{ctx.author.display_name} spent {flair.get_emoji("Primogem")} 1000 and leveled up!')
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
            current_active = s.query(GameCharacter).filter_by(active=True).first()
            if current_active.character.name == name:
                await ctx.send(f'{flair.get_emoji(name)} {name} is already your active character!')
                return
            char = s.query(Character).filter_by(name=name).first()
            if not char:
                await ctx.send(f'{name} is not a known character in Tevyat')
                return
            new_active = s.query(GameCharacter).filter_by(character_id=char.id).first()
            if not new_active:
                await ctx.send(f'{name} is not in your party')
                return
            new_active.active = True
            current_active.active = False
            await ctx.send(f'{flair.get_emoji(name)} {name} is now your active character!')

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
                respawn = self.convert_from_utc(user.deathtime, server_region).strftime("%I:%M %p, %d %b %Y")
                desc+= f"Respawn Time: {respawn}"
            active_char = s.query(GameCharacter).filter_by(profile_id=user.id,active=True).first()
            bench_char = s.query(GameCharacter).filter_by(profile_id=user.id,active=False).all()
            flair = self.bot.get_cog("Flair")
            embed = discord.Embed(title=f"{member.display_name.title()}'s profile",
            description=desc,
            color=flair.get_element_color(active_char.character.element)
            )
            embed.add_field(name=f'{flair.get_emoji("Primogem")} Primogems', value=user.primogems)
            embed.add_field(name='Active Character', value=f'{flair.get_emoji(active_char.character.name)} {active_char.character.name} C{active_char.constellation}')
            if bench_char:
                bench = ''
                for c in bench_char:
                    bench += f'\n{flair.get_emoji(c.character.name)} {c.character.name} C{c.constellation}'
                embed.add_field(name='Bench Characters', value=bench.strip(), inline=False)
            embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    def convert_from_utc(self, time, server_region):
        reminder_cog = self.bot.get_cog('Reminders')
        return reminder_cog.convert_from_utc(time, server_region)

    def check_user_status(self, user):
        now = datetime.utcnow()
        # check stamina
        if user.last_check+timedelta(seconds=self.REGEN_RATE) > now:
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
        if user.exp >= user.max_exp:
            user.level += 1
            user.exp = user.exp-user.max_exp
            user.max_exp=user.level*self.EXP_MULTIPLIER
            user.max_health=user.level*self.HP_MULTIPLIER
            user.max_stamina+= self.STAMINA_INCREMENT
            user.health=user.max_health
            user.deathtime=None
        return user

    def check_death(self, user):
        if user.health <= 0:
            user.deathtime=datetime.utcnow()+timedelta(hours=self.RESPAWN_TIME)
            user.stamina = 0
            user.health = 0
        return user

    def bonus_rate(self, user):
        element = 'Normal'
        constellation = 1
        for c in user.characters:
            if c.active:
                element=c.character.element
                constellation = c.constellation
                break
        constellation_bonus = (1-constellation)*0.2
        if element.lower() == self._todays_weather.lower():
            return self.WEATHER_MULTIPLIER+constellation_bonus
        else:
            return 1+constellation_bonus