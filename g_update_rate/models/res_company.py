import datetime
import logging
import re
from itertools import islice
from urllib.parse import quote, urlencode

import requests
from dateutil.relativedelta import relativedelta
from lxml import etree
from pytz import timezone

from odoo import api, fields, models

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

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_tax_totals(self, partner, tax_lines, amount_total, amount_untaxed, currency):
        res = super()._get_tax_totals(partner, tax_lines, amount_total, amount_untaxed, currency)
        
        # Forzar a que cada grupo conserve los montos independientes 
        # sin ocultar las retenciones o importes compensados
        for subtotal_key, groups in res.get('groups_by_subtotal', {}).items():
            for group in groups:
                # Evita que se sobreescriba el nombre del grupo si la suma neta da 0
                group['hide_base_amount'] = False
                
        return res
