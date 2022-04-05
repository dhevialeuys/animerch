from odoo import api, fields, models


class Accessories(models.Model):
    _name = 'animerch.accessories'
    _description = 'Assorted Anime Accessories'

    name = fields.Char(string='Name')
    material = fields.Selection(
        string='Material',
        selection=[('pvc', 'PVC'),
                    ('abs', 'ABS'),
                    ('metal', 'Metal'),
                    ('photo paper', 'Photo Paper'),
                    ('polyester fabric', 'Polyester Fabric'),
                    ('ivory', 'Ivory'),
                    ('cotton', 'Cotton'),
                    ('acrylic', 'Acrylic')])
    stock = fields.Integer(string='Stock')
    price = fields.Integer(string='Price')
    descript = fields.Char(string='Description')
    img = fields.Binary(string='Image')