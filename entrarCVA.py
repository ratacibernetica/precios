import urllib, urllib2, cookielib, HTMLParser
import BeautifulSoup

# #Class used to parse HTML to be scraped.
# class MyParser(HTMLParser.HTMLParser):
	# def __init__(self):
		# HTMLParser.HTMLParser.__init__(self)
		# self.data_type = ""
	# def handle_data(self, data):
		# if not self.data_type:
			# if data.lower() == "point balance":
				# self.data_type = "balance"
			# elif data.lower() == "points available to redeem":
				# self.data_type = "points available to redeem"
			# elif data.lower() == "pending points":
				# self.data_type = "pending points"
		# else:
			# print "%s: %s" % (self.data_type, data)
			# self.data_type = ""

usuario = "passatempo"
password = "bleach01"
filename = "lista.html"

#cookie storage
cj = cookielib.LWPCookieJar()

#create an opener
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

#Add useragent, sites don't like to interact programs.
opener.addheaders.append(('User-agent', 'Mozilla/4.0'))
opener.addheaders.append( ('Referer', 'http://www.grupocva.com') )

#Create initial request -- This is like when you first browse to the page.  Since the cookie jar was empty, it will
#be like you initially cleared them from your browser.
#Cookies may set at this point.
request = urllib2.Request("http://www.grupocva.com", None)
f = urllib2.urlopen(request)
f.close()

#Now you have to make a request like you submitted the form on the page.  
#Notice that two hidden fields plus the email and password fields are sent to the form processing page.
data = urllib.urlencode({"entrar": "+Entrar", "fUsuario": usuario, "fContrasenia" : password, "fmtipo":"contacto"})
request = urllib2.Request("https://www.grupocva.com/me_bpm/logincontrol.php", data)
f = urllib2.urlopen(request)

#Read the page.
# html = f.read()
# print html

data = urllib.urlencode({"fGiraRegistro": "", "fUsuarioNew": usuario, "fContraseniaNew" : password, "fmtipoNew":"contacto"})
request = urllib2.Request("https://www.grupocva.com/me_bpm/ControlInicioSesion.php", data)
f = urllib2.urlopen(request)

#Read the page.
# html = f.read()
# print html
request = urllib2.Request("http://www.grupocva.com/me_bpm/welcome/welcome.php",None)
f = urllib2.urlopen(request)
html = f.readlines()
for item in html: 
	if "ISAAC" in item: 
		print item


#Leer catalogo de productos con existencia en Puebla
data = urllib.urlencode({"fClave": "", "fCodFab": "", "fLibre" : "", "fMarca":"%", "fGrupo":"%", "fOrden":"2","fDisp":"1", "Submit2":"Generar"})
request = urllib2.Request("http://www.grupocva.com/me_bpm/Cotizaciones/CotizaListaPrecio.php", data)
f = urllib2.urlopen(request)
html = f.read()

# for item in html: 
	# if "fClave" in item: 
		# print item
		
# FILE = open(filename,"w")
# FILE.writelines(html)
# FILE.close()

f.close()


#Parse the html here (html contains the page markup). 
# parser = MyParser()
# parser.feed(html)

# #encode the login data. This will vary from site to site.
# #View the sites source code
# #Example###############################################
# #<form id='loginform' method='post' action='index.php'>
# #<div style="text-align: center;">
# #Username<br />
# #<input type='text' name='user_name' class='textbox' style='width:100px' /><br />
# #Password<br />
# #<input type='password' name='user_pass' class='textbox' style='width:100px' /><br />
# #<input type='checkbox' name='remember_me' value='y' />Remember Me<br /><br />
# #<input type='submit' name='login' value='Login' class='button' /><br />
# # login_data = urllib.urlencode({'fUsuario' : 'passatempo',
                               # # 'fContrasenia' : 'bleach01',
                               # # 'entrar' : 'Entrar'
                               # # })
# # resp = opener.open('http://www.grupocva.com/mkt/apoyo/web12/index.php', login_data)
# #you are now logged in and can access "members only" content.
# #when your all done be sure to close it

# #mypath = "http://www.grupocva.com/me_bpm/Cotizaciones/CotizaListaPrecio.php" 
# # mylines = resp.readlines();
# # for item in mylines: 
	# # print item
# # resp.close()

# import cookielib
# import urllib
# import urllib2

# url = 'www.grupocva.com/mkt/apoyo/web12/index.php'
# values = {'fUsuario' : 'passatempo',
          # 'fContrasenia' : 'bleach01',
          # 'password-password' : 'mypassword' 
		  # 'fmtipo
		  # }

# data = urllib.urlencode(values)
# cookies = cookielib.CookieJar()

# opener = urllib2.build_opener(
    # urllib2.HTTPRedirectHandler(),
    # urllib2.HTTPHandler(debuglevel=0),
    # urllib2.HTTPSHandler(debuglevel=0),
    # urllib2.HTTPCookieProcessor(cookies))

# response = opener.open(url, data)
# the_page = response.read()
# http_headers = response.info()
# # The login cookies should be contained in the cookies variable
