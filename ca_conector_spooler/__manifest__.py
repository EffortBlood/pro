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
{
    'name': 'Conector Spooler',
    'version': '14.0.1.0.1',
    'summary': 'Imprime en impresoras fiscales a traves Spoolers, enviando archivos de facturas',
    'description': 'Imprime en impresoras fiscales a traves de Spoolers',
    'category': 'Impresion Fiscal',
    'author': 'Carlos Alfonzo',
    'maintainer': 'Carlos Alfonzo',
    'company': 'Carlos Alfonzo',
    'website': '',
    'depends': [
        'base','base', 'point_of_sale'
        ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings.xml",
        "views/account_move_views.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
