# -*- coding: utf-8 -*-
from odoo import http

# class Centro(http.Controller):
#     @http.route('/centro/centro/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/centro/centro/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('centro.listing', {
#             'root': '/centro/centro',
#             'objects': http.request.env['centro.centro'].search([]),
#         })

#     @http.route('/centro/centro/objects/<model("centro.centro"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('centro.object', {
#             'object': obj
#         })