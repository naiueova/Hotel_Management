from odoo import fields, models, api

class HotelFloor(models.Model):
    _name = 'hotel.configuration.floor'
    _description = 'Hotel Floor'

    name = fields.Char(string='Floor Name', required=True)
    manager_id = fields.Many2one('res.partner', string='Manager', required=True)