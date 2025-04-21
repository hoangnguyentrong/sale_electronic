{
    'name': 'Electronic Store Sale User',
    'version': '17.0.1.0',
    'license': 'LGPL-3',
    'category': 'Sale',
    "sequence": 3,
    'summary': 'Electronic Store Sale User',
    'complexity': "easy",
    'author': 'Hoang Group',
    'depends': ['base', 'sale', 'sale_management', 'product'],
    'data': [
        # "views/sale_order_views.xml",
        # "views/menu_sale.xml",
        "views/res_users_view.xml",
        "views/menu.xml"
    ],
    'demo': [],
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
