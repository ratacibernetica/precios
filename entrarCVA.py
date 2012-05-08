import urllib, urllib2, cookielib

usuario = "passatempo"
password = "bleach01"
filename = "lista.html"
archivo = "lista.txt"
contenido = ""

#Descargar imagenes

def dImg(idImg,url):
	
	img = urllib.URLopener()
	img.retrieve(url,'imagenes/'+idImg+".jpg")
	print "imagen guardada"

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
contenido=""
for item in html:
	if j<10:
		if s+str(j)+'"' in item:
			contador = 1
			#con esto lee la siguiente linea HTML
			itemb = html[html.index(item)+contador]
			#Saca el texto entre los TAGS 
			codigo = stripHTMLTags(itemb)
			
			#El contador es el offset de lectura
			contador = 2
			itemb = html[html.index(item)+contador]
			nombre = stripHTMLTags(itemb)
			
			contador = 5
			itemb = html[html.index(item)+contador]
			marca = stripHTMLTags(itemb)
			

			while (itemb.find('<a href="'+"javascript:void(window.open('http://www.grupocva.com/me_bpm/detalle_articulo/me_articulo.php?fProdId=") < 0):
				contador += 1
				itemb = html[html.index(item)+contador]
			nombre2 = stripHTMLTags(itemb)
			
			
			
			while (itemb.find('id="fPrecioLista"') < 0):
				contador += 1
				itemb = html[html.index(item)+contador]
			precio = stripHTMLTags(itemb)
			
			itemb = html[html.index(item)+contador]
			while (itemb.find('id="fExistencia"') < 0):
				contador += 1
				itemb = html[html.index(item)+contador]
			itemb = itemb[72:]
			cantidad = itemb[:-6]
			
			itemb = html[html.index(item)+contador]
			
			while (itemb.find('id="ProdID"') < 0):
				contador += 1
				itemb = html[html.index(item)+contador]
			itemb = itemb[63:]
			productId = itemb[:-6]
			
			
			
			
			imagenUrl = "http://www.grupocva.com/me_bpm/detalle_articulo/imagen_art.php?fProd="+productId
			dImg(productId,imagenUrl)
			
			contenido += codigo+','+nombre+','+nombre2+','+marca+','+precio+','+productId+','+cantidad+','+productId+'\n'
			
			
			j += 1
					
contenido += "Fin del archivo"
			
			
			
			


print "Guardando a archivo " + archivo	+ "..."	
FILE = open(archivo,"w")
FILE.writelines(contenido)
FILE.close()
print "OK"
f.close()


