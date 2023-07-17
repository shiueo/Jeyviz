import logging


class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    white = "\x1b[37m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format_s = "(white){asctime}(reset) (level-color){levelname:<8}(reset) (green){name}(reset) {message}"
        format_s = format_s.replace("(white)", self.white + self.bold)
        format_s = format_s.replace("(reset)", self.reset)
        format_s = format_s.replace("(level-color)", log_color)
        format_s = format_s.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format_s, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)
