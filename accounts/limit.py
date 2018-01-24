# coding: utf8
from django.shortcuts import render
from functools import wraps
import logging
logger = logging.getLogger('django')

def LimitAccess(role, custom_template):
	if role == 'sa':
		template = custom_template
	else:
		template = 'limit.html'
	return template
