import discord
from discord.ext import commands

import asyncio
import requests

TOKEN = ''

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

declared_value = ""
telco = ""
serial = ""
code = ""

question_declared_value = f"Câu hỏi 1: Mệnh giá là? ( {declared_value})"
question_telco = f"Câu hỏi 2: Loại thẻ là? ( {telco})"
question_serial = f"Câu hỏi 3: Serial là? ( {serial})"
question_code = f"Câu hỏi 4: Mã thẻ là? ( {code})"

questions = [
    question_declared_value,
    question_telco,
    question_serial,
    question_code
]

answers = []

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def napthe(ctx):
    answers.clear()

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for question in questions:
        await ctx.send(question)
        try:
            message = await bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send('Bạn đã không trả lời kịp thời. Hãy thử lại.')
            return
        answers.append(message.content)

    # Lấy ID của người gửi
    user_id = ctx.author.id

    # Gửi dữ liệu qua URL của bạn
    url = 'https://mineperry.online/napthebot.php'
    params = {
        'user_id': user_id,
        'declared_value': answers[0],
        'telco': answers[1],
        'serial': answers[2],
        'code': answers[3]
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        await ctx.send("Dữ liệu đã được gửi thành công đến web PHP.")
    except requests.exceptions.RequestException as e:
        await ctx.send(f"Có lỗi xảy ra khi gửi dữ liệu: {e}")

@bot.command()
async def checkid(ctx):
    embed = discord.Embed(
        title=f"Your Discord ID",
        description=f"ID: {ctx.author.id}",
        color=discord.Color.dark_blue()
    )
    await ctx.send(embed=embed)

bot.run(TOKEN)
