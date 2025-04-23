from datetime import timedelta
from odoo import api, fields, models

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
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate_property', string='Property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7, inverse='_inverse_validity')
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    def _inverse_validity(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(days=record.validity)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            difference = record.date_deadline - record.create_date.date()
            record.validity = difference.days