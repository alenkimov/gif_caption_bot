import click

from bot.polling import run_polling
from bot.webhook import run_webhook


@click.group()
def cli():
    pass


@cli.command()
@click.option("--skip-updates", is_flag=True, default=False, help="Skip pending updates")
def polling(skip_updates: bool):
    run_polling(skip_updates)


@cli.command()
def webhook():
    run_webhook()
