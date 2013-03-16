#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from BeautifulSoup import BeautifulSoup
from lxml import etree

class Functions:
    '''This class contains functions to parse e-sim data directly from this game pages.
    After every function response to e-sim server is sended so pages are allays had to be updated between every functions calls.
    Class contains functions to get data and also to put data to e-sim game.
    So now you have chance to administrate your e-sim account from python script.'''
    def __init__(self,LoggedUserSesionClass):
        self.n=LoggedUserSesionClass.n
    def send_money(self, targetId, currencyId, summ, reason):
        response = self.n.post_page('donateMoney.html?id=' + targetId, {'currencyId':currencyId, 'sum':summ, 'reason':reason})
        return response

    def get_curent_money(self):
        '''Return dictionary containing currncy names as keys and curency quantify as value'''
        response = self.n.get_page('index.html')
        strona = response.read()
        kasa = {}
        waluta = re.findall('<img class="currencyFlag" (.*)align="absmiddle" src="http://e-sim.home.pl/testura/img/(.*)"><b>(.*)</b> (.*) <br/>', strona)
        for n in waluta:
            kasa[n[-1]] = n[-2]
        return kasa

    def get_curent_military_details(self):
        response = self.n.get_page('train.html')
        strona = response.read()
        curent_military_details = {}
        strenght_gained = re.findall('<div style="font-weight: bold; font-size: 14px;">Strength gained: <b style="color: #090;" >(.*)</b> </div>', strona)
        if len(strenght_gained) == 0:
            print 'You didnt train today'
            curent_military_details['Strenght Gained'] = 0
        else:
            curent_military_details['Strenght Gained'] = strenght_gained[-1]
        military_stats = re.search(re.compile('<h2 class="biggerFont" style="text-align:center">Military details</h2>(.*)<TD valign="top" style="width: 135px; text-align: left">', re.DOTALL), strona)
        if military_stats:
            curent_military_details['Total training sessions'] = re.findall('Total training sessions:</td> <td style="width:200px"><div class="statsLabel smallStatsLabel blueLabel"><p style="margin: 0px 4px;">(.*)</p></div></td></tr>', military_stats.group())[-1]
            curent_military_details['Strenght'] = re.findall('Strength:</td> <td style="width:200px"><div class="statsLabel smallStatsLabel blueLabel"><p style="margin: 0px 4px;">(.*)</p></div></td> </tr>', military_stats.group())[-1]
            curent_military_details['Military rank'] = re.findall('Military rank:</td> <td><div style="height:20px;" class="statsLabel smallStatsLabel blueLabel"><p style="margin: 0px 4px;">(.*)  <img style', military_stats.group())[-1]
            curent_military_details['Total damege done'] = re.findall('<tr> <td>Total damage done:</td> <td><div class="statsLabel smallStatsLabel blueLabel"><p style="margin: 0px 4px;">(.*)</p></div></td> </tr>', military_stats.group())[-1]
            damages = re.findall('<tr> <td>(.*):</td><td><div class="statsLabel smallStatsLabel blueLabel"><b style="margin-left:4px;">(.*)</b> / <b style="margin-right:4px;">(.*)</b></div></td></tr>', military_stats.group())
            for n in damages:
                curent_military_details[n[0] + " min"] = n[1]
                curent_military_details[n[0] + " max"] = n[2]
        return curent_military_details

    def get_workplace_info(self):
        response = self.n.get_page('work.html')
        strona = response.read()
        soup = BeautifulSoup(strona)
        workplace_info = {}
        if_worked_today = re.findall('Today work results', strona)
        if len(if_worked_today) == 0:
            workplace_info['Worked Today'] = 0
        else:
            workplace_info['Worked Today'] = 1
            workplace_info['Net Salary'] = str(soup.find('table', {'class':'attributesTable'}).contents[3].contents[3].contents[0].contents[1].contents[0])
            workplace_info['Income tax paid'] = str(soup.find('table', {'class':'attributesTable'}).contents[5].contents[3].contents[0].contents[1].contents[0])
            workplace_info['Xp gained'] = str(soup.find('table', {'class':'attributesTable'}).contents[11].contents[3].contents[0].contents[0].contents[0])
            workplace_info['Economy skill gained'] = str(soup.find('table', {'class':'attributesTable'}).contents[13].contents[3].contents[0].contents[0].contents[0])
            workplace_info['Working days in a row'] = str(soup.find('table', {'class':'attributesTable'}).contents[15].contents[3].contents[0].contents[0].contents[0])
            workplace_info['Your base productivity'] = str(soup.find('table', {'class':'attributesTable'}).contents[19].contents[3].contents[0].contents[0].contents[0])
            workplace_info['Total productivity'] = str(soup.find('table', {'class':'attributesTable'}).contents[23].contents[3].contents[0].contents[0].contents[0])
            workplace_info['Units produced'] = str(soup.find('table', {'class':'attributesTable'}).contents[25].contents[3].contents[0].contents[0].contents[0])
            workplace_info['Productivity modifiers'] = str(soup.find('table', {'class':'attributesTable'}).contents[21].contents[3].contents[1].contents[0].contents[0])
        if_have_job = re.findall('You have no job', strona)
        if len(if_have_job) == 0:
            workplace_info['Have job'] = 1
        else:
            workplace_info['Have job'] = 0
        return workplace_info


    def change_churency(self, buyerCurrencyId, sellerCurrencyId, ammount, offerId):
        change_churency_action = 'monetaryMarket.html?buyerCurrencyId=' + buyerCurrencyId + '&sellerCurrencyId=' + sellerCurrencyId
        response = self.n.post_page(change_churency_action, {'action':'buy', 'id':offerId, 'ammount':ammount})
        return response


    def get_monetary_market_offers_list(self, buyerCurrencyId, sellerCurrencyId):
        monetary_market_offers_list = []
        if buyerCurrencyId != sellerCurrencyId:
            get_monetary_market_offers_list_action = 'monetaryMarket.html?buyerCurrencyId=' + buyerCurrencyId + '&sellerCurrencyId=' + sellerCurrencyId
            response = self.n.get_page(get_monetary_market_offers_list_action)
            strona = response.read()
            soup = BeautifulSoup(strona)
            ile = len(re.findall('<img align="absmiddle" class="smallAvatar" src="http://e-sim.org:3000/avatars/(.*)">', str(soup)))
            if ile != 0:
                n = 3
                while n < ile * 2 + 2:
                    offer = {}
                    offer['Amount'] = str(soup.find('table', {'style':'width: 600px', 'class':'dataTable'}).contents[n].contents[3].contents[2].contents[0])
                    offer['Ratio'] = str(soup.find('table', {'style':'width: 600px', 'class':'dataTable'}).contents[n].contents[5].contents[1].contents[0])
                    offer['Id'] = str(re.findall('<input type="hidden" name="id" value="(.*)" />', str(soup.find('table', {'style':'width: 600px', 'class':'dataTable'}).contents[n].contents[7].contents[1].contents[3]))[0])
                    monetary_market_offers_list.append(offer)
                    n = n + 2
            else:
                monetary_market_offers_list.append('No offers')
        else:
            monetary_market_offers_list.append('Cant exchange same type monay')
        return monetary_market_offers_list

    def get_ids(self):
        get_monetary_market_offers_list_action = 'monetaryMarket.html'
        response = self.n.get_page(get_monetary_market_offers_list_action)
        strona = response.read()
        soup = BeautifulSoup(strona)
        all_ids = re.findall('<option value="([0-9]+)"(.*)>(.*) \((.*)\)</option>', str(soup.find('select', {'id':'offeredMoneyId', 'name':'offeredMoneyId'})))
        # ilosc=len(all_ids)
        IDS = []
        for kraj in all_ids:
            s = {}
            s['ID'] = kraj[0]
            s['Currency'] = kraj[-2]
            s['Name']=kraj[-1]
            IDS.append(s)
        return IDS

    def get_company_info(self, company_id):
        response = self.n.get_page('company.html?id=' + company_id)
        strona = response.read()
        soup = BeautifulSoup(strona)
        company_info = {}
        company_info['Employer Name'] = str(soup.find('table', {'style':'text-align: middle; vertical-align: middle; width: 580px'}).contents[0].contents[7].contents[1].contents[0])
        company_info['Employer Id'] = str(re.findall('(.*)=([0-9]+)">(.*)</a>', str(soup.find('table', {'style':'text-align: middle; vertical-align: middle; width: 580px'}).contents[0].contents[7].contents[1]))[0][-2])
        company_info['Company Name'] = str(soup.find('table', {'style':'text-align: middle; vertical-align: middle; width: 580px'}).contents[0].contents[1].contents[1].contents[0])
        company_info['Company Region'] = str(soup.find('table', {'style':'text-align: middle; vertical-align: middle; width: 580px'}).contents[0].contents[5].contents[1].contents[2].contents[0])
        company_info['Company Country'] = str(soup.find('table', {'style':'text-align: middle; vertical-align: middle; width: 580px'}).contents[0].contents[5].contents[1].contents[1]).strip().strip('\n -')
        company_info['Company Id'] = str(re.findall('(.*)=(.*)" style="font-weight: bold">(.*)</a>', str(soup.find('table', {'style':'text-align: middle; vertical-align: middle; width: 580px'}).contents[0].contents[1].contents[1]))[0][1])
        company_info['Product Type'] = re.findall('<img src="http://e-sim.home.pl/testura/img/productIcons/(.*).png" title="" />', str(soup.find('table', {'style':'text-align: middle; vertical-align: middle; width: 580px'}).contents[0].contents[3].contents[1].contents[1].contents[1]))[0]
        company_info['Product Quality'] = re.findall('<img src="http://e-sim.home.pl/testura/img/productIcons/q([1-5]).png" title="" />', str(soup.find('table', {'style':'text-align: middle; vertical-align: middle; width: 580px'}).contents[0].contents[3].contents[1].contents[1].contents[3]))[0]
        return company_info

    def get_battle_info(self, battleId):
        response = self.n.get_page('battle.html?id=' + battleId)
        strona = response.read()
        soup = BeautifulSoup(strona)
        binfo = {}
        binfo['Region Name'] = soup.find('div',{'style':'font-size: 21px; font-weight: bold; text-align: center'}).findChildren('a')[0].text
        binfo['Region ID'] = soup.find('div',{'style':'font-size: 21px; font-weight: bold; text-align: center'}).findChildren('a')[0].attrs[-1][-1].split('=')[-1]
        if re.findall('Resistance war', str(soup)):  # do rozbudowy
            binfo['Battle type'] = 'Resistance war'
        elif soup.find('div',{'style':'font-size: 21px; font-weight: bold; text-align: center'}).findChildren('a')[1]:
             binfo['Battle type'] = soup.find('div',{'style':'font-size: 21px; font-weight: bold; text-align: center'}).findChildren('a')[1].text
        else:
            binfo['Battle type'] = 'Normal Battle'
        binfo['Current Round'] = re.findall('<div style="font-size: 17px; font-weight: bold; color: #111">Round ([0-9]+)</div>', str(soup))[0]
        binfo['Defender'] = re.findall('src=\"http://e-sim.home.pl/testura/img/flags/medium/(.*)\.png\" class="bigFlag', str(soup))[0]
        binfo['Defender Alliases'] = re.findall('src="http://e-sim.home.pl/testura/img/flags/small/(.*)\.png\"', str(soup.find('div', {'style':'position: absolute; top: 100px; left: -10px; width: 150px; background: rgba(200,200,255, 0.9); z-index: 3; display: none; text-align: left; border: 1px solid rgb(75, 75, 255); border-radius: 3px; box-shadow: 3px 3px 3px rgb(120, 120, 120); text-shadow: 1px 1px 1px white'})))
        binfo['Atacker'] = re.findall('src=\"http://e-sim.home.pl/testura/img/flags/medium/(.*)\.png\" class="bigFlag', str(soup))[1]
        binfo['Atacker Alliases'] = re.findall('src="http://e-sim.home.pl/testura/img/flags/small/(.*)\.png\"', str(soup.find('div', {'style':'position: absolute; top: 100px; left: 390px; width: 150px; background: rgba(200,200,255, 0.9); z-index: 3; display: none; text-align: left; border: 1px solid rgb(75, 75, 255); border-radius: 3px; box-shadow: 3px 3px 3px rgb(120, 120, 120); text-shadow: 1px 1px 1px white'})))
        binfo['Current round ID']=str(dict(soup.find('input' ,{'type':"hidden" ,'id':"battleRoundId" ,'name':"battleRoundId"}).attrs)['value'])
        binfo['Defender Procent']=soup.find('div',{'id':'defenderPercent'}).text
        binfo['Atacker Procent']=soup.find('div',{'id':'attackerPercent'}).text
        binfo['Rounds won by defender']=re.findall('Rounds won by defender\(([0-9]+)\)',strona)[0]
        binfo['Rounds won by attacker']=re.findall('Rounds won by attacker\(([0-9]+)\)',strona)[0]
        binfo['Defenders total damge'] = soup.find('b',{'id':'defenderScore'}).text
        binfo['Atacker total damge'] = soup.find('b',{'id':'attackerScore'}).text

               #binfo['Round time']=soup.find('span',{'class':'countdown_row countdown_amount'}).text
        return binfo

    def get_inventory_info(self):
        response = self.n.get_page('index.html')
        strona = response.read()
        soup = BeautifulSoup(strona)
        inv = {}
        prodocts = soup.findAll('div' , {'class':'storageMini'})
        for p in prodocts:
            if re.findall('src="http://e-sim.home.pl/testura/img/productIcons/q([1-5])\.png', str(p)):
                inv[re.findall('src="http://e-sim.home.pl/testura/img/productIcons/(.*)\.png', str(p))[0] + 'Q' + re.findall('src="http://e-sim.home.pl/testura/img/productIcons/q([1-5])\.png', str(p))[0]] = re.findall('<div> ([0-9]+)</div>', str(p))[0]
            else:
                inv[re.findall('src="http://e-sim.home.pl/testura/img/productIcons/(.*)\.png', str(p))[0]] = re.findall('<div> ([0-9]+)</div>', str(p))[0]
        return inv

    def get_product_market_offers_list(self, resource, countryId, quality='0'):
        response = self.n.get_page('productMarket.html?resource='+resource+'&countryId='+countryId+'&quality='+quality)
        strona = response.read()
        soup = BeautifulSoup(strona)
        l=[]
        ilosc=len(re.findall('value="buy',str(soup)))
        if ilosc!=0:
            n=3
            while n<=ilosc+1:
                o={}
                o['Seller Name']=str(soup.find('table',{'style':'width: 550px; margin-left: auto; margin-right: auto;','class':'dataTable'}).contents[n].contents[3].contents[1].contents[0])
                o['Seller ID']=str(soup.find('table',{'style':'width: 550px; margin-left: auto; margin-right: auto;','class':'dataTable'}).contents[n].contents[3].contents[1].attrs[0][1].split('=')[-1])
                o['Seller Country']=str(re.findall('http://e-sim.home.pl/testura/img/flags/small/(.*).png',str(soup.find('table',{'style':'width: 550px; margin-left: auto; margin-right: auto;','class':'dataTable'}).contents[n].contents[3].contents[3].attrs[2][1]))[0])
                o['Stock']=str(soup.find('table',{'style':'width: 550px; margin-left: auto; margin-right: auto;','class':'dataTable'}).contents[n].contents[5].contents[0]).strip()
                o['Price']=str(soup.find('table',{'style':'width: 550px; margin-left: auto; margin-right: auto;','class':'dataTable'}).contents[n].contents[7].contents[2].contents[0])
                o['ID']=str(soup.find('table',{'style':'width: 550px; margin-left: auto; margin-right: auto;','class':'dataTable'}).contents[n].contents[9].contents[1].contents[1].attrs[2][1])
                l.append(o)
                n=n+2
        return l

    def eat_food(self, quality):
        response = self.n.post_page('eat.html', {'quality':str(quality)})
        s=response.read()
        hp=re.findall('eat more, your health will exceed 100hp', s)
        inv=re.findall('No food in your inventory',s)
        if hp:
            stat ="Your can't eat more, your health will exceed 100hp"
        elif inv:
            stat='No food in your inventory'
        else:
            stat='Done'
        return stat

    def use_gift(self, quality):
        response = self.n.post_page('gift.html', {'quality':str(quality)})
        s=response.read()
        hp=re.findall('eat more, your health will exceed 100hp', s)
        inv=re.findall('No gifts in your inventory',s)
        if hp:
             stat ="Your can't eat more, your health will exceed 100hp"
        elif inv:
            stat='No gifts in your inventory'
        else:
            stat='Done'
        return stat

    def work(self):
        '''Try to work, if error occured return error code if no errors return 0
        Error codes are:
        1 - you have no job
        2 - raw problem
        3 - no monay in company
        4 - alredy worked today
        '''
        w_info=self.get_workplace_info()
        have_job=w_info['Have job']
        worked=w_info['Worked Today']
        if worked==1:
            status=4
        else:
            if have_job==1:
                response = self.n.get_page("work.html?action=work")
                strona = response.read()
                raw_problem=re.findall('There is no raw in the company. You can resign and find another job', strona)
                m_problem=re.findall('There is no money in the company. You can resign and find another job', strona)
                if len(raw_problem)!=0:
                    status=2
                elif len(m_problem)!=0:
                    status=3
                else:
                    status=0
            else:
                status=1
        return status

    def get_job(self,Id):
        response=self.n.post_page('jobMarket.html', {'id':Id})
        return response

    def leave_job(self):
        response=self.n.get_page('work.html?action=leave')
        return response

    def train(self):
        if 'Train' in self.get_todays_tasks_list():
            response = self.n.post_page('train.html')
            status=0
        else:
            status=1
        return status

    def fight(self,weaponQuality,battleRoundId,side,value):
        if side=='a':
            side='attacker'
        elif side=='d':
            side='defender'
        if value==1:
            value='Fight (1 hit)'
        elif value==5:
            value='Berserk! (5 hits)'
        response=self.n.post_page('fight.html',{'weaponQuality' : str(weaponQuality), 'battleRoundId' : str(battleRoundId), 'side' : side, 'value' : value})
        soup=BeautifulSoup(response.read())
        results={}
        if re.findall('No health left',str(soup)):
            results['Error']='No health left'
        elif re.findall('Server overloaded',str(soup)):
             results['Error']='Server Overloaded'
        else:
            results['Hit type']=soup.find('b',{'class':"mediumStatsLabel blueLabel",'style':"padding:3px 5px;"}).text
            results['Damage done']=soup.find('table').findChildren('td')[1].text
            results['Your total damage']=soup.find('table').findChildren('td')[3].text
            results['Your base damage']=soup.find('table').findChildren('td')[5].text
            results['Damage required for next rank']=soup.find('table').findChildren('td')[7].text
            results['Weapon bonus']=soup.find('table').findChildren('td')[9].text
            results['Xp gained']=soup.find('table').findChildren('td')[11].text
            results['Health']=soup.find('table').findChildren('td')[13].text
        return results

    def get_my_info(self):
        '''This function returns all info about curetly logged in player'''
        response = self.n.get_page('index.html')
        parser = etree.HTMLParser()
        tree = etree.parse(response, parser)
        info = {}
        info['Nick'] = tree.xpath('//*[@id="userName"]')[0].text
        info['Level'] = tree.xpath('//*[@id="userMenu"]/div[2]/div[2]/b')[0].text.strip('Level: ')
        info['Rank'] = tree.xpath('//*[@id="userMenu"]/div[2]/div[3]/b')[0].text.strip('Rank: ')
        info['Xp'] = tree.xpath('//*[@id="stats"]/div[1]/b[3]')[0].text.split('/')[0]
        info['Xp to next Level'] = tree.xpath('//*[@id="stats"]/div[1]/b[3]')[0].text.split('/')[1]
        info['Curent Damage'] = tree.xpath('//*[@id="stats"]/div[2]/b[3]')[0].text.split('/')[0]
        info['Damage to next Rank'] = tree.xpath('//*[@id="stats"]/div[2]/b[3]')[0].text.split('/')[1]
        info['Economy skill'] = tree.xpath('//*[@id="stats"]/b[1]')[0].text.strip('Economy skill: ')
        info['Strenght'] = tree.xpath('//*[@id="stats"]/b[2]')[0].text.strip('Strength: ')

        info['Location'] = []
        reg = []
        reg.append(tree.xpath('//*[@id="stats"]/b[3]/a')[0].text)
        reg.append(tree.xpath('//*[@id="stats"]/b[3]/a')[0].attrib['href'].split('=')[1])

        c = []
        cn = (re.findall('http://e-sim.home.pl/testura/img/flags/small/(.+)\.png', tree.xpath('//*[@id="stats"]/img[2]')[0].attrib['src'])[0])
        c.append(cn)
        c.append(self.get_ids()[cn]['ID'])
        info['Location'].append(reg)
        info['Location'].append(c)

        info['Health'] = tree.xpath('//*[@id="healthBar"]')[0].text
        info['Citizenship'] = re.findall('http://e-sim.home.pl/testura/img/flags/small/(.+)\.png', tree.xpath('//*[@id="stats"]/img[2]')[0].attrib['src'])[0]
        info['Food limit'] = tree.xpath('//*[@id="foodLimit"]')[0].text
        info['Gift limit'] = tree.xpath('//*[@id="giftLimit"]')[0].text
        info['ID']=tree.xpath('//*[@id="userName"]')[0].attrib['href'][16:]

        return info

    def get_job_offers_list(self,countryId,minimalSkill):
        '''Return list containing job offers witch maching to input params -> countryId and minimalSkill
        Best pay job will have index 0'''
        response = self.n.get_page('jobMarket.html?countryId='+countryId+'&minimalSkill='+minimalSkill)
        strona = response.read()
        soup = BeautifulSoup(strona)
        l=[]
        tabela=soup.find('table', {'class':'dataTable'})
        ile=len(re.findall('<img src="http://e-sim.home.pl/testura/img/productIcons/q(.+).png" title="" />',str(tabela)))
        if ile!=0:
            n=3
            while n<= ile*2+1:
                offer={}
                offer['Employer Name']=str(soup.find('table', {'class':'dataTable'}).contents[n].contents[1].contents[1].contents[0])
                offer['Employer ID']=str(soup.find('table', {'class':'dataTable'}).contents[n].contents[1].contents[1].attrs[0][1].split('=')[-1])
                offer['Employer Country']=str(re.findall('http://e-sim.home.pl/testura/img/flags/small/(.*).png',str(soup.find('table', {'class':'dataTable'}).contents[n].contents[1].contents[3].attrs[2][1]))[0])
                offer['Company Name']=str(soup.find('table', {'class':'dataTable'}).contents[n].contents[3].contents[1].contents[0])
                offer['Company ID']=str(soup.find('table', {'class':'dataTable'}).contents[n].contents[3].contents[1].attrs[0][1].strip('company.html?id='))
                offer['Company Type']=str(re.findall('http://e-sim.home.pl/testura/img/productIcons/(.*).png',soup.find('table', {'class':'dataTable'}).contents[n].contents[5].contents[1].contents[1].contents[1].attrs[0][1])[0])
                offer['Salary']=str(soup.find('table', {'class':'dataTable'}).contents[n].contents[9].contents[2].contents[0])
                offer['Offer ID']=str(soup.find('table', {'class':'dataTable'}).contents[n].contents[11].contents[1].contents[1].attrs[2][1])
                l.append(offer)
                n=n+2

        return l

    def buy_item(self,item_id,quantity):
        '''Buy specify item by given item id'''
        response = self.n.post_page('productMarket.html',{'id':item_id,'action':'buy','quantity':quantity})
        return response

    def join_party(self,partyId):
        response = self.n.post_page('partyStatistics.html',{'id':partyId,'action':'JOIN'})
        return response

    def leave_party(self):
        response = self.n.post_page('partyStatistics.html',{'action':'LEAVE'})
        return response

    def buy_shares(self,stockcompanyId,volume,price):
        response = self.n.post_page('stockCompanyAction.html',{'id':stockcompanyId,'action':'POST_BUY_SHARES_OFFER','volume':volume,'price':price})
        return response

    def sell_shares(self,stockcompanyId,volume,price):
        response = self.n.post_page('stockCompanyAction.html',{'id':stockcompanyId,'action':'POST_SELL_SHARES_OFFER','volume':volume,'price':price})
        return response

    def get_newspaper_info(self,newspaperId):
        response = self.n.get_page('newspaper.html?id='+newspaperId)
        strona = response.read()
        soup = BeautifulSoup(strona)
        liczba = len(re.findall('<div class="bigArticleTab">([0-9]+)</div>',str(soup)))
        info={}
        info['Newspaper ID']=soup.find('div',{'style':'width:440px;','class':'testDivblue'}).contents[1].contents[3].contents[1].contents[1].attrs[0][1].split('=')[-1]
        info['Newspaper Name']=soup.find('div',{'style':'width:440px;','class':'testDivblue'}).contents[1].contents[3].contents[1].contents[1].contents[0]
        info['Redactor ID']=soup.find('div',{'style':'width:440px;','class':'testDivblue'}).contents[1].contents[1].contents[1].attrs[0][1].split('=')[-1]
        info['Redactor Name']=soup.find('div',{'style':'width:440px;','class':'testDivblue'}).contents[1].contents[1].contents[1].contents[0]
        info['Subs']=soup.find('div',{'style':'width:440px;','class':'testDivblue'}).contents[1].contents[5].contents[1].contents[0].contents[0].strip()
        info['Articles']=[]
        n=3
        while n<=liczba*2+1:
            l={}
            l['Name']=soup.find('table',{'class':'dataTable'}).contents[n].contents[1].contents[3].contents[1].contents[0] #nazwa
            l['ID']=soup.find('table',{'class':'dataTable'}).contents[n].contents[1].contents[3].contents[1].attrs[0][1].split('=')[-1]
            l['Votes']=soup.find('table',{'class':'dataTable'}).contents[n].contents[1].contents[1].contents[0]
            info['Articles'].append(l)
            n=n+2
        return info

    def vote(self,candidateId):
        response = self.n.post_page('newspaper.html?id=',{'action':'VOTE','candidateId':candidateId})
        return response

    def get_own_product_market_offers_list(self):
        response=self.n.get_page('citizenMarketOffers.html')
        l=[]
        soup=BeautifulSoup(response.read())
        tabela=soup.find('table',{'class':'dataTable'}).findChildren('tr')[1:]
        for x in tabela:
            o={}
            if len(x.contents[1].contents[1].contents[1].contents)!=5:
                o['Product']=str(x.contents[1].contents[1].contents[1].contents[1].attrs[0][1][46:-4])
            else:
                o['Product']=str(x.contents[1].contents[1].contents[1].contents[1].attrs[0][1][46:-4])+'Q' +str(x.contents[1].contents[1].contents[1].contents[3].attrs[0][1][47:-4])
            o['Stock']=x.contents[5].contents[0].strip()
            o['Price (Gross)']=x.contents[7].contents[2].contents[0]
            o['Price (Net)']=x.contents[9].contents[2].contents[0]
            o['Vat']=x.contents[11].contents[2].contents[0]
            o['Import Tax']=x.contents[13].contents[2].contents[0]
            o['ID']=x.contents[15].contents[1].contents[1].attrs[2][1]
            l.append(o)
        return l

    def add_citizen_to_friend_list(self,citizenId):
        response=self.n.get_page('friends.html?action=PROPOSE&id='+citizenId)
        return response

    def delate_own_product_market_offer(self,offerID):
        response=self.n.post_page('citizenMarketOffers.html', {'id':offerID,'action':'DELETE_OFFER'})
        return response

    def post_new_product_market_offer(self,countryId,product,quantity,price):
        response=self.n.post_page('citizenMarketOffers.html', {'countryId':countryId,'product':product,'quantity':quantity,'price':price,'action':'POST_OFFER'})
        return response

    def get_citizen_equipment_stats(self,citizenId):
        response=self.n.get_page('profile.html?id='+str(citizenId))
        soup=BeautifulSoup(response.read())
        eq={}
        eq['Damage min']=soup.find('div',{'id':'hitHelp'}).findChildren('b')[0].text
        eq['Damage max']=soup.find('div',{'id':'hitHelp'}).findChildren('b')[1].text
        eq['Critical Hit min']=soup.find('div',{'class':'equipmentBlueBox'}).findChildren('b')[0].text
        eq['Critical Hit max']=soup.find('div',{'class':'equipmentBlueBox'}).findChildren('b')[-1].text
        eq['Critical Hit chance']=soup.find('div',{'id':'criticalHelp'}).findChildren('b')[0].text
        eq['Miss chance']=soup.find('div',{'id':'missHelp'}).findChildren('b')[0].text
        eq['Chance to avoid DMG']=soup.find('div',{'id':'avoidHelp'}).findChildren('b')[0].text
        for s in soup.find('div',{'style':'float:left;margin-left:10px; width:240px;min-height:210px;'}).findChildren('div')[2].findChildren('div',{'style':'overflow:auto;'}):
            eq[s.findChild('div', {'class':"statsLabel smallDescLabel"}).text]=s.findChild('div', {'class':"statsLabelRight descStatsLabel blueLabel"}).text
        return soup

    def get_citizen_friends_list(self,citizenId):
        l=[]
        response=self.n.get_page('profile.html?id='+citizenId)
        soup=BeautifulSoup(response.read())
        count_pages=int(soup.find('ul',{'id':'pagination-digg'}).findChildren('li')[-2].text)+1
        for x in range(1,count_pages):
            response=self.n.get_page('profile.html?id='+citizenId+'&page='+str(x))
            soup=BeautifulSoup(response.read())
            for y in soup.findAll('div',{'style':'float: left; width: 92px; height: 75px; word-wrap: break-word'}):
                w={}
                w['Nick']=y.contents[1].contents[0]
                w['ID']=dict(y.contents[1].attrs)['href'][16:]
                w['Citizenship']=y.contents[3].attrs[2][1][45:-4]
                l.append(w)
        return l

    def get_citizen_medals_list(self,citizenId):
        response=self.n.get_page('profile.html?id='+citizenId)
        soup=BeautifulSoup(response.read())
        medals=soup.find('div',{'id':'medals'}).findChildren('div',{'class':'medal'})
        med={}
        for medal in medals:
            if medal.contents[-1].split('medals/')[-1][:-6]==u'emptyMedal':
                med[medal.findChildren('b')[0].text]='0'
            else:
                try:
                    med[medal.findChildren('b')[0].text]=str(medal.findChildren('div')[0].text[1:])
                except IndexError:
                    med[medal.findChildren('b')[0].text]='1'
        return med

    def get_game_day(self):
        response = self.n.get_page('index.html')
        return re.findall('day ([0-9]+)',response.read())[0]

    def send_ingame_message(self,receiverName,title,body):
        response=self.n.post_page('composeMessage.html',{'receiverName':receiverName,'title':title,'body':body,'action':'REPLY'})
        return response

    def get_todays_tasks_list(self):
        response=self.n.get_page('index.html')
        soup=BeautifulSoup(response.read())
        l=[]
        if soup.find('div',{'id':'showTutorialTutorial'}):
            for task in soup.find('div',{'id':'showTutorialTutorial'}).findChildren('span'):
                l.append(task.text)
        return l

    def get_server_time(self):
        soup=BeautifulSoup(self.n.get_page('index.html'))
        time={}
        time['Hour']=soup.find('b',{'id':'time'}).text.split(' ')[0].split(':')[0]
        time['Minutes']=soup.find('b',{'id':'time'}).text.split(' ')[0].split(':')[1]
        time['Day']=soup.find('b',{'id':'time'}).text.split(' ')[1].split('-')[0]
        time['Mounth']=soup.find('b',{'id':'time'}).text.split(' ')[1].split('-')[1]
        time['Year']=soup.find('b',{'id':'time'}).text.split(' ')[1].split('-')[2]
        return time

    def vote_for_article(self,articleId):
        return self.n.post_page('vote.html?id='+articleId)

    def subscrible_newspaper(self,newspaperId):
        return self.n.post_page('sub.html?id='+newspaperId)



