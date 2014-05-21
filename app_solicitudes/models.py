from django.db import models
from app_paciente.models import *
from app_usuario.models import *
from django.utils import timezone


PROCEDENCIA = (
    (1,'Quirofano'),
    (2,'Emergencia Pediatrica'),
    (3,'Emergencia Adultos'),
    (4,'Partos'),
    (5,'UCI'),
    (6,'Adicional'),
    (7,'Especial'),
    (8,'Traslado'),
    (9,'Otros'),
)

class Solicitud(models.Model):
    paciente        = models.ForeignKey(Paciente)
    medico          = models.ForeignKey(Medico)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    diagnostico     = models.CharField(max_length=50)
    fecha_ingreso   = models.DateField()
    fecha_salida    = models.DateField()
    procedencia     = models.IntegerField(choices=PROCEDENCIA)
    correo          = models.CharField(max_length=140)
    observacion     = models.CharField(max_length=140, null = True, blank = True)
    activa        	= models.BooleanField(default=True)
    
    def salida(self):
        return self.fecha_salida.strftime("%d/%m/%y")
        
    class Meta:
        verbose_name_plural = "Solicitudes"