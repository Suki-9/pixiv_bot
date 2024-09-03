import yaml
import yaml.parser

with open('config.yaml', 'r') as y:
  config = yaml.safe_load(y)

def get(key: str) -> any:
  return config[key] if key in config else None

def set(key: str, value: any) -> None:
  if not key in ['auto_archive_enable_channels']:
    raise ValueError('無効なキー')

  config[key] = value

  with open('config.yaml', 'w+',  encoding='utf-8') as f:
    f.write(yaml.dump(config))
