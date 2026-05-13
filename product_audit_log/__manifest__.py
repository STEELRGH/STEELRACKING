{
    'name': 'Bitácora de Cambios Contables en Productos',
    'version': '1.0',
    'summary': 'Rastreo de cambios en campos contables y UNSPSC',
    'category': 'Inventory',
    'author': 'Gerardo',
    'depends': ['product', 'account', 'product_unspsc'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}