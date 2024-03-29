import asyncio
import discord

async def paginate_embed(bot, ctx, pages):
    total_pages = len(pages)
    cur_page = 1
    cur_embed = pages[0]
    help_note = 'Click on ◀️▶️ to scroll pages. Click on ❌ to close help menu\nClick 📌 to keep current page (Expires in 60s otherwise)'
    cur_embed.set_footer(text=f'Page: {cur_page}/{total_pages}\n{help_note}')
    message = await ctx.send(embed=cur_embed)
    # getting the message object for editing and reacting

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")
    await message.add_reaction("📌")
    await message.add_reaction("❌")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️", "📌", "❌"] and reaction.message == message
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

            if str(reaction.emoji) == "▶️" and cur_page != total_pages:
                cur_page += 1
                cur_embed = pages[cur_page-1]
                cur_embed.set_footer(text=f'Page: {cur_page}/{total_pages}\n{help_note}')
                await message.edit(embed=cur_embed)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                cur_embed = pages[cur_page-1]
                cur_embed.set_footer(text=f'Page: {cur_page}/{total_pages}\n{help_note}')
                await message.edit(embed=cur_embed)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "❌":
                raise asyncio.TimeoutError
            elif str(reaction.emoji) == "📌":
                await message.remove_reaction(reaction, user)
                await message.remove_reaction("❌", bot.user)
                await message.remove_reaction("◀️", bot.user)
                await message.remove_reaction("▶️", bot.user)
                break
            else:
                await message.remove_reaction(reaction, user)
                # removes reactions if the user tries to go forward on the last page or
                # backwards on the first page
        except asyncio.TimeoutError:
            await message.delete()
            break
            # ending the loop if user doesn't react after x seconds

async def send_temp_embed(bot, ctx, embed, discord_file=None):
    extra_footer = f'\nExpires in 60s\nClick 📌 to keep it here or ❌ to close it'
    embed.set_footer(text=extra_footer)
    if discord_file is None:
        message = await ctx.send(embed=embed)
    else:
        message = await ctx.send(embed=embed, file=discord_file)

    await message.add_reaction("📌")
    await message.add_reaction("❌")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["📌", "❌"] and reaction.message == message
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example
            if str(reaction.emoji) == "📌":
                await message.remove_reaction(reaction, user)
                await message.remove_reaction("❌", bot.user)
                break
            elif str(reaction.emoji) == "❌":
                await message.remove_reaction(reaction, user)
                raise asyncio.TimeoutError
            else:
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await message.delete()
            break

async def send_game_embed_misc(ctx, title, description):
    embed = discord.Embed(title=title, description=description, colour=discord.Colour.purple())
    embed.set_footer(text=f'@{ctx.author.name}')
    await ctx.send(embed=embed)

async def send_action_embed(ctx, title, description, footer, color):
    embed = discord.Embed(title=title, description=description, colour=color)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_footer(text=footer)
    await ctx.send(embed=embed)