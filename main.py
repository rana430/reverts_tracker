import discord
from discord.ext import commands
import datetime
import sqlite3


connection = sqlite3.connect('db/reverts_database.db')
cursor = connection.cursor()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# @bot.event
# async def on_ready():
#    print(f'Logged in as {bot.user.name}')

# cursor.execute(
#         f'''
#             INSERT INTO members (member_id, member_name, gender, author, notes, date) VALUES (?, ?, ?, ?, ?, datetime('now'));
#         ''',( 124, "meow", "Male" , "ffiwen", "fioewhbfiew")
#     )


@bot.command()
async def show(ctx: commands.Context, role : discord.Role):
    for mem in ctx.guild.members:
        if role in mem.roles:
            await ctx.send(mem.id)

@bot.command()
async def add(ctx: commands.Context, mem: discord.Member, *, notes=None):
    is_male = discord.utils.get(mem.roles, id=1146032099854389249) != None
    username = mem.global_name or str(mem)
    author_username = ctx.author.global_name or str(ctx.author)

    cursor.execute(
        f'''
            INSERT INTO members (member_id, member_name, gender, author, notes, date) VALUES (?, ?, ?, ?, ?, datetime('now'));
        ''',( mem.id, username, "Male" if is_male else "Female", author_username, notes)
    ) 
    connection.commit()

def get_gender_from_roles(user):
    for role in user.roles:
        if role.name.lower() in ["male", "female", "non-binary", "other"]:
            return role.name
    return "Unknown"

bot.run('MTE0Mzg5OTM3MDI0MTEzODgzMg.Ga6GZx.-AnMH13r2hg7-16U6T8rwYV8XsC0xbwZWHYLY8')
