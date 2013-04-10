#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import env, local, cd, run
import sys
import os


sys.path += [os.path.realpath(os.path.dirname(__file__)).replace('\\', '/')]


env.hosts = ['gordio@bender.bloodhost.ru', ]
env.prod_path = '~/dev.gordio.pp.ua/'


def virtualenv(command):
	"""
	Run a command in the virtualenv. This prefixes the command with the source
	command.
	Usage:
		virtualenv('pip install django')
	"""
	source = 'source %(project_directory)s/bin/activate && ' % env
	run(source + command)


def init():
	""" Init application """
	from models import db
	print("Creates all database tables...")
	print("Database:", db.engine.url)
	db.create_all()


def deploy():
	pass
	#with cd(env.prod_path + 'app'):
		#run('virtualenv --no-site-packages venv', pry=True)
		#run('venv/bin/pip install -r requirements', pry=True)

	#with cd(env.prod_path + 'htdocs'):
		#run('ln -s ../app/static')
		#run('ln -s static/robots.txt')
		#run('ln -s ../app/_htaccess .htaccess')


# vim: set ts=4 sw=4 tw=100 fo-=t ff=unix ft=python:
