from datetime import timedelta
from odoo import api, fields, models

class EstateProperty(models.Model):
    _name = 'estate_property'
    _description = 'Real estate properties to be sold.'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()
    property_type_id = fields.Many2one("estate_property_type", string="Property Type")
    property_tag_ids = fields.Many2many("estate_property_tag", string="Tags")
    postcode = fields.Char()
    date_availability = fields.Date(string='Available From',
        copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )
    total_area = fields.Float(compute='_compute_total_area')
    state = fields.Selection(
        required=True,
        copy=False,
        default='new',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ]
    )
    user_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    offer_ids = fields.One2many('estate_property_offer', 'property_id', string='Offers')
    best_price = fields.Float(string='Best Offer', compute='_compute_best_price')
    active = fields.Boolean(default=True)

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = 0
            for offer_id in self.offer_ids:
                record.best_price = max(record.best_price, offer_id.price)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None