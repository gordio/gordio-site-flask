# -*- coding: utf-8 -*-

from flask.ext import wtf
from flask.ext.wtf import validators

from flask_wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.fields.html5 import EmailField #URLField
from wtforms.validators import Required, Length, Optional, Email


class ContactForm(Form):
	name = TextField("Name:", [
		Required(),
		Length(message=u"Bad name", min=4, max=125),
	])
	email = EmailField("Email:", [
		Required(),
		Email(message=u"Bad email"),
	])
	message = TextAreaField("Message:", [
		Required(),
		Length(message=u"So simple message", min=30),
	])
	#captcha = RecaptchaField("Captcha", [
		#Required(u'You must properly fill in the Captcha to submit this form.')
	#], public_key="6LfXBNkSAAAAAPt-HRo6mKp0x0bGbA1jO7q-gK3H", private_key="6LfXBNkSAAAAAOMJ_qGmQEAsylJu4JBDv3UyvJGR", secure=True)


class ArticleForm(Form):
	title = TextField("Title", [
		Required(),
		Length(min=5, max=200),
	])
	slug = TextField("Slug", [
		Required(),
		Length(min=3, max=200),
	])
	description = TextAreaField("Description", [
		Required(),
		Length(min=50, max=1000),
	])
	content = TextAreaField("Content", [
		Required(),
		Length(min=100, max=15000),
	])
	tags = TextField("Tags", [
		Optional(strip_whitespace=True),
	])
	pub_date = TextField("Publication Date", [
		Required(),
	])
	upd_date = TextField("Update Date", [
		#Required(),
	])