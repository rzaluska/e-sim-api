#!/usr/bin/env python
# -*- coding: utf-8 -*-
from modules.net.usersesion import LoggedUserSesion
from modules.wrappers.wraper import Functions

x=LoggedUserSesion(0,'login','password')
e=Functions(x)
print 'Api For PRIMERA Server Immported'
print e.train()
print e.work()
x.logout()
print 'Logout'
print '=============='
x=LoggedUserSesion(1,'login','password')
e=Functions(x)
print 'Api For SECURA Server Immported'
print e.train()
print e.work()
x.logout()
print 'Logout'
