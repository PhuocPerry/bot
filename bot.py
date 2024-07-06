import discord
from discord.ext import commands
import asyncio
import requests
from flask import Flask, request

app = Flask(__name__)

# Token của bot Discord của bạn
TOKEN = 'MTI1ODY3ODg2NDU1MzcwOTY1MA.GufZEJ.ktFffalT-t2Wozv3EPyWKpUgViVbsOraHI52sY'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@app.route('/')
def index():
    return "Welcome to the Discord bot web interface!"

@app.route('/checkid', methods=['GET'])
def checkid():
    user_id = request.args.get('user_id')
    if user_id:
        return f"User ID: {user_id}"
    else:
        return "No user ID provided!"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def checkid(ctx):
    user_id = ctx.author.id
    await ctx.send(f"Your ID: {user_id}")

@bot.command()
async def napthe(ctx):
    questions = [
        "Câu hỏi 1: Mệnh giá là?",
        "Câu hỏi 2: Loại thẻ là?",
        "Câu hỏi 3: Serial là?",
        "Câu hỏi 4: Mã thẻ là?"
    ]
    answers = []

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

    user_id = ctx.author.id
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

def run_discord_bot():
    bot.run(TOKEN)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(run_discord_bot())
    app.run(host='0.0.0.0', port=5000)
