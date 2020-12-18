GENSHIN_DATABASE_MD = '''
Access curated details on all things genshin from [Genshin Wiki](https://genshin-impact.fandom.com/wiki/Genshin_Impact_Wiki)

Run m!help genshin database for more details on each command

**Character:**
```
character           Get character details
ascensionmaterial   Get character ascension materials
talentmaterial      Get character talent lvlup materials
```
**Talent:**
```
talent              Get talent details
```
**Weapon:**
```
weapon              Get weapon details
weaponmaterial      Get weapon ascension materials
```
**Game:**
```
artifact            Get artifact set details
domain              Get domain details
material            Get material details
food                Get food details
enemy               Get enemy/boss details
```
'''

GENSHIN_DISCORD_MINIGAME = '''
Genshin minigame right on discord!

Run m!help genshin minigame for more details on each command

**Start Game:**
```
startadventure      Start your minigame profile
```
**Misc Actions:**
```
checkweather        Check daily ingame weather
claimdaily          Claim daily primogems
profile             Check game profile
wish                Make a wish!
primolvlup          Spend 3000 primogems and lvlup!
switchactive        Switch active character
```
**Stamina Actions:**
Commands that cost stamina
```
explore (10)        You never know what you might find
heal    (10)        Heal yourself
attack  (15)        Attack a player!
mug     (15)        Attempt to steal primogems
```
'''

REMINDERS_HELP = '''
Set reminders for genshin related activities.
Never lose out on resin

Run m!help reminders for more details on each command

**Reminders:**
```
remindme resin      Max resin
remindme specialty  Local specialty respawn
remindme mineral    Mining respawn
remindme artifact   Artifact run respawn
```
**Actions:**
```
checkreminders      Check active reminders
cancelreminder      Cancel an active reminder
```
'''

RESIN_STATUS = '''
Check the state of your resin in genshin

Run m!help resin status for more details on each command

**Commands:**
```
setresin            Set current ingame resin value
checkresin          Check current ingame resin value
timetoresin         Check time to reach a resin value
```
'''

GENSHIN_DB_CHAR = '''
Genshin character basic details, talent or constellation

> m!character <character name> optional: <option>

```
Options: \u2022 default - Character basic information
         \u2022 talents - Character talent list
         \u2022 constellations - Character constellations list
```
Example Usage:
```
m!character amber
m!character bennett talents
m!character keqing constellations
```
'''

GENSHIN_DB_CHAR_ASC = '''
Genshin ascension materials between 2 levels

> m!ascensionmaterial <character name> optional:<start lvl> <end lvl>
```
Inputs: Start Lvl:  Start counting from character level (Default:1)
        End Lvl:    Stop counting at character level (Default:90)
```
Example Usage:
```
m!ascensionmaterial amber
m!ascensionmaterial amber 1 90
m!ascensionmaterial amber 45 87
```
'''

GENSHIN_DB_TAL_MAT = '''
Genshin talent lvlup materials between 2 levels

> m!talentmaterial <character name> optional:<starting lvl> <target lvl>
```
Inputs: Starting Lvl:   Start material count from lvl,
                        not including current level (Default: 2)
        Target Lvl:     End material count to level (Default: 10)
```
Example Usage:
```
m!talent keqing
m!talent bennett 8 10
```
'''

GENSHIN_DB_TAL = '''
Genshin additional talent details

> m!talent <talent name>

Example Usage:
```
m!talent sharpshooter
m!talent Kaboom!
```
'''

GENSHIN_DB_WEAPON = '''
Genshin weapon details

> m!weapon <weapon name>

Example Usage:
```
m!weapon Amos' Bow
m!weapon prototype rancour
```
'''

GENSHIN_DB_WEAPON_MAT = '''
Genshin weapon ascension materials between 2 levels

> m!weaponmaterial <weapon name> optional:<starting lvl> <target lvl
```
Inputs: Starting Lvl:   Start material count from lvl,
                        not including current level (Default: 1)
        Target Lvl:     End material count to level (Default: 90)
```
Example Usage:
```
m!weaponmaterial solar pearl
m!weaponmaterial skyward harp 5 10
```
'''

GENSHIN_DB_MATERIAL = '''
Genshin material details

> m!material <material name>

Example Usage:
```
m!material dandelion seed
m!material sharp arrowhead
```
'''

GENSHIN_DB_FOOD = '''
Genshin material details

> m!food <material name>

Example Usage:
```
m!food apple
m!food mysterious bolognese
```
'''

