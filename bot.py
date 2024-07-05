import discord
from discord.ext import commands
from discord.ui import Button, View
import requests

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
SERVER_URL = 'YOUR_SERVER_URL'  # URL máy chủ thứ 3 để gửi dữ liệu

bot = commands.Bot(command_prefix='!')

user_data = {}  # Dictionary để lưu thông tin người dùng

class PurchaseView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Có", style=discord.ButtonStyle.green, custom_id="yes_button"))
        self.add_item(Button(label="Không", style=discord.ButtonStyle.red, custom_id="no_button"))

    @discord.ui.button(label="Có", style=discord.ButtonStyle.green)
    async def yes_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Hãy nhập thông tin của bạn:")
        self.user_input = await bot.wait_for('message', check=lambda message: message.author == interaction.user)
        user_data[interaction.user.id] = self.user_input.content
        data_to_send = {
            'user_id': interaction.user.id,
            'user_input': self.user_input.content
        }
        requests.post(SERVER_URL, json=data_to_send)
        await interaction.followup.send(f"Đã lưu thông tin: {self.user_input.content} và gửi đến máy chủ.")

    @discord.ui.button(label="Không", style=discord.ButtonStyle.red)
    async def no_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Bạn đã chọn không mua hàng.")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def mua(ctx):
    await ctx.send("Bạn có muốn mua hàng không?", view=PurchaseView())

bot.run(TOKEN)
