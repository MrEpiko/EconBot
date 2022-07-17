import disnake
from disnake.ext import commands, tasks
import json

class Economy(commands.Cog, name="Economy"):
 
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["balance"], help="Check balance of a user.")
    async def bal(self, ctx, member:disnake.Member = None):

        user = member or ctx.author

        with open("./databases/balances.json", "r+") as f:
            data = json.load(f)

        users_balance = 0
        if str(user.id) in data:
            users_balance = data[str(user.id)]["balance"]

        await ctx.send(embed=disnake.Embed(title="User's balance", description=f"{user.mention} currently has **{users_balance}$** in their pocket.", color=disnake.Colour.green()))    
        
    @commands.command(help="Change user's balance.")
    @commands.is_owner()
    async def setbalance(self, ctx, member:disnake.Member, amount:int):

        with open("./databases/balances.json", "r+") as f:
            data = json.load(f)

        data[str(member.id)] = {"balance": amount}   

        with open("./databases/balances.json", "w") as fw:
            json.dump(data, fw, indent=4)

        await ctx.send(embed=disnake.Embed(title="Set balance", description=f"Successfully set {member.mention}'s balance to **{amount}$**!", color=disnake.Colour.green()))       

    @commands.command(help="Send user some money.")
    async def pay(self, ctx, member:disnake.Member, amount:int):

        if amount <= 0:
            await ctx.send(embed=disnake.Embed(title="Pay", description=f"{ctx.author.mention}, you can't send that amount of money!", color=disnake.Colour.green()))    
            return

        with open("./databases/balances.json", "r+") as f:
            data = json.load(f)

        senders_balance = 0
        if str(ctx.author.id) in data:
            senders_balance = data[str(ctx.author.id)]["balance"]

        if senders_balance < amount:
            await ctx.send(embed=disnake.Embed(title="Pay", description=f"{ctx.author.mention}, you don't have enough money to complete this transaction! \n\nYou need **{amount - senders_balance}$** more!", color=disnake.Colour.green()))    
            return

        data[str(ctx.author.id)]["balance"] -= amount
        
        receivers_balance = 0
        if str(member.id) in data:
            receivers_balance = data[str(member.id)]["balance"]

        data[str(member.id)] = {"balance": receivers_balance + amount}       

        with open("./databases/balances.json", "w") as fw:
            json.dump(data, fw, indent=4)

        await ctx.send(embed=disnake.Embed(title="Pay", description=f"{ctx.author.mention}, you have successfully sent {member.mention} **{amount}$**!", color=disnake.Colour.green()))       

    @commands.command(help="Purchase something!")
    async def buy(self, ctx, price:int):

        if price <= 0:
            await ctx.send(embed=disnake.Embed(title="Buy", description=f"{ctx.author.mention}, that price is invalid!", color=disnake.Colour.green()))    
            return

        with open("./databases/balances.json", "r+") as f:
            data = json.load(f) 

        balance = 0
        if str(ctx.author.id) in data:
            balance = data[str(ctx.author.id)]["balance"]

        if balance < price: 
            await ctx.send(embed=disnake.Embed(title="Buy", description=f"{ctx.author.mention}, you don't have enough money to complete this transaction! \n\nYou need **{price - balance}$** more!", color=disnake.Colour.green()))    
            return 

        data[str(ctx.author.id)]["balance"] -= price

        with open("./databases/balances.json", "w") as fw:
            json.dump(data, fw, indent=4)

        await ctx.send(embed=disnake.Embed(title="Buy", description=f"{ctx.author.mention}, you have successfully bought a very interesting item for **{price}$**!", color=disnake.Colour.green()))       
    

def setup(bot):
    bot.add_cog(Economy(bot))