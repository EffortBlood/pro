# -*- coding: utf-8 -*-

from odoo import fields, models, api
import os
import platform
import csv
from odoo.http import request

from . import ext_doc

from datetime import datetime
import re
import logging
_logger = logging.getLogger(__name__)

#Extension de los archivos de respuesta fiscal para SuperSpooler. Considerar mayusculas/minusculas
EXTENSION_ARCHIVO_RESPUESTA = "RES"
COLUMNAS_RES = ['fecha', 'hora', 'ref_interna', 'numero_fiscal', 'tipo', 'estatus', 'proximo_z', 'serial_impresora', 'doc_afectado']

#Prefijo archivos de facturas y notas de credito para SuperSpooler
PREFIJO_FACTURAS = "fa"
PREFIJO_NOTAS_CREDITO = "nc"
DELIMITADOR_CSV = '\t'
ERROR_ARCHIVO = "error_archivo"
ERROR_DATOS = "error_datos"
ERROR_DOCUMENTO_NOEXISTE = "error_documento_no_existe"
DATOS_CARGADOS = "cargado"
DATOS_PENDIENTES = 'pendiente'
DATOS_ANULADOS = 'anulado'    #Marca un documento para no procesarlo, es decir, no intentar cargar su info fiscal
CARPETA_ENTRADA = '/var/lib/odoo/facturas_txt'

def gen_archivo_factura( invoi ):
    #doc = extraer( invoi )

    '''
    _logger.info("-----------   Inicio debug Spooler  -----------------")
    _logger.info("Spooler REMOTE_ADDR: " + request.httprequest.environ['REMOTE_ADDR'])
    _logger.info("Spooler HTTP_USER_AGENT: " + request.httprequest.environ['HTTP_USER_AGENT'])
    #_logger.info("Spooler" + request.httprequest.environ['HTTP_X_REAL_IP'])
    _logger.info("Spooler SERVER_NAME: " + request.httprequest.environ['SERVER_NAME'])
    _logger.info("Company: " + invoi.env.company.name)
    _logger.info("-----------   Fin debug  Spooler  ----------------")
    '''

    doc = ext_doc.extraer_documento( invoi )
    if doc:
        nombre = preparar_nombre_archivo( invoi, doc )
    else:
        return {}

    if doc['tipodoc'] == "fac":
        f = open(nombre, "w")
        f.write ( "FACTURA:         {}".format( doc['numero'] ) + "\n" )
    elif doc['tipodoc'] ==  "nc":
        f = open(nombre, "w")
        f.write ( "DEVOLUCION:      {}".format( doc['numero'] ) + "\n" )
    else:
        return {}

    escribir_archivo_factura(f, doc)
    #cargar_datos_fiscales( doc['numero'], doc['tipodoc'], invoi )
    return doc


def preparar_nombre_archivo( invoi, doc):
    numero_doc = doc['numero']
    tipo_doc = doc['tipodoc']

    datos = invoi.env['pos.config'].search([], limit=1) 

    if datos:
        carpeta= datos['carpeta_txt']

    #if not isinstance(carpeta, str):
    #    carpeta = ""

    #NOTA: carpeta por defecto en servidor local ~/facturas_txt (<home/usuario/facturas_txt>)
    #NOTA: carpeta por defecto en contenedor docker /var/lib/odoo/facturas_txt
    #NOTA: carpeta por defecto en Odoo SH /home/odoo/spooler/[sucursal/]facturas
    if (not datos) or (carpeta == "") or (not isinstance(carpeta, str)):
        carpeta = os.path.expanduser("/tmp") if platform.system() == "Linux" else "c:\\temp"
        #NOTA: carpeta por defecto en contenedor docker /var/lib/odoo/facturas_txt

    ip_cliente = request.httprequest.environ['REMOTE_ADDR']
    separador = "/" if platform.system() == "Linux" else "\\"
    estacion = invoi.env['num.estacion'].search([('nombre','=', ip_cliente )])
    #extension = estacion['numero_estacion'] if estacion else "001"
    #01/07/2022: Se deja la extension en .odo y cada estacion tendra su carpeta. Se definen en data.xml
    extension = "odo"
    subc = estacion['sub_carpeta'] if estacion['sub_carpeta'] else ""

    if subc != "":
        carpeta = carpeta + separador + subc

    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    #numerosf = re.findall(r'\d+', numero_doc )
    #numfactura = numerosf[len( numerosf ) -1 ]

    if tipo_doc == "fac":
        nombre = carpeta + separador + "fa" + numero_doc + "." + extension
    elif tipo_doc ==  "nc":
        nombre = carpeta + separador + "nc" + numero_doc + "." + extension
    else:
        nombre = ""

    return nombre


