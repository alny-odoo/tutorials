from odoo import models, fields, exceptions, Command
class EstateProperty(models.Model):
    _inherit="estate.property"

    def action_sold(self):
        super(EstateProperty,self).action_sold()
        for record in self:
            invoice_vals = {
                'partner_id': record.buyer_id.id,
                'move_type' : 'out_invoice',
                'line_ids' : [
                    Command.create(
                        {
                            'name': record.name,
                            'quantity': 1,
                            'price_unit': 0.06*record.selling_price
                        }
                    ),
                    Command.create(
                        {
                            'name': 'Administrative Fees',
                            'quantity': 1,
                            'price_unit': 100
                        }
                    )
                ]
            }

            self.env["account.move"].create(invoice_vals)