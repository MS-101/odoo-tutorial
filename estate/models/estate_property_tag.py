from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate_property_tag'
    _description = 'Tags of real estate properties.'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Name of property tag must be unique!')
    ]
