from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate_property_tag'
    _description = 'Tags of real estate properties.'

    name = fields.Char(required=True)
