{
    'name': "OWL Dashboard",

    'summary': "OWL Tutorial Custom Dashboard",


    'author': "Hoang",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'OWL',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base_setup','web','sale','board'],
    'data': [
        'views/sales_dashboard.xml',
        'views/sales_dashboard_menu.xml',
    ],
    'sequence': -1,
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            "dashboard/static/src/**/*",

        ],
    },
}