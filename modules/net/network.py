#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, urllib2, cookielib

class AuthNetworkTools:
    '''Class for general usage when it is going to use cookies for tracking user sesion on web page.'''
    def __init__(self,base_url):
        self.bu=base_url
        self.cookie_file = 'login.cookies'
        self.cj = cookielib.MozillaCookieJar(self.cookie_file)
        self.opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),urllib2.HTTPHandler(debuglevel=0),urllib2.HTTPSHandler(debuglevel=0),urllib2.HTTPCookieProcessor(self.cj))
        # pretend we're a web browser and not a python script
        self.opener.addheaders = [
        ('User-agent', ('Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4')),
        ('Connection', ('keep alive')),
        ('Content-Type', ('application/x-www-form-urlencoded'))
        ]
        # open the front page of the website to set and save initial cookies
        self.response = self.opener.open(self.bu)
        self.cj.save()

    def get_page(self,url):
        self.u=self.bu+url
        self.response = self.opener.open(self.u)
        self.cj.save()
        return self.response

    def post_page(self,url,data={}):
        self.u=self.bu+url
        self.form_data =  urllib.urlencode(data)
        self.response = self.opener.open(self.u,self.form_data)
        self.cj.save()
        return self.response

    def return_raw_page(self,page):
        return page.read()

class SimpleUrl:
    '''This class is only for open simple pages. It can't use cookies but it is faster than AuthNetworkTools class.'''
    def __init__(self,base):
        self.ba=base

    def open_url(self,url):
        u=self.ba+url
        response=urllib2.urlopen(u)
        return response

class CustomUrl:
    def open(self,url):
        return urllib2.urlopen(url)
