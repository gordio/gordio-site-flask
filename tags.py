# -*- coding: utf-8 -*-
from flask import g


def parse_tags(string):
	tags = []

	for tag in string.split(','):
		tags += [tag.strip()]

	return tags


def get_tag(tag_title):
	__cur = g.db.execute('SELECT id, title FROM tags WHERE title=?', (tag_title, ))
	try:
		return [dict(id=row[0], title=row[1]) for row in __cur.fetchall()][0]
	except Exception, e:
		return []


def create_tag(title):
	g.db.execute('INSERT INTO tags (title)'
		'VALUES (?)',
		(
			title,
		)
	)
	return get_tag(title)

# vim: set fdm=marker fdc=0 ts=4 sw=4 tw=100 fo-=t ff=unix ft=python:
