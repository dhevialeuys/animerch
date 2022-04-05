from odoo import api, fields, models


class Poster(models.Model):
    _name = 'animerch.poster'
    _description = 'Many Poster You Can Get Here'

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
    size = fields.Char(string='Size')
    stock = fields.Integer(string='Stock')
    price = fields.Integer(string='Price')
    descript = fields.Char(string='Description')
    img = fields.Binary(string='Image')