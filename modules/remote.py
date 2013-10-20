#!/usr/bin/env python
# -*- coding: utf-8 -*-

from network.network import CookieAuth
from wrappers.wraper import LoggedUserSesion

esim = LoggedUserSesion(CookieAuth,0)
esim.login("","")
