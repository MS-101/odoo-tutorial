from odoo import Command, models

class EstateProperty(models.Model):
    _inherit = "estate_property"

    def _create_invoice(self):
        invoice_vals = {
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'journal_id': 1,
            'invoice_line_ids': [
                Command.create({
                    'name': 'Sales fee',
                    'quantity': 1,
                    'price_unit': 0.06 * self.selling_price,
                }),
                Command.create({
                    'name': 'Administrative fees',
                    'quantity': 1,
                    'price_unit': 100000,
                })
            ],
        }

        return self.env['account.move'].create(invoice_vals)

    def action_sold(self):
        self._create_invoice()

        return super().action_sold()
