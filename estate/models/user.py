from odoo import fields, models

class User(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate_property", "user_id", string="Properties",
        domain="['|', ('state', '=', 'new'), ('state', '=', 'offer_received')]")
