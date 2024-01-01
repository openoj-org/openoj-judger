import logging
from colorama import init, Fore, Style

def prepare_logger() -> logging.Logger:
    """
    Prepare logger

    Returns:
        logging.Logger
    """
    # Prepare logger
    init()

    log_format = '%(filename)s - %(asctime)s - %(levelname)s - %(message)s'
    logger = logging.getLogger('colored_logger')
    logger.setLevel(logging.INFO)

    class ColoredFormatter(logging.Formatter):
        COLORS = {
            'DEBUG': Fore.CYAN,
            'INFO': Fore.GREEN,
            'WARNING': Fore.YELLOW,
            'ERROR': Fore.RED,
            'CRITICAL': Style.BRIGHT + Fore.RED
        }

        def format(self, record):
            log_message = super().format(record)
            log_level_color = self.COLORS.get(record.levelname, Fore.WHITE)
            return f"{log_level_color}{log_message}{Style.RESET_ALL}"

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter(log_format))

    if not logger.hasHandlers():
        logger.addHandler(console_handler)
    # End of logger preparation
    return logger