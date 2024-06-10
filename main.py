import json
from datetime import datetime
import discord
import os
from dotenv import load_dotenv
import tempfile
import audit_log_formatter

load_dotenv()
bot = discord.Bot()


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
            logs = await ctx.guild.audit_logs(limit=limit).flatten()
            audit_log_json = await audit_log_formatter.to_json(logs, limit)
        except discord.errors.Forbidden:
            await ctx.respond("The bot is missing permissions to access the audit log.")
            return
        with tempfile.NamedTemporaryFile(mode='w+b') as tmp:
            tmp.write(json.dumps(audit_log_json, indent=4).encode())
            tmp.seek(0)
            await ctx.respond(file=discord.File(fp=tmp.name,
                                                filename=f"audit_log_export_{datetime.strftime(datetime.now(), '%d-%m-%Y, %H-%M-%S')}.json"))
    elif data_type == "CSV":
        logs = await ctx.guild.audit_logs(limit=limit).flatten()
        temp_file = await audit_log_formatter.to_csv(logs, limit)
        temp_file.seek(0)
        await ctx.respond(file=discord.File(fp=temp_file.name,
                                            filename=f"audit_log_export_{datetime.strftime(datetime.now(), '%d-%m-%Y, %H-%M-%S')}.csv"))


bot.run(os.getenv("BOT_TOKEN"))
