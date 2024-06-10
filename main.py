import json
from datetime import datetime
import inspect
import discord
import os

from dotenv import load_dotenv
import tempfile

load_dotenv()
bot = discord.Bot()


def debug(argument):
    cf = inspect.currentframe()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f'{current_time} - {cf.f_back.f_lineno}: {argument}')


async def audit_log_to_json(guild: discord.Guild, limit=1000):
    logs = await guild.audit_logs(limit=limit).flatten()
    logs_json = []

    for log in logs:
        log_dict = {
            'target': str(log.target),
            'user_id': str(log.user.id),
            'username': str(log.user.name),
            'action': str(log.action.name),
            'reason': log.reason,
            'created_at': log.created_at.isoformat(),
        }

        """change_dict = {
            'before': log.changes.before,
            'after': log.changes.after
        }
        log_dict['changes'].append(change_dict)
"""
        logs_json.append(log_dict)

    return logs_json


def audit_log_to_csv(audit_log):
    tmp = tempfile.NamedTemporaryFile(mode="w")
    tmp.write(",".join(audit_log[0].keys()))
    tmp.write("\n")
    for log_dict in audit_log[1:]:
        for value in log_dict.values():
            tmp.write(f"{value},")
        tmp.write("\n")

    return tmp


@bot.event
async def on_ready():
    print("Bot started as {0.user}".format(bot))


def data_type_autocomplete(ctc: discord.AutocompleteContext):
    options = ["JSON", "CSV"]
    return options


@bot.slash_command(name="export")
async def export(ctx,
                 data_type: discord.Option(name="data_type",
                                           description="Which data type should the audit log be exported in?",
                                           required=True,
                                           input_type=discord.SlashCommandOptionType.string,
                                           autocomplete=data_type_autocomplete
                                           ),
                 limit: discord.Option(
                     name="limit",
                     description="How many entries should be exported? (Default: 1000)",
                     required=False,
                     input_type=discord.SlashCommandOptionType.integer,
                     default=1000
                 )
                 ):
    await ctx.defer()
    if data_type == "JSON":
        try:
            audit_log_json = await audit_log_to_json(ctx.guild, limit)
        except discord.errors.Forbidden:
            await ctx.respond("The bot is missing permissions to access the audit log.")
            return
        with tempfile.NamedTemporaryFile(mode='w+b') as tmp:
            tmp.write(json.dumps(audit_log_json, indent=4).encode())
            tmp.seek(0)
            await ctx.respond(file=discord.File(fp=tmp.name,
                                                filename=f"audit_log_export_{datetime.strftime(datetime.now(), '%d-%m-%Y, %H-%M-%S')}.json"))
    elif data_type == "CSV":
        audit_log_json = await audit_log_to_json(ctx.guild, limit)
        temp_file = audit_log_to_csv(audit_log_json)
        temp_file.seek(0)
        await ctx.respond(file=discord.File(fp=temp_file.name,
                                            filename=f"audit_log_export_{datetime.strftime(datetime.now(), '%d-%m-%Y, %H-%M-%S')}.csv"))


bot.run(os.getenv("BOT_TOKEN"))
