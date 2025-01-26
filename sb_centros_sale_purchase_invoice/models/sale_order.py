# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    _description = 'Campo para relacionar al centro'


    centro_id = fields.Many2one('centros', string='Centro de Venta', required=True, domain=[('state', '=', 'active')])


    def create_invoices(self, grouped=False, final=False):
        """Sobrescribe la función de creación de facturas para agregar el centro automáticamente."""
        invoices = super(SaleOrderInherit, self).create_invoices(grouped=grouped, final=final)
        for invoice in invoices:
            invoice.centro_id = self.centro_id
        return invoices