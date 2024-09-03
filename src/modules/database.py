import sqlite3

def dict_factory(cursor, row):
  d = {}
  for idx, col in enumerate(cursor.description):
    d[col[0]] = row[idx]
  return d

class DataBase:
  _conn: sqlite3.Connection

  def __init__( self, path):
    self._conn = sqlite3.connect(path)
    self._conn.row_factory = dict_factory

  def tx( self ):
    return self._conn.cursor()
  
  def commit( self ):
    self._conn.commit()

  def rollback( self ):
    self._conn.rollback()

class Archive(DataBase):
  keys = {
    'pixiv_illust': ['id', 'title', 'caption', 'artist', 'thumbnail', 'create_date'],
    'pixiv_artist': ['id', 'name', 'icon'],
    'pixiv_tag_bind': ['illust_id', 'name']
  }

  def __init__( self):
    super().__init__("archive/archive.db")

    cur = self.tx()
    cur.execute("CREATE TABLE IF NOT EXISTS pixiv_illust (id INTGER UNIQUE, title TEXT, caption TEXT, thumbnail TEXT, artist INTGER, create_date INTGER);")
    cur.execute("CREATE TABLE IF NOT EXISTS pixiv_tag_bind (illust_id INTGER, name TEXT);")
    cur.execute("CREATE TABLE IF NOT EXISTS pixiv_artist (id INTGER UNIQUE, name TEXT, icon TEXT);")

    self.commit()

  def registry_artist(self, artist_meta: dict, tx: sqlite3.Cursor | None = None):
    dict_keys = artist_meta.keys()

    for expected_key in self.keys['pixiv_artist']:
      if not expected_key in dict_keys:
        raise ValueError(f'Expected key {expected_key} is missing')

    cur = self.tx() if tx == None else tx
    cur.execute(
      f"INSERT INTO pixiv_artist (id, name, icon) SELECT * FROM (SELECT ?, ?, ?) AS temp_table WHERE NOT EXISTS (SELECT * FROM pixiv_artist WHERE id = ?);",
      (artist_meta['id'], artist_meta['name'], artist_meta['icon'], artist_meta['id'])
    )

    if (tx == None):
      self.commit()

  def registry_illust( self, illust_meta: dict, tx: sqlite3.Cursor | None = None):
    dict_keys = illust_meta.keys()

    for expected_key in self.keys['pixiv_illust']:
      if not expected_key in dict_keys:
        raise ValueError(f'Expected key {expected_key} is missing')

    cur = self.tx() if tx == None else tx

    cur.execute(
      "INSERT INTO pixiv_illust (id, title, caption, thumbnail, artist, create_date) VALUES (?, ?, ?, ?, ?, ?);",
      (illust_meta['id'], illust_meta['title'], illust_meta['caption'], illust_meta['thumbnail'], illust_meta['artist']['id'], illust_meta['create_date'])
    )

    for tag in illust_meta['tags']:
      cur.execute(
        "INSERT INTO pixiv_tag_bind (illust_id, name) VALUES (?, ?);",
        (illust_meta['id'], tag)
      )

    if (tx == None):
      self.commit()

  def delete(self, id: str | int, tx: sqlite3.Cursor | None = None):
    cur = self.tx() if tx == None else tx
    cur.execute("DELETE FROM pixiv_illust WHERE id = ?;", (str(id),))

    if (tx == None):
      self.commit()

  def get( self, id: str | int):
    cur = self.tx()

    illust = cur.execute("SELECT * FROM pixiv_illust WHERE id = ?;", (str(id),)).fetchone()

    if illust == None:
      return None

    illust['artist'] = cur.execute("SELECT * FROM pixiv_artist WHERE id = ?;", (illust['artist'],)).fetchone()
    illust['tags'] = map(lambda row: row['name'], cur.execute("SELECT name FROM pixiv_tag_bind WHERE illust_id = ?;", (illust['id'],)).fetchall())

    return illust

class User(DataBase):
  keys = {
    'user_config': ['userId', 'pixiv_token', 'enable_private']
  }

  def __init__(self):
    super().__init__("archive/user_data.db")

    cur = self._conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS user_config(user_id INTGER UNIQUE, pixiv_token TEXT, enable_private BOOLEAN DEFAULT false);")

    self._conn.commit()

  def update(self, id: str, key: str, value: str):
    if not key in self.keys['user_config']:
      raise ValueError(f"存在しないKey '{key}' が指定されました。")

    cur = self.tx()

    if None == cur.execute('SELECT user_id FROM user_config WHERE user_id = ?;', (id,)).fetchone():
      cur.execute('INSERT INTO user_config (user_id) VALUES (?);', (id,))

    cur.execute(f'UPDATE user_config SET {key} = ? WHERE user_id = ?;', (value, id))

    self.commit()

  def delete( self, id: str | int):
    cur = self.tx()
    cur.execute("DELETE FROM user_config WHERE id = ?;", (str(id),))

  def get( self, id: str | int):
    return self.tx().execute(f"SELECT * FROM user_config WHERE user_id = ?;", (str(id),)).fetchone()

archive_db = Archive()
user_db = User()
