"""Official bot for LyInterviews

Functions:
- Ticket system (Interviews system)
- Joins (welcomes)"""

import hikari
import lightbulb
import miru

from lightbulb.ext import tasks

bot = lightbulb.BotApp(token='ODYyMDkwNDAwMjE0NDE3NDU5.YOTSQA._MXYdr2G5rKbn_PTgJKCv5i_EqU', intents=hikari.Intents.ALL, default_enabled_guilds=(940352032190132306,))
miru.load(bot)
tasks.load(bot)

COGS = ['interviews', 'joins']

for cog in COGS:
    bot.load_extensions('extensiones.' + cog)

bot.run()
