from odoo import api, fields, models, _
from datetime import timedelta
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    audit_log_ids = fields.One2many(
        'auditlog.log', 'sale_order_id', string="Bảng theo dõi")
    
    audit_log_line_ids = fields.One2many(
        comodel_name='auditlog.log.line',
        inverse_name='log_id',
        string='Log Lines',
        compute='_compute_log_lines',
        store=False  # Không cần lưu DB nếu chỉ hiển thị
    )

    @api.depends('audit_log_ids.line_ids')
    def _compute_log_lines(self):
        for rec in self:
            all_lines = rec.audit_log_ids.mapped('line_ids')
            rec.audit_log_line_ids = all_lines

    # product_uom_qty = fields.Float(
    #     string="Quantity",
    #     # compute='_compute_product_uom_qty',
    #     digits='Product Unit of Measure', default=0.0,
    #     store=True, readonly=False, required=True,
    #     # precompute=True
    # )
