# -*- coding: utf-8 -*-
# from odoo import http


# class SbCentrosSalePurchaseInvoice(http.Controller):
#     @http.route('/sb_centros_sale_purchase_invoice/sb_centros_sale_purchase_invoice', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sb_centros_sale_purchase_invoice/sb_centros_sale_purchase_invoice/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sb_centros_sale_purchase_invoice.listing', {
#             'root': '/sb_centros_sale_purchase_invoice/sb_centros_sale_purchase_invoice',
#             'objects': http.request.env['sb_centros_sale_purchase_invoice.sb_centros_sale_purchase_invoice'].search([]),
#         })

#     @http.route('/sb_centros_sale_purchase_invoice/sb_centros_sale_purchase_invoice/objects/<model("sb_centros_sale_purchase_invoice.sb_centros_sale_purchase_invoice"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sb_centros_sale_purchase_invoice.object', {
#             'object': obj
#         })
