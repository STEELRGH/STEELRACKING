from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    log_ids = fields.One2many('product.config.log', 'product_tmpl_id', string='Historial de Cambios')

    def write(self, vals):
        # Campos solicitados
        tracked_fields = [
            'property_account_income_id', 
            'property_account_expense_id', 
            'unspsc_code_id'
        ]
        
        # Diccionario para nombres legibles en el log
        field_labels = {
            'property_account_income_id': 'Cuenta de Ingresos',
            'property_account_expense_id': 'Cuenta de Gastos',
            'unspsc_code_id': 'Código UNSPSC'
        }

        for record in self:
            log_entries = []
            for field in tracked_fields:
                if field in vals:
                    # Valor anterior
                    old_raw = getattr(record, field)
                    old_name = old_raw.display_name if old_raw else "Vacío"
                    
                    # Nuevo valor
                    new_val_id = vals.get(field)
                    if new_val_id:
                        # Buscamos el nombre del nuevo registro relacionado
                        comodel = self.env[record._fields[field].comodel_name]
                        new_name = comodel.browse(new_val_id).display_name
                    else:
                        new_name = "Vacío"

                    if old_name != new_name:
                        log_entries.append(f"[{field_labels.get(field)}] cambió de: '{old_name}' a: '{new_name}'")
            
            if log_entries:
                self.env['product.config.log'].create({
                    'product_tmpl_id': record.id,
                    'modification': "\n".join(log_entries),
                    'user_id': self.env.user.id,
                    'date': fields.Datetime.now(),
                })
                
        return super(ProductTemplate, self).write(vals)