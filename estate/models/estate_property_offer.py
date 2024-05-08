from odoo import fields, models, api    
class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", selection=[("accepted", "Accepted"),("refused","Refused")], copy=False)

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Datetime(string="Deadline", compute="_compute_deadline_date", inverse="_inverse_deadline_date")
    @api.depends("validity", "create_date")
    def _compute_deadline_date(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Datetime.add(record.create_date,days=record.validity)
            else:
                record.date_deadline = fields.Datetime.add(fields.Datetime.now(), days=record.validity)
    def _inverse_deadline_date(self):
        for record in self:
            if record.create_date:
                record.validity = record.date_deadline.day - record.create_date.day