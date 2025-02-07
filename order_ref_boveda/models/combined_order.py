from odoo import api, fields, models, tools

class CombinedOrder(models.Model):
    _name = 'combined.order'
    _description = 'Órdenes Combinadas de Venta y Compra'
    _auto = False  # Es una vista SQL, no una tabla real

    id = fields.Integer('ID', readonly=True)
    name = fields.Char('Referencia de Orden', readonly=True)
    date_order = fields.Datetime('Fecha de Orden', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Cliente/Proveedor', readonly=True)
    order_type = fields.Selection([
        ('sale', 'Orden de Venta'),
        ('purchase', 'Orden de Compra'),
    ], string='Tipo de Orden', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW combined_order AS (
                SELECT
                    id,
                    name,
                    date_order,
                    partner_id,
                    'sale' as order_type
                FROM sale_order
                UNION ALL
                SELECT
                    -id,  -- IDs negativos para órdenes de compra
                    name,
                    date_order,
                    partner_id,
                    'purchase' as order_type
                FROM purchase_order
            )
        """)

    def name_get(self):
        result = []
        for record in self:
            order_type = dict(self._fields['order_type'].selection).get(record.order_type)
            name = f"{order_type}: {record.name}"
            result.append((record.id, name))
        return result
