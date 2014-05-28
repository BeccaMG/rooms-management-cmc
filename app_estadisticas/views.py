from django.shortcuts import render
# Manejo de Sesion
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# General HTML
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from app_solicitudes.models import *
from app_camas.models import *
import datetime
from django.utils import timezone
import pdb

from django.utils import simplejson

# Termometro = {'fecha':camas}
camas_libres = Habitacion.objects.all().filter(estado='D')
camas_verdes = Ingreso.objects.all().filter(habitacion__estado='O') 
camas_amarillas = Ingreso.objects.all().filter(habitacion__estado='O') 
camas_rojas = Ingreso.objects.all().filter(habitacion__estado='O') 
camas = [camas_libres, camas_verdes, camas_amarillas, camas_rojas]
Termometro = {'2014-05-26':camas}

@login_required(login_url='/')
def termometro(request):
	
	now = timezone.now()
	nowS = str(now.date())
	
	if (nowS > Termometro.keys()[-1]):
	
		camas_libres = Habitacion.objects.all().filter(estado='D')
		dos_dias = now - datetime.timedelta(days=2)
		cuatro_dias = now - datetime.timedelta(days=4)
		cinco_dias = now - datetime.timedelta(days=5)
		
		dos_diasS = str(dos_dias.date())
		cuatro_diasS = str(cuatro_dias.date())
		cinco_diasS = str(cinco_dias.date())
		
		camas_verdes = Ingreso.objects.all().filter(habitacion__estado='O', fecha_ingreso__gte=dos_diasS,fecha_ingreso__lte=nowS)  
		camas_amarillas = Ingreso.objects.all().filter(habitacion__estado='O', fecha_ingreso__gte=cuatro_diasS,fecha_ingreso__lte=dos_diasS)  
		camas_rojas = Ingreso.objects.all().filter(habitacion__estado='O', fecha_ingreso__lt=cuatro_diasS)	
		 
		Termometro[nowS] = [camas_libres, camas_verdes, camas_amarillas, camas_rojas]
		
		info = {
			'Termometro':Termometro,	
		}
	else:
	
		hoy = date.today
		info = {
			'Termometro':Termometro,
		}
		
	return render_to_response('estadistica_termometro.html',info,context_instance=RequestContext(request))

@login_required(login_url='/')
def matriz(request):
	
	hab_libre =  [ item for item in Habitacion.objects.all().filter(estado='D') ]
	hab_alta = [ item for item in Habitacion.objects.all().filter(estado='A') ]
	hab_ocu = [ item for item in Habitacion.objects.all().filter(estado='O') ]
	hab_limp = [ item for item in Habitacion.objects.all().filter(estado='L') ]
	hab_mant = [ item for item in Habitacion.objects.all().filter(estado='M') ]
	
	habs = hab_libre + hab_alta + hab_ocu + hab_limp + hab_mant
	habs.sort( key = lambda x: x.numero , reverse = False )
	info = {}
	info['habs'] = habs
	
	return render_to_response('estadistica_matriz.html',info,context_instance=RequestContext(request))
	
	
	
