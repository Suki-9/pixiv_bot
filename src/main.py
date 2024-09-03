from modules import config
from bot import client

def main():
  client.run(config.get('DISCORD_TOKEN'))

if __name__ == "__main__":
  main()
