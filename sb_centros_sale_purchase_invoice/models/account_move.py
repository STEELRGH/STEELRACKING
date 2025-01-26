# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    _description = 'Campo para relacionar al centro'


    centro_id = fields.Many2one('centros', string='Centro Asociado')