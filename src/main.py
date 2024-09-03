import os
from modules import config
from bot import client

def main():
  if not os.path.exists('archive/icons'):
    os.makedirs('archive/icons')

  if not os.path.exists('archive/thumbnail'):
    os.makedirs('archive/thumbnail')

  client.run(config.get('DISCORD_TOKEN'))

if __name__ == "__main__":
  main()
