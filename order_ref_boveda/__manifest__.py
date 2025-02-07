# -*- encoding: utf-8 -*-
{
    "name": 'SO/PO Boveda Fiscal',
    'license': 'GPL-3',
    "version": '17.1',
    "author": 'DuvanDevs',
    "category": '',
    "website": "",
    "description": """Permite seleccionar y asociar una venta/compra en los CFDI descargados""",
    "depends": ['base', 'cfdi_boveda_fiscal','sale','purchase'],
    "data": [
        'security/ir.model.access.csv',
        'views/cfdi_download_data_view.xml',
        'views/orders_reference_view.xml',
    ],
    "installable": True,
    "auto_install": False,
}
