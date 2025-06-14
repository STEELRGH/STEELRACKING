from odoo import api, fields, models, Command, _

class ResCompany(models.Model):
    _inherit = 'res.company'


    @api.model
    def run_update_currency(self):
        """ This method is called from a cron job to update currency rates.
        """
        records = self.search([
            ('currency_next_execution_date', '<=', fields.Date.today()),
            ('parent_id', '=', False),
        ])
        if records:
            to_update = self.env['res.company']
            for record in records:
                if record.currency_interval_unit == 'daily':
                    next_update = relativedelta
                elif record.currency_interval_unit == 'weekly':
                    next_update = relativedelta
                elif record.currency_interval_unit == 'monthly':
                    next_update = relativedelta
                else:
                    record.currency_next_execution_date = False
                    continue
                record.currency_next_execution_date = datetime.date.today()
                to_update += record
            to_update.with_context(suppress_errors=True).update_currency_rates()
