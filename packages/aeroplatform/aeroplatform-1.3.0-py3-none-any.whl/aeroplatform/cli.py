import click
import os
import logging
import sys
from .account.commands import account

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)



@click.group()
def cli():
    pass


cli.add_command(account)

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=os.environ.get('LOGLEVEL', 'INFO').upper(),
                        format='%(filename)s %(lineno)d: %(message)s')
    cli()
