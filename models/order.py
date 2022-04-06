from email.policy import default
from odoo.exceptions import ValidationError
from odoo import api, fields, models


class Order(models.Model):
    _name = 'animerch.order'
    _description = 'New Description'

    orderactiondetail_ids = fields.One2many(
        comodel_name='animerch.orderactiondetail', 
        inverse_name='orderaction_id', 
        string='Action Figure')

    orderaccdetail_ids = fields.One2many(
        comodel_name='animerch.orderaccdetail', 
        inverse_name='orderacc_id', 
        string='Accessories')

    orderposterdetail_ids = fields.One2many(
        comodel_name='animerch.orderposterdetail', 
        inverse_name='orderposter_id', 
        string='Poster')
    
    name = fields.Char(string='Order ID', required=True)
    order_date = fields.Datetime(string='Order Date', default = fields.Datetime.now)
    delivery_date = fields.Date(string='Delivery Date', default = fields.Date.today())
    buyer = fields.Many2one(
        comodel_name='res.partner',
        string='Buyer',
        domain=[('the_customer', '=', True)], store = True)
    total = fields.Integer(compute='_compute_total', string='Total', store = True)
    
    @api.depends('orderactiondetail_ids', 'orderaccdetail_ids', 'orderposterdetail_ids')
    def _compute_total(self):
        for record in self:
            a = sum(self.env['animerch.orderactiondetail'].search([('orderaction_id', '=', record.id)]).mapped('price'))
            b = sum(self.env['animerch.orderaccdetail'].search([('orderacc_id', '=', record.id)]).mapped('price'))
            c = sum(self.env['animerch.orderposterdetail'].search([('orderposter_id', '=', record.id)]).mapped('price'))
            record.total = a + b + c  

    accounting = fields.Boolean(string='Already Paid', default=False)
    def invoice(self):
        invoices = self.env['account.move'].create({
            'move_type' : 'out_invoice',
            'partner_id' : self.buyer,
            'invoice_date' : self.order_date,
            'invoice_line_ids' : [(0, 0, {
                'product_id' : 0,
                'quantity' : 1,
                'price_unit' : self.total,
                'price_subtotal' : self.total,
            })]
        })
        self.accounting = True
        return invoices

class OrderActionDetail(models.Model):
    _name = 'animerch.orderactiondetail'
    _description = 'New Description'

    orderaction_id = fields.Many2one(comodel_name='animerch.order', string='Orders')
    action_id = fields.Many2one(
        comodel_name='animerch.actionfigure',
        string='Action Figure',
        domain=[('stock', '>', '0')])
    name = fields.Char(string='Name')
    unit_price = fields.Integer(compute='_compute_unit_price', string='Unit Price')
    
    @api.depends('action_id')
    def _compute_unit_price(self):
        for record in self:
            record.unit_price = record.action_id.price
    
    qty = fields.Integer(string='Quantity')
    
    @api.onchange('qty')
    def onchange_qty(self):
        for record in self:
            if record.qty > record.action_id.stock:
                raise ValidationError("Insufficient stock of action figure!")
    
    
    price = fields.Integer(compute='_compute_price', string='Price')
    
    @api.depends('unit_price', 'qty')
    def _compute_price(self):
        for record in self:
            record.price = record.unit_price * record.qty
    
    @api.model
    def create(self, vals):
        record = super(OrderActionDetail, self).create(vals)
        if record.qty:
            self.env['animerch.actionfigure'].search([('id', '=', record.action_id.id)]).write({'stock':record.action_id.stock-record.qty})
            return record


class OrderAccDetail(models.Model):
    _name = 'animerch.orderaccdetail'
    _description = 'New Description'

    orderacc_id = fields.Many2one(comodel_name='animerch.order', string='Orders')
    acc_id = fields.Many2one(
        comodel_name='animerch.accessories', 
        string='Accessories')
    name = fields.Char(string='Name')
    unit_price = fields.Integer(compute='_compute_unit_price', string='Unit Price')
    
    @api.depends('acc_id')
    def _compute_unit_price(self):
        for record in self:
            record.unit_price = record.acc_id.price
    
    qty = fields.Integer(string='Quantity')
    
    @api.onchange('qty')
    def onchange_qty(self):
        for record in self:
            if record.qty > record.acc_id.stock:
                raise ValidationError("Insufficient stock of accessories!")
    
    price = fields.Integer(compute='_compute_price', string='Price')
    
    @api.depends('qty', 'unit_price')
    def _compute_price(self):
        for record in self:
            record.price = record.unit_price * record.qty
    
    @api.model
    def create(self, vals):
        record = super(OrderAccDetail, self).create(vals)
        if record.qty:
            self.env['animerch.accessories'].search([('id', '=', record.acc_id.id)]).write({'stock':record.acc_id.stock-record.qty})
            return record

class OrderPosterDetail(models.Model):
    _name = 'animerch.orderposterdetail'
    _description = 'New Description'

    orderposter_id = fields.Many2one(comodel_name='animerch.order', string='Orders')
    poster_id = fields.Many2one(comodel_name='animerch.poster', string='Poster')
    name = fields.Char(string='Name')
    unit_price = fields.Integer(compute='_compute_unit_price', string='Unit Price')
    
    @api.depends('poster_id')
    def _compute_unit_price(self):
        for record in self:
            record.unit_price = record.poster_id.price
    qty = fields.Integer(string='Quantity')
    
    @api.onchange('qty')
    def onchange_qty(self):
        for record in self:
            if record.qty > record.poster_id.stock:
                raise ValidationError("Insufficient stock of posters!")

    price = fields.Integer(compute='_compute_price', string='Price')
    
    @api.depends('qty', 'unit_price')
    def _compute_price(self):
        for record in self:
            record.price = record.unit_price * record.qty
    
    @api.model
    def create(self, vals):
        record = super(OrderPosterDetail, self).create(vals)
        if record.qty:
            self.env['animerch.poster'].search([('id', '=', record.poster_id.id)]).write({'stock':record.poster_id.stock-record.qty})
            return record