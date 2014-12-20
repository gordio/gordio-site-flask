from fabric.decorators import task
from fabric.context_managers import settings
from fabric.api import require, env, local, abort, cd, run as frun
from fabric.contrib.console import confirm
from fabric.colors import green, red


env.user  = 'gordio'
env.hosts = ["gordio.pp.ua", ]


@task
def build():
    """ Build project environment """
    stage('Updating virtual environment...')
    run('[ -d venv ] || virtualenv venv --no-site-packages --python=python3')
    run('venv/bin/pip install --upgrade -r requirements.txt')


@task
def run(host="127.0.0.1"):
    """ Start project in debug mode (for development) """
    run('venv/bin/python run.py')


def stage(message):
    """ Show `message` about current stage """
    print(green("\n *** {0}".format(message), bold=True))
