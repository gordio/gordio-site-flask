# -*- coding: utf-8 -*-


def markdown(data):
	""" Return HTML5 created from markdown """
	from markdown import markdown
	from flask import Markup

	# don't process for empty var
	if not data:
		return data

	html = markdown(data, output_format='html5')
	return Markup(html)


def datetimefmt(date, fmt='%c'):
	""" Return formated data string """
	import datetime

	# check whether the value is a datetime object
	if not isinstance(date, (datetime.date, datetime.datetime)):
		try:
			date = datetime.datetime.strptime(str(date), '%Y-%m-%d').date()
		except Exception, e:
			return date

	return date.strftime(fmt)


def timesince(dt, default="just now"):
	""" Returns string representing "time since" e.g. 3 days ago, 5 hours ago etc. """
	import datetime

	now = datetime.utcnow()
	diff = now - dt
	periods = (
		(diff.days / 365, "year", "years"),
		(diff.days / 30, "month", "months"),
		(diff.days / 7, "week", "weeks"),
		(diff.days, "day", "days"),
		(diff.seconds / 3600, "hour", "hours"),
		(diff.seconds / 60, "minute", "minutes"),
		(diff.seconds, "second", "seconds"),
	)

	for period, singular, plural in periods:
		if period:
			return "%d %s ago" % (period, singular if period == 1 else plural)

	return default
