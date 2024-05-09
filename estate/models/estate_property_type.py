from odoo import fields,models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    sequence = fields.Integer(string='Sequence', default=1, help="Used to order stages, Lower is better")
    name = fields.Char(string="Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offer")
    offer_count = fields.Integer(string="Offer Count", compute="_offer_count_handler")

    @api.depends("offer_ids")
    def _offer_count_handler(self):
        for record in self:
            record.offer_count=len(record.offer_ids)
        return True




    _sql_constraints = [('check_type_unique', 'unique(name)','The type has to be unique')]
