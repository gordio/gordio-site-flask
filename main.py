#!/usr/bin/env python
from flask import Flask, g, render_template, flash, redirect, session, request, url_for, abort, Response
from flask.ext.assets import Environment
from datetime import datetime
from functools import wraps


# PREPARE
app = Flask(__name__, static_url_path='')
app.config.from_pyfile('config.py')


# TEMPLATE
assets = Environment(app)
assets.url = app.static_url_path

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


# Auth
def check_auth(username, password):
	""" This function is called to check if a user + pass is valid """
	return username == app.config["HTTP_AUTH_USER"] and password == app.config["HTTP_AUTH_PASS"]

def authenticate():
	""" Sends a 401 response that enables basic auth """
	return Response(
		'Could not verify your access level for that URL.', 401,
		{'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated


# VIEWS
@app.route('/')
def vcard():
	return render_template('vcard.html', **locals())


@app.route('/about/')
def about():
	return render_template('about.html', **locals())


# Articles {{{
@app.route('/articles/view/<slug>/')
def articles_view(slug):
	""" Show article from <slug> or 404 """
	from models import Article

	article = Article.by_slug(slug).filter(Article.pub_date < datetime.now()).first_or_404()

	return render_template('articles/view.html', **locals())


@app.route('/articles/add/', methods=['GET', 'POST'])
@requires_auth
def articles_add():
	""" Add new article or render form """
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
					tags += [Tag.query.filter(Tag.title==t)[0]]
				except Exception:
					tags += [Tag(t)]

		try:
			pub_date = datetime.strptime(form.pub_date.data, '%Y-%m-%d %H:%M:%S')
		except ValueError:
			flash("Can't parse date.", 'error')
		else:
			article = Article(
				form.title.data,
				form.description.data,
				form.content.data,
				tags=tags,
				slug=form.slug.data,
				pub_date=pub_date,
			)

			db.session.add(article)
			db.session.commit()

			flash("Article added.", 'success')
			return redirect(url_for('articles_view', slug=article.slug))

	return render_template('articles/add.html', **locals())


@app.route('/articles/edit/<slug>/', methods=['GET', 'POST'])
@requires_auth
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
		form.description.data = article.description
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
			article.description = form.description.data
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

				# Get or create
				try:
					article.tags += [Tag.query.filter(Tag.title == t)[0]]
				except Exception:
					article.tags += [Tag(t)]

			db.session.commit()

			flash("Article updated success.", 'success')
			return redirect(url_for('articles_view', slug=form.slug.data))

	return render_template('articles/edit.html', **locals())


@app.route('/articles/', defaults={'page': 1})
@app.route('/articles/page/<int:page>/')
def articles_list(page):
	""" Render all articles """
	from models import Article
	count = app.config['ARTICLES_PER_PAGE']

	articles = Article.query.filter(Article.pub_date < datetime.now())\
	.order_by(Article.pub_date.desc()) #FIXME: .limit(count).offset((count * page) - count)

	for article in articles:
		try:
			desc, cont = article.content.split(u"<!-- cut -->")
		except Exception:
			# FIXME: Use first paragraph
			pass
		else:
			article.description = desc

	return render_template('articles/list.html', **locals())


# Tags
@app.route('/articles/tagged/<tag_slug>/', defaults={'page': 1})
@app.route('/articles/tagged/<tag_slug>/page/<int:page>/')
def articles_tagged(tag_slug, page):
	""" Render articles with <tag_slug> """
	from models import Article, Tag

	tag = Tag.by_slug(tag_slug).first_or_404()
	articles = tag.articles.filter(Article.pub_date < datetime.now())

	return render_template('articles/list.html', **locals())
# }}}


# Contact Page {{{
@app.route('/contacts/', methods=['GET', 'POST'])
def contacts():
	""" Render and processing contact form """
	import time
	from forms import ContactForm

	form = ContactForm(request.form)

	if request.method == 'POST' and form.validate():
		send_time = session.get('contacts_send_next_message_time') or 0
		if send_time > int(time.time()):
			flash("Very frequantly.", 'error')
			return render_template('contacts.html', **locals())


		from smtplib import SMTP
		try:
			from email.MIMEText import MIMEText
			msg = MIMEText(form.message.data.encode('UTF-8'), 'plain')
		except:
			from email.mime.text import MIMEText
			msg = MIMEText(form.message.data, 'plain')


		msg.set_charset("UTF-8")
		msg['Subject'] = "GWP: '%s'" % form.name.data
		msg['From'] = form.email.data

		mail = SMTP(app.config['SMTP_HOST'], app.config['SMTP_PORT'])
		mail.set_debuglevel(False)
		mail.login(app.config['SMTP_LOGIN'], app.config['SMTP_PASSWORD'])

		try:
			mail.sendmail('noreply@gordio.pp.ua', app.config['MSG_EMAILS'], msg.as_string())
		except Exception:
			flash("Unknown server error.", 'error')
			mail.close()
		else:
			flash("Message sended.", 'success')
			session['contacts_send_next_message_time'] = int(time.time()) + (60 * 15) # 15 min
			session.modified = True
			mail.close()
			return redirect(url_for('contacts'), code=302)

	return render_template('contacts.html', form=form)


if __name__ == '__main__':
	app.run()
