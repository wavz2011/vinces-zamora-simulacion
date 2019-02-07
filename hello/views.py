#para importar clases y metodos
#from .alisamiento import alisamiento
from random import random, randrange
import math
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.messages import get_messages
from django.contrib import messages

from .forms import linealForm,adiForm, multiForm, randomForm, pruebaForm, sideseo, generaForm

	      
datos = {}
numeros = []
#almacena para generar txtfield para numeros en promedio movil
genera = {}

#llamamos al metodo - ojo esto es una prueba
#alisamiento()
def profile(request):
	if request.method == 'POST':
		return redirect("postData")
	else:
		
		return render(request, "profile.html")


def prueba(nr):
		#variable iniciada de la media
		#print(nr)
		media=0
		#variable m para sumar los valores de 
		m=0
		#contador
		count=0
		#calcular la media
		for i in nr:
			m=m+i
			#definimos el contador
			count=count+1
			#realizamos el calculo donde m es el total de la suma de los numeros y count es el numero ejemplo 160/3
			media=round((m/count),3)
		#print("media: ",media)
		
		#print("n=",count)
		N=count
		#Sean n1 y n2 el número de observaciones individuales por encima y por debajo de la media,
		#respectivamente y sea b como el número total de corridas.

		#arreglo de signos para el posterior calculo de las variables
		nX = []
        
		for i in nr:
			#Denotaremos con un signo - a aquel número que se encuentre por debajo de la media.
			if i <  media:
				nX.append('-')
			else:
				#Denotaremos con un signo + a aquel número que se encuentre por arriba de la media.
				if i >=  media:
					nX.append('+')
		#print(nX)

		#obtencion de la variable  b  numero de corridas o rachas 
		y=0
		b=0
		for i2 in nX:
			if i2 != y:
				b = b+1
			y=i2
		#print('Numero de rachas : ',b)

		#n1 número de observaciones individuales por encima de la media 
		y=0
		n1=0
		for i2 in nX:
			if i2 == "+":
				n1 = n1+1
			y=i2
		#print('Casos >= media :' ,n1)

		#n1 número de observaciones individuales por debajo de la media 
		y=0
		n2=0
		for i2 in nX:
			if i2 == "-":
				n2 = n2+1
			y=i2
		#print('Casos < media :',n2)

		#print('Casos totales :',n1+n2)
		
		sms = ''

		u= 0
		q= 0
		z= 0

		if b <= 2:
			#print('numero de corridas muy bajo por lo que se puede definir que los datos no son aleatorios')
			sms='numero de corridas muy bajo por lo que se puede definir que los datos no son aleatorios'
			s=""
		else:
			if n1<20 and n2<20 :
				#print("no se aproxima a una distribución normal ya que n1 o n2 <20")
			 	#valor critico para confiabilidad del 95 %
				#z=1,96
	        	#primera formula Esperado cuando no se aproxima a la distribuicion binomial
				u = round((2*(n1*n2)/N)+(1/2),3)
				#print("ur=",u)

				#segunda formula
				a= 2*(n1*n2)
				b1 = a-N
				q = round(math.sqrt(a*b1 /(N**2*(N-1))),3)
				#print("qr= ",q)

				#pedir variable de significancia por formulaio confiabilidad del 95%
				#valor critico
				s=1.96
				#print('val Crit',s , ' nivel de confianza del 95%')
				#tercera formula

				z = round((b - u)/ q,3)
				#print("variable z=",z)

				if -s <= z <= s:
					sms=' Son numeros aleatorios'
					#print('-s = -',s,'< z = ',z,' < s ',s)
				else:
					sms='No son numeros aleatorios'
					#print('no son numeros aleatorios')


			else:
				#print("se aproxima a la normal")
				
				#valor critico para confiabilidad del 95 %
				#z=1,96
	        	#primera formula Esperado
				u = round((2*(n1*n2)/N)+1,3)
				#print("ur=",u)

				#segunda formula
				a= 2*(n1*n2)
				b1 = a-N
				q = round(math.sqrt(a*b1 /(N**2*(N-1))),3)
				#print("qr= ",q)

				#pedir variable de significancia por formulaio confiabilidad del 95%
				#valor critico
				s=1.96
				#print('val Crit',s , ' nivel de confianza del 95%')
				#tercera formula

				z = round((b - u)/ q,3)
				#print("variable z=",z)

				if -s <= z <= s:
					sd='-s = -',s,'< z = ',z,' < s ',s 
					#print(sd)
					sms='la hipótesis de independencia no puede ser rechazada sobre la base de esta prueba ya que se cumple ',sd, ' por lo que los numeros son aleatorios'
					
				else:
					sd='-s = -',s,'< z = ',z,' < s ',s
					sms='la hipótesis de independencia es rechazada ya que no se cumple ',sd,' por lo que los numeros no son aleatorios'
					#print(sd)
				
		context={"media":media,"n1":n1,"n2":n2,"sms":sms,"u":u,"q":q,"z":z,"b":b,"s":s}
		#print(context)
		return context
		

# Create your views here.
#Metodo de congruencias lineal o mixto
def lineal(request):
	global datos
	if request.method == 'POST':
			#check = sideseo(request.POST)
			#instance = form.save(commit=False)
		m1 = request.POST.get("M","")
		Xn1 = request.POST.get("Xn","")
		a1 = request.POST.get("A","")
		c1 = request.POST.get("C","")
		n1 = request.POST.get("N","")

		m=int(m1)
		Xn=int(Xn1)
		a=int(a1)
		c=int(c1)
		n=int(n1)

		nr = []
		nX = ''
		rX = ''
		listaFrame=''
		for i in range (1, n+1) :
			n=i
			axn=(Xn*a)+c
			axnm=axn%m
			r=round(axnm/m,3)
			nr.append({'n':i,'Xn':Xn,'r':r,'axn':axn,'axnm':axnm})
			listaFrame+=str(r)+ ' '
			Xn = axnm
			nX = nX + str(n) + ','
			rX = rX + str(r) + ','
		#Haceer las pruebas
		nr1=[]
		for n  in nr:
			#print (n.get('r'))
			nr1.append(n.get('r'))
					
		h = prueba(nr1)

		media=h.get('media')
		n1=h.get('n1')
		n2=h.get('n2')
		sms=h.get('sms')
		u=h.get('u')
		q=h.get('q')
		b=h.get('b')
		z=h.get('z')
		s=h.get('s')

		datos = {
			"metodo":"Lineal",
			"icono":"fa fa-line-chart",
			"m":nr,
			"n":nX,
			"r":rX,
			"i" : n,
			"media":media,
			"n1":n1,
			"n2":n2,
			"sms":sms,
			"u":u,
			"q":q,
			"b":b,
			"z":z,
			"s":s,
			"listaFrame":listaFrame
		}

		return redirect("postData")
	else:
		datos = {}
		return render(request, "lineal.html")


def aditivo(request):
	global datos
	if request.method == 'POST':
		form = adiForm(request.POST or None)

		if form.is_valid():
			#instance = form.save(commit=False)
			m = form.cleaned_data.get("M")
			Xo = form.cleaned_data.get("Xo")
			Xn = form.cleaned_data.get("Xn")
			n = form.cleaned_data.get("N")
			nr = []
			nX = ''
			rX = ''
			for i in range (1, n+1) :
				n=i
				varx=Xn+Xo
				Xn=Xo
				cant=varx
				Xo=cant%m
				div=round(Xo/(m-1),3)
				nr.append({'n':n,'Xn':Xn,'cant':cant,'Xo':Xo,'div':div})
				nX = nX + str(i) + ','
				rX = rX + str(div) + ','

			#Haceer las pruebas
			nr1=[]
			for n  in nr:
				#print (n.get('div'))
				nr1.append(n.get('div'))
			
			#realizamos la prueba y obtenemos los datos		
			h = prueba(nr1)
			media=h.get('media')
			n1=h.get('n1')
			n2=h.get('n2')
			sms=h.get('sms')
			u=h.get('u')
			q=h.get('q')
			b=h.get('b')
			z=h.get('z')
			s=h.get('s')

			datos = {
				"metodo":"Aditivo",
				"icono":"fa fa-plus",
				"m":nr,
				"n":nX,
				"r":rX,
				"i" : n,
				"media":media,
				"n1":n1,
				"n2":n2,
				"sms":sms,
				"u":u,
				"q":q,
				"b":b,
				"z":z,
				"s":s,
			}
		return redirect("postData")
	else:
		datos = {}
		form = adiForm()
		return render(request, "aditivo.html", {'form': form})				



