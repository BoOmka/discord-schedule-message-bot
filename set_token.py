import mmap
import re

import click


@click.command()
@click.argument('token', type=click.STRING)
def set_token(token: str):
    try:
        with open('.env', 'r') as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as f:
            found = bool(re.search(br'DISCORD_TOKEN=.*', f))
            f.seek(-1, 2)
            has_newstring = f.read() == b'\n'
    except (FileNotFoundError, ValueError):
        found = False
        has_newstring = True

    if not found:
        with open('.env', 'a') as f:
            if not has_newstring:
                f.write('\n')
            f.write(f"DISCORD_TOKEN='{token}'")
            f.write('\n')


if __name__ == '__main__':
    set_token()
