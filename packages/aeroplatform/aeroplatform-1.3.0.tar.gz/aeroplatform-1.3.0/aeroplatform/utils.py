import click
import os


def cyan(string: str):
    return click.style(string, fg='cyan')


def magenta(string: str):
    return click.style(string, fg='magenta')


def red(string: str):
    return click.style(string, fg='red')


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_BASE = "https://site.aeroplatform.co.uk"
NAME_LOWER = "aero"
NAME_UPPER = "Aero"
NAME_ASCII = cyan('\n'
                  ',adPPYYba,   ,adPPYba,  8b,dPPYba,   ,adPPYba, \n'  
                  '""     `Y8  a8P_____88  88P    "Y8  a8"     "8a\n'  
                  ',adPPPPP88  8PP"""""""  88          8b       d8\n'  
                  '88,    ,88  "8b,   ,aa  88          "8a,   ,a8"\n'  
                  '`"8bbdP"Y8   `"Ybbd8"   88           `"YbbdP"  \n')


def print_welcome():
    click.echo(NAME_ASCII)
    click.echo(f'Welcome to {magenta(NAME_UPPER)}!')
    click.echo("A Data Platform designed to put developers first.")
    click.echo(f"For more information, visit {cyan(SITE_BASE)}")