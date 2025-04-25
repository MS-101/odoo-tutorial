from datetime import timedelta
from odoo import api, exceptions, fields, models, tools

class EstateProperty(models.Model):
    _name = 'estate_property'
    _description = 'Real estate properties to be sold.'
    _order = 'id desc'

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

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be positive!'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'Selling price must be positive!')
    ]

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

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError('Cancelled properties cannot be sold!')
            record.state = 'sold'

        return True
    
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError('Sold properties cannot be cancelled!')
            record.state = 'cancelled'

        return True

    @api.constrains('expected_price')
    def _check_expected_price(self):
        self.selling_price_constraint()

    @api.constrains('selling_price')
    def _check_selling_price(self):
        self.selling_price_constraint()

    def selling_price_constraint(self):
        precision_digits = 2

        for record in self:    
            if (
                not(tools.float_is_zero(record.selling_price, precision_digits=precision_digits))
                and tools.float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=precision_digits) in (-1, 0)
            ):
                raise exceptions.ValidationError('Selling price must be atleast 90 %% of the expected price!')

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise exceptions.UserError('Cannot sell property that is not new or cancelled!')
