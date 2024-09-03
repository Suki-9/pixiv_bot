import discord
from typing import List
from modules import utils

def gen_post(meta_data: dict, title: str | None = None , files: List[discord.File] = []):  
  return {
    'embed': discord.Embed(
      title = meta_data['title'] if title == None else title,
      color = 0x1092de,
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
    'files': [
      discord.File(fp=f"archive/icons/{meta_data['artist']['icon']}",  filename=meta_data['artist']['icon'], spoiler=False),
      discord.File(fp=f"archive/thumbnail/{meta_data['thumbnail']}",   filename=meta_data['thumbnail'],      spoiler=False)
    ] + files,
  }
