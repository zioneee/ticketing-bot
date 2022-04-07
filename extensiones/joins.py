import hikari
import lightbulb

plugin_joins = lightbulb.Plugin('pluginJoins')


@plugin_joins.listener(hikari.MemberCreateEvent)
async def joins(event: hikari.MemberCreateEvent) -> None:
    embed = hikari.Embed(description=""":scroll: | Welcome to LyInterviews
 
   ✶﹕Hey! <@!{}> Welcome to our Discord!

Don't forget to check our information channels to know 
more about us.""".format(event.member.id), color=0x480aba)
    embed.set_thumbnail(event.member.avatar_url or event.member.default_avatar_url)
    await plugin_joins.bot.rest.create_message(941470787959934997, embed=embed)
    await plugin_joins.bot.rest.add_role_to_member(940352032190132306, event.member.id, 946277453461065728)


def load(bot):
    bot.add_plugin(plugin_joins)


def unload(bot):
    bot.remove_plugin(plugin_joins)
