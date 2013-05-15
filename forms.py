# -*- coding: utf-8 -*-
from flask.ext import wtf
from flask.ext.wtf import validators


class ContactForm(wtf.Form):
	name = wtf.TextField("Name:", [
		validators.Required(),
		validators.Length(message=u"Bad name", min=4, max=125),
	])
	email = wtf.html5.EmailField("Email:", [
		validators.Required(),
		validators.Email(message=u"Bad email"),
	])
	message = wtf.TextField("Message:", [
		wtf.Required(),
		validators.Length(message=u"So simple message", min=30),
	], widget=wtf.TextArea())
	#captcha = wtf.RecaptchaField("Captcha", [
		#validators.Required(u'You must properly fill in the Captcha to submit this form.')
	#], public_key="6LfXBNkSAAAAAPt-HRo6mKp0x0bGbA1jO7q-gK3H", private_key="6LfXBNkSAAAAAOMJ_qGmQEAsylJu4JBDv3UyvJGR", secure=True)


class ArticleForm(wtf.Form):
	title = wtf.TextField("Title", [
		validators.Required(),
		validators.Length(min=5, max=200),
	])
	slug = wtf.TextField("Slug", [
		validators.Required(),
		validators.Length(min=3, max=200),
	])
	description = wtf.TextField("Description", [
		validators.Required(),
		validators.Length(min=50, max=1000),
	], widget=wtf.TextArea())
	content = wtf.TextField("Content", [
		validators.Required(),
		validators.Length(min=100, max=5000),
	], widget=wtf.TextArea())
	tags = wtf.TextField("Tags", [
		validators.Optional(strip_whitespace=True),
	])
	pub_date = wtf.TextField("Publication Date", [
		validators.Required(),
	])
	upd_date = wtf.TextField("Update Date", [
		#validators.Required(),
	])
