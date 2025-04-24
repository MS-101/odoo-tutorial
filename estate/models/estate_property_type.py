from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate_property_type'
    _description = 'Types of real estate properties.'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1)
    property_ids = fields.One2many('estate_property', 'property_type_id', string='Properties')

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Name of property type must be unique!')
    ]