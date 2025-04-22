from odoo import api, fields, models, _
from datetime import timedelta
from odoo.exceptions import ValidationError, UserError


class MasterLocation(models.Model):
    _name = 'master.location'
    _description = "Master Location"
    _rec_name = 'location_name_id'

    location_name_id = fields.Char(store=True, string="Location Name")
    city_id = fields.Many2one('master.city', string="City")
    district_id = fields.Many2one('master.district', string="District")
    ward_id = fields.Many2one('master.ward', string="Ward")
    street = fields.Char(string="Street")
    code = fields.Char(string="Code")


class MasterCity(models.Model):
    _name = 'master.city'
    _description = "Master City"

    code = fields.Char(string='Code', size=4, required=True)
    name = fields.Char(string='Name', size=100, required=True)
    district_ids = fields.One2many(
        'master.district', 'city_id', string="District")


class MasterDistrict(models.Model):
    _name = 'master.district'
    _description = "Master District"

    code = fields.Char(string='Code', size=11, required=True)
    name = fields.Char(string='Name', size=128, required=True)
    city_id = fields.Many2one('master.city', string="City")
    # ward_ids = fields.One2many('master.ward', 'district_id', string="Ward")


class MasterWard(models.Model):
    _name = 'master.ward'
    _description = "Master Ward"

    code = fields.Char(string='Code', size=11, required=True)
    name = fields.Char(string='Name', size=128, required=True)
    district_id = fields.Many2one('master.district', string="District")
    city_id = fields.Many2one('master.city', string="City",
                              ondelete='resctrict', related="district_id.city_id")
