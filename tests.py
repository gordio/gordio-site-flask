#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from main import app
from models import db, Article, Tag


class TestCase(unittest.TestCase):
	def setUp(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
		self.app = app.test_client()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()


if __name__ == '__main__':
	unittest.main()


# vim: set fdm=marker fdc=0 ts=4 sw=4 tw=100 fo-=t ff=unix ft=python: