# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Centros(models.Model):
    _name = 'centros'
    _description = 'Centro de Venta y Compra'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Habilitar chatter

    
    name = fields.Char(string='Nombre del Centro', required=True)
    location = fields.Char(string='Ubicación', required=False)
    sale_order_ids = fields.One2many('sale.order', 'centro_id', string='Órdenes de Venta')
    purchase_order_ids = fields.One2many('purchase.order', 'centro_id', string='Órdenes de Compra')
    company_id = fields.Many2one(comodel_name="res.company", default=lambda self: self.env.company.id, readonly=True, string="Compañía") 
    state = fields.Selection(
        [
            ('draft', 'Borrador'),
            ('active', 'Activo'),
            ('inactive', 'Inactivo')
        ],
        string='Estado',
        default='draft',
        required=True
    )
    # manager_id = fields.Many2one('res.users', string='Responsable')
    # employee_ids = fields.Many2many('hr.employee', string='Empleados Asignados')
    # stock_location_id = fields.Many2one('stock.location', string='Ubicación de Inventario')

    @api.depends('sale_order_ids', 'purchase_order_ids')
    def _compute_total_transactions(self):
        for record in self:
            record.total_transactions = len(record.sale_order_ids) + len(record.purchase_order_ids)

    total_transactions = fields.Integer(string='Transacciones Totales', compute='_compute_total_transactions', store=True)



    def action_draft(self):
        for record in self:
            record.state = 'draft'

    def action_active(self):
        for record in self:
            record.state = 'active'

    def action_inactive(self):
        for record in self:
            record.state = 'inactive'