from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description="Estate Property Tag"

    name = fields.Char(string='name', required=True)

    _sql_constraints = [('check_tag_unique', 'unique(name)','The type has to be unique')]