import discord
from settings import TOKEN
from discord.ext import commands
from discord import app_commands
import lgoic
import time
import os

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())



@bot.event
async def on_ready():
    print("Bot is Up and Ready!")
    try:
        synched = await bot.tree.sync()
        print(f'Synched {len(synched)} command(s)')
    except Exception as e:
        print(e)

last_message_times = {}

COOLDOWN = 5

@bot.tree.command(name='generate', description='Generate an image.')
async def generate(interaction: discord.Integration, imagedescription: str, width : int, height : int):
    user_id = interaction.user.id
    if user_id in last_message_times:
        elapsed_time = time.time() - last_message_times[user_id]
        if elapsed_time < COOLDOWN:
            await interaction.user.send(
                f"Пожалуйста, подождите {COOLDOWN - elapsed_time:.1f} секунд перед отправкой следующего запроса.")
            return

    last_message_times[user_id] = time.time()

    generatingtext = await interaction.user.send("Генерирую картинку..")

    api = lgoic.Text2ImageAPI('https://api-key.fusionbrain.ai/', '846277557559B13E622645DA5AB58748',
                            '059D5209F8B1ADA3A143688C82563907')
    model_id = api.get_model()
    imagename = imagedescription+".jpg"
    image = api.generate_and_save_image(imagedescription, model_id, imagename,width,height)

    await interaction.user.send(file=discord.File(imagename))

    os.remove(imagename)
    await generatingtext.delete()

@bot.tree.command(name='help', description='What this bot does?')
async def help(interaction: discord.Integration):
    await interaction.response.send_message("Привет! Я бот для генерации картинок. Отправь мне текстовое описание желаемой картинки, и я создам ее. Например, напиши: 'Котик с крыльями ангела, сидящий на облаке' " )








bot.run(token=TOKEN)