def multiplicativo(request):
	global datos
	
	if request.method == 'POST':
		form = multiForm(request.POST or None)	
		if form.is_valid():
			#instance = form.save(commit=False)
			m = form.cleaned_data.get("M")
			Xn = form.cleaned_data.get("Xn")
			a = form.cleaned_data.get("A")
			c = form.cleaned_data.get("C")
			n = form.cleaned_data.get("N")
			nr = []
			#variables para el grafico
			nX = ''
			rX = ''
	
			for i in range (1, n+1) :
				n=i
				axn=(Xn*a)
				axnm=axn%m
				r=round(axnm/m,3)
				nr.append({'n':i,'Xn':Xn,'r':r,'axn':axn,'axnm':axnm})
				Xn = axnm
				nX = nX + str(i) + ','
				rX = rX + str(r) + ','
				

			#Haceer las pruebas
			nr1=[]
			for n  in nr:
				#print (n.get('r'))
				nr1.append(n.get('r'))
						
			h = prueba(nr1)
			media=h.get('media')
			n1=h.get('n1')
			n2=h.get('n2')
			sms=h.get('sms')
			u=h.get('u')
			q=h.get('q')
			b=h.get('b')
			z=h.get('z')
			s=h.get('s')
				

			datos = {
				"metodo":"Multiplicativo",
				"icono":"fa fa-times",
				"m":nr,
				"n":nX,
				"r":rX,
				"i" : n,
				"media":media,
				"n1":n1,
				"n2":n2,
				"sms":sms,
				"u":u,
				"q":q,
				"b":b,
				"z":z,
				"s":s,
			}	
		return redirect("postData")
	else:
		datos = {}
		form = multiForm()
		return render(request, "multiplica.html", {'form': form})
	

def random(request):
	import math
	import random
	#print(random)
	global datos
	
	if request.method == 'POST':
		form = randomForm(request.POST or None)

		#print (dir(form))
		if form.is_valid():
			#instance = form.save(commit=False)
			n = form.cleaned_data.get("N")
			nr = []
			nX = ''
			rX = ''
		
			for i in range (1, n+1) :
				
				n=i
				x=random.randrange(0,100)
				y=x/100
				nr.append({'n':n,'y':y})
				nX = nX + str(i) + ','
				rX = rX + str(y) + ','

				#hacemos la prueba respectiva
			nr1=[]
			for n  in nr:
				#print (n.get('y'))
				nr1.append(n.get('y'))
						
			h = prueba(nr1)
			media=h.get('media')
			n1=h.get('n1')
			n2=h.get('n2')
			sms=h.get('sms')
			u=h.get('u')
			q=h.get('q')
			b=h.get('b')
			z=h.get('z')
			s=h.get('s')
		
				
			datos = {
				"metodo":"Random",
				"icono":"fa fa-random",
				"m":nr,
				"n":nX,
				"r":rX,
				"i" : n,
				"media":media,
				"n1":n1,
				"n2":n2,
				"sms":sms,
				"u":u,
				"q":q,
				"b":b,
				"z":z,
				"s":s,
			}
		return redirect("postData")
	else:
		datos = {}
		form = randomForm()
		return render(request, "random.html", {'form': form})
	


def postData(request):
	global datos, numeros
	#print(datos)
	
	if datos == {}:
		#print("no hay contexto")
		return redirect("lineal")
	else:
		if request.method == 'POST':
			print("Es un Post")
			#logica cuando se envia un formulario desde la Url Post data

		else:
			context = datos
			form = sideseo()
			context['form'] = form
			#print(context)
			return render(request,"detailData.html",context)



#Iframes
def metodoLineal(request):
	global datos
	if request.method == 'POST':
			#check = sideseo(request.POST)
			#instance = form.save(commit=False)
		m1 = request.POST.get("M","")
		Xn1 = request.POST.get("Xn","")
		a1 = request.POST.get("A","")
		c1 = request.POST.get("C","")
		n1 = request.POST.get("N","")

		m=int(m1)
		Xn=int(Xn1)
		a=int(a1)
		c=int(c1)
		n=int(n1)

		nr = []
		nX = ''
		rX = ''
		listaFrame=''
		for i in range (1, n+1) :
			n=i
			axn=(Xn*a)+c
			axnm=axn%m
			r=round(axnm/m,3)
			nr.append({'n':i,'Xn':Xn,'r':r,'axn':axn,'axnm':axnm})
			listaFrame+=str(r)+ ' '
			Xn = axnm
			nX = nX + str(n) + ','
			rX = rX + str(r) + ','
		#Haceer las pruebas
		nr1=[]
		for n  in nr:
			#print (n.get('r'))
			nr1.append(n.get('r'))
					
		h = prueba(nr1)

		media=h.get('media')
		n1=h.get('n1')
		n2=h.get('n2')
		sms=h.get('sms')
		u=h.get('u')
		q=h.get('q')
		b=h.get('b')
		z=h.get('z')
		s=h.get('s')

		datos = {
			"metodo":"Lineal",
			"icono":"fa fa-line-chart",
			"m":nr,
			"n":nX,
			"r":rX,
			"i" : n,
			"media":media,
			"n1":n1,
			"n2":n2,
			"sms":sms,
			"u":u,
			"q":q,
			"b":b,
			"z":z,
			"s":s,
			"listaFrame":listaFrame
		}

		return redirect("metodoPostData")
	else:
		datos = {}
		return render(request, "linealFrame.html")
def metodoAditivo(request):
	global datos
	if request.method == 'POST':
		form = adiForm(request.POST or None)

		if form.is_valid():
			#instance = form.save(commit=False)
			m = form.cleaned_data.get("M")
			Xo = form.cleaned_data.get("Xo")
			Xn = form.cleaned_data.get("Xn")
			n = form.cleaned_data.get("N")
			nr = []
			nX = ''
			rX = ''
			listaFrame=''
			for i in range (1, n+1) :
				n=i
				varx=Xn+Xo
				Xn=Xo
				cant=varx
				Xo=cant%m
				div=round(Xo/(m-1),3)
				nr.append({'n':n,'Xn':Xn,'cant':cant,'Xo':Xo,'div':div})
				listaFrame+=str(div)+ ' '
				nX = nX + str(i) + ','
				rX = rX + str(div) + ','

			#Haceer las pruebas
			nr1=[]
			for n  in nr:
				#print (n.get('div'))
				nr1.append(n.get('div'))
			
			#realizamos la prueba y obtenemos los datos		
			h = prueba(nr1)
			media=h.get('media')
			n1=h.get('n1')
			n2=h.get('n2')
			sms=h.get('sms')
			u=h.get('u')
			q=h.get('q')
			b=h.get('b')
			z=h.get('z')
			s=h.get('s')

			datos = {
				"metodo":"Aditivo",
				"icono":"fa fa-plus",
				"m":nr,
				"n":nX,
				"r":rX,
				"i" : n,
				"media":media,
				"n1":n1,
				"n2":n2,
				"sms":sms,
				"u":u,
				"q":q,
				"b":b,
				"z":z,
				"s":s,
				"listaFrame":listaFrame
			}
		return redirect("metodoPostData")
	else:
		datos = {}
		form = adiForm()
		return render(request, "aditivoFrame.html", {'form': form})				



def metodoMultiplicativo(request):
	global datos
	
	if request.method == 'POST':
		form = multiForm(request.POST or None)	
		if form.is_valid():
			#instance = form.save(commit=False)
			m = form.cleaned_data.get("M")
			Xn = form.cleaned_data.get("Xn")
			a = form.cleaned_data.get("A")
			c = form.cleaned_data.get("C")
			n = form.cleaned_data.get("N")
			nr = []
			#variables para el grafico
			nX = ''
			rX = ''
			listaFrame=''
	
			for i in range (1, n+1) :
				n=i
				axn=(Xn*a)
				axnm=axn%m
				r=round(axnm/m,3)
				nr.append({'n':i,'Xn':Xn,'r':r,'axn':axn,'axnm':axnm})
				listaFrame+=str(r)+ ' '
				Xn = axnm
				nX = nX + str(i) + ','
				rX = rX + str(r) + ','
				

			#Haceer las pruebas
			nr1=[]
			for n  in nr:
				#print (n.get('r'))
				nr1.append(n.get('r'))
						
			h = prueba(nr1)
			media=h.get('media')
			n1=h.get('n1')
			n2=h.get('n2')
			sms=h.get('sms')
			u=h.get('u')
			q=h.get('q')
			b=h.get('b')
			z=h.get('z')
			s=h.get('s')
				

			datos = {
				"metodo":"Multiplicativo",
				"icono":"fa fa-times",
				"m":nr,
				"n":nX,
				"r":rX,
				"i" : n,
				"media":media,
				"n1":n1,
				"n2":n2,
				"sms":sms,
				"u":u,
				"q":q,
				"b":b,
				"z":z,
				"s":s,
				"listaFrame":listaFrame
			}	
		return redirect("metodoPostData")
	else:
		datos = {}
		form = multiForm()
		return render(request, "multiplicaFrame.html", {'form': form})
	

