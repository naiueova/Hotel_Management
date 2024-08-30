from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    amenity_id = fields.Many2one('hotel.configuration.amenity', string="Hotel Amenity", readonly=True)