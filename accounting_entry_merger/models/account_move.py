from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    related_move_lines = fields.One2many(
        comodel_name='account.move.line',
        compute='_compute_related_move_lines',
        string='Líneas Relacionadas',
    )

    def _compute_related_move_lines(self):
        for move in self:
            related_lines = self.env['account.move.line']
            if move.ref:
                # Buscar todas las líneas de apuntes contables con la misma referencia
                related_lines = self.env['account.move.line'].search([
                    ('move_id.ref', '=', move.ref),
                    ('move_id', '!=', move.id),
                ])
            move.related_move_lines = related_lines
