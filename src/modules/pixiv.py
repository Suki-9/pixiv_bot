import os
import shutil

import modules.utils as utils
from  modules.database import archive_db

from gppt import GetPixivToken
from pixivpy3 import AppPixivAPI
from py7zr import SevenZipFile

def get_refresh_token(username: str, password: str) -> str:
 return GetPixivToken(headless=True).login(username=username, password=password)["refresh_token"]

def archive(refresh_token: str, url: str) -> str:
  id = url.split('/')[-1]

  archive_path = f"archive/{id}.7z"
  tmp_path = f"archive/tmp_{id}"

  archived = archive_db.get(id)

  if archived != None:
    archived['archive_path'] = archive_path
    return archived

  api = AppPixivAPI()
  api.auth(refresh_token=refresh_token)

  illust = api.illust_detail(id)['illust']
  meta_data = {
    'id': illust['id'],
    'title': illust['title'],
    'tags': map(lambda obj: obj['name'], illust['tags']),
    'caption': illust['caption'],
    'create_date': utils.str2time(illust['create_date']).timestamp(),
    'thumbnail': illust['image_urls']['large'].split('/')[-1],
    'archive_path': archive_path,
    'artist': {
      'id': illust['user']['id'], 
      'name': illust['user']['name'],
      'icon': illust['user']['profile_image_urls']['medium'].split('/')[-1]
    }
  }

  try:
    tx = archive_db.tx()

    archive_db.registry_illust(meta_data, tx)
    archive_db.registry_artist(meta_data['artist'], tx)

    if os.path.exists(tmp_path):
      shutil.rmtree(tmp_path)

    os.makedirs(tmp_path)

    if not os.path.exists('archive/icons'):
      os.makedirs('archive/icons')

    if not os.path.exists('archive/thumbnail'):
      os.makedirs('archive/thumbnail')

    api.download(illust['user']['profile_image_urls']['medium'], path=f'archive/icons')
    api.download(illust['image_urls']['large'], path=f'archive/thumbnail')

    for media in illust["meta_pages"]:
      api.download(media["image_urls"]["large"], path=tmp_path)

    if 'meta_single_page' in illust and 'original_image_url' in illust['meta_single_page']:
      api.download(illust['meta_single_page']['original_image_url'], path=tmp_path)

    with SevenZipFile(archive_path, 'w') as z:
      for file in os.listdir(tmp_path):
        z.write(f"{tmp_path}/{file}", file)

    shutil.rmtree(tmp_path)

    archive_db.commit()

  except ValueError as e:
    archive_db.rollback()
    raise ValueError(e)

  except Exception as e:
    print(e)
    archive_db.rollback()
    raise Exception("不明なエラー")

  return meta_data
