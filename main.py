#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, g, render_template, flash, redirect, session, request, url_for, abort
from flask.ext.assets import Environment
import sqlite3
from datetime import datetime


# PREPARE {{{
app = Flask(__name__, static_url_path='')
app.config.from_pyfile('config.py')

assets = Environment(app)

# TEMPLATE
app.jinja_env.add_extension('utils.jinja.htmlcompress.HTMLCompress')

from utils.jinja.filters import markdown, datetimefmt, timesince
app.add_template_filter(markdown)
app.add_template_filter(datetimefmt, name="datetime")
app.add_template_filter(timesince)

@app.context_processor
def now_context():
	return dict(now=datetime.now())

# ERRORS
if not app.config['DEBUG']:
	@app.errorhandler(404)
	def page_not_found(error):
		return 'This page does not exist', 404

	@app.errorhandler(500)
	def page_not_found(error):
		return 'Server error', 500

	@app.errorhandler(sqlite3.DatabaseError)
	def special_exception_handler(error):
		return 'Database connection failed', 500
# }}}


# VIEWS
@app.route('/')
def index():
	return render_template('index.html', **locals())


# Articles {{{
@app.route('/article/add/', methods=['GET', 'POST'])
def article_add():
	from models import Article, Tag, db
	from forms import ArticleForm

	form = ArticleForm()

	form.pub_date.data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	form.upd_date.data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	if request.method == 'POST' and form.validate():
		tags = []
		if form.tags.data:
			tags_raw = form.tags.data.split(',')
			for t in tags_raw:
				t = t.strip()
				try:
					tags += [Tag.query.filter(title==t)[0]]
				except Exception:
					tags += [Tag(t)]

		try:
			pub_date = datetime.strptime(form.pub_date.data, '%Y-%m-%d %H:%M:%S')
		except ValueError:
			flash("Can't parse date.", 'error')
		else:
			article = Article(
				form.title.data,
				form.content.data,
				tags=tags,
				slug=form.slug.data,
				pub_date=pub_date,
			)

			db.session.add(article)
			db.session.commit()

			flash("Article added.", 'success')
			return redirect(url_for('article_view', slug=article.slug))

	return render_template('article/add.html', **locals())


@app.route('/article/<slug>/')
def article_view(slug):
	""" Show article from <slug> or 404 """
	from models import Article

	article = Article.by_slug(slug).filter(Article.pub_date < datetime.now()).first_or_404()

	return render_template('article/view.html', **locals())


@app.route('/article/<slug>/edit/', methods=['GET', 'POST'])
def article_edit(slug):
	""" Render edit article form by <slug> or update data from `POST` """
	from models import Article, Tag, db
	from forms import ArticleForm

	article = Article.by_slug(slug=slug).first_or_404()
	form = ArticleForm()

	if request.method != 'POST':
		# init form data from object
		form.title.data = article.title
		form.slug.data = article.slug
		form.content.data = article.content
		tags = [t.title for t in article.tags]
		for t in tags:
			if form.tags.data:
				form.tags.data += ", " + t
			else:
				form.tags.data = t
		form.pub_date.data = article.pub_date.strftime("%Y-%m-%d %H:%M:%S")
		form.upd_date.data = article.upd_date.strftime("%Y-%m-%d %H:%M:%S")
	else:
		if form.validate():
			article.title = form.title.data
			article.slug = form.slug.data
			article.content = form.content.data
			article.pub_date = datetime.strptime(form.pub_date.data, '%Y-%m-%d %H:%M:%S')

			# autonow if empty or error
			try:
				upd_datetime = datetime.strptime(form.upd_date.data, '%Y-%m-%d %H:%M:%S')
			except Exception:
				article.upd_date = datetime.now()

			article.tags = []
			tags_raw = form.tags.data.split(',')
			for t in tags_raw:
				t = t.strip()
				try:
					article.tags += [Tag.query.filter(title==t)[0]]
				except Exception:
					article.tags += [Tag(t)]

			db.session.commit()

			flash("Updated. Sucessfull update article.", 'success')
			return redirect(url_for('article_view', slug=form.slug.data))

	return render_template('article/edit.html', **locals())


@app.route('/articles/', defaults={'page': 1})
@app.route('/articles/page/<int:page>/')
def articles(page):
	""" Render all articles """
	from models import Article

	articles = Article.query.filter(Article.pub_date < datetime.now()).order_by(Article.pub_date)

	for article in articles:
		try:
			desc, cont = article['content'].split("<!-- cut -->")
		except Exception:
			# FIXME: Use first paragraph
			pass
		else:
			article.update({'description': desc, 'content': cont})

	return render_template('article/list.html', **locals())


# Tags
@app.route('/articles/tagged/<tag_slug>/', defaults={'page': 1})
@app.route('/articles/tagged/<tag_slug>/page/<int:page>/')
def articles_tagged(tag_slug, page):
	""" Render articles from tag_slug """
	from models import Article, Tag

	tag = Tag.by_slug(tag_slug).first_or_404()
	articles = tag.articles.filter(Article.pub_date < datetime.now())

	return render_template('article/list.html', **locals())
# }}}


# Contact Page {{{
@app.route('/contacts/', methods=['GET', 'POST'])
def contacts():
	import time
	from forms import ContactForm

	form = ContactForm(request.form)

	if request.method == 'POST' and form.validate():
		# Проверка на частоту отправок
		send_time = session.get('contacts_send_next_message_time')
		if send_time > int(time.time()):
			flash("Very frequently", 'error')
			return render_template('contacts.html', **locals())


		from smtplib import SMTP
		from email.MIMEText import MIMEText

		msg = MIMEText(form.message.data.encode('UTF-8'), 'plain')
		msg.set_charset("UTF-8")
		msg['Subject'] = "GWP: '%s'" % form.name.data
		msg['From'] = form.email.data

		mail = SMTP('smtp.bloodhost.ru', 25)
		mail.set_debuglevel(False)
		mail.login('noreply@gordio.pp.ua', '35056')

		try:
			mail.sendmail('noreply@gordio.pp.ua', ['gordio@ya.ru',], msg.as_string())
		except Exception:
			flash("Sorry, unknown error detected.", 'error')
			mail.close()
		else:
			flash("Message send successful", 'success')
			# записываем дату отправки
			session['contacts_send_next_message_time'] = int(time.time()) + (60 * 15) # 15 минут
			mail.close()
			return redirect(url_for('contacts'))

	return render_template('contacts.html', form=form)
# }}}


if __name__ == '__main__':
	app.run()


# vim: set fdm=marker ts=4 sw=4 noet tw=100 fo-=t ff=unix:
