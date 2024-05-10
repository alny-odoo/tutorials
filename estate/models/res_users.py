from odoo import fields, models

class Res_Users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesperson_id", string="Property",  domain=[('state', 'in', ['new','offerReceived'])])