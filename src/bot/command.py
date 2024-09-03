import os
import shutil
import discord
from bot.message import gen_post
from py7zr import SevenZipFile
from pixivpy3 import PixivError
from modules import pixiv, utils, logger, config, database

async def sendOkResponse(interaction: discord.Interaction, title: str = '', description: str = '', embed: discord.Embed | None = None, files: List[discord.File] = []) -> None:
  logger.success('pixiv_bot.action', f'Send message.')
  return await interaction.followup.send(
    embed = discord.Embed(
      color = 0x14c900,
      title = title,
      description = description
    ) if embed == None else embed,
    files=files,
    ephemeral = True
  )

async def sendErrResponse(interaction: discord.Interaction, type: str = 'Unknown', description: str = '', embed: discord.Embed | None = None, files: List[discord.File] = []) -> None:
  logger.err('pixiv_bot.action', f'Send error message.')
  return await interaction.followup.send(
    embed=discord.Embed(
      color = 0xff0000,
      title = f'{type} error',
      description = description
    ) if embed == None else embed,
    files=files,
    ephemeral = True
  )

@tree.command(name="show",description="アーカイブを表示します.")
async def show_archive(interaction: discord.Interaction, url :str):
  await interaction.response.defer()

  user = user_db.get(interaction.user.id)

  if user == None or user['user_id'] == None:
    return await sendErrResponse(interaction, 'Pixiv', '/updateでトークンを更新してみて')

  try:
    async def send(title: str):
      await interaction.followup.send(
        embed = discord.Embed(
          title = title,
          color = 0x0059ff,
          description = f"### [Original Link](https://www.pixiv.net/artworks/{meta_data['id']})",
        ).set_author(
          name = meta_data['artist']['name'],
          url = f"https://www.pixiv.net/users/{meta_data['artist']['id']}",
          icon_url=f"attachment://{meta_data['artist']['icon']}"
        ).set_thumbnail(
          url = f"attachment://{meta_data['thumbnail']}"
        ).add_field(
          name = "Description",
          value = utils.html_parser(meta_data['caption']),
          inline = False
        ).add_field(
          name = "タグ",
          value = "\n".join(list(map(lambda tag: f"[{tag}](https://www.pixiv.net/tags/{tag}/artworks)", meta_data['tags']))),
          inline = False
        ),
        files = [
          discord.File(fp=f"archive/icons/{meta_data['artist']['icon']}",  filename=meta_data['artist']['icon'], spoiler=False),
          discord.File(fp=f"archive/thumbnail/{meta_data['thumbnail']}",  filename=meta_data['thumbnail'],      spoiler=False)
        ],
      )

    meta_data, file_path = pixiv.archive(user['pixiv_token'], url if utils.is_url(url) else f'https://www.pixiv.net/artworks/{url}')
    tmp_path = f"archive/tmp_{meta_data['id']}"
    thread_name = f"{meta_data['title']} (ID: {meta_data['id']})"

    for thread in interaction.channel.threads:
      if thread_name == thread.name and client.user.id == thread.owner_id:
        return await sendOkResponse(interaction, **gen_post(meta_data, thread.mention))

    if os.path.exists(tmp_path):
      shutil.rmtree(tmp_path)

    os.makedirs(tmp_path)

    with SevenZipFile(file_path, mode='r') as archive:
      archive.extractall(tmp_path)

    thread = await interaction.channel.create_thread(name=thread_name)

    for file in sorted(os.listdir(tmp_path)):
      await thread.send(
        file = discord.File(fp = f'{tmp_path}/{file}', filename = file, spoiler = False)
      )

    await sendOkResponse(interaction, **gen_post(meta_data, thread.mention))
    logger.err('pixiv_bot.command', e)
    logger.err('pixiv_bot.command', e)

  except Exception as e:
    logger.err('pixiv_bot.command', e)
    await sendErrResponse(interaction, 'Unknown', e)

  finally:
    if os.path.exists(tmp_path):
      shutil.rmtree(tmp_path)

