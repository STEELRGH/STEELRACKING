from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    referencia_xml = fields.Many2one(
        'cfdi.download.data',
        string='Referencia XML',
    )

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    referencia_xml = fields.Many2one(
        'cfdi.download.data',
        string='Referencia XML',
    )
