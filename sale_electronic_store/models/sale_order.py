from odoo import api, fields, models, _
from datetime import timedelta
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # product_uom_qty = fields.Float(
    #     string="Quantity",
    #     # compute='_compute_product_uom_qty',
    #     digits='Product Unit of Measure', default=0.0,
    #     store=True, readonly=False, required=True,
    #     # precompute=True
    # )

    quantity = fields.Float(string="QUantity")