import discord
from discord.ext import commands
from datetime import datetime
import sqlite3
import aiosql


connection = sqlite3.connect("db/reverts_database.db")
cr = connection.cursor()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# @bot.event
# async def on_ready():
#    print(f'Logged in as {bot.user.name}')

"""@bot.command()
async def show(ctx: commands.Context, role : discord.Role):
    for mem in ctx.guild.members:
        if role in mem.roles:
            await ctx.send(mem.id)
"""


@bot.command()
async def add(ctx: commands.Context, mem: discord.Member, *, notes=None):
    is_male = discord.utils.get(mem.roles, id=1146032099854389249) != None
    username = mem.global_name or str(mem)
    cr.execute(
        f"""
        SELECT * FROM REVERTS WHERE revert_id = ? ;
        """,
        (mem.id,),
    )
    row = cr.fetchone()

    if row is not None:
        embed = discord.Embed(
            title="This user is already recorded! ", color=discord.Color.red()
        )
        await ctx.send(embed=embed)

        return

    cr.execute(
        f"""
            INSERT INTO REVERTS (revert_id, gender, mod_id, notes, date) VALUES (?, ?, ?, ?, datetime('now'));
        """,
            (mem.id, "Male" if is_male else "Female", ctx.author.id, notes),
    )
    cr.execute("INSERT INTO HISTORY (revert_id, mod_id, notes, date) VALUES (?, ?, ?, datetime('now'));", (mem.id, ctx.author.id, notes))
    connection.commit()


@bot.command()
async def info(ctx: commands.Context, mem: discord.Member):
    cr.execute("SELECT * FROM REVERTS WHERE revert_id = ?;", (mem.id,))
    row = cr.fetchone()

    fmt_date = discord.utils.format_dt(datetime.fromisoformat(row[4]), style="D")

    if row:  # print (row)
        embed = discord.Embed(title="User Information: ", color=discord.Color.blue())
        embed.add_field(name="User : ", value=f"<@{row[1]}>", inline=                                                                                                               True)
        embed.add_field(name="Gender: ", value=row[2], inline=False)
        embed.add_field(name="Main mod in contact: ", value=f"<@{row[3]}>", inline=True)
        embed.add_field(name="Date of last follow up: ", value=fmt_date, inline=False)
        embed.add_field(name="Follow-up notes: ", value=row[5], inline=False)

        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="the user is not found! ", color=discord.Color.red()
        )
        await ctx.send(embed=embed)


@bot.command()
async def update(ctx: commands.Context, mem: discord.Member, *, new_notes=None):
    cr.execute("SELECT * FROM REVERTS WHERE revert_id = ?", (mem.id,))
    row = cr.fetchone()
    if row is None:
        print("Couldn't find")
        return

   
    new_notes = new_notes or row[5]
    cr.execute(
        f"""
            UPDATE REVERTS 
            SET mod_id = ? , notes = ? ,date = datetime('now')
            WHERE revert_id = ? 
         """,
        (
            ctx.author.id,
            new_notes,
            mem.id,
        ),
    )
    cr.execute(
        "INSERT INTO HISTORY (revert_id, mod_id, notes, date) VALUES (?,?,?, datetime('now'))",
        (mem.id, ctx.author.id, new_notes),
    )

    connection.commit()


@bot.command()
async def history(ctx: commands.Context, mem: discord.Member):
    cr.execute("SELECT mod_id, date, notes FROM HISTORY WHERE revert_id = ?", (mem.id, ))

    rows = cr.fetchall()

    embed = discord.Embed(title=f"History for")
    embed.colour = discord.Colour.from_rgb(255, 255, 255)
    embed.description = f"<@{mem.id}>"
    for row in rows:
        mod_id, date, notes = row
        date = discord.utils.format_dt(datetime.fromisoformat(date), style="D")
        embed.add_field(name="Mod", value=f"<@{mod_id}> at {date}")
        embed.add_field(name="Note", value=notes, inline=False)

    await ctx.send(embed=embed)


bot.run("MTE0Mzg5OTM3MDI0MTEzODgzMg.Ga6GZx.-AnMH13r2hg7-16U6T8rwYV8XsC0xbwZWHYLY8")