def metodoRandom(request):
	import math
	import random
	#print(random)
	global datos
	
	if request.method == 'POST':
		form = randomForm(request.POST or None)
		


		#print (dir(form))
		if form.is_valid():
			#instance = form.save(commit=False)
			n = form.cleaned_data.get("N")
			nr = []
			nX = ''
			rX = ''
			listaFrame=''
		
			for i in range (1, n+1) :
				
				n=i
				x=random.randrange(0,100)
				y=x/100
				nr.append({'n':n,'y':y})
				listaFrame+=str(y)+ ' '
				nX = nX + str(i) + ','
				rX = rX + str(y) + ','

				#hacemos la prueba respectiva
			nr1=[]
			for n  in nr:
				#print (n.get('y'))
				nr1.append(n.get('y'))
						
			h = prueba(nr1)
			media=h.get('media')
			n1=h.get('n1')
			n2=h.get('n2')
			sms=h.get('sms')
			u=h.get('u')
			q=h.get('q')
			b=h.get('b')
			z=h.get('z')
			s=h.get('s')
		
				
			datos = {
				"metodo":"Random",
				"icono":"fa fa-random",
				"m":nr,
				"n":nX,
				"r":rX,
				"i" : n,
				"media":media,
				"n1":n1,
				"n2":n2,
				"sms":sms,
				"u":u,
				"q":q,
				"b":b,
				"z":z,
				"s":s,
				"listaFrame":listaFrame
			}
		return redirect("metodoPostData")
	else:
		datos = {}
		form = randomForm()
		return render(request, "randomFrame.html", {'form': form})

def metodoPostData(request):
	global datos, numeros
	#print(datos)
	
	if datos == {}:
		#print("no hay contexto")
		return redirect("metodoLineal")
	else:
		if request.method == 'POST':
			print("Es un Post")
			#logica cuando se envia un formulario desde la Url Post data

		else:
			context = datos
			form = sideseo()
			context['form'] = form
			#print(context)
			return render(request,"detailDataFrame.html",context)

def datosGrafico(n,data):
	lista = []
	for i in range(0,n):
		lista.append({'x':i+1,'y':data[i]})
	return lista

def datosGrafico2(n,data):
	lista = []
	for i in range(0,n):
		lista.append({'x':i+1,'y':data[i]})
	return lista


def promedioMovil(request):
	if request.method == 'POST':	
		#alf=request.POST.get('alfa', '')
		
		la=request.POST.get('var', '')
		n1=request.POST.get('n', '')
		n= int(n1)
		v=int(la)
		#print(n)
		x=[]
		m=[]
		
		for i in range(1,n+1):
			lnx = request.POST.get('llegada'+str(i), '')
			ln = float(lnx)
			#print(n)
			x.append(ln)
			m.append(i)
		#print(x);
		#print(m);

		lista1 = datosGrafico(n,x)
    
		#llama al metodo alisamiento
		result=calPromMov(m,x,v)
		
		m=result[0]
		lt2 = result[1]
		holi = result[2]
		lista2 = datosGrafico(n,lt2)

		

		#print(holi)
		context={
			"m":m,
			"lista1":lista1,
			"lista2":lista2,
			"pronos":holi,
		}
		#print(context)
		return render(request, "detailPromedioM.html",context)
	else:
		datos=[0.339,0.431,0.241,0.304,0.132,0.071,0.913,0.941,0.698,0.657]
		return render(request, "promedioMovil.html",{"datos":datos})

def calPromMov(periodo,datos,variable):
    l_pronostico=[]
    l_error=[]
    l_error2=[]

    inicio=0
    final=variable
    suma=0.0
    promedio=0.0
    suma_error=0.0
    suma_error2=0.0
    n=len(datos)
    for i in range(0,variable):
        l_pronostico.append(0)
        l_error.append(0)
        l_error2.append(0)

    for calc in range(variable-1,n):
        suma=0.0
        for k in range(inicio,final):
            suma=round(suma+datos[k],3)

        promedio=round(suma/variable,3)
        l_pronostico.append(promedio)
        inicio=inicio+1
        final=final+1

    for  sa in range(0,len(l_pronostico)-1):
        if l_pronostico[sa]>0:
            xn = datos[sa]
            pro=l_pronostico[sa]
            er = round(xn - pro, 3)
            l_error.append(er)
            er2 = round(er * er, 3)
            l_error2.append(er2)

    for er in l_error:
        suma_error=round(suma_error+er,3)


    for  er2 in l_error2:
        suma_error2=round(suma_error2+er2,3)

    lista=[]

    #print(periodo,datos,l_pronostico,l_error,l_error2)
    #print (periodo,datos,"lista",l_pronostico,"error",l_error,"error2",l_error2,suma_error,suma_error2)
    #return datos,"lista",l_pronostico,"error",l_error,"error2",l_error2,suma_error,suma_error2
    periodo.append(n+1)
    datos.append("Pronostico")
    l_error.append('-')
    l_error2.append('-')

    periodo.append(n+2)
    datos.append("Suma")
    l_pronostico.append("-")
    l_error.append(suma_error)
    l_error2.append(suma_error2)

    nr=[]
    for k in range(0, n+2):
    	nr.append({'n':periodo[k],'Xn':datos[k],'Sn':l_pronostico[k],'err':l_error[k],'err2':l_error2[k]})
    	#print(" "+str(listaN[k])+" "+str(listaXn[k])+" "+str(listaSn[k])+" "+str(listaEr[k]))
    l_pronostico.pop(n+1)
    return nr,l_pronostico,[{'x':n+1,'y':l_pronostico[n]}]

def alisamiento(request):
	if request.method == 'POST':	
		alf=request.POST.get('alfa', '')
		event=request.POST.get('n', '')
		a=float(alf)
		n=int(event)
		#print(n)
		lista=[]
		for i in range(1,n+1):
			lnx = request.POST.get('llegada'+str(i), '')
			ln = float(lnx)
			#print(n)
			lista.append(ln)

		lista1 = datosGrafico(n,lista)
		#print(lista1)
		#n=int(event)
		#lista=[293,283,322,355,346,379,381,431,424,433,470,481,549,544,601,587,644,660]
		#print(lista)
		#llama al metodo alisamiento
		result=calcularAliExpo(a,n,lista)
		m=result[0]
		lt2 = result[1]
		holi = result[2]
		
		lista2 = datosGrafico(n,lt2)
		#print(result)


		context={
			"m":m,
			"alfa":a,
			"lista1":lista1,
			"lista2":lista2,
			"pronos":holi,
		}
		#print(context)
		return render(request, "detailAlisamiento.html",context)
	else:
		datos=[0.339,0.431,0.241,0.304,0.132,0.071,0.913,0.941,0.698,0.657]
		return render(request, "alisamiento.html",{"datos":datos})


def calcularAliExpo (aentrada,nentrada,lista):
    # pide alfa
    #a = float(input("Ingrese alfa"))
    # pide la cantidad de eventos N
    #n = int(input("Ingrese la cantidad eventos "))
    a=aentrada
    n=nentrada
    listaXn = lista
    listaN = []
    listaSn = []
    listaEr = []
    bandera = 1
    sn=0
    xn=0
    er=0
    for i in range(1, n + 1):  # repite n interaciones
        x = round(randrange(200,350))  # calcula el numero random con 3 interaciones
        #listaXn.append(float(x))#guarda xn
        listaN.append(i)  # guarda xn
	
    #print('la lista n es ',listaN)
    #print('la lista Xn es ',listaXn)

    for j in range(0,n):

        if (bandera == 1):  # en caso de ser la primera interacion asigna 0 en SN
            listaSn.append(0)
            listaEr.append(0)
            bandera=2
        else:
            if(bandera==2):
                sn=listaXn[0] #toma el primer valor de Xn
                listaSn.append(sn) #en caso de ser la segunda interacion asigna en valor anterior de Xn
                xn= listaSn[1] #guarda el valor actual de xn
                er= xn-sn #calcula el error
                listaEr.append(er)
                bandera = 0

            else:
                #print("entro")
                sn0 = listaSn[j-1] #valor anterior de sn
                xn0 = listaXn[j-1] #valor anterior de xn
                sn= a*xn0+(1-a)*sn0
                xn=  listaXn[j]
                er= xn-sn
                listaSn.append(sn)
                listaEr.append(er)
                #print("sn anterior"+str(sn0))
                #print("xn anterior" + str(xn0))

    #para calcular el ultima valor
    sn0 = listaSn[n- 1]  # valor anterior de sn
    xn0 = listaXn[n- 1]  # valor anterior de xn
    sn = a * xn0 + (1 - a) * sn0
    listaXn.append("Pronostico")
    listaSn.append(sn)
    listaEr.append(0)
    listaN.append(n+1)
    nr=[]
    for k in range(0, n+1):
    	nr.append({'n':listaN[k],'Xn':listaXn[k],'Sn':round(listaSn[k],3),'err':round(listaEr[k],3),'err2':round(listaEr[k]*round(listaEr[k],3))})
    	#print(" "+str(listaN[k])+" "+str(listaXn[k])+" "+str(listaSn[k])+" "+str(listaEr[k]))
    return nr ,listaSn,[{'x':k+1,'y':listaSn[k]}]


