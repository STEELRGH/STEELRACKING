# -*- coding: utf-8 -*-
# from odoo import http


# class SbCustomReportsMovill(http.Controller):
#     @http.route('/sb_custom_reports/sb_custom_reports', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sb_custom_reports/sb_custom_reports/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sb_custom_reports.listing', {
#             'root': '/sb_custom_reports/sb_custom_reports',
#             'objects': http.request.env['sb_custom_reports.sb_custom_reports'].search([]),
#         })

#     @http.route('/sb_custom_reports/sb_custom_reports/objects/<model("sb_custom_reports.sb_custom_reports"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sb_custom_reports.object', {
#             'object': obj
#         })

