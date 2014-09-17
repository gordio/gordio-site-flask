from flask.ext.sqlalchemy import SQLAlchemy
import datetime
from main import app
from utils.slughifi import slughifi


db = SQLAlchemy(app)


tags = db.Table('tags',
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
	db.Column('article_id', db.Integer, db.ForeignKey('article.id'))
)


class Article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	slug = db.Column(db.String(80), unique=True)
	description = db.Column(db.Text)
	content = db.Column(db.Text)
	tags = db.relationship('Tag', secondary=tags, backref=db.backref('articles', lazy='dynamic'))
	pub_date = db.Column(db.DateTime)
	upd_date = db.Column(db.DateTime)

	def __init__(self, title, description, content, tags=None, slug=None, pub_date=None, upd_date=None):
		self.title = title
		self.slug = slug or slughifi(title)
		self.description = description
		self.content = content
		self.tags = tags or []
		self.pub_date = pub_date or datetime.datetime.utcnow()

		if not self.upd_date and not upd_date:
			upd_date = datetime.datetime.utcnow()
		self.upd_date = upd_date

	def __unicode__(self):
		return '<Article: %r>' % self.title

	def __repr__(self):
		return unicode(self).encode('utf-8')

	@classmethod
	def by_slug(cls, slug):
		return cls.query.filter(cls.slug==slug)


class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), unique=True)
	slug = db.Column(db.String(100), unique=True)

	def __init__(self, title, slug=None):
		self.title = title
		if not slug:
			slug = slughifi(title)
		self.slug = slug

	def __unicode__(self):
		return '<Tag: %r>' % self.title

	def __repr__(self):
		return unicode(self).encode('utf-8')

	@classmethod
	def by_slug(cls, slug):
		return cls.query.filter(cls.slug==slug)

	#@classmethod
	#def get_by_title(cls, slug):
		#return cls.get


class FeedBack(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(100))
	content = db.Column(db.Text)
	send_date = db.Column(db.DateTime)

	def __init__(self, name, email, content, send_date=None):
		self.name = title
		self.email = email
		self.content = content
		self.send_date = send_date or datetime.datetime.utcnow()

	def __unicode__(self):
		return '<Feedback: %r (%r)>' % (self.name, self.email)

	def __repr__(self):
		return unicode(self).encode('utf-8')

	@classmethod
	def send(cls, slug):
		return cls.query.filter(cls.slug==slug)
