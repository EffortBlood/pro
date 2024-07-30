# -*- coding: utf-8 -*-

from odoo import fields, models, api
import json
import re

import logging
_logger = logging.getLogger(__name__)
 
def extraer_documento(invoi):
    if invoi.move_type != 'out_invoice' and invoi.move_type != 'out_refund':
        dfc = {}
    else:
        pos = 0
        ditems = {}
        descuento = 0.0
        #modificado para considerar descripcion de ventas y mejorar lectura
        for item_fact in invoi.invoice_line_ids:
            ditems[pos] = {
                'descripcion': item_fact.product_id.description_sale if item_fact.product_id.description_sale else item_fact.product_id.name, 
                'codigoprod': item_fact.product_id.product_tmpl_id.id,
                'cantidad': item_fact.quantity, 
                'iva': item_fact.tax_ids[0].amount if item_fact.tax_ids else 0.0, 
                'precio':  item_fact.price_subtotal/item_fact.quantity if item_fact.quantity != 0 else 0.0, 
                'descuento': item_fact.discount }

            #Asegura que si la cantidad es cero(0.0), el renglon completo tenga todo en cero. Remueve calculos erroneos
            if (ditems[pos]['cantidad'] == 0.0):
                ditems[pos]['descuento'] = ditems[pos]['iva'] = ditems[pos]['precio'] = 0.0

            descuento = descuento + item_fact.discount * (item_fact.price_unit * item_fact.quantity)/100
            pos += 1

        cont = 0
        pitems = {}

        #Obtiene los items de pagos. Considera el origen y tipo de documento: desde POS o Facturacion, Factura o NC
        if (invoi.move_type == 'out_invoice' or invoi.move_type == 'out_refund'):
            if (len(invoi.pos_order_ids) > 0) and (invoi.move_type != 'out_refund'):   #Factura originada en el POS no-devolucion
                for item_pago in invoi.pos_order_ids[0].payment_ids:
                    clave = item_pago.payment_method_id.display_name
                    if clave in pitems:
                        pitems[clave]["monto"] += item_pago.amount
                    else:
                        pitems[clave] = {'monto': item_pago.amount }
            elif (invoi.move_type != 'out_refund') and invoi.invoice_payments_widget: #Factura originada por backend/Facturacion
                if type (invoi.invoice_payments_widget) is dict:
                    midata = invoi.invoice_payments_widget
                else:
                    midata = json.loads(invoi.invoice_payments_widget)

                if midata:
                    for item_pago in midata['content']:
                        pitems[item_pago["journal_name"]] = {'monto': item_pago["amount"] }

        #Obtiene el documento para casos de devoluciones/NC
        if invoi.move_type == 'out_refund':
            if invoi.reversed_entry_id.name:
                referencia = invoi.reversed_entry_id.name
            else:
                refs = invoi.env['account.move'].search([('ref', '=', invoi.ref.replace("REEMBOLSO", "")), ('move_type', '=', 'out_invoice')], limit=1)
                referencia = refs.name if refs.name else ""
        else:
            referencia = ""

        #Descuentos: el SSP l maneja global y el sistema por item, para manejarse debe aclararse bien el tema

        #Elimina caracteres especiales del numero de factura y solo toma los digitos finales
        #Previamente se hacia en spooler.doc pero solo afectaba el nombre del archivo y no valor dentro del txt
        #Afecta los nombres de archivo, pues el numero es parte de estos
        #Es posible que se repitan numeros el siguiente año. Puede resolverse concatenando año + numero
        #Cualquier adaptacion se haria aqui
        numerosf = re.findall(r'\d+', invoi.name )
        numfactura = numerosf[len( numerosf ) -1 ]

        if referencia != "":
            ref_tmp = re.findall(r'\d+', referencia )
            referencia = ref_tmp[len( ref_tmp ) -1 ]

        dfc = {}
        dfc = {
        'tipodoc': 'fac' if invoi.move_type == 'out_invoice' else 'nc' if invoi.move_type == 'out_refund' else '*',
        'numero': numfactura,
        'fecha': invoi.date.strftime("%d/%m/%Y"),
        'cliente': str(invoi.partner_id.name),
        'rif':  str(invoi.partner_id.vat) if invoi.partner_id.vat else "",
        'dir1': str(invoi.partner_id.street) if invoi.partner_id.street else "",
        'dir2': str(invoi.partner_id.street2) if invoi.partner_id.street2 else "",
        'telefono': str(invoi.partner_id.phone) if invoi.partner_id.phone else "",
        'productos': ditems,
        'pagos': pitems,
        'efectivo': pitems.get('Efectivo Bs') if pitems.get('Efectivo Bs') else {'monto': 0.0},
        'banco': pitems.get('Banco') if pitems.get('Banco') else {'monto': 0.0},
        'tarj_debito': pitems.get('Tarjeta de debito') if pitems.get('Tarjeta de debito') else {'monto': 0.0}, 
        'tarj_credito': pitems.get('Tarjeta de credito') if pitems.get('Tarjeta de credito') else {'monto': 0.0},
        'trans_bs': pitems.get('Transferencia Bs') if pitems.get('Transferencia Bs') else {'monto': 0.0},
        'zelle': pitems.get('Zelle') if pitems.get('Zelle') else {'monto': 0.0},
        'trans_euro': pitems.get('trans_euro') if pitems.get('trans_euro') else {'monto': 0.0},
        'efectivo_usd': pitems.get('Efectivo USD') if pitems.get('Efectivo USD') else {'monto': 0.0},
        'efectivo_euro': pitems.get('efectivo_euro') if pitems.get('efectivo_euro') else {'monto': 0.0},
        'pago_movil': pitems.get('Pago movil') if pitems.get('Pago movil') else {'monto': 0.0},
        'credito':  pitems.get('Credito') if pitems.get('Credito') else {'monto': 0.0},
        'sub_total': invoi.amount_untaxed,
        'porc_descuento': 0.0,
        'total_pagar': invoi.amount_total,
        'factura_afectada': referencia
        }

    return dfc
