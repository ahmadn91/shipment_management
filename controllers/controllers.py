# -*- coding: utf-8 -*-
# from odoo import http


# class ShipmentManagement(http.Controller):
#     @http.route('/shipment_management/shipment_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/shipment_management/shipment_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('shipment_management.listing', {
#             'root': '/shipment_management/shipment_management',
#             'objects': http.request.env['shipment_management.shipment_management'].search([]),
#         })

#     @http.route('/shipment_management/shipment_management/objects/<model("shipment_management.shipment_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('shipment_management.object', {
#             'object': obj
#         })
