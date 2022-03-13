# LYDARK STUDIOS 2022

import hikari
import lightbulb
import miru

import uuid
import sqlite3


plugin_interviews = lightbulb.Plugin('PluginInterviews')
conn = sqlite3.connect('lyinterviews.db')
c = conn.cursor()

areas = {1: ['🪓', 'Builders']}


def gen_custom_id():
    custom_id = str(uuid.uuid1())
    c.execute('INSERT INTO custom_ids VALUES(?, ?)', (custom_id, 0))
    conn.commit()
    return custom_id


class InitializeInterview(miru.Button):

    def __init__(self, custom_id=gen_custom_id(), **kwargs):
        self.custom_id = custom_id
        super().__init__(**kwargs, custom_id=custom_id)

    async def callback(self, ctx: miru.Context):
        """What do we want to do, when an interview gets initialized?

        - Create a text channel following the format interview-XXXX, inside
        the Interview Text Channels Category.
        - Create a voice channel following the format Interview Voice-XXXX, inside
        the Interview Voice Channels Category.

        - Place a message inside the recently created text channel.
        """


@plugin_interviews.command()
@lightbulb.option('channel', 'Select the channel where to send the panel', required=True, type=hikari.TextableChannel, channel_types=[hikari.ChannelType.GUILD_TEXT])
@lightbulb.command('send-panel', 'Send the panel to a channel')
@lightbulb.implements(lightbulb.SlashCommand)
async def send_panel(ctx: lightbulb.SlashContext) -> None:
    embed = hikari.Embed(description='')


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin_interviews)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin_interviews)
