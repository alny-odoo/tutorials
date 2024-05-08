from odoo import fields,models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    
    name = fields.Char(string="name", required=True)

    _sql_constraints = [('check_type_unique', 'unique(name)','The type has to be unique')]
