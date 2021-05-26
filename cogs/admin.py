import aiosqlite
import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, module: str):
        try:
            self.bot.load_extension(f"cogs.{module.lower()}")

            await ctx.send(f"**{module.title()}** has been loaded.")
        except Exception as e:
            await ctx.send(f"**{module.title()}** could not be reloaded.")


    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, module: str):
        try:
            self.bot.unload_extension(f"cogs.{module.lower()}")

            await ctx.send(f"**{module.title()}** has been unloaded.")
        except Exception as e:
            await ctx.send(f"**{module.title()}** could not be reloaded.")


    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, module: str):
        try:
            if module.lower() == 'all':
                extensions = ["cogs.normal", "cogs.admin", "cogs.events", "cogs.economy"]
                for i in extensions:
                    self.bot.reload_extension(i)
                
                await ctx.send(f"All modules have been reloaded.")
            else:
                if module.lower() == 'eco':
                    self.bot.reload_extension(f"cogs.economy")
                else:
                    self.bot.reload_extension(f"cogs.{module.lower()}")
                    await ctx.send(f"**{module.title()}** has been reloaded.")

        except Exception as e:
            await ctx.send(f"**{module.title()}** could not be reloaded.")
    

    @commands.command(hidden=True)
    @commands.is_owner()
    async def create(self, ctx, table: str):
        async with aiosqlite.connect('economy.db') as db:

            if table == 'shop':
                await db.execute('''CREATE TABLE IF NOT EXISTS shop (item_id int, item_name text, price int, effect_id int)''')
                await db.commit()

            elif table == 'player':
                await db.execute('''CREATE TABLE IF NOT EXISTS player (id int, cash int, bank int)''')
                await db.commit()
            
            elif table == 'effects':
                await db.execute('''CREATE TABLE IF NOT EXISTS effects (id int, effect int, name text)''')
                await db.commit()

            await ctx.send("Table created!")
    

    @commands.command(hidden=True)
    @commands.is_owner()
    async def delete(self, ctx, table: str):
        async with aiosqlite.connect('economy.db') as db:

            if table == 'shop':
                await db.execute('''DROP TABLE IF EXISTS shop''')
                await db.commit()

            elif table == 'player':
                await db.execute('''DROP TABLE IF EXISTS player''')
                await db.commit()
            
            elif table == 'effects':
                await db.execute('''DROP TABLE IF EXISTS effects''')
                await db.commit()

            await ctx.send("Table deleted!")
    

    @commands.command(hidden=True)
    @commands.is_owner()
    async def effectcreate(self, ctx, effect_id, effect, effect_name: str):    
        async with aiosqlite.connect('economy.db') as db:
            realgrab = await db.execute(f"SELECT id FROM effects where id={effect_id}")
            real = await realgrab.fetchall()

            if real == []:
                await db.execute(f"INSERT INTO effects(id, effect, name) VALUES (?, ?, ?)", (effect_id, effect, effect_name))
                data = await db.execute(f"SELECT id FROM effects where id={effect_id}")
                rows = await data.fetchall()

                if rows == []:
                    await ctx.send("Effect could not be created sorry.")
                
                else:
                    effect_id_grab = await db.execute(f"SELECT id FROM effects where id={effect_id}")
                    effect_name_grab = await db.execute(f"SELECT name FROM effects where id={effect_id}")
                    effect_grab = await db.execute(f"SELECT effect FROM effects where id={effect_id}")

                    effect_id_real = await effect_id_grab.fetchone()
                    effect_name_real = await effect_name_grab.fetchone()
                    effect_real = await effect_grab.fetchone()

                    await db.commit()
                    await ctx.send(f"Effect **{effect_name_real[0].title()}** has been created with Id `{effect_id_real[0]}`. It has the effect <:cashs:846266738067767326> x{effect_real[0]}")
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def effectremove(self, ctx, effect_id):    
        async with aiosqlite.connect('economy.db') as db:
            realgrab = await db.execute(f"SELECT id FROM effects where id={effect_id}")
            real = await realgrab.fetchall()

            if real == []:
                await ctx.send("There is no effect with that Id.")

            else:
                await db.execute(f"DELETE FROM effects WHERE id={effect_id}")

                data = await db.execute(f"SELECT id FROM effects where id={effect_id}")
                rows = await data.fetchall()

                if rows == []:
                    await ctx.send("Effect has been deleted!")

                    await db.commit()
                
                else:
                    await ctx.send(f"Effect could not be deleted.")
    

    @commands.command(hidden=True)
    @commands.is_owner()
    async def effects(self, ctx):
        async with aiosqlite.connect('economy.db') as db:
            data = await db.execute(f"SELECT * FROM effects")
            effects = await data.fetchall()

            if effects == []:
                await ctx.send("Effects could not be loaded.")

            else:
                feild_desc = f""

                for effect in effects:
                    feild_desc += f"`{effect[0]}` | **{effect[2].title()}** | <:cashs:846266738067767326> x{effect[1]}\n"
                
                embed = discord.Embed(title=f"Shop", color=0x818ca1, description="All the effects")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.add_field(name="Items", value=feild_desc, inline=True)

                await ctx.send(embed=embed)
                


    @commands.command(hidden=True)
    @commands.is_owner()
    async def itemadd(self, ctx, id_item: int, name_item: str, price_item: int, effect_item: int):
        async with aiosqlite.connect('economy.db') as db:
            realgrab = await db.execute(f"SELECT item_id FROM shop where item_id={id_item}")
            real = await realgrab.fetchall()

            if real == []:
                await db.execute(f"INSERT INTO shop(item_id, item_name, price, effect_id) VALUES (?, ?, ?, ?)", (id_item, name_item, price_item, effect_item))

                data = await db.execute(f"SELECT item_id FROM shop where item_id={id_item}")
                rows = await data.fetchall()

                effects = await db.execute(f"SELECT effect_id FROM shop where item_id={id_item}")
                effect = await effects.fetchone()

                real_effects = effects = await db.execute(f"SELECT id FROM effects where id={effect_item}")
                real_effect = await real_effects.fetchone()

                if rows == []:
                    await ctx.send(f"Item could not be created... sorry.")

                else:
                    if effect[0] == real_effect[0]:
                        item_id_grab = await db.execute(f"SELECT item_id FROM shop where item_id={id_item}")
                        item_name_grab = await db.execute(f"SELECT item_name FROM shop where item_id={id_item}")
                        item_price_grab = await db.execute(f"SELECT price FROM shop where item_id={id_item}")
                        work_grab = effects = await db.execute(f"SELECT effect FROM effects where id={effect_item}")

                        working = await work_grab.fetchone()
                        item_id = await item_id_grab.fetchone()
                        item_name = await item_name_grab.fetchone()
                        item_price = await item_price_grab.fetchone()

                        await db.commit()
                        await ctx.send(f"Item {item_name[0].title()} has been created with a price of {item_price[0]} and an Id of {item_id[0]}. It has an effect of <:cashs:846266738067767326> x{working[0]}")

                    else:
                        await ctx.send("Thats not a real effect id.")

            else:
                await ctx.send(f"An item with that Id is already a thing. {real}")
        
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def itemremove(self, ctx, id_item: int):
        async with aiosqlite.connect('economy.db') as db:
            realgrab = await db.execute(f"SELECT item_id FROM shop where item_id={id_item}")
            real = await realgrab.fetchone()

            if real == ():
                await ctx.send("There is no item with that Id.")
                
            else:
                await db.execute(f"DELETE FROM shop WHERE item_id={id_item}")

                data = await db.execute(f"SELECT item_id FROM shop where item_id={id_item}")
                rows = await data.fetchall()

                await db.commit()

                if rows == []:
                    await ctx.send("Item has been deleted!")
                

                else:
                    await ctx.send(f"Item could not be deleted.")
        

    @commands.command(hidden=True, aliases=['ads','aset'])
    @commands.is_owner()
    async def adminset(self, ctx, user: discord.Member, cash: int, bank: int):
        async with aiosqlite.connect('economy.db') as db:

            await db.execute(f"UPDATE player SET cash={cash}, bank={bank} WHERE id={user.id}")
            await db.commit()

            await ctx.send(f"{user.mention} account has been set to <:cashs:846266738067767326> {cash} and <:banks:846267878827491338> {bank}.")
    

    @commands.command(hidden=True, aliases=['aa','aadd', 'admina'])
    @commands.is_owner()
    async def adminadd(self, ctx, user: discord.Member, cash: int, bank: int):
        async with aiosqlite.connect('economy.db') as db:
            bankgrab = await db.execute(f"SELECT bank FROM player where id={user.id}")
            cashgrab = await db.execute(f"SELECT cash FROM player where id={user.id}")

            acash = await cashgrab.fetchone()
            abank = await bankgrab.fetchone()

            await db.execute(f"UPDATE player SET cash={acash[0] + cash}, bank={abank[0] + bank} WHERE id={user.id}")
            await db.commit()

            await ctx.send(f"<:cashs:846266738067767326> {cash} and<:banks:846267878827491338> {bank} have been added to {user.mention} character.")


    @commands.command(hidden=True, aliases=['asub','admins', 'as'])
    @commands.is_owner()
    async def adminsubtract(self, ctx, user: discord.Member, cash: int, bank: int):
        async with aiosqlite.connect('economy.db') as db:
            bankgrab = await db.execute(f"SELECT bank FROM player where id={user.id}")
            cashgrab = await db.execute(f"SELECT cash FROM player where id={user.id}")

            acash = await cashgrab.fetchone()
            abank = await bankgrab.fetchone()

            if int(acash[0] - cash) < 0 or int(abank[0] - bank) < 0:
                await ctx.send("You can't give a user negative money")

            else:
                await db.execute(f"UPDATE player SET cash={acash[0] - cash}, bank={abank[0] - bank} WHERE id={user.id}")
                await db.commit()

                await ctx.send(f"<:cashs:846266738067767326> {cash} and<:banks:846267878827491338> {bank} have been removed to {user.mention} character.")
    

    @commands.command(hidden=True, aliases=['act', 'ac'])
    @commands.is_owner()
    async def activtiy(self, ctx, new_type: str, new_status: str, *, new_name: str):

        if new_type.lower() == 'gameing':

            if new_status.lower() == 'idle':
                activity = discord.Game(name=new_name)
                await self.bot.change_presence(status=discord.Status.idle, activity=activity)
            
            elif new_status.lower() == 'online':
                activity = discord.Game(name=new_name)
                await self.bot.change_presence(status=discord.Status.online, activity=activity)
            
            elif new_status.lower() == 'offline':
                activity = discord.Game(name=new_name)
                await self.bot.change_presence(status=discord.Status.invisible, activity=activity)
            
            elif new_status.lower() == 'busy' or new_status.lower() == 'dnd':
                activity = discord.Game(name=new_name)
                await self.bot.change_presence(status=discord.Status.dnd, activity=activity)
        
        elif new_type.lower() == 'watching':

            if new_status.lower() == 'idle':
                activity = discord.Activity(type=discord.ActivityType.watching, name=new_name)
                await self.bot.change_presence(status=discord.Status.idle, activity=activity)
            
            elif new_status.lower() == 'online':
                activity = discord.Activity(type=discord.ActivityType.watching, name=new_name)
                await self.bot.change_presence(status=discord.Status.online, activity=activity)
            
            elif new_status.lower() == 'offline':
                activity = discord.Activity(type=discord.ActivityType.watching, name=new_name)
                await self.bot.change_presence(status=discord.Status.invisible, activity=activity)
            
            elif new_status.lower() == 'busy' or new_status.lower() == 'dnd':
                activity = discord.Activity(type=discord.ActivityType.watching, name=new_name)
                await self.bot.change_presence(status=discord.Status.dnd, activity=activity)
        
        elif new_type.lower() == 'listening':

            if new_status.lower() == 'idle':
                activity = discord.Activity(type=discord.ActivityType.listening, name=new_name)
                await self.bot.change_presence(status=discord.Status.idle, activity=activity)
            
            elif new_status.lower() == 'online':
                activity = discord.Activity(type=discord.ActivityType.listening, name=new_name)
                await self.bot.change_presence(status=discord.Status.online, activity=activity)
            
            elif new_status.lower() == 'offline':
                activity = discord.Activity(type=discord.ActivityType.listening, name=new_name)
                await self.bot.change_presence(status=discord.Status.invisible, activity=activity)
            
            elif new_status.lower() == 'busy'or new_status.lower() == 'dnd':
                activity = discord.Activity(type=discord.ActivityType.listening, name=new_name)
                await self.bot.change_presence(status=discord.Status.dnd, activity=activity)

        await ctx.send(f"{self.bot.user.mention} activity has been to changed to {new_type.title()} with the name {new_name} and has the status {new_status.title()}")


def setup(bot):
    bot.add_cog(Admin(bot))
