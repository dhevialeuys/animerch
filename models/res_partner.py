from email.policy import default
from odoo import api, fields, models


class Partner(models.Model):
    _name_ = 'animerch.partner'
    _inherit = 'res.partner'
    
    the_customer = fields.Boolean(string='Customer', default = False)
