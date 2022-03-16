# LYDARK STUDIOS 2022
import asyncio

import hikari
import lightbulb
import miru

import uuid
import sqlite3

plugin_interviews = lightbulb.Plugin('PluginInterviews')
conn = sqlite3.connect('lyinterviews.db')
c = conn.cursor()

FORM = """What is your real name?
Where are you from?
How old are you?"""

LYCLOUD_INT_CREATED = """**・⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢୨୧⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢・**

╭╯ <a:pestanita:953458330825805874> ╰╮**LyHosting**

** `☁` | LyCloud Interview**

Welcome to your interview <@!{}>, we are really happy to have you here!
before someone attends you, please answer these questions:

Are you currently on another hosting company?
What charge would you like to join?
Have you worked before on a hosting company?
How good your level is at working with vps?
Do you have any technical issue? (Broken microphone,
My pc isn't working)

__*We have a huge schedule! Please be patience,*__
__*someone will attend you as soon as possible*__
**・⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢୨୧⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢・**"""

LYDARK_INT_CREATED = """**・⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢୨୧⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢・**
╭╯ <a:pestanita:953458330825805874> ╰╮**LyInterviews**

** `✨` | LyDark Network Interview**

Welcome to your interview <@!{}>, we are really happy to have you here!
before someone attends you, please answer these questions:

Do you have previous experience in any other network?
What area would you like to join?
Are you currently staff on other network?
Why would you like to join us?
Do you have any technical issue? (Broken microphone,
My pc isn't working)

__*We have a huge schedule! Please be patience,*__
__*someone will attend you as soon as possible*__
**・⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢୨୧⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢・**"""

LYMARKET_INT_CREATED = """**・⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢୨୧⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢・**
╭╯ <a:pestanita:953458330825805874> ╰╮**LyInterviews**

** `🍀` | LyMarket Interview**

Welcome to your interview <@!{}>, we are really happy to have you here!
before someone attends you, please answer these questions:

What department would you like to join?
Why would you like to join us?
Do you have any technical issue? (Broken microphone,
My pc isn't working)

__*We have a huge schedule! Please be patience,*__
__*someone will attend you as soon as possible*__
**・⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢୨୧⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢⌢・**"""

areas = {1: {'emoji': '☁', 'label': 'LyCloud', 'form': [FORM, [0, 0, 0]], 'int_crt': LYCLOUD_INT_CREATED},
         2: {'emoji': '✨', 'label': 'LyDark  Network', 'form': [FORM, [0, 0, 0]], 'int_crt': LYDARK_INT_CREATED},
         3: {'emoji': '🍀', 'label': 'LyMarket', 'form': [FORM, [0, 0, 0]], 'int_crt': LYMARKET_INT_CREATED}
         }

txt_input_styles = {0: hikari.TextInputStyle.SHORT, 1: hikari.TextInputStyle.PARAGRAPH}


def gen_custom_id(id_type: int, area_id: int = None) -> str:
    """Different custom id types:

    - 0: `Initialize interview button`

    - 1: `Delete interview button`

    - 2: `Close interview button`

    - 3: `Re-open interview button`
    """
    custom_id = str(uuid.uuid1())
    if area_id:
        c.execute('INSERT INTO custom_ids VALUES(?, ?, ?)', (custom_id, area_id, id_type))
    else:
        c.execute('INSERT INTO custom_ids(custom_id, type) VALUES(?, ?)', (custom_id, id_type))
    conn.commit()
    return custom_id


def get_interview_id() -> str:
    c.execute('SELECT count FROM interviews_counter ORDER BY count DESC LIMIT 1')
    res = c.fetchone()
    if not res:
        c.execute('INSERT INTO interviews_counter VALUES(?)', (1,))
        conn.commit()
        return '0001'

    num = res[0] + 1
    c.execute('INSERT INTO interviews_counter VALUES(?)', (num,))
    conn.commit()

    if num > 9:
        if num > 99:
            if num > 999:
                return str(num)
            else:
                return str("0" + str(num))
        else:
            return str("00" + str(num))
    else:
        return str("000" + str(num))


async def close_interview(user_id: int) -> None:
    c.execute('SELECT channel_id, vc_id FROM interviews WHERE user_id = ?', (user_id,))
    res = c.fetchone()

    await plugin_interviews.bot.rest.delete_permission_overwrite(res[0], user_id)
    await plugin_interviews.bot.rest.delete_permission_overwrite(res[1], user_id)

    c.execute('UPDATE interviews SET status = ? WHERE user_id = ?', (0, user_id))
    conn.commit()


