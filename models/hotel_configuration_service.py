from odoo import fields, models, api

class HotelService(models.Model):
    _name = 'hotel.configuration.service'
    _description = 'Hotel Service'

    name = fields.Char(string='Service Name', required=True)
    price = fields.Float(string='Price', required=True)