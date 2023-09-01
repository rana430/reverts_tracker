import sqlite3
from datetime import datetime

import discord
import matplotlib.pyplot as plt
from decouple import config
from discord.ext import commands

connection = sqlite3.connect("db/reverts_database.db")
cr = connection.cursor()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.add_cog(MyCog(bot))


class MyCog(commands.Cog, name="btengan"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        return await commands.has_role(884918189727825960).predicate(ctx)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, err: commands.CommandError):
        if isinstance(err, commands.MissingRole):
            embed = discord.Embed(description="❌ **Sorry you are not a mod **", color=discord.Color.red())
            await ctx.send(embed=embed)

        elif isinstance(err, commands.MissingRequiredArgument):
            embed = discord.Embed(description="❌ **You didn't provide the user **", color=discord.Color.red())
            await ctx.send(embed=embed)

        else:
            raise err

    @commands.command()
    async def add(self, ctx: commands.Context, mem: discord.Member, *, notes=None):
        is_male = discord.utils.get(mem.roles, id=884923006319734814) != None
        username = mem.global_name or str(mem)
        cr.execute(
            f"""
            SELECT * FROM REVERTS WHERE revert_id = ? ;
            """,
            (mem.id,),
        )
        row = cr.fetchone()

        if row is not None:
            embed = discord.Embed(description="**This user has been recorded already ** ", color=discord.Color.red())
            await ctx.send(embed=embed)

            return

        cr.execute(
            f"""
                INSERT INTO REVERTS (revert_id, gender, mod_id, notes, date) VALUES (?, ?, ?, ?, datetime('now'));
            """,
            (mem.id, "Male" if is_male else "Female", ctx.author.id, notes),
        )
        cr.execute(
            "INSERT INTO HISTORY (revert_id, mod_id, notes, date) VALUES (?, ?, ?, datetime('now'));",
            (mem.id, ctx.author.id, notes),
        )
        connection.commit()
        embed = discord.Embed(description="✅ **Added user successfully**", color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx: commands.Context, mem: discord.Member):
        cr.execute("SELECT * FROM REVERTS WHERE revert_id = ?;", (mem.id,))
        row = cr.fetchone()

        fmt_date = discord.utils.format_dt(datetime.fromisoformat(row[4]), style="D")

        if row:
            embed = discord.Embed(title="User Information: ", color=discord.Color.blue())
            embed.add_field(name="User : ", value=f"<@{row[1]}>", inline=True)
            embed.add_field(name="Gender: ", value=row[2], inline=False)
            embed.add_field(name="Main mod in contact: ", value=f"<@{row[3]}>", inline=True)
            embed.add_field(name="Date of last follow up: ", value=fmt_date, inline=False)
            embed.add_field(name="Follow-up notes: ", value=row[5], inline=False)

            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="the user is not found! ", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command()
    async def update(self, ctx: commands.Context, mem: discord.Member, *, new_notes=None):
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
        embed = discord.Embed(description="✅ **The user has been updated successfully**", color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command()
    async def history(self, ctx: commands.Context, mem: discord.Member):
        cr.execute("SELECT mod_id, date, notes FROM HISTORY WHERE revert_id = ?", (mem.id,))

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


@bot.command(name="graphs")
async def graphs(ctx: commands.Context):
    cr.execute("SELECT gender, count(gender) FROM REVERTS GROUP BY gender;")
    rows = cr.fetchall()
    genders = [item[0] for item in rows]
    counts = [item[1] for item in rows]
    colors = ["#F79BD3", "#91C8E4"]
    plt.pie(counts, labels=genders, autopct="%1.1f%%", startangle=140, colors=colors)
    plt.axis("equal")
    plt.title("Reverts statistics")
    plt.savefig("plot.png")
    embed = discord.Embed(
        title="Graph Embed", description="This is a graph generated by the bot.", color=discord.Color.blue()
    )
    file = discord.File("plot.png", filename="plot.png")
    embed.set_image(url="attachment://plot.png")
    await ctx.send(embed=embed, file=file)


bot.run(config("BOT_TOKEN"))