class RejectForm(miru.Modal):

    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(title='Reject', timeout=300)

    async def callback(self, ctx: miru.ModalContext) -> None:
        dm = await plugin_interviews.bot.rest.create_dm_channel(self.user_id)
        values = [value for value in ctx.values.values()]
        await dm.send('Your interview has been rejected.\n\nReason: ```{}```'.format(values[0]))


class FormLogView(miru.View):

    def __init__(self, log: str, user_id: int) -> None:
        self.log = log
        self.user_id = user_id
        super().__init__(timeout=600)

    @miru.button(label='Take interview', style=hikari.ButtonStyle.PRIMARY, emoji='✅')
    async def take_interview_button(self, _: miru.Button, ctx: miru.Context):
        for child in self.children:
            child.disabled = True
        self.log += '\n\nInterview taken by <@!{}>'.format(ctx.user.id)
        await ctx.edit_response(content=self.log, components=self.build(), user_mentions=True, role_mentions=True)
        c.execute('UPDATE interviews SET interviewer_id = ? WHERE user_id = ?', (ctx.user.id, self.user_id))
        conn.commit()

        c.execute('SELECT channel_id, vc_id FROM interviews WHERE user_id = ?', (self.user_id,))
        res = c.fetchone()

        await plugin_interviews.bot.rest.edit_permission_overwrites(res[0], ctx.user.id,
                                                                    target_type=hikari.PermissionOverwriteType.MEMBER,
                                                                    allow=hikari.Permissions.VIEW_CHANNEL)
        await plugin_interviews.bot.rest.edit_permission_overwrites(res[1], ctx.user.id,
                                                                    target_type=hikari.PermissionOverwriteType.MEMBER,
                                                                    allow=hikari.Permissions.VIEW_CHANNEL)

        await plugin_interviews.bot.rest.create_message(res[0], 'Hey! <@!{}> took this interview, they\'ll be attending you <@!{}>'.format(ctx.user.id, self.user_id))

    @miru.button(label='Reject interview', style=hikari.ButtonStyle.DANGER, emoji='⛔')
    async def reject_interview_button(self, _: miru.Button, ctx: miru.Context):
        modal = RejectForm(self.user_id)
        modal.add_item(miru.TextInput(label='Reason', style=hikari.TextInputStyle.PARAGRAPH, required=True))

        await modal.send(ctx.interaction)
        await modal.wait()

        for child in self.children:
            child.disabled = True

        self.log += '\n\nInterview rejected by <@!{}>'.format(ctx.user.id)
        await ctx.edit_response(content=self.log, components=self.build(), user_mentions=True, role_mentions=True)

        await close_interview(self.user_id)

    async def on_timeout(self) -> None:
        c.execute('SELECT user_id FROM interviews WHERE user_id = ?', (self.user_id,))
        res = c.fetchone()
        if not res:
            return

        for child in self.children:
            child.disabled = True

        self.log += '\n\nInterview timed out! :('
        await self.message.edit(content=self.log, components=self.build(), user_mentions=True, role_mentions=True)


class FormModal(miru.Modal):

    def __init__(self, area_id) -> None:
        super().__init__(title=areas[area_id]['label'], timeout=600)
        self.area_id = area_id

    async def callback(self, ctx: miru.ModalContext) -> None:
        # Submit the form.
        c.execute('UPDATE form_replies SET submit = ? WHERE user_id = ?', (1, ctx.user.id))
        conn.commit()
        log = "<@&953095866292531210> New interview request!\nUser: <@!{}>\n\n".format(ctx.user.id)
        counter = 0
        values = [value for value in ctx.values.values()]
        for line in areas[self.area_id]['form'][0].splitlines():
            log += "\n" + line + "\n```Answer: " + values[counter] + "```"
            counter += 1

        view = FormLogView(log, ctx.user.id)
        message = await plugin_interviews.bot.rest.create_message(953088221145874443, log, components=view.build(), user_mentions=True, role_mentions=True)
        view.start(message)


