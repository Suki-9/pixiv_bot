import re
from datetime import datetime
from typing import List, Any
from urllib.parse import urlparse

def str2time(time: str, fmt: str = '%Y-%m-%dT%H:%M:%S') -> datetime:
  if not type(time) is str:
    raise TypeError('間違った型の引数が与えられました')

  return datetime.strptime(time.split('+')[0], fmt)

def is_url(url: str) -> bool:
  if not type(url) is str:
    raise TypeError('間違った型の引数が与えられました')

  return urlparse(url).scheme != ''

def is_list(list: List[Any] | Any) -> bool:
  return type(list) is List

def html_parser(html: str):
  if not type(html) is str:
    raise TypeError('間違った型の引数が与えられました')

  # 改行
  html = re.sub(r'<br\s*/>', '\n', html)
  
  # strongタグ
  for match in re.findall(r'<strong>.*?<\/strong>', html):
    text = re.search(r'(?<=<strong>).*?(?=<\/strong>)', match).group()
    html = html.replace(match, f'**{text}**')

  # aタグ
  for match in re.findall(r'<a.*>.*?<\/a>', html):
    link = match.replace(re.search(r'<a.*?>', match).group(), '').replace('</a>', '')
    text = re.search(r'(?<=href=").*?(?=")', match).group()
    html = html.replace(match,f"[{link}]({text})")

  return html
