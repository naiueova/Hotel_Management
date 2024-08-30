from odoo import fields, models, api

class HotelAmenity(models.Model):
    _name = "hotel.configuration.amenity"
    _description = "Hotel Amenity"

    name = fields.Char(string="Amenity Name", required=True)
    image = fields.Binary(string="Image")
    product_id = fields.Many2one('product.template', string="Linked Product", readonly=True)
    
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Amenity name must be unique!'),
    ]

    @api.model
    def create(self, vals):
        amenity = super(HotelAmenity, self).create(vals)

        product_vals = {
            'name': amenity.name,
            'type': 'product',  
            'image_1920': amenity.image,  
            'amenity_id': amenity.id,  
        }
        product = self.env['product.template'].create(product_vals)

        amenity.product_id = product.id

        return amenity