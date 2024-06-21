import discord
from settings import TOKEN
from discord.ext import commands
from discord import app_commands
import lgoic

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())



@bot.event
async def on_ready():
    print("Bot is Up and Ready!")
    try:
        synched = await bot.tree.sync()
        print(f'Synched {len(synched)} command(s)')
    except Exception as e:
        print(e)


@bot.event
async def on_message(message):
    if message.author != bot.user:
        await message.author.send("Generating image, please wait.")

        api = lgoic.Text2ImageAPI('https://api-key.fusionbrain.ai/', 'key',
                            'secret key')
        model_id = api.get_model()
        imagename = message.content+".jpg"
        image = api.generate_and_save_image(message, model_id, imagename)

        await message.author.send(file=discord.File(imagename))


bot.run(token=TOKEN)