def datosGraficoRegre(n,data1,data2):
	lista = []
	for i in range(0,n):
		lista.append({'x':data1[i],'y':data2[i]})
	return lista

def regreLineal(request):
	
	if request.method == 'POST':	
		nx=request.POST.get('n', '')
		fx=request.POST.get('FX', '')
		valor_predecir = float(fx)
		n = int(nx)
		x=[]
		for i in range(1,n+1):
			lnx = request.POST.get('x'+str(i), '')
			ln = float(lnx)
			#print(n)
			x.append(ln)
		y=[]
		for i in range(1,n+1):
			lny = request.POST.get('y'+str(i), '')
			ln = float(lny)
			#print(n)
			y.append(ln)

		lista1 = datosGraficoRegre(n,x,y)
		#print(lista1)


		xcuad=0
		xy=0
		ycuad=0
		n=0
		sumx=0
		sumy=0
		sumxcuad=0
		sumxy=0
		sumycuad=0

		if len(x) != len(y):
			print("los valores de x no coinciden con los valores de y")
		else:
			#print("N"," ", "X","     ","Y","  ","X^2","     ","XY","     ","Y^2")
			#calculando
			nr=[]
			nx = ''
			ny = ''

			for i in range(len(x)):
				#hacemos todos los calculos respectivos
				#x^2
				nx = nx + str(x[i]) + ','
				ny = ny + str(y[i]) + ','

				xcuad = x[i]*x[i]
				#xy
				xy=x[i]*y[i]
				#y^2
				ycuad=y[i]*y[i]
				# mostramos los datos por pantalla n, x , y , x^2 , xy , y^2
				#print(i+1," ", x[i],"  ",y[i]," ",xcuad,"   ",xy,"   ",ycuad)
				nr.append({'n':i+1,'x':x[i],'y':y[i],'x2':xcuad,'xy':xy,'y2':ycuad})
				#numeros
				n=n+1
				#suma de x
				sumx= sumx+x[i]
				#suma de y
				sumy= sumy+y[i]
				#suma de x^2
				sumxcuad = sumxcuad+xcuad
				#suma de xy
				sumxy = sumxy+xy
				#suma de y^2
				sumycuad = sumycuad+ycuad

			#print("N=",n, "Σx=",sumx ,"Σy=", sumy,"Σx^2=",sumxcuad,"Σxy=",sumxy,"Σy^2=",sumycuad)
			#print("Calculando ecuaciones - Metodo determinante")
			#calculo la determinante
			deter = round((n*sumxcuad)-(sumx*sumx),3)
			#calculo de a0
			a0 = round(((sumy*sumxcuad)-(sumx*sumxy))/deter,3)
			#calculo de a1
			a1 = round(((n*sumxy)-(sumx*sumy))/deter,3)

			pron= round(a0+a1*valor_predecir,3)

			valfin=""
			resfin=[]
			newy=[]
			for i in x:
				valfin = valfin + str(round(a0+a1*i,3))+','
				#resfin.append(round(a0+a1*i,3))
				resfin.append({'x':i,'y':round(a0+a1*i,3)})
				newy.append(round(a0+a1*i,3))
			
			#print(newy)
			lista2 = datosGraficoRegre(n,x,newy)

			grafPron=[{'x':valor_predecir,'y':pron}]
			
			#print("El pronostico es:",pron)
			context={
				"metodo":"Regrecion Lineal",
				"m":nr,
				"n":n,
				"sumx":sumx,
				"sumy":sumy,
				"sumxcuad":sumxcuad,
				"sumxy":sumxy,
				"sumycuad":sumycuad,
				"xn":nx,
				"yn":ny,
				"fin":valfin,
				"predecir":valor_predecir,
				"pron":pron,
				"a0":a0,
				"a1":a1,
				"resfin":resfin,
				"lista1":lista1,
				"lista2":lista2,
				"pronos":grafPron,
			}
			#print(context)
		return render(request, "detailPronos.html",context)
	else:
		llega=[100,200,300,400,500,600,700]
		sirve=[40,50,50,70,65,65,80]
		return render(request, "regresionLineal.html",{"llega":llega,"sirve":sirve})


def regreCuadrado(request):
	
	if request.method == 'POST':
		nx=request.POST.get('n', '')
		fx=request.POST.get('FX', '')
		valor_predecir = int(fx)
		n = int(nx)
		x=[]
		for i in range(1,n+1):
			lnx = request.POST.get('x'+str(i), '')
			ln = float(lnx)
			#print(n)
			x.append(ln)
		y=[]
		for i in range(1,n+1):
			lny = request.POST.get('y'+str(i), '')
			ln = float(lny)
			#print(n)
			y.append(ln)

		lista1 = datosGrafico(n,y)
		#print(lista1)
		#Declaro variables necesarias para metodo cuadrado
		xcuad=0
		xcub=0
		xcuar=0
		xy=0
		xcuady=0
		n=0
		sumx=0
		sumy=0
		sumxcuad=0
		sumxcub=0
		sumxcuar=0
		sumxy=0
		sumxcuady=0


		if len(x) != len(y):
			print("los valores de x no coinciden con los valores de y")
		else:
			ln=''
			nr=[]
			nx = ''
			ny = ''
			#print("Datos")
			#print("N"," ", "X","     ","Y","  ","X^2","     ","x^3","     ","x^4","     ","XY","     ","x^2 y")
			#calculando
			for i in range(len(x)):
				#hacemos todos los calculos respectivos
				#x^2
				xcuad = round(x[i]*x[i],1)
				#x^3
				xcub = round(x[i]*x[i]*x[i],1)
				#x^4
				xcuar = round(x[i]*x[i]*x[i]*x[i],1)
				#xy
				xy= round(x[i]*y[i],1)
				#y^2
				xcuady= round(x[i]*x[i]*y[i],1)
				# mostramos los datos por pantalla n, x , y , x^2 , xy , y^2
				#print(i+1,"  ", x[i],"  ",y[i]," ",xcuad,"   ",xcub,"   ",xcuar,"   ",xy,"   ",xcuady)

				nr.append({'n':i+1,'x':x[i],'y':y[i],'x2':xcuad,'x3':xcub,'x4':xcuar,'xy':xy,'x2y':xcuady})

				#numeros
				n=n+1
				ln=ln + str(n+1) + ','
				
				#suma de x
				sumx= round(sumx+x[i],1)
				#suma de y
				sumy= round(sumy+y[i],1)
				#suma de x^2
				sumxcuad = round(sumxcuad+xcuad,1)
				#suma de x^3
				sumxcub = round(sumxcub+xcub,1)
				#suma de x^4
				sumxcuar = round(sumxcuar+xcuar,1)
				#suma de xy
				sumxy = round(sumxy+xy,1)
				#suma de y^2
				sumxcuady = round(sumxcuady+xcuady,1)

			#print("Sumatorias")
			#print("N=",n, "Σx=",sumx ,"Σy=", sumy,"Σx^2=",sumxcuad,"Σx^3=",sumxcub,"Σx^4=",sumxcuar,"Σxy=",sumxy,"Σx^2 y=",sumxcuady)
			#print("Calculando ecuaciones - Metodo determinante")


			#metodo de determinantes en ecuacion de 3 incognitas
			#Calcular Determinante 
			dete1 =(n*sumxcuad*sumxcuar)+(sumx*sumxcub*sumxcuad)+(sumxcuad*sumx*sumxcub)
			dete2 =(sumxcuad*sumxcuad*sumxcuad)+(sumxcub*sumxcub*n)+(sumxcuar*sumx*sumx)
			dete =dete1-dete2
			#print(dete)
			
			#caluclar a0
			a001=(sumy*sumxcuad*sumxcuar)+(sumxy*sumxcub*sumxcuad)+(sumxcuady*sumx*sumxcub)
			a002=(sumxcuad*sumxcuad*sumxcuady)+(sumxcub*sumxcub*sumy)+(sumxcuar*sumx*sumxy)
			a00=a001-a002
			a0=round(a00/dete,2)
			#print("El valor de a0 es: ",a0)
			
			#caluclar a1
			a011=(n*sumxy*sumxcuar)+(sumx*sumxcuady*sumxcuad)+(sumxcuad*sumy*sumxcub)
			a012=(sumxcuad*sumxy*sumxcuad)+(sumxcub*sumxcuady*n)+(sumxcuar*sumy*sumx)
			a01=a011-a012
			a1=round(a01/dete,2)
			#print("El valor de a1 es: ",a1)

			#caluclar a2
			a021=(n*sumxcuad*sumxcuady)+(sumx*sumxcub*sumy)+(sumxcuad*sumx*sumxy)
			a022=(sumy*sumxcuad*sumxcuad)+(sumxy*sumxcub*n)+(sumxcuady*sumx*sumx)
			a02=a021-a022
			a2=round(a02/dete,4)
			#print("El valor de a2 es: ",a2)


			#mostrando valor de a0 y x1
			#print("El valor de a0 es:",a0)
			#print("El valor de a1 es:",a1)
			##calculando pronostico
			pron= round(a0+a1*valor_predecir+a2*(valor_predecir*valor_predecir),2)

			valfin=""
			resfin=[]
			for i in x:
				valfin = valfin + str(round(a0+a1*i+a2*(i*i),3))+','
				#resfin.append(round(a0+a1*i,3))

			
			lista1 = datosGrafico(n,y)

			#print(resfin)

			#print("El pronostico es:",pron)
			context={
				"metodo":"Regrecion Cuadratica",
				"m":nr,
				"n":n,
				"ln":ln,
				"sumx":sumx,
				"sumy":sumy,
				"sumxcuad":sumxcuad,
				"sumxcub":sumxcub,
				"sumxcuar":sumxcuar,
				"sumxy":sumxy,
				"sumxcuady":sumxcuady,
				"xn":nx,
				"yn":ny,
				"fin":valfin,
				"predecir":valor_predecir,
				"pron":pron,
				"a0":a0,
				"a1":a1,
				"a2":a2,
				"resfin":resfin,
				"lista1":lista1,
			}
			#print(context)
		return render(request, "detailPronosCuad.html",context)
	else:
		llega=[-5,-4,-3,-2,-1,0,1,2,3,4,5]
		sirve=[23.2,31.4,39.8,50.2,62.9,76.0,92.0,105.7,122.8,131.7,151.1]
		return render(request, "regresionCuadrado.html",{"llega":llega,"sirve":sirve})


