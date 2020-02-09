# -*- coding: utf-8 -*-
import models

from odoo import api, SUPERUSER_ID

def drop_journal(cr, registry):
  env = api.Environment(cr, SUPERUSER_ID, {})
  journal_ids = env['account.journal'].search([('code', 'in',['INV','BILL'])])
  for j in journal_ids:
    j.sudo().unlink()
  tax_ids = env['account.tax'].search([('name', 'in',['Tax 15.00%','Impuesto 15.00%'])])
  for t in tax_ids:
    t.sudo().unlink()
  partner_ids = env['res.partner'].search([('vat', '=', True)])
  for p in partner_ids:
    p.nit = p.vat
  company_ids = env['res.company'].search(['|', ('vat', '=', True),('company_registry','=',True)])
  for p in partner_ids:
    p.nit = p.vat
    p.nrc = p.company_registry
    
  '''tax = env['account.tax'].create({
    'chart_template_id': env.ref('sv_coa'),
    'name':"Retencion 1 %",
    'description':"RETENCION 1%",
    'amount': -1,
    'amount_type':"percent",
    'type_tax_use':"sale",
    'account_id': env.ref('iva_retencion'),
    'refund_account_id': env.ref('iva_retencion'),
    #'tag_ids': [(6,0,[env.ref('tax_tag_04')])],
    'tax_group_id': env.ref('tax_group_iva_retencion')
  })
  
  p_fiscal = env['account.fiscal.position.tax'].search([('id','=', env.ref('position_tax_gran_ventas_2'))])
  p_fiscal.write({
    'tax_dest_id':tax})'''
      