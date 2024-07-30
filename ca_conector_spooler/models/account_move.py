# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
#from spooler import gen_archivo_factura as generar
from . import spooler

class AccountMove(models.Model):
    _inherit = 'account.move'

    estado_data_fiscal = fields.Selection([
        ('pendiente', 'Pendiente'),            #No se ha intentado cargar
        ('error_datos', 'Error de datos'),     #datos no presentes o con formato incorrecto
        ('error_archivo', 'Error de archivo'), #Aechivo no encontrado
        ('cargado', 'Cargado')                 #Cargado correctamente
    ], default='pendiente', string='Estatus data fiscal', readonly=True, invisible=True)

    numero_reporte_z = fields.Char(string='Reporte Z', readonly=True, invisible=True)
    serial_impresora_fiscal = fields.Char(string='Serial impresora fiscal', readonly=True, invisible=True)

    def generar_archivo_factura(self):
        #generar(self)
        spooler.gen_archivo_factura(self)

