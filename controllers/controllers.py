# -*- coding: utf-8 -*-
# from odoo import http


# class Animerch(http.Controller):
#     @http.route('/animerch/animerch/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/animerch/animerch/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('animerch.listing', {
#             'root': '/animerch/animerch',
#             'objects': http.request.env['animerch.animerch'].search([]),
#         })

#     @http.route('/animerch/animerch/objects/<model("animerch.animerch"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('animerch.object', {
#             'object': obj
#         })
