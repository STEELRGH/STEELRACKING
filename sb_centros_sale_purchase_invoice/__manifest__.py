# -*- coding: utf-8 -*-
{
    'name': "sb_centros_sale_purchase_invoice",

    'summary': """
        Gestión de centros de venta y compra en Odoo""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Josué Flores Osorio [josueflores.05@gmail.com]",
    'website': "https://smart-business.co/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/Purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'views/centros.xml',
        'views/sale_order_view.xml',
        'views/purchase_order_view.xml',
        'views/account_move_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
