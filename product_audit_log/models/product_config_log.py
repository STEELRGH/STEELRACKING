from odoo import models, fields, api
from odoo.exceptions import UserError

class ProductConfigLog(models.Model):
    _name = 'product.config.log'
    _description = 'Bitácora de Cambios de Producto'
    _order = 'date desc'

    product_tmpl_id = fields.Many2one('product.template', string='Producto', ondelete='cascade')
    user_id = fields.Many2one('res.users', string='Usuario', default=lambda self: self.env.user, readonly=True)
    modification = fields.Text(string='Modificación', readonly=True)
    date = fields.Datetime(string='Fecha', default=fields.Datetime.now, readonly=True)

    def unlink(self):
        raise UserError("Está estrictamente prohibido eliminar registros de la bitácora de cambios.")