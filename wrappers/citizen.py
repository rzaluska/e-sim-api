#!/usr/bin/env python
# -*- coding: utf-8 -*-

def __init__(self,LoggedUserSesionClass,citizenId):
    self.n=LoggedUserSesionClass.n
    response=self.n.get_page('profile.html?id='+str(citizenId))
    self.soup=BeautifulSoup(response)

