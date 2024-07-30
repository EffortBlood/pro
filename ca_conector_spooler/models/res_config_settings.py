# -*- coding: utf-8 -*-
from odoo import api, fields, models
import platform

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    #carpeta_facturas = fields.Char(string="Carpeta facturas")
    carpeta_txt = fields.Char(related="pos_config_id.carpeta_txt", readonly=False )
    extension_archivos = fields.Char(related="pos_config_id.extension_archivos", readonly=False, required=True)
    sub_carpeta_txt = fields.Char(related="pos_config_id.sub_carpeta_txt", readonly=False, required=False)
    numero_estacion = fields.Integer(related="pos_config_id.numero_estacion", readonly=False, required=True)

    '''
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['carpeta_facturas'] = self.env['ir.config_parameter'].sudo().get_param("base.carpeta_facturas", default="c:\\facturas" if platform.system() == "Windows" else "~/facturas")
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].set_param("base.carpeta_facturas", self.carpeta_facturas or '')
        super(ResConfigSettings, self).set_values()
    '''