from flask import Flask, request, render_template
import discord
from discord.ext import commands
import asyncio

app = Flask(__name__)
bot = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    global bot
    token = request.form['token']

    bot = commands.Bot(command_prefix="!")

    async def start_bot():
        await bot.login(token)
        await bot.connect()

    asyncio.run(start_bot())
    return f'Logged in as {bot.user}'

@app.route('/send-message', methods=['POST'])
def send_message():
    global bot
    if bot is None:
        return 'Bot is not logged in.'

    channel_id = int(request.form['channelId'])
    message = request.form['message']
    channel = bot.get_channel(channel_id)

    if channel:
        asyncio.run(channel.send(message))
        return 'Message sent successfully!'
    else:
        return 'Channel not found.'

if __name__ == '__main__':
    app.run(debug=True)
