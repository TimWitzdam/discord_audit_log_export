import asyncio
import json
from datetime import datetime
import discord
import os

from discord.ext import tasks
from dotenv import load_dotenv
import tempfile
import audit_log_formatter
import embeds

load_dotenv()
bot = discord.Bot()


@tasks.loop(seconds=185)
async def game():
    if not bot.is_ready():
        return
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/help"))
    await asyncio.sleep(60)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name=str(len(bot.guilds)) + " Servers | /help"))
    await asyncio.sleep(60)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="/invite | /help"))
    await asyncio.sleep(60)

game.start()


@bot.event
async def on_ready():
    print("Bot started as {0.user}".format(bot))


def data_type_autocomplete(ctc: discord.AutocompleteContext):
    options = ["JSON", "CSV"]
    return options


@bot.slash_command(name="export", description="Export the audit log of your server in JSON or CSV format")
async def export(ctx,
                 data_type: discord.Option(name="data_type",
                                           description="Which data type should the audit log be exported in?",
                                           required=True,
                                           input_type=discord.SlashCommandOptionType.string,
                                           autocomplete=data_type_autocomplete
                                           ),
                 limit: discord.Option(
                     name="limit",
                     description=f"How many entries should be exported? (Default: {os.getenv('DEFAULT_LIMIT')})",
                     required=False,
                     input_type=discord.SlashCommandOptionType.integer,
                     default=os.getenv("DEFAULT_LIMIT")
                 )
                 ):
    try:
        if int(limit) > int(os.getenv("MAX_LIMIT")):
            await ctx.respond(embed=embeds.limit_exceeded())
            return
    except ValueError:
        await ctx.respond(embed=embeds.limit_exceeded())
        return

    await ctx.defer()
    if data_type == "JSON":
        try:
            logs = await ctx.guild.audit_logs(limit=int(limit)).flatten()
        except discord.errors.Forbidden:
            await ctx.respond(embed=embeds.missing_permissions())
            return
        audit_log_json = await audit_log_formatter.to_json(logs)
        with tempfile.NamedTemporaryFile(mode='w+b') as tmp:
            tmp.write(json.dumps(audit_log_json, indent=4).encode())
            tmp.seek(0)
            await ctx.respond(embed=embeds.successfully_exported(), file=discord.File(fp=tmp.name,
                                                                                      filename=f"audit_log_export_{datetime.strftime(datetime.now(), '%d-%m-%Y, %H-%M-%S')}.json"))
            tmp.close()
    elif data_type == "CSV":
        try:
            logs = await ctx.guild.audit_logs(limit=int(limit)).flatten()
        except discord.errors.Forbidden:
            await ctx.respond(embed=embeds.missing_permissions())
            return
        temp_file = await audit_log_formatter.to_csv(logs)
        await ctx.respond(embed=embeds.successfully_exported(), file=discord.File(fp=temp_file.name,
                                                                                  filename=f"audit_log_export_{datetime.strftime(datetime.now(), '%d-%m-%Y, %H-%M-%S')}.csv"))
        temp_file.close()
    else:
        await ctx.respond(embed=embeds.invalid_data_type())


@bot.slash_command(name="invite", description="Invite the bot to your server")
async def invite(ctx):
    await ctx.respond(embed=embeds.invite())


@bot.slash_command(name="help", description="Show all the available commands")
async def help(ctx):
    await ctx.respond(embed=embeds.help())


bot.run(os.getenv("BOT_TOKEN"))
