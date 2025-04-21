from odoo import api, fields, models, _
from datetime import timedelta
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    quantity = fields.Integer(string="Available", default = 0)
