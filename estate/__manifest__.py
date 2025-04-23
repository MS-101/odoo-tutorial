{
    'name': 'estate',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
        'security/ir.model.access.csv',
    ],
    'author': 'Martin Šváb',
    'description': 'Demo project for learning how to work in odoo framework.',
    'application': True
}