GENSHIN_DB_ARTIFACT = '''
Genshin artifact set details

> m!artifact <artifact name>

Example Usage:
```
m!artifact gladiator's finale
m!artifact berserker
```
'''

GENSHIN_DB_DOMAIN = '''
Genshin domain details

> m!domain <domain name> optional: <level> <day of the week>
```
level :             Domain Floor Level (Default: Max Level)
day of the week :   Day of the week (Default: Sunday for 
                    domains dependant on days)
```
Example Usage:
```
m!domain Midsummer Courtyard
m!domain forsaken rift 3
m!domain ceceilia garden 3 monday
```
'''


GENSHIN_DB_ENEMY = '''
Genshin enemy/boss details

> m!enemy <enemy name>

Example Usage:
```
m!enemy hilichurls
m!enemy dvalin
```
'''

GENSHIN_REMINDME = '''
Set reminders. Mona will dm you when its time!

> m!remindme <option> <values>
```
Options: \u2022 resin - Max Resin reminder. Value = current resin value
         \u2022 specialty - Local Specialty reminder
         \u2022 mineral - Mineral Mining reminder
         \u2022 artifact - Artifact Run reminder
```
Example Usage:
```
m!remindme resin 50
m!remindme specialty
m!remindme mineral
m!remindme artifact
```
'''

GENSHIN_CHECKREMINDERS = '''
Check active reminders. Mona will dm you your reminder list

> m!checkreminders
Example Usage:
```
m!checkreminders
```
'''

GENSHIN_CANCELKREMINDERS = '''
Cancel an active reminder.
Run m!checkreminders to get reminder id.

> m!cancelreminder <reminder ID or all>

Example Usage:
```
m!cancelreminder 5
m!cancelreminder all
```
'''

GENSHIN_RESIN_SET = '''
Set current genshin ingame resin value. Mona will track your resin replenishment.
Note: This does not set a reminder. Reminder has to be enabled separately.
However if reminder is already active, reminder will automatically be readjusted

> m!setresin <current resin>

Example Usage:
```
m!setresin 120
m!setresin 69
```
'''

GENSHIN_RESIN_CHECK = '''
Check current resin value. Only valid if m!setresin or m!remindme resin has been used

> m!checkresin

Example Usage:
```
m!checkresin
```
'''

GENSHIN_RESIN_TIME = '''
Checks time resin reaches a desired value

> m!timetoresin <desired resin>

Example Usage:
```
m!timetoresin 120
m!timetoresin 42
```
'''

GENSHIN_GAME_START = '''
Starts genshin game adventure. Choose an initial character

> m!startadventure <character>

Example Usage:
```
m!startadventure diluc
m!startadventure mona
```
'''

GENSHIN_GAME_WEATHER = '''
Checks weather of discord genshin.
Weather changes every 4 hours, perks may affect active character.

> m!checkweather

Example Usage:
```
m!checkweather
```
'''

GENSHIN_GAME_CLAIM  = '''
Claim 300 primogems every 24 hours

> m!claimdaily

Example Usage:
```
m!claimdaily
```
'''

GENSHIN_GAME_PROFILE = '''
Check your own or your friend's profile
Target must have started their adventure

> m!profile optional: <user>

Example Usage:
```
m!profile
m!profile @Mona
```
'''

GENSHIN_GAME_SWITCH = '''
Switch your active character with your bench characters if you have any.
Active characters affect actions ingame

> m!switchactive <target character>

Example Usage:
```
m!switchactive amber
m!switchactive mona
```
'''

GENSHIN_GAME_WISH = '''
You know the drill! Make a wish! 

> m!wish optional: <times to wish>

Example Usage:
```
m!wish
m!wish 10
m!wish 420
```
'''

GENSHIN_GAME_PRIMOLVLUP = '''
Levelup instantly at the cost of 3000 primogems 

> m!primolvlup

Example Usage:
```
m!primolvlup
```
'''

GENSHIN_GAME_EXPLORE = '''
Explore the corners of digital tevyat and see what you find 

> m!explore

Example Usage:
```
m!explore
```
'''

GENSHIN_GAME_ATTACK = '''
Attack an enemy. Attack a friend
But be careful... 

> m!attack <target user>

Example Usage:
```
m!attack @Mona
m!attack @Someone
```
'''

GENSHIN_GAME_HEAL = '''
Keep yourself healthy, heal yourself
Chance to fully heal

> m!heal

Example Usage:
```
m!heal
```
'''

GENSHIN_GAME_MUG = '''
Attempt to steal some primogems from a player
Bare your own consequences

> m!mug <Target User>

Example Usage:
```
m!mug @Someone
m!mug @Mona
```
'''