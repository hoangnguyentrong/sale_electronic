from odoo import api, fields, models, _
from datetime import timedelta
from odoo.exceptions import ValidationError, UserError


class AuditlogLog(models.Model):
    _inherit = 'auditlog.log'
    _description = 'AuditLog Inherit'

    sale_order_id = fields.Many2one('sale.order', string="Đơn đặt hàng")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("model_id"):
                raise UserError(_("No model defined to create log."))

            model = self.env["ir.model"].sudo().browse(vals["model_id"])
            vals.update({
                "model_name": model.name,
                "model_model": model.model,
            })

            # Nếu là model vehicle.contract thì gán vehicle_contract_id
            if model.model == 'sale.order':
                vals["sale_order_id"] = vals.get("res_id")

        return super().create(vals_list)
