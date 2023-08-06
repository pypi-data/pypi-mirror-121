from sys import stdout

__all__ = ['Logger']

class Colors(object):
    RED = "\033[0;31m"
    LIGHT_RED = "\033[1;31m"
    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    DARK_GRAY = "\033[1;30m"
    YELLOW = "\033[93m"
    END = "\033[0m"


class Levels(object):
    VERBOSE = 0  # Verbose
    DEBUG = 1  # Debug
    INFO = 2  # Info
    WARNING = 3  # Warning
    ERROR = 4  # Error
    CRITICAL = 5  # Critical


class Logger:
    def __init__(self, **kwargs):
        self.logger_name = kwargs.get("name", "Clog")
        self.logger_level = kwargs.get("level", Levels.INFO)
        return

    def __log(self, **kwargs) -> None:
        msg = kwargs.get("msg", "")
        level = kwargs.get("level", Levels.INFO)
        color = kwargs.get("color", Colors.BLUE)

        if level >= self.logger_level:
            stdout.write(f"{color}[{self.logger_name}] {msg}{Colors.END}\n")
            stdout.flush()
        return

    """Change logger options while initialized"""

    def change_level(self, level: Levels):
        self.logger_level = level
        self.verbose(f"Logger level changed to {level}")

    def change_name(self, name: str):
        self.logger_name = name
        self.verbose(f"Logger name changed to {name}")

    """Log to stdout """

    def verbose(self, msg: str) -> None:
        self.__log(msg=msg, level=Levels.VERBOSE, color=Colors.PURPLE)

    def debug(self, msg: str) -> None:
        self.__log(msg=msg, level=Levels.DEBUG, color=Colors.PURPLE)

    def log(self, msg: str) -> None:
        self.__log(msg=msg, level=Levels.INFO, color=Colors.GREEN)

    def info(self, msg: str) -> None:
        self.__log(msg=msg, level=Levels.INFO, color=Colors.BLUE)

    def warning(self, msg: str) -> None:
        self.__log(msg=msg, level=Levels.WARNING, color=Colors.YELLOW)

    def error(self, msg: str) -> None:
        self.__log(msg=msg, level=Levels.ERROR, color=Colors.RED)

    def critical(self, msg: str) -> None:
        self.__log(msg=msg, level=Levels.CRITICAL, color=Colors.LIGHT_RED)