def escribir_archivo_factura(f, doc):
    f.write ( "FECHA:           " + doc['fecha'] + "\n"  )
    f.write ( "CLIENTE:         " + doc['cliente'] + "\n"  )
    f.write ( "RIF:             " + doc['rif'] + "\n" if doc['rif'] else "RIF:" + "\n" )
    f.write ( "DIRECCION1:      " + doc['dir1'] + "\n"  if doc['dir1'] else "DIRECCION:" + "\n"  )
    f.write ( "DIRECCION2:      " + doc['dir2'] + "\n" if doc['dir2'] else "DIRECCION2:" + "\n" )
    f.write ( "TELEFONO:        " + doc['telefono'] + "\n" if doc['telefono'] else "TELEFONO:" + "\n" )

    f.write ( "DESCRIPCION                                                 COD          CANT.    IVA    PRECIO UNIT\n")

    # Items 
    FFISCAL_LONG_MAX_DESCRIPCION = 60
    for pos in doc['productos']:
        # Separar la descripcion del item en lineas segun la longitud maxima por linea 
        item_fact = doc['productos'][pos]
        desc = item_fact['descripcion'] if item_fact['descripcion'] else " " #Si agregan items vacios
        long_desc = len( desc )
        lst_descripciones_item = [ desc[i:i+FFISCAL_LONG_MAX_DESCRIPCION] for i in range(0, long_desc, FFISCAL_LONG_MAX_DESCRIPCION ) ]

        #Guarda cada parte de la descripcion en lineas separadas, en las lineas adicionales solo va Descripcion
        #y el esto de las columnas en blanco, en caso de haber lineas adicionales
        
        # Escribe los items formateados en el archivo
        f.write( "{:<60}".format( lst_descripciones_item[0] ) )
        f.write( "{:<8}".format( item_fact['codigoprod'] ) )
        f.write( "{:>10.2f}".format( item_fact['cantidad'] ) )

        f.write( "{:>8.2f}".format( item_fact['iva'] ) )

        f.write( "{:>12.2f}".format( item_fact['precio'] ) + "\n"  )

        #Escribe las lineas adicionales de la descripcion
        pos = 1
        while pos < len( lst_descripciones_item ):
            f.write( "{:<60}".format( lst_descripciones_item[pos] ) + "\n" )
            pos += 1
    
    # Totales
    f.write ( "SUB-TOTAL:      {:>10.2f}".format(doc['sub_total']) + "\n")
    f.write ( "DESCUENTO:      {:>10.2f}".format(0.0) + "\n")
    f.write ( "TOTAL A PAGAR:  {:>10.2f}".format(doc['total_pagar']) + "\n")

    f.write ( "EFECTIVO:       {:>10.2f}".format(doc['efectivo']['monto']) + "\n" )
    f.write ( "CHEQUES:        {:>10.2f}".format(doc['banco']['monto']) + "\n" )
    f.write ( "TARJ/DEBITO:    {:>10.2f}".format(doc['tarj_debito']['monto']) + "\n" )
    f.write ( "TARJ/CREDITO:   {:>10.2f}".format(doc['tarj_credito']['monto']) + "\n" )
    f.write ( "Tranf en Bs:    {:>10.2f}".format(doc['trans_bs']['monto']) + "\n" )
    f.write ( "Transf en USD:  {:>10.2f}".format(0.0) + "\n" )
    f.write ( "Zelle:          {:>10.2f}".format(doc['zelle']['monto']) + "\n" )
    f.write ( "Efect USD:      {:>10.2f}".format(doc['efectivo_usd']['monto']) + "\n" )
    f.write ( "Efect EURO:     {:>10.2f}".format(doc['efectivo_euro']['monto']) + "\n" )
    f.write ( "Pago movil:     {:>10.2f}".format(doc['pago_movil']['monto']) + "\n" )
    f.write ( "CREDITO:        {:>10.2f}".format(doc['credito']['monto']) + "\n" )

    # Notas 
    f.write ( "NOTA 1:        " + "\n")
    f.write ( "NOTA 2:        " + "\n")
    f.write ( "NOTA 3:        " + "\n")
    f.write ( "NOTA 4:        " + "\n")

    #if doc['tipodoc'] == "nc":
    if (doc['factura_afectada'] != "") :
        f.write ( "FACTURAAFECTADA:       {}".format(doc['factura_afectada']) + "\n" )
