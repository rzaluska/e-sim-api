#!/usr/bin/env python
# -*- coding: utf-8 -*-

from network import AuthNetworkTools

class LoggedUserSesion:
    '''Arguments for class are server, login and password.'''
    def __init__(self, server,login, password):
        if server == 0:
            self.n = AuthNetworkTools("http://primera.e-sim.org/")
        elif server == 1:
            self.n = AuthNetworkTools("http://secura.e-sim.org/")
        self.n.post_page('login.html', {'login':login, 'password':password})

    def logout(self):
        response = self.n.get_page('logout.html')
        if response.code == 200:
            s = 'OK'
        else:
            s = 'ERROR'
        return s