def lineaEspera(request):
	
	if request.method == 'POST':	
		la=request.POST.get('landa', '')
		ni=request.POST.get('niu', '')
		n1=request.POST.get('n', '')
		n= int(n1)
		
		landa=float(la)
		mi_u = float(ni)
		#lista_alea_llegada=[0.339,0.431,0.241,0.304,0.132,0.071,0.913,0.941,0.698,0.657]
		lista_alea_llegada=[]
		for i in range(1,n+1):
			lnx = request.POST.get('llegada'+str(i), '')
			ln = float(lnx)
			#print(n)
			lista_alea_llegada.append(ln)

		#print(lista_alea_llegada);

		#lista_aleatorieo_servicio=[0.104,0.318,0.183,0.773,0.250,0.561,0.286,0.599,0.149,0.058]
		lista_aleatorieo_servicio=[]
		for i in range(1,n+1):
			lnx = request.POST.get('servicio'+str(i), '')
			#print(lnx)
			ln = float(lnx)
			#print(n)
			lista_aleatorieo_servicio.append(ln)

		#print(lista_aleatorieo_servicio)
		#lista_alea_llegada= eval('[' + lle + ']')
		#lista_aleatorieo_servicio= eval('[' + ser + ']')
		#declaro variables de entrada
		l_t_llegada=[]
		l_t_servicio=[]
		l_t_exa_llegada=[0]
		l_h_iniciacion=[0]
		l_h_teriacion=[0]
		l_t_espera=[0]
		l_t_sistema=[0]
		t_llegada = 0
		t_servicio = 0
		h_exata_llegada=0
		h_iniciacion = 0
		h_termiacion = 0
		t_espera = 0
		t_sistema = 0


		if len(lista_alea_llegada) != len(lista_aleatorieo_servicio):
			print("los valores de la llegada no coinciden con los valores de el servicio")
		else:
			#print(landa,mi_u,lista_alea_llegada,lista_aleatorieo_servicio)
			

		    for llegada in range(0,len(lista_alea_llegada)):
		        t_llegada= round((-(1/landa) * math.log(lista_alea_llegada[llegada])),3)
		        l_t_llegada.append(t_llegada)


		    for servicio in range(0,len(lista_aleatorieo_servicio)):
		        t_espera= round((-(1/mi_u)* round(math.log(lista_aleatorieo_servicio[servicio]),3)),3)
		        l_t_servicio.append(t_espera)

		    for h_exacta in l_t_llegada:
		        h_exata_llegada= round(h_exacta+h_exata_llegada,4)
		        l_t_exa_llegada.append(h_exata_llegada)

		    bandera = len(lista_alea_llegada)
		    contador = 0
		    while (bandera>0):
		        h_iniciacion=max(round(l_t_exa_llegada[contador+1],3), round(l_h_teriacion[contador],3))
		        l_h_iniciacion.append(h_iniciacion)
		        h_termiacion=round(l_t_servicio[contador]+l_h_iniciacion[contador+1],3)
		        l_h_teriacion.append(h_termiacion)
		        contador=contador+1
		        bandera = bandera - 1

		    bandera = len(l_h_teriacion)
		    contador2 = 0
		    while (bandera>0):
		        t_espera=round(l_h_iniciacion[contador2]-l_t_exa_llegada[contador2],3)
		        l_t_espera.append(t_espera)
		        contador2=contador2+1
		        bandera = bandera - 1



		    bandera=len(lista_alea_llegada)
		    contador3 = 0
		    while (bandera>0):
		        t_sistema=round(l_t_espera[contador3+2]+l_t_servicio[contador3],3)
		        l_t_sistema.append(t_sistema)
		        contador3=contador3+1
		        bandera = bandera - 1

		    l_t_espera.pop(0)

		    

		    l_t_exa_llegada.pop(0)
		    l_h_iniciacion.pop(0)
		    l_h_teriacion.pop(0)
		    l_t_espera.pop(0)
		    l_t_sistema.pop(0)

		    #print("\n", lista_alea_llegada, "\n", lista_aleatorieo_servicio, "\n", l_t_llegada, "\n", l_t_servicio, "\n",
		      #        l_t_exa_llegada, "\n", l_h_iniciacion, "\n", l_h_teriacion, "\n", l_t_espera, "\n", l_t_sistema,"\n Este metodo lo pueden utilizar para las listas",)

		    total=[]
		    n=len(l_t_sistema)

		    for i in range(0,n):
		    	termina = round(l_h_iniciacion[i]-l_t_exa_llegada[i],3)
		    	total.append({'n':i+1,'llegada':lista_alea_llegada[i],'servicio':lista_aleatorieo_servicio[i],
		    		't_llegada':l_t_llegada[i],'t_servicio':l_t_servicio[i],'h_llegada':l_t_exa_llegada[i],'h_inicio':l_h_iniciacion[i],
		    		'h_termina':l_h_teriacion[i],'t_espera':termina,'t_sistema':l_t_sistema[i]})

		    print('Tiempo de llegada',suma(l_t_exa_llegada))


		    context = {
		    	"total":total,
		    	"m_t_llega":promedio(l_t_exa_llegada),
		    	"m_t_inicio":promedio(l_h_iniciacion),
		    	"m_t_termina":promedio(l_h_teriacion),
		    	"m_t_espera":promedio(l_t_espera),
		    	"m_t_sistema":promedio(l_t_sistema),
		    	"t_t_llega":suma(l_t_exa_llegada),
		    	"t_t_inicio":suma(l_h_iniciacion),
		    	"t_t_termina":suma(l_h_teriacion),
		    	"t_t_espera":suma(l_t_espera),
		    	"t_t_sistema":suma(l_t_sistema),
		    	"n":n+1,

		    }

		    #print(context)
		
	

		return render(request, "detailEspera.html",context)
	else:
		llega=[0.339,0.431,0.241,0.304,0.132,0.071,0.913,0.941,0.698,0.657]
		sirve=[0.104,0.318,0.183,0.773,0.250,0.561,0.286,0.599,0.149,0.058]
		#llega=[0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
		#sirve=[0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
		return render(request, "lineaEspera.html",{"llega":llega,"sirve":sirve})

