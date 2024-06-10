import os
import discord


def help():
    embed = discord.Embed(title="Help", description="This bot exports the audit log of your server in JSON or CSV "
                                                    "format.\n The bot is fully open source: [Github]("
                                                    "https://github.com/TimWitzdam/discord_audit_log_export)",
                          color=0xf8c434)
    embed.add_field(name="Commands", value="`/export [data_type]` - This command exports the audit log of your server "
                                           "in JSON or CSV format."
                                           "\n `/invite` - Invite the bot to your own server! ", inline=False)
    embed.set_footer(text="Made by @nightslide_",
                     icon_url="https://witzdam.com/images/pfp.webp")
    return embed


def missing_permissions():
    embed = discord.Embed(title="Missing permissions", description="The bot is missing permissions to access the audit "
                                                                   "log.", color=discord.Color.red())
    embed.set_footer(text="Made by @nightslide_",
                     icon_url="https://witzdam.com/images/pfp.webp")
    return embed


def successfully_exported():
    embed = discord.Embed(title="Successfully exported",
                          description="The audit log has been successfully exported. \n\n"
                                      "Consider giving the bot a star on [Github]("
                                      "https://github.com/TimWitzdam/discord_audit_log_export)!",
                          color=0xf8c434)
    embed.set_footer(text="Made by @nightslide_",
                     icon_url="https://witzdam.com/images/pfp.webp")
    return embed


def invalid_data_type():
    embed = discord.Embed(title="Invalid data type", description="The data type you entered is invalid. "
                                                                 "Please enter either `JSON` or `CSV`.",
                          color=discord.Color.red())
    embed.set_footer(text="Made by @nightslide_",
                     icon_url="https://witzdam.com/images/pfp.webp")
    return embed


def invite():
    embed = discord.Embed(title="Invite", description="You can invite me to your server by clicking "
                                                      f"[here]({os.getenv('BOT_INVITE')})",
                          color=0xf8c434)
    embed.set_footer(text="Made by @nightslide_",
                     icon_url="https://witzdam.com/images/pfp.webp")
    return embed


def limit_exceeded():
    embed = discord.Embed(title="Limit exceeded", description=f"The limit you entered is too high. "
                                                              f"The maximum limit is {os.getenv('MAX_LIMIT')}.",
                          color=discord.Color.red())
    embed.set_footer(text="Made by @nightslide_",
                     icon_url="https://witzdam.com/images/pfp.webp")
    return embed
