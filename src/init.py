import os

def main():
  if not os.path.exists('archive'):
    os.makedirs('archive')

  if not os.path.exists('archive/icons'):
    os.makedirs('archive/icons')

  if not os.path.exists('archive/thumbnail'):
    os.makedirs('archive/thumbnail')

if __name__ == "__main__":
  main()