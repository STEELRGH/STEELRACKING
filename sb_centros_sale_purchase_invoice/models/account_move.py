# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    _description = 'Campo para relacionar al centro'


    centro_id = fields.Many2one('centros', string='Puntos de venta')
    exchange_rate = fields.Float(string="Tipo de Cambio", digits=(12, 6), help="Tipo de cambio de la factura.")

    @api.onchange('currency_id')
    def _onchange_currency(self):
        """Actualizar el tipo de cambio basado en la moneda seleccionada"""
        if self.currency_id and self.company_id.currency_id:
            self.exchange_rate = self.currency_id._convert(
                1, self.company_id.currency_id, self.company_id, fields.Date.today()
            )

    # purchase_id = fields.Many2one('purchase.order', string="Purchase Order", compute="_compute_purchase_id", store=True)

    # @api.depends('invoice_line_ids.purchase_line_id.order_id')
    # def _compute_purchase_id(self):
    #     for record in self:
    #         purchase_orders = record.invoice_line_ids.mapped('purchase_line_id.order_id')
    #         record.purchase_id = purchase_orders[0] if purchase_orders else False