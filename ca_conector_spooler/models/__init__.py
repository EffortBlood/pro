# -*- coding: utf-8 -*-
#################################################################################################
#
#    Interfaz Odoo con Asistente Fiscal Super Spooler
#
#    Febrero 2022
#    Autor: Carlos Alfonzo (calfonzodaly@gmail.com)
#
#    Interfaz para impresion en impresoras fiscales, a traves del Asistete Fiscal Super Spooler
#
#
##################################################################################################

import os
from . import ext_doc
from . import IAsistenteFiscal
from . import num_estacion
from . import spooler
from . import account_move
from . import pos_order
from . import res_config_settings