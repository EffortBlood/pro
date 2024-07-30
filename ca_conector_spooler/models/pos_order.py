# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from datetime import timedelta
from functools import partial
from itertools import groupby

import psycopg2
import pytz
import re

from odoo import api, fields, models, tools, _
from odoo.tools import float_is_zero, float_round, float_repr, float_compare
from odoo.exceptions import ValidationError, UserError
from odoo.http import request
from odoo.osv.expression import AND
import base64

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _generate_pos_order_invoice(self):
        moves = self.env['account.move']

        for order in self:
            # Force company for all SUPERUSER_ID action
            if order.account_move:
                moves += order.account_move
                continue

            if not order.partner_id:
                raise UserError(_('Please provide a partner for the sale.'))

            move_vals = order._prepare_invoice_vals()
            new_move = order._create_invoice(move_vals)

            order.write({'account_move': new_move.id, 'state': 'invoiced'})
            new_move.sudo().with_company(order.company_id)._post()
            new_move.generar_archivo_factura()
            moves += new_move
            order._apply_invoice_payments()

        if not moves:
            return {}

        return {
            'name': _('Customer Invoice'),
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
            'res_model': 'account.move',
            'context': "{'move_type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': moves and moves.ids[0] or False,
        }

class PosConfig(models.Model):
    _inherit = 'pos.config'

    carpeta_txt = fields.Char(string='Carpeta principal', required=True, help='Carpeta principal de archivos txt de facturas. Si es la misma para varias cajas, repetirla en cada una')
    extension_archivos = fields.Char(string='Extension de archivos', required=True, help='Extension para los archivos generados. Por defecto es .odo, tambien puede ser  numero segun las estacion .001, .002, .003, etc. NO debe incluir el punto')
    sub_carpeta_txt = fields.Char(string='Sub carpeta', required=False, help='Define la carpeta para archivos txt de las facturas para esta caja')
    numero_estacion = fields.Integer(string='Numero estacion', required=True, default = 0, help='Numero de estacion. Genera extensiones de los archivos (.001, .002, etc.). 0 = .odo')