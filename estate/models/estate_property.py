# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, exceptions, tools

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "property_type_id, id desc"
    


    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Date Availability', copy=False, default=fields.Datetime.add(fields.Datetime.today(), months = 3))
    expected_price = fields.Float(string='Expected Price', required= True)
    selling_price = fields.Float(string='Selling Price', copy=False, readonly=True)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(selection=[('north', 'North'),('east','East'),('south','South'),('west','West')],string='Garden Orientation')
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(readonly=True, selection=[('new', 'New'),('offerReceived', 'Offer Received'), ('offerAccepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')], default='new', copy=False, string='Status')

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer","property_id" ,string="Offers")

    total_area = fields.Integer(compute="_compute_area", readonly=True, string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_offer", readonly=True, string="Best Offer")

    has_offer = fields.Boolean(string="Offer Accepted", readonly=True)
    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            prices = record.mapped('offer_ids.price')
            if prices:
                record.best_price = max(prices)
            else:
                record.best_price = None

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden is False:
            self.garden_orientation = None
            self.garden_area = 0
        else:
            self.garden_orientation = 'north'
            self.garden_area = 10

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise exceptions.UserError("Canceled properties cannot be sold")
            else:
                record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            record.state = "canceled"
        return True 
        
    # def button_visibility_handler(self):
    #     for record in self:
    #         if record.state in ("canceled", "sold"):
    #             return True
    #         return False

    _sql_constraints = [('check_excpected_price_gte0', 'CHECK(expected_price >= 0)','The expected price has to be greater than 0'),
    ('check_selling_price_gte0', 'CHECK(selling_price >= 0)','The selling price has to be greater than 0')]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if tools.float_compare(record.selling_price, 0.9*record.expected_price, 3) < 0 and not tools.float_is_zero(record.selling_price, 3):
                raise exceptions.ValidationError("The selling price is lower than 90%% of the expected price")