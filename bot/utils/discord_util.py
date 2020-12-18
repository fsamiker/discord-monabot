import asyncio

async def paginate_embed(bot, ctx, pages):
    total_pages = len(pages)
    cur_page = 1
    cur_embed = pages[0]
    help_note = 'Click on ◀️▶️ to scroll pages. Click on ❌ to close help menu'
    cur_embed.set_footer(text=f'Page: {cur_page}/{total_pages}\n{help_note}')
    message = await ctx.send(embed=cur_embed)
    # getting the message object for editing and reacting

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")
    await message.add_reaction("❌")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️", "❌"] and reaction.message == message
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
            else:
                await message.remove_reaction(reaction, user)
                # removes reactions if the user tries to go forward on the last page or
                # backwards on the first page
        except asyncio.TimeoutError:
            await message.delete()
            break
            # ending the loop if user doesn't react after x seconds