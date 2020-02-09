# -*- coding: utf-8 -*-
from amount_to_text_sv import amount_to_text
from odoo import api, fields, models, _, exceptions

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    inv_refund_id = fields.Many2one('account.invoice','Factura Relacionada', copy=False, track_visibility='onchange')

    state_refund = fields.Selection([
            ('refund','Retificada'),
            ('no_refund','No Retificada'),
        ], string="Retificada", index=True, readonly=True, default='no_refund',
        track_visibility='onchange', copy=False)
    
    amount_text = fields.Char(string=_('Amount to text'), store=True, readonly=True,
                              compute='_amount_to_text',track_visibility='onchange')
       
    @api.one
    @api.depends('amount_total')
    def _amount_to_text(self):
        self.amount_text = amount_to_text(self.amount_total)
    
    @api.multi
    def invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        self.ensure_one()
        self.sent = True
        
        report = self.journal_id.type_report
        
        if report == 'ccf':
            return self.env['report'].get_action(self, 'l10n_invoice_sv.report_invoice_main_ccf')
        if report == 'fcf':
            return self.env['report'].get_action(self, 'l10n_invoice_sv.report_invoice_main_fcf')
        if report == 'exp':
            return self.env['report'].get_action(self, 'l10n_invoice_sv.report_invoice_main_exp')
        if report == 'ndc':
            return self.env['report'].get_action(self, 'l10n_invoice_sv.report_invoice_main_ndc')
        if report == 'anu':
            return self.env['report'].get_action(self, 'l10n_invoice_sv.report_invoice_main_anu')
        if report == 'axp':
            return self.env['report'].get_action(self, 'l10n_invoice_sv.report_invoice_main_axp')
        
        return self.env['report'].get_action(self, 'account.report_invoice')
    
    @api.multi
    def msg_error(self,campo):
      raise exceptions.ValidationError("No puede emitir un documento si falta un campo Legal "\
                                       "Verifique %s" % campo)
      return True
    
    @api.multi
    def action_invoice_open(self):
        '''validamos que partner cumple los requisitos basados en el tipo
        de documento de la sequencia del diario selecionado'''
        inv_type = self.type
        #si es factura normal
        type_report = self.journal_id.type_report
    
        if type_report == 'ccf':
          if not self.partner_id.nrc:
            self.msg_error("N.R.C.")
          if not self.partner_id.nit:
            self.msg_error("N.I.T.")
          if not self.partner_id.giro:
            self.msg_error("Giro")
    
        if type_report == 'fcf':
          if not self.partner_id.nit:
            self.msg_error("N.I.T.")
          if self.partner_id.company_type == 'person':
            if not self.partner_id.dui:
              self.msg_error("D.U.I.")
          
        if type_report == 'exp':
            for l in self.invoice_line_ids:
                if not l.product_id.arancel_id:
                    self.msg_error("Posicion Arancelaria del Producto %s" %l.product_id.name)
    
        #si es retificativa
        if type_report == 'ndc':
          if not self.partner_id.nrc:
            self.msg_error("N.R.C.")
          if not self.partner_id.nit:
            self.msg_error("N.I.T.")
          if not self.partner_id.giro:
            self.msg_error("Giro")
        
        return super(AccountInvoice, self).action_invoice_open()