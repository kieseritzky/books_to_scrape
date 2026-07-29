import logging

# Creating formatters for the handlers
formatter = logging.Formatter(
    "{asctime} - {name} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

# Creating handlers for console output and file output
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")

# Assinging formatters to the created handlers
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Setting seperate log levels for the console and file output
console_handler.setLevel("DEBUG")
file_handler.setLevel("WARNING")

# Creating a root logger
root = logging.getLogger()
root.addHandler(console_handler)
root.addHandler(file_handler)
root.setLevel("DEBUG")
