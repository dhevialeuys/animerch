from odoo import api, fields, models


class ActionFigure(models.Model):
    _name = 'animerch.actionfigure'
    _description = 'Berbagai Macam Action Figure Anime'

    name = fields.Char(string='Name')
    material = fields.Selection(string='Material', selection=[('pvc', 'PVC'), ('abs', 'ABS')])
    features = fields.Char(string='Features')
    size = fields.Integer(string='Total Height (cm)')
    stock = fields.Integer(string='Stock')
    price = fields.Integer(string='Price')
    descript = fields.Char(string='Description')
    img = fields.Binary(string='Image')