class InitializeInterview(miru.Button):

    def __init__(self, area_id: int, custom_id: str = None) -> None:
        if not custom_id:
            custom_id = gen_custom_id(0, area_id)
        self.area_id = area_id
        label = areas[area_id]['label']
        emoji = areas[area_id]['emoji']
        super().__init__(style=hikari.ButtonStyle.PRIMARY, label=label, emoji=emoji, custom_id=custom_id)

    async def callback(self, ctx: miru.Context) -> None:
        """What do we want to do, when an interview gets initialized?

        - Insert all values in the database table

        - Create a text channel following the format interview-XXXX, inside the Interview Text Channels Category.

        - Create a voice channel following the format Interview Voice-XXXX, inside the Interview Voice Channels Category.

        - Place a message inside the recently created text channel.

        - Open a modal for the user, with a small form.
        """

        c.execute('SELECT channel_id FROM interviews WHERE user_id = ? AND status = ?', (ctx.user.id, 1))
        already_on_an_interview = c.fetchone()
        if already_on_an_interview:
            await ctx.respond('You are not allowed to create more than one interview at once. Please attend your current one at <#{}>'.format(already_on_an_interview[0]), flags=hikari.MessageFlag.EPHEMERAL)
            return

        modal = FormModal(self.area_id)
        cnt = 0
        for line in areas[self.area_id]['form'][0].splitlines():
            modal.add_item(miru.TextInput(label=line, style=txt_input_styles[areas[self.area_id]['form'][1][cnt]], required=True))
            cnt += 1

        c.execute('INSERT INTO form_replies VALUES(?, ?)', (ctx.user.id, 0))
        conn.commit()

        await modal.send(ctx.interaction)

        await modal.wait()

        c.execute('SELECT submit FROM form_replies WHERE user_id = ? AND submit = ?', (ctx.user.id, 1))
        submitted = c.fetchone()
        c.execute('DELETE FROM form_replies WHERE user_id = ?', (ctx.user.id,))
        conn.commit()

        if not submitted:
            await ctx.respond('Your form was not registered.', flags=hikari.MessageFlag.EPHEMERAL)
            return

        perms = [hikari.PermissionOverwrite(
            type=hikari.PermissionOverwriteType.ROLE,
            id=940352032190132306,
            deny=hikari.Permissions.VIEW_CHANNEL
        ), hikari.PermissionOverwrite(
            type=hikari.PermissionOverwriteType.MEMBER,
            id=ctx.user.id,
            allow=hikari.Permissions.VIEW_CHANNEL
        )]
        interview_id = get_interview_id()
        channel = await plugin_interviews.bot.rest.create_guild_text_channel(940352032190132306,
                                                                             'interview-{}'.format(interview_id),
                                                                             topic='{} {}'.format(
                                                                                 areas[self.area_id]['label'],
                                                                                 areas[self.area_id]['emoji']),
                                                                             category=953286012799443064,
                                                                             permission_overwrites=perms)
        vc_channel = await plugin_interviews.bot.rest.create_guild_voice_channel(940352032190132306,
                                                                                 'Interview Voice-{}'.format(
                                                                                     interview_id),
                                                                                 category=953286077916016660,
                                                                                 permission_overwrites=perms)

        await ctx.respond('Your interview was created! Check <#{}> for more information.'.format(channel.id), flags=hikari.MessageFlag.EPHEMERAL)
        c.execute('INSERT INTO interviews(channel_id, vc_id, user_id, status) VALUES(?, ?, ?, ?)', (channel.id, vc_channel.id, ctx.user.id, 1))
        conn.commit()

        view = miru.View(timeout=None)
        view.add_item(CloseInterview())
        view.add_item(DeleteInterview())

        message = await channel.send(areas[self.area_id]['int_crt'].format(ctx.user.id), components=view.build())
        view.start(message)


class DeleteInterview(miru.Button):

    def __init__(self, custom_id: str | None=None) -> None:
        if not custom_id:
            gen_custom_id(1)
        super().__init__(style=hikari.ButtonStyle.DANGER, label='Delete interview', emoji='🚫', custom_id=custom_id)

    async def callback(self, ctx: miru.Context) -> None:
        if 946277431403225118 not in ctx.member.role_ids:
            await ctx.respond('You cannot delete your interview!', flags=hikari.MessageFlag.EPHEMERAL)
            return

        c.execute('SELECT vc_id FROM interviews WHERE channel_id = ?', (ctx.channel_id,))
        res = c.fetchone()

        await ctx.respond('This interview will be deleted in 5 seconds...')
        await asyncio.sleep(5)

        await plugin_interviews.bot.rest.delete_channel(res[0])
        await plugin_interviews.bot.rest.delete_channel(ctx.channel_id)

        c.execute('DELETE FROM interviews WHERE channel_id = ?', (ctx.channel_id,))
        conn.commit()


class ReOpenInterview(miru.Button):

    def __init__(self, custom_id: str | None=None) -> None:
        if not custom_id:
            gen_custom_id(3)
        super().__init__(style=hikari.ButtonStyle.SUCCESS, label='Re-Open interview', emoji='🔓', custom_id=custom_id)

    async def callback(self, ctx: miru.Context) -> None:
        c.execute('SELECT vc_id, user_id FROM interviews WHERE channel_id = ?', (ctx.channel_id,))
        res = c.fetchone()

        await plugin_interviews.bot.rest.edit_permission_overwrites(ctx.channel_id, res[1],
                                                                    target_type=hikari.PermissionOverwriteType.MEMBER,
                                                                    allow=hikari.Permissions.VIEW_CHANNEL)
        await plugin_interviews.bot.rest.edit_permission_overwrites(res[0], res[1],
                                                                    target_type=hikari.PermissionOverwriteType.MEMBER,
                                                                    allow=hikari.Permissions.VIEW_CHANNEL)

        await ctx.respond('Interview has been re-opened. <@!{}>'.format(res[1]))
        c.execute('UPDATE interviews SET status = ? WHERE channel_id = ?', (1, ctx.channel_id))
        conn.commit()


