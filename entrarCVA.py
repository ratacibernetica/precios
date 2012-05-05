import urllib, urllib2, cookielib, HTMLParser
import BeautifulSoup

usuario = "passatempo"
password = "bleach01"
filename = "lista.html"

#Funcion para quitar el codigo HTML de las lineas
def stripHTMLTags (html):
  """
    Strip HTML tags from any string and transfrom special entities
  """
  import re
  text = html
 
  # apply rules in given order!
  rules = [
    { r'>\s+' : u'>'},                  # remove spaces after a tag opens or closes
    { r'\s+' : u' '},                   # replace consecutive spaces
    { r'\s*<br\s*/?>\s*' : u'\n'},      # newline after a <br>
    #{ r'</(div)\s*>\s*' : u'\n'},       # newline after </p> and </div> and <h1/>...
    #{ r'</(p|h\d)\s*>\s*' : u'\n\n'},   # newline after </p> and </div> and <h1/>...
    { r'<head>.*<\s*(/head|body)[^>]*>' : u'' },     # remove <head> to </head>
    { r'<a\s+href="([^"]+)"[^>]*>.*</a>' : u'' },  # show links instead of texts
    { r'[ \t]*<[^<]*?/?>' : u'' },            # remove remaining tags
    { r'^\s+' : u'' }                   # remove spaces at the beginning
  ]
 
  for rule in rules:
    for (k,v) in rule.items():
      regex = re.compile (k)
      text  = regex.sub (v, text)
 
  # replace special strings
  special = {
    '&nbsp;' : ' ', '&amp;' : '&', '&quot;' : '"',
    '&lt;'   : '<', '&gt;'  : '>'
  }
 
  for (k,v) in special.items():
    text = text.replace (k, v)
 
  return text


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

data = urllib.urlencode({"fGiraRegistro": "", "fUsuarioNew": usuario, "fContraseniaNew" : password, "fmtipoNew":"contacto"})
request = urllib2.Request("https://www.grupocva.com/me_bpm/ControlInicioSesion.php", data)
f = urllib2.urlopen(request)

request = urllib2.Request("http://www.grupocva.com/me_bpm/welcome/welcome.php",None)
f = urllib2.urlopen(request)
html = f.readlines()
for item in html: 
	if "ISAAC" in item: 
		item = stripHTMLTags(item)
		print item

print "Descargando documento, espere por favor"
#Leer catalogo de productos con existencia en Puebla
data = urllib.urlencode({"fClave": "", "fCodFab": "", "fLibre" : "", "fMarca":"%", "fGrupo":"%", "fOrden":"2","fDisp":"1", "Submit2":"Generar"})
request = urllib2.Request("http://www.grupocva.com/me_bpm/Cotizaciones/CotizaListaPrecio.php", data)
f = urllib2.urlopen(request)
html = f.readlines()

#Buscamos el numero de productos encontrados (i) para ir iterando entre las "fPartidas"

print "Leyendo cantidad de archivos..."
i=0
for item in html: 
	if "registros" in item: 
		item2 = stripHTMLTags(item)
		item2 = item2[33:]
		i=int(item2)
		print "Numero de productos encontrados :"+str(i)
		
		
print "Iterando en fPartidas..."
#Iteramos en todos los productos para obterner su informacion
s='id="fPartida'
j=0
for item in html:
	if j<i:
		if s+str(j)+'"' in item: 
			print item
			j = j+1

#Guardar Archivo
"""
print "Guardando a archivo " + filename	+ "..."	
FILE = open(filename,"w")
FILE.writelines(html)
FILE.close()
print "OK"
"""
f.close()


