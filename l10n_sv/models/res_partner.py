# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions
class Partner(models.Model):
    _inherit = 'res.partner'
    
    dui = fields.Char(string="D.U.I.")
    nit = fields.Char(string="N.I.T.")
    nrc = fields.Char(string="N.R.C.")
    giro = fields.Char(string="Giro")