class CloseInterview(miru.Button):

    def __init__(self, custom_id: str | None=None):
        if not custom_id:
            gen_custom_id(2)
        super().__init__(style=hikari.ButtonStyle.SECONDARY, label='Close interview', emoji='🔒', custom_id=custom_id)

    async def callback(self, ctx: miru.Context):
        if 946277431403225118 not in ctx.member.role_ids:
            await ctx.respond('You cannot close your interview!', flags=hikari.MessageFlag.EPHEMERAL)
            return

        c.execute('SELECT user_id FROM interviews WHERE channel_id = ?', (ctx.channel_id,))
        res = c.fetchone()
        await close_interview(res[0])

        view = miru.View(timeout=None)
        view.add_item(ReOpenInterview())

        embed = hikari.Embed(description='This interview has been closed.', color=0x480aba)
        embed.set_footer(text=ctx.user.username, icon=ctx.user.avatar_url or ctx.user.default_avatar_url)
        message: miru.InteractionResponse = await ctx.respond(embed=embed, components=view.build())

        view.start(await message.retrieve_message())


@plugin_interviews.listener(hikari.StartedEvent)
async def init_views(_: hikari.StartedEvent) -> None:
    c.execute('SELECT * FROM custom_ids')
    res = c.fetchall()
    if not res:
        return

    for custom_id, area_id, view_type in res:  # [(1, 1, 1), (2, 1, 1)]
        match view_type:
            case 0:  # Init interview view
                view = miru.View(timeout=None)
                init_interview_btn = InitializeInterview(area_id, custom_id)
                view.add_item(init_interview_btn)

                view.start_listener()
            case 1:  # Delete interview button
                view = miru.View(timeout=None)
                init_dlt_btn = DeleteInterview(custom_id)
                view.add_item(init_dlt_btn)

                view.start_listener()
            case 2:  # Close interview button
                view = miru.View(timeout=None)
                init_cls_btn = CloseInterview(custom_id)
                view.add_item(init_cls_btn)

                view.start_listener()
            case 3:  # Re-open interview button
                view = miru.View(timeout=None)
                init_re_open_btn = ReOpenInterview(custom_id)
                view.add_item(init_re_open_btn)

                view.start_listener()


@plugin_interviews.command()
@lightbulb.option('channel', 'Select the channel where to send the panel', required=True, type=hikari.TextableChannel,
                  channel_types=[hikari.ChannelType.GUILD_TEXT])
@lightbulb.command('send-panel', 'Send the panel to a channel')
@lightbulb.implements(lightbulb.SlashCommand)
async def send_panel(ctx: lightbulb.SlashContext) -> None:
    embed = hikari.Embed(description="""**<:tilde_rojo:953458397439725569> | Join us**

Do you want to be part of our family? 
Get ready and get an interview!

*Who we are?*
**LyDark Studios** is a company focused on digital markets, willing to
create different sub companies for each **digital market**.

Right now we have some sub companies you can apply for,
depending on what sub company and department you want to join.
    
**<a:tilde_verde:953457957855703100> | Our sub companies**

**❱ LyCloud `☁` **
**❱ LyDark Network `✨` **
**❱ LyMarket `🍀` **""", color=0x480aba)
    embed.set_footer('LyInterviews 2022')

    view = miru.View(timeout=None)
    for area in areas:
        view.add_item(InitializeInterview(area))

    message = await plugin_interviews.bot.rest.create_message(ctx.options.channel.id, embed=embed, components=view.build())
    view.start(message)

    await ctx.respond('Panel was successfully sent!', flags=hikari.MessageFlag.EPHEMERAL)


@plugin_interviews.command()
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command('reset-interviews-counter', 'Reset the interviews counter')
@lightbulb.implements(lightbulb.SlashCommand)
async def reset_int_counter(ctx: lightbulb.SlashContext) -> None:
    c.execute('DELETE FROM interviews_counter')
    conn.commit()
    await ctx.respond('Interviews counter has been reset successfully.', flags=hikari.MessageFlag.EPHEMERAL)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin_interviews)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin_interviews)
