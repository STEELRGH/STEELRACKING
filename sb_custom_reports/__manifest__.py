# -*- coding: utf-8 -*-
{
    'name': "sb_custom_reports",

    'summary': "Personalización del formato reporte de factura, ventas, complemento de pago, nota de credito",

    'description': """
Long description of module's purpose
    """,

    'author': "Josué Flores Osorio [josueflores.05@gmail.com]",
    'website': "https://smart-business.co/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'l10n_mx_edi', 'sale_management', 'sb_centros_sale_purchase_invoice'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'reports/action_report.xml',
        # 'reports/report_invoice_document.xml',
        'reports/external_layout_striped_inherit.xml',
        'reports/document_tax_totals_template_extend.xml',
        'reports/tax_groups_totals_extend.xml',
        'reports/report_invoice_document_inherit.xml',
        'reports/report_payment_receipt_document_inherit.xml',
        'reports/report_saleorder_document_inherit.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'sb_custom_reports/static/src/scss/**/*',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

