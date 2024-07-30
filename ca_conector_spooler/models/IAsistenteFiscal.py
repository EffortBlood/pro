# -*- coding: utf-8 -*-
from odoo import models, fields

class IAsistenteFiscal(models.Model):
    _name = 'iasistente.fiscal'
    _description = 'Interfaz Asistente Fiscal Super Spooler'

    nombre_empesa =fields.Char('Empresa', required=True, index=False)
    #rif_empresa = fields.Char('RIF', required=False, index=False)
    carpeta_facturas = fields.Char('Carpeta', required=False, index=False)
    #carpeta_spooler = fields.Char('Carpeta spooler', required=False, index=False)
    #licencia_spooler = fields.Char('Licencia Spooler', required=False, index=False)
    #licencia_conector = fields.Char('Licencia conector', required=False, index=False)
    #fecha_inicio = fields.Date('Fecha inicio')
    #fecha_vencimiento = fields.Date('Fecha vencimiento')
    notas = fields.Text('Notas internas')
