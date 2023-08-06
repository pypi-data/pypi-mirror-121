import fire
from pygoat.echo.echo import echo_cmd

def cli():
    return fire.Fire({
        "echo": echo_cmd
    })
