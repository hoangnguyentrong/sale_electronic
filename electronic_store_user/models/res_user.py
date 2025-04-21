# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime,timedelta, date


class Users(models.Model):
    _inherit = 'res.users'

    # name = fields.Char(related='partner_id.name', inherited=True, readonly=False, store=True)
    # street = fields.Char()
    # phone = fields.Char()
    # email = fields.Char()
    # id_card = fields.Char('ID Card Number')