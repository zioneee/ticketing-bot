import hikari
import lightbulb

plugin_joins = lightbulb.Plugin('pluginJoins')


@plugin_joins.listener(hikari.MemberCreateEvent)
async def joins(event: hikari.MemberCreateEvent) -> None:
    embed = hikari.Embed(description="""Welcome {} to LyInterviews!
ㆍPlease read <#941471720588607509>, <#941471856660185119> and <#941471648538849330> to 
know who we are. 
ㆍOpen an interview in <#941471112175435866>. We are waiting for you!""", color=0x480aba)
    embed.set_thumbnail(event.member.avatar_url or event.member.default_avatar_url)
    await plugin_joins.bot.rest.create_message(941470787959934997, embed=embed)


def load(bot):
    bot.add_plugin(plugin_joins)


def unload(bot):
    bot.remove_plugin(plugin_joins)
