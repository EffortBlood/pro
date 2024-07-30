# -*- coding: utf-8 -*-
#############################################################################
#
#    Carlos Alfonzo
#
#    Modelo para el manejo de estaciones de caja - POS y el respectivo nombramiento de
#	 los archivos de facturas txt, segun el numero de estacion
#############################################################################

from odoo import fields, models, api

class NumEstacion(models.Model):
    _name = 'num.estacion'
    nombre = fields.Char('Nombre', required=True)                   # Direccion IP
    numero_estacion = fields.Char('Numero estacion', required=True) # 3 digitos: 001, 002, 003, etc. Será extension de archivo
    sub_carpeta = fields.Char('Subcarpeta', required=False)         # Subcarpeta para archivos de la estacion