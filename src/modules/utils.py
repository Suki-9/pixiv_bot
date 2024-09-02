from datetime import datetime
from typing import List, Any
from urllib.parse import urlparse

def str2time(str: str):
  return datetime.strptime(str.split('+')[0], '%Y-%m-%dT%H:%M:%S')

def is_url(srt: str) -> bool:
  return urlparse(srt).scheme != ''

def is_list(list: List[Any] | Any) -> bool:
  return type(list).__name__ == 'list'
