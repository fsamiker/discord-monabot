GENSHIN_GENERAL_MD = '''
There are currently **4 main categories** of commands.

To user commands, prefix with `m!`
Example: `m!character mona`

💽 Genshin Database:
`character` `ascensionmaterial` `talent` `talentmaterial` `material` 
`food` `weapon` `weaponmaterial` `artifact` `domain` `enemy`

⏰ Reminders:
`remindme resin` `remindme specialty` `remindme artifact`
`checkreminders` `cancelreminder`

🌙 Resin Status:
`setresin` `checkresin` `timetoresin` `spendresin`

🕹️ Genshin Minigame:
`startadventure` `leaderboard` `checkweather` `claimdaily` `profile`
`wish` `primolvlup` `switchactive` `checkabyss` `explore` `attack` `mug`
`attackabyss` `vote`

**Misc:**
```
vote                Support Mona if you've enjoyed the bot
updates             Monabot update logs
support             Support resource links
invitemona          Share Monabot with your friends
```
'''

GENSHIN_GENERAL_MD_V2 = '''
```diff
- You are currently viewing a shortened version of `help` as a permission seems to be missing for Mona
- Kindly enable *Manage Message* permission to enable a richer help interface
```

To user commands, prefix with `m!`
Example: `m!character mona`

There are currently **4 main categories** of commands.
use `m!help <command name>` for more details

💽 Genshin Database:
`character` `ascensionmaterial` `talent` `talentmaterial` `material` 
`food` `weapon` `weaponmaterial` `artifact` `domain` `enemy`

⏰ Reminders:
`remindme resin` `remindme specialty` `remindme artifact`
`checkreminders` `cancelreminder`

🌙 Resin Status:
`setresin` `checkresin` `timetoresin` `spendresin`

🕹️ Genshin Minigame:
`startadventure` `leaderboard` `checkweather` `claimdaily` `profile`
`wish` `primolvlup` `switchactive` `checkabyss` `explore` `attack` `mug`
`attackabyss` `vote`

**Misc:**
```
vote                Support Mona if you've enjoyed the bot
updates             Monabot update logs
support             Support resource links
invitemona          Share Monabot with your friends
```
'''

GENSHIN_DATABASE_MD = '''
Access curated details on all things genshin from [Genshin Wiki](https://genshin-impact.fandom.com/wiki/Genshin_Impact_Wiki)

Run `m!help` genshin database or `m!help<command name>` for more details on each command

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

Run `m!help genshin minigame` or `m!help<command name>` for more details on each command

**Start Game:**
```
startadventure      Start your minigame profile
```
**Misc Actions:**
```
leaderboard         Check game leaderboard
checkweather        Check daily ingame weather
claimdaily          Claim daily primogems
profile             Check game profile
wish                Make a wish!
primolvlup          Spend 3000 primogems and lvlup!
switchactive        Switch active character
checkabyss          Check Discord Abyss
vote                Get 1000 primogems for supporting monabot
```
**Stamina Actions:**
Commands that cost stamina
```
explore     (10)    You never know what you might find
heal        (10)    Heal yourself
attack      (15)    Attack a player!
mug         (15)    Attempt to steal primogems
attackabyss (15)    Attack the abyss boss
```
'''

REMINDERS_HELP = '''
Set reminders for genshin related activities.
Never lose out on resin

Run `m!help reminders` for or `m!help<command name>` more details on each command

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

Run `m!help resin status` or `m!help<command name>` for more details on each command

**Commands:**
```
setresin            Set current ingame resin value
checkresin          Check current ingame resin value
timetoresin         Check time to reach a resin value
spendresin          Spend resin amount from resin value
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
Options: 
\u2022 resin - Max Resin reminder. Value = current resin value, target value (default: 160)
\u2022 specialty - Local Specialty reminder
\u2022 mineral - Mineral Mining reminder
\u2022 artifact - Artifact Run reminder
\u2022 wei - Unusual Hilichurl respawn reminder
\u2022 custom - Custom Reminder (Max 3 per user) Value = duration (Max 60 days), message
```
Example Usage:
```
m!remindme resin 50
m!remindme resin 50 120
m!remindme specialty
m!remindme mineral
m!remindme artifact
m!remindme wei
m!remindme custom 5d5hr5min5sec take a shower
m!remindme custom 30d wish mona happy birthday
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

GENSHIN_CANCEL_REMINDERS = '''
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

> m!setresin <current resin> optional: <time left to next resin>

timeleft: Time remaining to next resin. Allows for a more accurate adjustment of resin time (default: 8min)

Example Usage:
```
m!setresin 120
m!setresin 69 3min
m!setresin 42 5min50sec
m!setresin 88 50sec
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

GENSHIN_RESIN_SPEND = '''
Subtract resin value from current resin amount

> m!spendresin <resin used>

Example Usage:
```
m!spendresin 120
m!spendresin 50
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
Claim 1000 primogems every 24 hours

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
Active characters affect actions ingame and helps you take advantage of the weather

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
Note: Max 10 times at a time

Example Usage:
```
m!wish
m!wish 10
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
Explore the corners of digital teyvat and see what you find

Stamina cost: 10

> m!explore optional: <number of times>
Note: Max 10 times at a time

Example Usage:
```
m!explore
m!explore 10
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

Stamina cost: 10

> m!heal

Example Usage:
```
m!heal
```
'''

GENSHIN_GAME_MUG = '''
Attempt to steal some primogems from a player
Bare your own consequences

Stamina cost: 15

> m!mug <Target User>

Example Usage:
```
m!mug @Someone
m!mug @Mona
```
'''

GENSHIN_GAME_CHECKABYSS = '''
Check what lurks in the abyss.
Attempt to slay any bosses that dares disrupt discord

\u2022 Abyss resets every 4 days
\u2022 Bosses spawned only last for 3 days

Team up with you friends and try to defeat the boss.\n\u2022 The player that deals the killing blow will grant participants of their guild the winners pot!\n\u2022 Every other player that participated in taking down the boss will earn the consolation prize.

> m!checkabyss

Example Usage:
```
m!checkabyss
```
'''

GENSHIN_GAME_ATTACKABYSS = '''
Charge into the abyss and contribute to taking down the boss that lurks

Stamina cost: 15

> m!attackabyss

Example Usage:
```
m!attackabyss
```
'''

GENSHIN_GAME_LEADERBOARDS= '''
Check the leaderboards in your guild or all across discord
Options:
\u2022 global
\u2022 guild (default)

> m!leaderboard optional:<option>

Example Usage:
```
m!leaderboard
m!leaderboard global
```
'''

GENSHIN_UPDATE= '''
Check latest update logs
Mona will bring up the latest 3 updates

> m!updates

Example Usage:
```
m!updates
```
'''

GENSHIN_SUPPORT= '''
Monabot support resource links

> m!support

Example Usage:
```
m!support
```
'''

GENSHIN_INVITE_MONA= '''
Get Monabot invite link with recommended permissions

> m!invitemona

Example Usage:
```
m!invitemona
```
'''

TIMEZONE_NOTICE = '''
```fix
[NOTICE: Discord DM channels do not support timezones. Times seen are defaulted to GMT.
Kindly send command from a guild channel for times corrected to guild server's region]
```'''
GENSHIN_VOTE_MONA= '''
Vote for Monabot on TopGG if you've enjoyed the bot

1000 minigame primogems will be given each time you vote as a thank you
Must have started adventure with `m!startadventure` to recieve primogems

Voting available every 12 hours

> m!vote

Example Usage:
```
m!vote
```
'''
