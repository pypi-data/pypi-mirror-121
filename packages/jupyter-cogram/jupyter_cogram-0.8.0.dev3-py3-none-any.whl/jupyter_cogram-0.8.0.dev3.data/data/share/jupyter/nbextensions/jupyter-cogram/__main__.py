import argparse
import sys
from pathlib import Path
from typing import Text

config_location = Path().home() / ".ipython/nbextensions/jupyter-cogram"
token_file_name = "cogram_auth_token"
log_file_name = "cogram_access_log"


def install_token(token: Text) -> None:
    loc = config_location.absolute()

    if not loc.is_dir():
        loc.mkdir(parents=True)

    p = loc / token_file_name

    p.write_text(token)

    print(f"Successfully stored API token at '{p}' 🎉")


def add_log_file() -> None:
    p = config_location.absolute() / log_file_name
    if not p.is_file():
        p.touch()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set your Cogram API token")
    parser.add_argument(
        "-t",
        "--token",
        help="Your Cogram API token",
        required=True,
    )

    token = parser.parse_args().token

    if not token:
        print(
            "⚠️  Could not find token! The full command is\n"
            "python3 -m jupyter_cogram --token YOUR_TOKEN"
        )
        sys.exit(1)

    # noinspection PyBroadException
    try:
        install_token(token)
        add_log_file()
    except Exception as e:
        print("⚠️  Could not install token:\n{e}")
