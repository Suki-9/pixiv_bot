import re
import discord
from typing import List
from pixivpy3 import PixivError
from bot import client, tree
from bot.message import gen_post
from modules import logger, config, database, pixiv


async def sendOkResponse(channel: discord.TextChannel, title: str = '', description: str = '', embed: discord.Embed | None = None, files: List[discord.File] = []) -> None: # type: ignore
  logger.success('pixiv_bot.action', f'Send message.')
  return await channel.send(
    embed = discord.Embed(
      color = 0x14c900,
      title = title,
      description = description
    ) if embed == None else embed,
    files=files,
    ephemeral = True
  )

async def sendErrResponse(channel: discord.TextChannel, type: str = 'Unknown', description: str = '', embed: discord.Embed | None = None, files: List[discord.File] = []) -> None:
  logger.err('pixiv_bot.action', f'Send error message.')
  return await channel.send(
    embed=discord.Embed(
      color = 0xff0000,
      title = f'{type} error',
      description = description
    ) if embed == None else embed,
    files=files,
    ephemeral = True
  )

@client.event
async def on_ready():
  logger.info('pixiv_bot.event', 'on_ready')
  await tree.sync()

@client.event
async def on_message(message: discord.Message):
  if message.author.bot:
    return

  logger.info('pixiv_bot.event', 'on_message')
  
  if message.channel.id in (config.get('auto_archive_enable_channels') or []):
    for link in re.findall(r'https://www.pixiv.net/artworks/[0-9]+', message.content):
      user = database.user_db.get(message.author.id)

      if user == None or user['user_id'] == None: continue

      try:
        meta_data = pixiv.archive(user['pixiv_token'], link)

        await message.channel.send(**gen_post(meta_data, files = [
          discord.File(fp=meta_data['archive_path'], spoiler=False)
        ]))

      except ValueError as e:
        logger.err('pixiv_bot.command', e)
        await sendErrResponse(message.channel, 'Value', e)

      except PixivError as e:
        logger.err('pixiv_bot.command', e)
        await sendErrResponse(message.channel, 'Pixiv', e)

      except Exception as e:
        logger.err('pixiv_bot.command', e)
        await sendErrResponse(message.channel, 'Unknown', e)
