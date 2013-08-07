from fabric.api import env, execute, cd, run, local, put

env.user  = 'gordio'
env.hosts = ["gordio.pp.ua", ]


def deploy():
	execute(update)

def update():
	with cd("gordio.pp.ua/app/"):
		run('git pull', pty=True)