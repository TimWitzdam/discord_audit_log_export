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


async def audit_log_to_json(guild: discord.Guild):
    logs = await guild.audit_logs(limit=100).flatten()
    logs_json = []

    for log in logs:
        log_dict = {
            'target': str(log.target),
            'user_id': str(log.user.id),
            'username': str(log.user.name),
            'action': str(log.action.name),
            'reason': log.reason,
            'created_at': log.created_at.isoformat(),
            'changes': []
        }

        """change_dict = {
            'before': log.changes.before,
            'after': log.changes.after
        }
        log_dict['changes'].append(change_dict)
"""
        logs_json.append(log_dict)

    print(logs_json, type(logs_json))
    return logs_json


@bot.event
async def on_ready():
    print("Bot started as {0.user}".format(bot))


def data_type_autocomplete(ctc: discord.AutocompleteContext):
    options = ["JSON", "Excel"]
    return options


@bot.slash_command(name="export")
async def export(ctx,
                 data_type: discord.Option(name="data_type",
                      description="Which data type should the audit log be exported in?",
                      required=True,
                      input_type=discord.SlashCommandOptionType.string,
                      autocomplete=data_type_autocomplete
                      )
                 ):
    if data_type == "JSON":
        audit_log_json = await audit_log_to_json(ctx.guild)
        tmp = tempfile.NamedTemporaryFile(delete=True)
        tmp.write(json.dumps(audit_log_json))
        return await ctx.respond(file=discord.File(tmp.name))


bot.run(os.getenv("BOT_TOKEN"))
