from odoo import fields, models, api, exceptions  
class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    

    price = fields.Float(string="Price")
    state = fields.Selection(string="Status", selection=[("accepted", "Accepted"),("refused","Refused")], copy=False, readonly=True)

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Datetime(string="Deadline", compute="_compute_deadline_date", inverse="_inverse_deadline_date")

    property_type_id = fields.Many2one('estate.property.type', related="property_id.property_type_id", name="Type", store=True)

    @api.model_create_multi
    def create(self, vals):
        for value in vals:
            if value["price"] <= self.env["estate.property"].browse(value["property_id"]).best_price:
                raise exceptions.UserError("A higher offer already exists") 
            self.env["estate.property"].browse(value["property_id"]).state = "offerReceived"
        return super().create(vals)


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

    def action_accept(self):
        for record in self:
            if not record.property_id.has_offer:
                record.state = "accepted"
                record.property_id.state = "offerAccepted"
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                record.property_id.has_offer = True
            else:
                raise exceptions.UserError("There is an offer accepted already")
        return True
        
    def action_refuse(self):
        for record in self:
            if record.state == "accepted":
                record.state = "refused"
                record.property_id.has_offer = False
                record.property_id.buyer_id = None
                record.property_id.selling_price = None
            else:
                record.state = "refused"
        return True

    _sql_constraints = [('check_price_gte0', 'CHECK(price >= 0)','The price has to be greater than 0')]