def lineaEsperaMonte(request):
	if request.method == 'POST':	
	#obtenemos los valores de la demanda para resolver por medio de montecarlo
		# n de la demanda		
		n1=request.POST.get('nDeman', '')
		#convertimos el valor obtenido en int para realizar las operaciones
		nDeman= int(n1)
		#Array Valor inicializado
		valor=[]
		#ciclo que de acuerdo a los valores de la demanda recorre y obtiene el valor de los text box del "valor" de la demanda
		for i in range(1,nDeman+1):
			#print(i)
			lnx = request.POST.get('demValor'+str(i), '')
			#print(lnx)
			ln = float(lnx)
			#print(n)
			valor.append(ln)
		
		#Array px inicializado
		px=[]
		#ciclo que de acuerdo a los valores de la demanda recorre y obtiene el valor de los text box del "px" de la demanda
		for i in range(1,nDeman+1):
			#obtenemos los input name demPx1, demPxdemPx2,.....etc
			lnx = request.POST.get('demPx'+str(i), '')
			ln = float(lnx)
			#print(n)
			px.append(ln)
		#print(valor,px);

	#obtenemos los valores de la demanda para resolver por medio de montecarlo
		# n de la demanda		
		n2=request.POST.get('nRetra', '')
		#convertimos el valor obtenido en int para realizar las operaciones
		#print("el valor",n2)
		nRetra= int(n2)
		#Array Valor inicializado
		valor1=[]
		#ciclo que de acuerdo a los valores de la demanda recorre y obtiene el valor de los text box del "valor" de la demanda
		for i in range(1,nRetra+1):
			#print(i)
			lnx = request.POST.get('retraValor'+str(i), '')
			#print(lnx)
			ln = float(lnx)
			#print(n)
			valor1.append(ln)
		
		#Array px inicializado
		px1=[]
		#ciclo que de acuerdo a los valores de la demanda recorre y obtiene el valor de los text box del "px" de la demanda
		for i in range(1,nRetra+1):
			#obtenemos los input name demPx1, demPxdemPx2,.....etc
			lnx = request.POST.get('retraPx'+str(i), '')
			ln = float(lnx)
			#print(n)
			px1.append(ln)
		#print(valor1,px1);


	#obtener los numeros aleatorios
		# n de los numeros aleatorios
		n3=request.POST.get('n', '')
		nAlea= int(n3)
		
		deman=[]
	#ciclo que de acuerdo al nAlea de los numeros aleatorios rreccorre y obtiene los numeros aleatorios de la demanda
		for i in range(1,nAlea+1):
			#obtenemos los input name llagada1, llagada2,.....etc
			lnx = request.POST.get('llegada'+str(i), '')
			ln = float(lnx)
			#print(n)
			deman.append(ln)

		#print(v);

	#ciclo que de acuerdo al nAlea de los numeros aleatorios rreccorre y obtiene los numeros aleatorios de la retraso
		retra=[]
		for i in range(1,nAlea+1):
			lnx = request.POST.get('servicio'+str(i), '')
			ln = float(lnx)
			#print(n)
			retra.append(ln)	
		#print(deman,retra);

		llegaMonte=calculoMontecarlo(valor,px,deman)

		#print(demandaMonte)

		l_valor=llegaMonte[0]
		l_px=llegaMonte[1]
		l_acumulada=llegaMonte[2]
		l_desde=llegaMonte[3]
		l_hasta=llegaMonte[4]


		l_demanda=[]

		for i in range(0,len(llegaMonte[0])):
			l_demanda.append({"valor":l_valor[i],"px":l_px[i],"acumulado":l_acumulada[i],"desde":l_desde[i],"hasta":l_hasta[i]})


		serviMonte=calculoMontecarlo(valor1,px1,retra)

		#print(demandaMonte)

		l_valor1=serviMonte[0]
		l_px1=serviMonte[1]
		l_acumulada1=serviMonte[2]
		l_desde1=serviMonte[3]
		l_hasta1=serviMonte[4]


		l_retraso=[]

		for i in range(0,len(serviMonte[0])):
			l_retraso.append({"valor":l_valor1[i],"px":l_px1[i],"acumulado":l_acumulada1[i],"desde":l_desde1[i],"hasta":l_hasta1[i]})



		demandaMonte = metodo_linea_esperaMontecarlo(valor,px,valor1,px1,deman,retra)
		

		llegaAle=demandaMonte[0]
		sirveAle=demandaMonte[1]
		t_llegada=demandaMonte[2]
		t_servicio=demandaMonte[3]
		h_llegada=demandaMonte[4]
		h_inicio=demandaMonte[5]
		h_termina=demandaMonte[6]
		t_espera=demandaMonte[7]
		t_sistema=demandaMonte[8]

		lista_total=[]
		n=0;

		for i in range(0,len(demandaMonte[0])):
			n=i+1
			lista_total.append({"n":i+1,"llegada":llegaAle[i],"servicio":sirveAle[i],"t_llegada":t_llegada[i],"t_servicio":t_servicio[i],"h_llegada":h_llegada[i],"h_inicio":h_inicio[i],"h_termina":h_termina[i],"t_espera":t_espera[i],"t_sistema":t_sistema[i]})

		#print(lista_total)


		context = {
			"total":lista_total,
			"n":n+1,
			"m_t_llega":promedio(h_llegada),
		    "m_t_inicio":promedio(h_inicio),
		    "m_t_termina":promedio(h_termina),
		    "m_t_espera":promedio(t_espera),
		    "m_t_sistema":promedio(t_sistema),
		    "t_t_llega":suma(h_llegada),
		    "t_t_inicio":suma(h_inicio),
		    "t_t_termina":suma(h_termina),
		    "t_t_espera":suma(t_espera),
		    "t_t_sistema":suma(t_sistema),
			"demanda":l_demanda,
			"retraso":l_retraso,
			
	    }

		    #print(context)

		return render(request, "detailEsperaMonte.html",context)
	else:
		valor=[0,1,2,3,4]
		px=[0,0.25,0.2,0.4,0.15]

		valor1=[0,1,2,3,4,6]
		px1=[0.1,0.35,0.25,0.15,0.1,0.05]

		deman=[0.901,0.724,0.829,0.506,0.596,0.457,0.789,0.174,0.363,0.309]
		retra=[0.247,0.920,0.101,0.515,0.951,0.482,0.082,0.100,0.880,0.500]
		#deman=[0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
		#retra=[0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]

		context = {
			"valor":valor,
			"px":px,
			"valor1":valor1,
			"px1":px1,
			"deman":deman,
			"retra":retra,
	    }
		return render(request, "lineaEsperaMonte.html",context)

def metodo_linea_esperaMontecarlo(valor_llegada,proba_llegada,valor_servi,proba_serv,lista_alea_llegada,
                                  lista_aleatorieo_servicio):
    l_t_llegada=[]
    l_t_servicio=[]
    l_t_exa_llegada=[0]
    l_h_iniciacion=[0]
    l_h_teriacion=[0]
    l_t_espera=[0]
    l_t_sistema=[0]
    t_llegada = 0
    t_servicio = 0
    h_exata_llegada=0
    h_iniciacion = 0
    h_termiacion = 0
    t_espera = 0
    t_sistema = 0
    l_monte_llega=[]
    l_monte_servi=[]

    montacarlo_llegada=calculoMontecarlo(valor_llegada,proba_llegada,lista_alea_llegada)
    montacarlo_servicio = calculoMontecarlo(valor_servi, proba_serv, lista_aleatorieo_servicio)

    #print(montacarlo_llegada)
    l_monte=montacarlo_llegada[6]
    for llegada in range(0,len(l_monte)):
        l_t_llegada.append(l_monte[llegada])

    l_monte_servi=montacarlo_servicio[6]
    for servicio in range(0,len(l_monte_servi)):
        l_t_servicio.append(l_monte_servi[servicio])

    for h_exacta in l_t_llegada:
        h_exata_llegada= round(h_exacta+h_exata_llegada,4)
        l_t_exa_llegada.append(h_exata_llegada)

    bandera = len(lista_alea_llegada)
    contador = 0
    while (bandera>0):
        h_iniciacion=max(round(l_t_exa_llegada[contador+1],3), round(l_h_teriacion[contador],3))
        l_h_iniciacion.append(h_iniciacion)
        h_termiacion=round(l_t_servicio[contador]+l_h_iniciacion[contador+1],3)
        l_h_teriacion.append(h_termiacion)
        contador=contador+1
        bandera = bandera - 1


    bandera = len(l_h_teriacion)-1
    contador2 = 0
    suma_tiempo_espera=0
    while (bandera>0):
        t_espera=round(l_h_iniciacion[contador2+1]-l_t_exa_llegada[contador2+1],3)
        l_t_espera.append(t_espera)
        suma_tiempo_espera = t_espera + suma_tiempo_espera
        contador2=contador2+1
        bandera = bandera - 1

    bandera=len(l_h_teriacion)-1
    contador3 = 0
    suma_tiempo_servicio = 0
    while (bandera>0):
        t_sistema=round(l_t_espera[contador3+1]+l_t_servicio[contador3],3)
        l_t_sistema.append(t_sistema)
        suma_tiempo_servicio = t_sistema + suma_tiempo_servicio
        contador3=contador3+1
        bandera = bandera - 1


    # Funcion que recibe una lista de valores y retorna el promedio de ellos
    def promedio(lista):
        sumaParcial = 0
        for valor in lista:
            sumaParcial=valor+sumaParcial
        cantidadValores = len(lista)
        return round(sumaParcial / float(cantidadValores),3)

    def promedio_con_0(lista):
        sumaParcial = 0
        for valor in lista:
            sumaParcial = valor + sumaParcial
        cantidadValores = len(lista)-1
        return round(sumaParcial / float(cantidadValores), 3)

    posicion = 0
    posicion = len(l_t_servicio) - 1
    l = 0.0
    lq = 0.0
    l = round(suma_tiempo_servicio / l_t_servicio[posicion], 3)
    lq = round(suma_tiempo_espera / l_t_servicio[posicion], 3)

    l_t_exa_llegada.pop(0)
    l_h_iniciacion.pop(0)
    l_h_teriacion.pop(0)
    l_t_espera.pop(0)
    l_t_sistema.pop(0)
   
    return lista_alea_llegada, lista_aleatorieo_servicio, l_t_llegada, l_t_servicio, l_t_exa_llegada, l_h_iniciacion, l_h_teriacion, l_t_espera, l_t_sistema, \
           promedio(l_t_llegada), promedio(l_t_servicio), promedio_con_0(l_t_exa_llegada), promedio_con_0(l_h_iniciacion), promedio_con_0(l_h_teriacion), promedio_con_0(l_t_espera), promedio_con_0(l_t_sistema), \
           montacarlo_llegada[0],montacarlo_llegada[1],montacarlo_llegada[2],montacarlo_llegada[3],montacarlo_llegada[4],\
           montacarlo_servicio[0],montacarlo_servicio[1],montacarlo_servicio[2],montacarlo_servicio[3],montacarlo_servicio[4],l,lq




