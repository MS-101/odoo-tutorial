from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = 'estate_property_type'
    _description = 'Types of real estate properties.'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1)
    property_ids = fields.One2many('estate_property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate_property_offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(computed='_compute_offer_count')

    @api.depends('offer_ids.price')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Name of property type must be unique!')
    ]

    # Add the field offer_count to estate.property.type. It is a computed field that counts the number of offers for a given property type (use offer_ids to do so).