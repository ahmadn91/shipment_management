# -*- coding: utf-8 -*-
{
    'name': "Shipment",

    'summary': """Shipment Management""",

    'description': """For Managing Shipment & Transfares""",

    'author': "INTEGRATED PATH",
    'website': "https://www.int-path.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Delivery',
    'version': '1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base','product','purchase'],

    # always loaded
    'data': [
        'security/shipment_user_group.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/shipment_shipment_view.xml'
    ],
}
