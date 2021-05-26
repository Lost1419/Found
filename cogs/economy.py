import aiosqlite
import discord
import random
import time
from discord.ext import commands


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    @commands.command()
    async def start(self, ctx):
        async with aiosqlite.connect('economy.db') as db:
            data = await db.execute(f"SELECT id FROM player where id={ctx.author.id}")
            rows = await data.fetchall()

            if rows == []:
                await db.execute(f"INSERT INTO player VALUES ({ctx.author.id}, 100, 0)")
                bankgrab = await db.execute(f"SELECT bank FROM player where id={ctx.author.id}")
                cashgrab = await db.execute(f"SELECT cash FROM player where id={ctx.author.id}")

                cash = await cashgrab.fetchone()
                bank = await bankgrab.fetchone()
                bankEmbed = discord.Embed(title=f"{ctx.author.name}'s Vault", color=0x818ca1, description=f"<:cashs:846266738067767326> **Cash**: {cash[0]}\n<:banks:846267878827491338> **Bank**: {bank[0]}")

                bankEmbed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send("Your character has been created!!!", embed=bankEmbed)
                
                await db.commit()
            else:
                await ctx.send("You already have a character created. Try using `!bank`!")
    

    @commands.command(aliases=['dep', 'depo'])
    async def deposit(self, ctx, amount):
        async with aiosqlite.connect('economy.db') as db:
            data = await db.execute(f"SELECT id FROM player where id={ctx.author.id}")
            rows = await data.fetchall()

            if rows == []:
                await ctx.send("You currently don't have an character. Use `!start` to make a character!")
            else:
                bankgrab = await db.execute(f"SELECT bank FROM player where id={ctx.author.id}")
                cashgrab = await db.execute(f"SELECT cash FROM player where id={ctx.author.id}")
                cash = await cashgrab.fetchone()
                bank = await bankgrab.fetchone()

                if amount.lower() == "all":
                    await db.execute(f"UPDATE player SET cash=0, bank={cash[0] + bank[0]} WHERE id={ctx.author.id}")
                    await ctx.send(f"**<:cashs:846266738067767326> {cash[0]}** has been deposited into your <:banks:846267878827491338> bank!")
                
                    await db.commit()
                
                else:
                    if cash[0] >= int(amount):

                        await db.execute(f"UPDATE player SET cash={cash[0] - int(amount)}, bank={int(amount) + bank[0]} WHERE id={ctx.author.id}")
                        await ctx.send(f"**<:cashs:846266738067767326> {amount}** has been deposited into your <:banks:846267878827491338> bank!")
                    
                        await db.commit()

                    elif cash[0] < int(amount):
                        await ctx.send("You don't have that much money noob.")
                    
                    else:
                        await ctx.send("What are you even trying to do???")
    

    @commands.command(aliases=['with', 'draw'])
    async def withdraw(self, ctx, amount):
        async with aiosqlite.connect('economy.db') as db:
            data = await db.execute(f"SELECT id FROM player where id={ctx.author.id}")
            rows = await data.fetchall()

            if rows == []:
                await ctx.send("You currently don't have an character. Use `!start` to make a character!")
            else:
                bankgrab = await db.execute(f"SELECT bank FROM player where id={ctx.author.id}")
                cashgrab = await db.execute(f"SELECT cash FROM player where id={ctx.author.id}")
                cash = await cashgrab.fetchone()
                bank = await bankgrab.fetchone()

                if amount.lower() == "all":
                    await db.execute(f"UPDATE player SET cash={cash[0] + bank[0]}, bank=0 WHERE id={ctx.author.id}")
                    await ctx.send(f"**<:cashs:846266738067767326> {bank[0]}** has been withdrawen from your <:banks:846267878827491338> bank!")
                
                    await db.commit()
                
                else:
                    if bank[0] >= int(amount):

                        await db.execute(f"UPDATE player SET cash={cash[0] + int(amount)}, bank={bank[0] - int(amount)} WHERE id={ctx.author.id}")
                        await ctx.send(f"**<:cashs:846266738067767326> {amount}** has been withdrawen from your <:banks:846267878827491338> bank!")
                    
                        await db.commit()

                    elif cash[0] < int(amount):
                        await ctx.send("You don't have that much money noob.")
                    
                    else:
                        await ctx.send("What are you even trying to do???")
    

    @commands.command()
    async def bank(self, ctx, user: discord.Member=None):
        if user == None:
            async with aiosqlite.connect('economy.db') as db:
                data = await db.execute(f"SELECT id FROM player where id={ctx.author.id}")
                rows = await data.fetchall()

                if rows == []:
                    await ctx.send("You currently don't have an character. Use `!start` to make a character!")

                else:
                    bankgrab = await db.execute(f"SELECT bank FROM player where id={ctx.author.id}")
                    cashgrab = await db.execute(f"SELECT cash FROM player where id={ctx.author.id}")

                    cash = await cashgrab.fetchone()
                    bank = await bankgrab.fetchone()

                    embed = discord.Embed(title=f"{ctx.author.name}'s Valt", color=0x818ca1, description=f"<:cashs:846266738067767326> **Cash**: {cash[0]}\n<:banks:846267878827491338> **Bank**: {bank[0]}")
                    embed.set_thumbnail(url=ctx.author.avatar_url)

                    await ctx.send(embed=embed)
        
        else:
            async with aiosqlite.connect('economy.db') as db:
                data = await db.execute(f"SELECT id FROM player where id={ctx.author.id}")
                rows = await data.fetchall()

                if rows == []:
                    await ctx.send("That user doesn't have a character.")

                else:
                    bankgrab = await db.execute(f"SELECT bank FROM player where id={user.id}")
                    cashgrab = await db.execute(f"SELECT cash FROM player where id={user.id}")

                    cash = await cashgrab.fetchone()
                    bank = await bankgrab.fetchone()

                    embed = discord.Embed(title=f"{user.name}'s Valt", color=0x818ca1, description=f"<:cashs:846266738067767326> **Cash**: {cash[0]}\n<:banks:846267878827491338> **Bank**: {bank[0]}")
                    embed.set_thumbnail(url=user.avatar_url)

                    await ctx.send(embed=embed)
    

    @commands.command(aliases=['w', 'wrk'])
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        async with aiosqlite.connect('economy.db') as db:
            data = await db.execute(f"SELECT id FROM player where id={ctx.author.id}")
            rows = await data.fetchall()

            if rows == []:
                await ctx.send("You currently don't have an character. Use `!start` to make a character!")
            else:
                bankgrab = await db.execute(f"SELECT bank FROM player where id={ctx.author.id}")
                cashgrab = await db.execute(f"SELECT cash FROM player where id={ctx.author.id}")
                cash = await cashgrab.fetchone()
                bank = await bankgrab.fetchone()

                responses = ["You worked as a volunteer at a hostpital and they gave you ", "You work at a car wash and they pay you ", "You cleaned all your neigbors yards and got ", "You went around fixing people's computers and were given "]
                amount = random.randrange(1000, 2000)

                await db.execute(f"UPDATE player SET cash={cash[0] + int(amount)} WHERE id={ctx.author.id}")
                await ctx.send(f"{random.choice(responses)} <:cashs:846266738067767326> {amount}.")

                await db.commit()
    
    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, ctx, amount: int):
        async with aiosqlite.connect('economy.db') as db:
            data = await db.execute(f"SELECT id FROM player where id={ctx.author.id}")
            rows = await data.fetchall()

            if rows == []:
                await ctx.send("You currently don't have an character. Use `!start` to make a character!")

            else:
                cashgrab = await db.execute(f"SELECT cash FROM player where id={ctx.author.id}")
                cash = await cashgrab.fetchone()

                if cash[0] >= amount:
                    choices = ['heads', 'tails']
                    
                    odds = random.randrange(1, 2)

                    chances = random.choice(choices)
                    player_choice = random.choice(choices)

                    await ctx.send(f"<:coin:846904863325814805> You flip a coin and choose {player_choice} <:coin:846904863325814805>")
                    time.sleep(1.2)

                    if chances == player_choice and odds == 1:
                        await ctx.send(f"<:coin:846904863325814805> You got {player_choice} and got x2 as much, you got <:cashs:846266738067767326> {amount * 2} <:coin:846904863325814805>")
                        await db.execute(f"UPDATE player SET cash={cash[0] + int(amount * 2)} WHERE id={ctx.author.id}")

                        await db.commit()

                    else:
                        if player_choice == "heads":
                            await ctx.send(f"You got tails and lost all your money.")
                        else:
                            await ctx.send(f"Yoou got heads and lost all your money.")

                        await db.execute(f"UPDATE player SET cash={cash[0] - int(amount)} WHERE id={ctx.author.id}")

                        await db.commit()
                
                else:
                    await ctx.send(f"You don't have <:cashs:846266738067767326> {amount} you fool.")
        

    @commands.command()
    async def slots(self, ctx, amount: int):
        async with aiosqlite.connect('economy.db') as db:
            data = await db.execute(f"SELECT id FROM player where id={ctx.author.id}")
            rows = await data.fetchall()

            if rows == []:
                await ctx.send("You currently don't have an character. Use `!start` to make a character!")

            else:
                cashgrab = await db.execute(f"SELECT cash FROM player where id={ctx.author.id}")
                cash = await cashgrab.fetchone()

                if cash[0] >= amount:
                    choices = ['❤️', '🔷', '⭐']

                    first = random.choice(choices)
                    second = random.choice(choices)
                    third = random.choice(choices)

                    await ctx.send(f"<:coin:846904863325814805> You pull the lever... <:coin:846904863325814805>")
                    time.sleep(1.2)

                    if first == second and second == third:
                        await ctx.send(f"<:coin:846904863325814805> You got `|{first}|{second}|{third}|` and got <:cashs:846266738067767326> {amount * 2}. Thats x2 as much!! <:coin:846904863325814805>")
                        
                        await db.execute(f"UPDATE player SET cash={cash[0] + int(amount * 2)} WHERE id={ctx.author.id}")
                        await db.commit()

                    elif first == second or second == third or first == third:
                        await ctx.send(f"🎊 You got `|{first}|{second}|{third}|` and got <:cashs:846266738067767326> {int(amount * 1.5)}. Thats x1.5 as much!! 🎉")

                        await db.execute(f"UPDATE player SET cash={cash[0] + int(amount * 1.5)} WHERE id={ctx.author.id}")
                        await db.commit()
                    
                    else:
                        await ctx.send(f"Looks like todays your unlucky day. You got `|{first}|{second}|{third}|` and lost all You money.")

                        await db.execute(f"UPDATE player SET cash={cash[0] - int(amount)} WHERE id={ctx.author.id}")
                        await db.commit()
                
                else:
                    await ctx.send(f"You don't have <:cashs:846266738067767326> {amount} you fool.")


    @commands.command(aliases=['r', 'take'])
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def rob(self, ctx, user: discord.Member):
        async with aiosqlite.connect('economy.db') as db:
            data = await db.execute(f"SELECT id FROM player where id={ctx.author.id}")
            rows = await data.fetchall()

            data2 = await db.execute(f"SELECT id FROM player where id={user.id}")
            rows2 = await data2.fetchall()

            if rows == []:
                await ctx.send("You currently don't have an character. Use `!start` to make a character!")

            elif rows2 == []:
                await ctx.send(f"{user.mention} does not have a character.")

            else:
                cashgrab = await db.execute(f"SELECT cash FROM player where id={ctx.author.id}")
                cash = await cashgrab.fetchone()

                Usercashgrab = await db.execute(f"SELECT cash FROM player where id={user.id}")
                Usercash = await Usercashgrab.fetchone()

                if cash[0] >= 500:
                    chances = random.randrange(1, 2)

                    if chances == 2 and Usercash[0] >= 500:
                        amount = random.randrange(500, Usercash[0])

                        await db.execute(f"UPDATE player SET cash={cash[0] - int(amount)} WHERE id={user.id}")
                        await ctx.send(f"{ctx.author.emention}, you have stolen <:cashs:846266738067767326> {amount} from {user.mention}.")

                        await db.commit()

                    elif Usercash[0] < 500:
                        await ctx.send(f"Stop trying to rob a poor person {ctx.author.mention}")

                    else:
                        await db.execute(f"UPDATE player SET cash={cash[0] - 500} WHERE id={ctx.author.id}")

                        await ctx.send(f"You were caught trying to rob {user.mention} and had to pay them <:cashs:846266738067767326> 500. Don't rob people next time.")

                        await db.commit()
                
                else:
                    await ctx.send("You need to have <:cashs:846266738067767326> 500 in cash before you can rob someone.")

    
    @commands.command()
    async def shop(self, ctx):
        async with aiosqlite.connect('economy.db') as db:
            data = await db.execute(f"SELECT * FROM shop")
            shop = await data.fetchall()

            if shop == []:
                await ctx.send("Shop could not be loaded.")

            else:
                feild_desc = f""

                for item in shop:
                    effects_id = await db.execute(f"SELECT effect_id FROM shop WHERE item_id={item[0]}")
                    effect_id = await effects_id.fetchone()

                    grab_mul = await db.execute(f"SELECT effect FROM effects WHERE id={effect_id[0]}")
                    mul = await grab_mul.fetchone()

                    feild_desc += f"`{item[0]}` | **{item[1].title()}** | <:cashs:846266738067767326> {item[2]}\n   *<:cashs:846266738067767326> x{mul[0]}*\n"
                
                embed = discord.Embed(title=f"Shop", color=0x818ca1, description="A shop to buy all your items in!")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.add_field(name="Items", value=feild_desc, inline=True)

                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Economy(bot))
