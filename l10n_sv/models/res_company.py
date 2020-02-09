# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions
class Company(models.Model):
    _inherit = 'res.company'
    
    nrc = fields.Char(string="N.R.C.")
    nit = fields.Char(string="N.I.T.")
    giro = fields.Char(string="Giro")