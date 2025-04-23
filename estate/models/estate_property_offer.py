from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate_property_offer'
    _description = 'Buyer bids for our real estate properties.'

    price = fields.Float()
    status = fields.Selection(copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ]
    )
    partner_id = fields.Many2one('res.partner', string='partner', required=True)
    property_id = fields.Many2one('estate_property', string='Property', required=True)