@tree.command(name="archive",description="イラストをアーカイブします.")
async def archive(interaction: discord.Interaction, url :str):
  await interaction.response.defer()

  user = user_db.get(interaction.user.id)

  if user == None or user['user_id'] == None:
    return await sendErrResponse(interaction, 'Pixiv', '/updateでトークンを更新してみて')

  try:
    meta_data, file_path = pixiv.archive(user['user_id'], url if utils.is_url(url) else f'https://www.pixiv.net/artworks/{url}')

    await sendOkResponse(interaction, **gen_post(meta_data, files = [
      discord.File(fp=meta_data['archive_path'], spoiler=False)
    ]))

  except ValueError as e:
    logger.err('pixiv_bot.command', e)

    logger.err('pixiv_bot.command', e)

  except Exception as e:
    logger.err('pixiv_bot.command', e)

@tree.command(name="update",description="refresh_tokenのアップデート, 受け取ったクレデンシャル情報は処理後破棄されます.")
async def update_pixivToken(interaction: discord.Interaction, user_name: str, password: str):
  try:
    await interaction.response.defer()

    user_db.update(interaction.user.id, 'pixiv_token', pixiv.get_refresh_token(user_name, password))
    
    await interaction.followup.send(
      embed = discord.Embed(
        color = 0x14c900,
        title = 'Update success',
        description = 'refresh_tokenを更新完了'
      ),
      ephemeral = True
    )

  except PixivError:
    logger.err('Pixiv', e)
    await sendErrResponse(interaction, 'Pixiv', 'refresh_tokenの取得に失敗したかも')

  except Exception as e:
    logger.err('Unknown', e)
    await sendErrResponse(interaction, 'Unknown', e)

@tree.command(name="setting", description="設定")
@discord.app_commands.describe(key='項目のKey')
@discord.app_commands.choices(key=[
  discord.app_commands.Choice(value='enable_private',       name='Botからの返信を公開'),
  discord.app_commands.Choice(value='disable_private',      name='Botからの返信を非公開'),
  discord.app_commands.Choice(value='enable_auto_archive',  name='自動アーカイブを有効化'),
  discord.app_commands.Choice(value='disable_auto_archive', name='自動アーカイブを無効化'),
])
async def setting(interaction: discord.Interaction, key: str, value: str | None):
  try:
    await interaction.response.defer()

    # ユーザー個々の設定
    if key in ['enable_private', 'disable_private']:
      database.user_db.update(interaction.user.id, key, value)
      await sendOkResponse(interaction, 'Update success', f"{key}を{value}へ更新.")

      return

    # 自動アーカイブの設定
    if key in ['enable_auto_archive', 'disable_auto_archive']:
      enable_channels = config.get('auto_archive_enable_channels') or []
      channel_id = interaction.channel_id

      if key == 'enable_auto_archive':
        if channel_id in enable_channels:
          await sendErrResponse(interaction, 'Bad request', f"{interaction.channel.name}では既に有効です。")
        else:
          config.set('auto_archive_enable_channels', enable_channels + [ channel_id ])
          await sendOkResponse(interaction, 'Success', f"{interaction.channel.name}で有効になりました")

      if key == 'disable_auto_archive': 
        if channel_id in enable_channels:
          config.set('auto_archive_enable_channels', enable_channels.remove(channel_id))
          await sendOkResponse(interaction, 'Success', f"{interaction.channel.name}で無効になりました")
        else:
          await sendErrResponse(interaction, 'Bad request', f"{interaction.channel.name}では既に無効です。")

      return

    await sendErrResponse(interaction, 'Bad request', f'{key}は存在しないキーです')

  except ValueError as e:
    logger.err('Value', e)
    await sendErrResponse(interaction, 'Value', e)

  except Exception as e:
    logger.err('Unknown', e)
    await sendErrResponse(interaction, 'Unknown', e)

@tree.command(name="help",description="使いかた")
async def help(interaction: discord.Interaction):  
  await interaction.response.send_message(
    embed = discord.Embed(
      title="設定可能な項目一覧",
      description=""
    ).add_field(
      name="Key一覧",
      value="- setting"
    ),
    ephemeral=True,
  )