def montecarlo(request):
	
	if request.method == 'POST':	
		
		#obtenemos los valores de la demanda para resolver por medio de montecarlo
		# n de la demanda		
		n1=request.POST.get('nDeman', '')
		#convertimos el valor obtenido en int para realizar las operaciones
		nDeman= int(n1)
		#Array Valor inicializado
		valor=[]
		#ciclo que de acuerdo a los valores de la demanda recorre y obtiene el valor de los text box del "valor" de la demanda
		for i in range(1,nDeman+1):
			#print(i)
			lnx = request.POST.get('demValor'+str(i), '')
			#print(lnx)
			ln = float(lnx)
			#print(n)
			valor.append(ln)
		
		#Array px inicializado
		px=[]
		#ciclo que de acuerdo a los valores de la demanda recorre y obtiene el valor de los text box del "px" de la demanda
		for i in range(1,nDeman+1):
			#obtenemos los input name demPx1, demPxdemPx2,.....etc
			lnx = request.POST.get('demPx'+str(i), '')
			ln = float(lnx)
			#print(n)
			px.append(ln)
		#print(valor,px);


	#obtener los numeros aleatorios
		# n de los numeros aleatorios
		n3=request.POST.get('n', '')
		nAlea= int(n3)
		
		deman=[]
	#ciclo que de acuerdo al nAlea de los numeros aleatorios rreccorre y obtiene los numeros aleatorios de la demanda
		for i in range(1,nAlea+1):
			#obtenemos los input name llagada1, llagada2,.....etc
			lnx = request.POST.get('llegada'+str(i), '')
			ln = float(lnx)
			#print(n)
			deman.append(ln)

		#print(v);

		demandaMonte=calculoMontecarlo(valor,px,deman)

		#print(demandaMonte)

		l_valor=demandaMonte[0]
		l_px=demandaMonte[1]
		l_acumulada=demandaMonte[2]
		l_desde=demandaMonte[3]
		l_hasta=demandaMonte[4]


		l_demanda=[]

		for i in range(0,len(demandaMonte[0])):
			l_demanda.append({"valor":l_valor[i],"px":l_px[i],"acumulado":l_acumulada[i],"desde":l_desde[i],"hasta":l_hasta[i]})


		l_numerosAleatorios=demandaMonte[5]
		l_Pronostico=demandaMonte[6]

		l_resultado=[]
		for i in range(0,len(demandaMonte[5])):
			#print({"nAleatorio":l_numerosAleatorios[i],"resultado":l_Pronostico[i]})
			l_resultado.append({"n":i+1,"nAleatorio":l_numerosAleatorios[i],"resultado":l_Pronostico[i]})

		#print(l_Pronostico)
		total = suma(l_Pronostico)
		#print(total)

		context = {
			"n":nDeman,
			"demanda":l_demanda,
			"resultado":l_resultado,
			"nResult":len(l_numerosAleatorios),
			"total":total,
	    }

		    #print(context)

		return render(request, "detailMontecarlo.html",context)
	else:
		valor=[1,2,3,4,5]
		px=[0.05,0.25,0.35,0.20,0.15]


		deman=[0.339,0.431,0.241,0.304,0.132,0.071,0.913,0.941,0.698,0.657]
		retra=[0.104,0.318,0.183,0.773,0.250,0.561,0.286,0.599,0.149,0.058]
		#deman=[0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
		#retra=[0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]

		context = {
			"valor":valor,
			"px":px,
			"deman":deman,
			"retra":retra,
	    }
		return render(request, "montecarlo.html",context)



