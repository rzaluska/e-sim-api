#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from network import SimpleUrl

class OfficialApi:
    '''Wrapper around official e-sim's API'''
    def __init__(self, server):
        if server == 0:
            self.n = SimpleUrl("http://primera.e-sim.org/")
        elif server == 1:
            self.n = SimpleUrl("http://secura.e-sim.org/")

    def get_citizen_by_id(self,citizenId):
        page=self.n.open_url('apiCitizenById.html?id='+citizenId)
        return json.loads(page.read())

    def get_citizen_by_name(self,name):
        page=self.n.open_url('apiCitizenByName.html?name='+name)
        return json.loads(page.read())

    def get_military_unit_by_id(self,mu_id):
        page=self.n.open_url('apiMilitaryUnitById.html?id='+mu_id)
        return json.loads(page.read())

    def get_military_unit_members_list(self,mu_id):
        page=self.n.open_url('apiMilitaryUnitMembers.html?id='+mu_id)
        return json.loads(page.read())

