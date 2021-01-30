def mention_by_id(member_id):
    return f'<@{member_id}>'

async def retrieve_user(bot, member_id):
    user = await bot.get_user(member_id)
    if user is None:
        user = await bot.fetch_user(member_id)
    return user