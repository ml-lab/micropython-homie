import sys
import time
from watchdog.observers import Observer
import os
import click

# md homie
# md homie/node

# requirements: pip install -r watchdog

# usage: python watch.py homie


class EventHandler():

    def dispatch(self, event, *args, **kwargs):
        command = 'mpfshell -n -c \"open ttyUSB0; put \\\"{}\\\"\"'.format(event.src_path)
        print("updating {}".format(event.src_path))
        os.system(command)
        print("done update")
        





@click.group()
def cli():
    pass

@click.group()
def sync():
    pass

@sync.command()
@click.option('--path', default="homie", help='which directory to watch')
def watch(path):
    print("watching...")
    observer = Observer()
    observer.schedule(EventHandler(), path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    

@sync.command()
def init():
    os.system('mpfshell -n -c \"open ttyUSB0; md homie\"')
    os.system('mpfshell -n -c \"open ttyUSB0; md homie/node\"')
    
cli.add_command(sync)

if __name__ == '__main__':
    cli()
