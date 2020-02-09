# -*- coding: utf-8 -*-
import models
import wizard


from odoo import api, SUPERUSER_ID

def invoices_refunds(cr, registry):
  env = api.Environment(cr, SUPERUSER_ID, {})
  inv_obj = env['account.invoice']
  inv_ids = inv_obj.search([('type','=','out_invoice'),
            ('state','=','paid'),])
  for inv_id in inv_ids:
    refund_id = inv_obj.search([('origin','=',inv_id.number)])
    refund_data = inv_obj.browse(refund_id)
    if refund_id and len(refund_id) < 2:
      inv_id.inv_refund_id = refund_data.id
      refund_data.write({
        'inv_refund_id':inv_id.id,
        'state_refund': 'refund'})
