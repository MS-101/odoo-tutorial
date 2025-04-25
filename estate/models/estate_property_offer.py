from datetime import timedelta
from odoo import api, exceptions, fields, models

class EstatePropertyOffer(models.Model):
    _name = 'estate_property_offer'
    _description = 'Buyer bids for our real estate properties.'
    _order = 'price desc'

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
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

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
            if record.create_date and record.date_deadline:
                difference = record.date_deadline - record.create_date.date()
                record.validity = difference.days

    def action_accept(self):
        for record in self:
            property = record.property_id

            for offer_id in property.offer_ids:
                if offer_id.status == 'accepted':
                    raise exceptions.UserError('Cannot accept two different offers!')

            property.selling_price = record.price
            property.partner_id = record.partner_id
            property.state = 'offer_accepted'
            record.status = 'accepted'

        return True
    
    def action_refuse(self):
        for record in self:
            record.status = 'refused'

        return True
    
    @api.model
    def create(self, vals):
        property_id = self.env['estate_property'].browse(vals['property_id'])
        
        if property_id.best_price > vals['price']:
            raise exceptions.UserError('Cannot create offer with lower than best price!')
        property_id.state = 'offer_received'

        return super().create(vals)