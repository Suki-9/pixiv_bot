import datetime

class Color:
	BLACK          = '\033[30m'
	RED            = '\033[31m'
	GREEN          = '\033[32m'
	YELLOW         = '\033[33m'
	BLUE           = '\033[34m'
	MAGENTA        = '\033[35m'
	COLOR_DEFAULT  = '\033[39m'
	BOLD           = '\033[1m'
	RESET          = '\033[0m'

def info(by: str,message: str) -> None:
  print(f"{Color.BOLD}{Color.BLACK}{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {Color.BLUE}INFO     {Color.RESET}{Color.MAGENTA}{by}{Color.RESET} {message}")

def success(by: str,message: str) -> None:
  print(f"{Color.BOLD}{Color.BLACK}{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {Color.GREEN}SUCCESS  {Color.RESET}{Color.MAGENTA}{by}{Color.RESET} {message}")

def warn(by: str,message: str) -> None:
  print(f"{Color.BOLD}{Color.BLACK}{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {Color.YELLOW}WARN     {Color.RESET}{Color.MAGENTA}{by}{Color.RESET} {message}")

def err(by: str,message: str) -> None:
  print(f"{Color.BOLD}{Color.BLACK}{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {Color.RED}ERROR    {Color.RESET}{Color.MAGENTA}{by}{Color.RESET} {message}")
