# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'
    _description = 'Campo para relacionar al centro'


    centro_id = fields.Many2one('centros', string='Centro de Compra', required=True, domain=[('state', '=', 'active')])



    def action_create_invoice(self):
        """Sobrescribe la confirmación del pedido de compra para vincular el centro en la factura."""
        result = super(PurchaseOrderInherit, self).action_create_invoice()
        for order in self:
            for invoice in order.invoice_ids:
                invoice.centro_id = order.centro_id
        return result

    