def inventarioMontecarlo(request):
	if request.method == 'POST':	
	#obtenemos los valores de la demanda para resolver por medio de montecarlo
		# n de la demanda		
		n1=request.POST.get('nDeman', '')
		#convertimos el valor obtenido en int para realizar las operaciones
		nDeman= int(n1)
		#Array Valor inicializado
		valor=[]
		#ciclo que de acuerdo a los valores de la demanda recorre y obtiene el valor de los text box del "valor" de la demanda
		for i in range(1,nDeman+1):
			#print(i)
			lnx = request.POST.get('demValor'+str(i), '')
			#print(lnx)
			ln = float(lnx)
			#print(n)
			valor.append(ln)
		
		#Array px inicializado
		px=[]
		#ciclo que de acuerdo a los valores de la demanda recorre y obtiene el valor de los text box del "px" de la demanda
		for i in range(1,nDeman+1):
			#obtenemos los input name demPx1, demPxdemPx2,.....etc
			lnx = request.POST.get('demPx'+str(i), '')
			ln = float(lnx)
			#print(n)
			px.append(ln)
		#print(valor,px);

	#obtenemos los valores de la demanda para resolver por medio de montecarlo
		# n de la demanda		
		n2=request.POST.get('nRetra', '')
		#convertimos el valor obtenido en int para realizar las operaciones
		#print("el valor",n2)
		nRetra= int(n2)
		#Array Valor inicializado
		valor1=[]
		#ciclo que de acuerdo a los valores de la demanda recorre y obtiene el valor de los text box del "valor" de la demanda
		for i in range(1,nRetra+1):
			#print(i)
			lnx = request.POST.get('retraValor'+str(i), '')
			#print(lnx)
			ln = float(lnx)
			#print(n)
			valor1.append(ln)
		
		#Array px inicializado
		px1=[]
		#ciclo que de acuerdo a los valores de la demanda recorre y obtiene el valor de los text box del "px" de la demanda
		for i in range(1,nRetra+1):
			#obtenemos los input name demPx1, demPxdemPx2,.....etc
			lnx = request.POST.get('retraPx'+str(i), '')
			ln = float(lnx)
			#print(n)
			px1.append(ln)
		#print(valor1,px1);


	#obtener los numeros aleatorios
		# n de los numeros aleatorios
		n3=request.POST.get('n', '')
		nAlea= int(n3)
		
		deman=[]
	#ciclo que de acuerdo al nAlea de los numeros aleatorios rreccorre y obtiene los numeros aleatorios de la demanda
		for i in range(1,nAlea+1):
			#obtenemos los input name llagada1, llagada2,.....etc
			lnx = request.POST.get('llegada'+str(i), '')
			ln = float(lnx)
			#print(n)
			deman.append(ln)

		#print(v);

	#ciclo que de acuerdo al nAlea de los numeros aleatorios rreccorre y obtiene los numeros aleatorios de la retraso
		retra=[]
		for i in range(1,nAlea+1):
			lnx = request.POST.get('servicio'+str(i), '')
			ln = float(lnx)
			#print(n)
			retra.append(ln)	
		#print(deman,retra);

		#obtenemos las variables principales
		n4=request.POST.get('r', '')
		#print(n4)
		r= float(n4)
		n5=request.POST.get('q', '')
		q= float(n5)
		n6=request.POST.get('inicial', '')
		inv= float(n6)
		n7=request.POST.get('co', '')
		co= float(n7)
		n8=request.POST.get('ch', '')
		ch= float(n8)
		n9=request.POST.get('cf', '')
		cf= float(n9)
		#Hacemos el calculo respectivo para el inventario a pelo seco :v sin llamar a metodos

		demandaMonte=calculoMontecarlo(valor,px,deman)
		retrasoMonte=calculoMontecarlo(valor1,px1,retra)

		#print(demandaMonte,retrasoMonte)

		l_valor=demandaMonte[0]
		l_px=demandaMonte[1]
		l_acumulada=demandaMonte[2]
		l_desde=demandaMonte[3]
		l_hasta=demandaMonte[4]

		l_demanda=[]

		for i in range(0,len(demandaMonte[0])):
			l_demanda.append({"valor":l_valor[i],"px":l_px[i],"acumulado":l_acumulada[i],"desde":l_desde[i],"hasta":l_hasta[i]})


		l_valor1=retrasoMonte[0]
		l_px1=retrasoMonte[1]
		l_acumulada1=retrasoMonte[2]
		l_desde1=retrasoMonte[3]
		l_hasta1=retrasoMonte[4]

		l_retraso=[]

		for i in range(0,len(retrasoMonte[0])):
			l_retraso.append({"valor":l_valor1[i],"px":l_px1[i],"acumulado":l_acumulada1[i],"desde":l_desde1[i],"hasta":l_hasta1[i]})

		demanda = calculoMontecarloInv(valor,px)
		retraso=calculoMontecarloInv(valor1,px1)

		#print(demanda,retraso)
		lista_valor=demanda[0]
		lista_desde=demanda[3]
		lista_hasta=demanda[4]

		lista_valor1=retraso[0]
		lista_desde1=retraso[3]
		lista_hasta1=retraso[4]

		bandera=0
		entrega=0
		banfalta=0
		fin=inv
		isTheDay=0
		lista_total=[]
		#Lista para totales
		l_faltante=[]
		l_mantener=[]
		l_ordenar=[]
		#print("Semana","ri","demanda","inicial","ingresos","final","faltante","mantener","ordenar","ri","tiempo de entrega","dia entrega")
		for i in range(0,len(deman)):
		    n=i+1
		    #metodo montecarlo al primer valor aleatorio
		    vardeman=calculo(deman[i],lista_desde,lista_hasta,lista_valor)  
		    #inicial es igual al anterior
		    inicial=fin
		    #resa en uno
		    #si valor inicial es menor a la demanda
		    if inicial<vardeman:
		        #final es igual a 0
		        fin=0
		    else:
		        #fina es igual al inv inicial - la demanda
		        fin=inicial-vardeman

		    #Si es el dia de entrega
		    if n==isTheDay:
		    	if fin<=r:	
			        print(r,fin)
			        #realizo la entrega
			        bandera=0
			        entrega=1
			        #si hay faltante y si es el dia de entrega
			        if banfalta==1:
			            #print('Hay faltante')
			            #realizo la entrega
			            #ingreso es igual a q
			            ingreso=q
			            #costo de ordenar un pedido
			            ordenar=co
			            #final es igual al ingreso menos la demanda
			            fin=ingreso-vardeman
			            #ya no hay faltantes 

		    else:
		        ingreso=0
		        ordenar=0
		    
		    if ingreso==inicial:
		        #print("bingo")
		        if inicial<vardeman or ingreso<vardeman:
		            faltante = cf
		            banfalta=1
		        
		    else:
		        if inicial<vardeman :
		            faltante = cf
		            banfalta=1
		        else:  
		            faltante = 0
		            banfalta=0
		    
		    if ingreso>inicial:
		        faltante=0

		    mantener=ch*fin
		    
		    varretra=0
		    diaentrega=0
		    if bandera==0:
		    	if fin<=r:

			        varretra=calculo(retra[i],lista_desde1,lista_hasta1,lista_valor1)
			        diaentrega=(n+varretra)+1
			        print(r,fin)
			        isTheDay=diaentrega
			        #print("Ahora el dia de entrega es el",isTheDay)
			        bandera=1
		    else:
		        varretra=0
		        diaentrega=0      
		    l_faltante.append(faltante)
		    l_mantener.append(mantener)
		    l_ordenar.append(ordenar)

		    #print(n,deman[i],vardeman,inicial,ingreso,fin,faltante,mantener,ordenar,retra[i],varretra,diaentrega)
		    lista_total.append({"n":n,"aleaDem":deman[i],"demandaMonte":vardeman,"inv":inicial,"ingresos":ingreso,"final":fin,"faltante":faltante,"mantener":mantener,"ordenar":ordenar,"retraAlea":retra[i],"tiempoEntrega":varretra,"diaEntrega":diaentrega})


		#print(l_faltante,l_mantener,l_ordenar)

		t_faltante=suma(l_faltante)
		t_mantener=suma(l_mantener)
		t_ordenar=suma(l_ordenar)



		context = {
			"total":lista_total,
			"n":n,
			"t_faltante":t_faltante,
			"t_mantener":t_mantener,
			"t_ordenar":t_ordenar,
			"r":r,
			"q":q,
			"inicial":inicial,
			"co":co,
			"ch":ch,
			"cf":cf,
			"demanda":l_demanda,
			"retraso":l_retraso,
			
	    }

		    #print(context)

		return render(request, "detailInvMonte.html",context)
	else:
		valor=[1,2,3,4,5]
		px=[0.05,0.25,0.35,0.20,0.15]

		valor1=[2,3,4,5]
		px1=[0.20,0.50,0.20,0.10]


		deman=[0.339,0.431,0.241,0.304,0.132,0.071,0.913,0.941,0.698,0.657]
		retra=[0.104,0.318,0.183,0.773,0.250,0.561,0.286,0.599,0.149,0.058]
		#deman=[0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
		#retra=[0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]

		context = {
			"valor":valor,
			"px":px,
			"valor1":valor1,
			"px1":px1,
			"deman":deman,
			"retra":retra,
	    }

		return render(request, "inventarioMontecarlo.html",context)

######Metodo Montecarlo iventario

######Metodo Montecarlo
def calculoMontecarlo(v,f,n):
    valor=[]
    frecuencia=[]
    numeros_aleatoreos=[]
    for item1 in v:
        valor.append(float(item1))

    for item2 in f:
        frecuencia.append(float(item2))

    for item3 in n:
        numeros_aleatoreos.append(float(item3))


    l_acumulada=[]
    l_desde=[0]
    l_valor_simulado=[]
    acumulada=0.0
    suma=0.0
    promedio=0.0
    contador=0
    for fre in frecuencia:
        acumulada=round(acumulada+frecuencia[contador],3)
        l_acumulada.append(acumulada)
        contador=contador+1

    contador_d=0
    for des in l_acumulada:
        l_desde.append(round(l_acumulada[contador_d]+0.001,3))
        contador_d=contador_d+1

    conrador3=0
    rango=len(numeros_aleatoreos)
    for nu in range(0, rango):
        valor_simulado=calculo(numeros_aleatoreos[conrador3],l_desde,l_acumulada,valor)
        l_valor_simulado.append(valor_simulado)
        suma=suma+valor_simulado
        conrador3=conrador3+1
    #print(valor,frecuencia,l_acumulada,l_desde,l_acumulada,)

    promedio=round(suma/len(numeros_aleatoreos),3)
    return valor,frecuencia,l_acumulada,l_desde,l_acumulada,numeros_aleatoreos,l_valor_simulado



def calculoMontecarloInv(v,f):
    valor=[]
    frecuencia=[]
    for item1 in v:
        valor.append(float(item1))

    for item2 in f:
        frecuencia.append(float(item2))

    l_acumulada=[]
    l_desde=[0]
    l_valor_simulado=[]
    acumulada=0.0
    suma=0.0
    promedio=0.0
    contador=0
    for fre in frecuencia:
        acumulada=round(acumulada+frecuencia[contador],3)
        l_acumulada.append(acumulada)
        contador=contador+1

    contador_d=0
    for des in l_acumulada:
        l_desde.append(round(l_acumulada[contador_d]+0.001,3))
        contador_d=contador_d+1

    return valor,frecuencia,l_acumulada,l_desde,l_acumulada


def calculo(numero_aleatoreo, lista_desde, lista_hasta, lista_valor):
    valor_simulado=0

    for i in range(0, len(lista_valor)):
        if numero_aleatoreo >= lista_desde[i] and numero_aleatoreo < lista_hasta[i]:
            valor_simulado = lista_valor[i]
    #print(valor_simulado)
    return valor_simulado



    # Funcion que recibe una lista de valores y retorna el promedio de ellos
def promedio(lista):

    sumaParcial=0
    for valor in lista:
        sumaParcial=sumaParcial+valor
					
        #print(sumaParcial)
        cantidadValores = len(lista)

        #print(len(lista))
    return round(sumaParcial / float(cantidadValores),3)

def suma(lista):
    sumaParcial=0
    for valor in lista:
        sumaParcial=sumaParcial+valor
    return round(sumaParcial,3)