from odoo import api, fields, models, tools

class CfdiDownloadData(models.Model):
    _inherit = 'cfdi.download.data'

    order_reference = fields.Many2one(
        'combined.order',
        string="Referencia de Orden",
    )

    def write(self, vals):
        # Almacenar los valores anteriores de 'order_reference'
        prev_order_references = {rec.id: rec.order_reference for rec in self}
        res = super(CfdiDownloadData, self).write(vals)
        for record in self:
            prev_order_reference = prev_order_references.get(record.id)
            new_order_reference = record.order_reference
            # Si 'order_reference' cambió, actualizar los pedidos correspondientes
            if prev_order_reference != new_order_reference:
                # Limpiar 'referencia_xml' del pedido anterior
                if prev_order_reference:
                    self._update_order_referencia_xml(prev_order_reference, None)
                # Establecer 'referencia_xml' en el nuevo pedido
                if new_order_reference:
                    self._update_order_referencia_xml(new_order_reference, record)
        return res

    def create(self, vals):
        record = super(CfdiDownloadData, self).create(vals)
        if record.order_reference:
            record._update_order_referencia_xml(record.order_reference, record)
        return record

    def _update_order_referencia_xml(self, combined_order, cfdi_record):
        order_type = combined_order.order_type
        order_id = abs(combined_order.id)  # Usamos 'abs' por los IDs negativos
        if order_type == 'sale':
            order = self.env['sale.order'].browse(order_id)
        else:
            order = self.env['purchase.order'].browse(order_id)
        # Actualizar el campo 'referencia_xml' en el pedido
        order.write({'referencia_xml': cfdi_record and cfdi_record.id or False})