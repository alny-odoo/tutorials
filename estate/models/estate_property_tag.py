from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description="Estate Property Tag"
    _order = "name"

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')
    _sql_constraints = [('check_tag_unique', 'unique(name)','The type has to be unique')]