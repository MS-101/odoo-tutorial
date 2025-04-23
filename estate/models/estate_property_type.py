from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate_property_type'
    _description = 'Types of real estate properties.'

    name = fields.Char(required=True)
