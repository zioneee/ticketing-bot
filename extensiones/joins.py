import hikari
import lightbulb

plugin_joins = lightbulb.Plugin('pluginJoins')


@plugin_joins.listener(hikari.MemberCreateEvent)
async def joins(event: hikari.MemberCreateEvent) -> None:
    embed = hikari.Embed(description="""**💼  | LyInterviews**

*・Welcome to the official LyInterviews Discord <@!{}>!*

Here you can have an interview to join any of **LyDark Studios** sub company, we
can't wait anymore to have you in our family! Get an interview here! <#941471112175435866>
 
Remember to always follow our <#941471648538849330> as well as Discord tos.""".format(event.member.id), color=0x480aba)
    embed.set_thumbnail(event.member.avatar_url or event.member.default_avatar_url)
    await plugin_joins.bot.rest.create_message(941470787959934997, embed=embed)


def load(bot):
    bot.add_plugin(plugin_joins)


def unload(bot):
    bot.remove_plugin(plugin_joins)
