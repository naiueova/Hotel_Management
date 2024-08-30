from odoo import models, fields, api

class HotelRoomAmenities(models.Model):
    _name = 'hotel.room.amenities'
    _description = 'Room Amenities'

    room_id = fields.Many2one('hotel.configuration.room', string="Room", required=True, ondelete='cascade')
    amenity_id = fields.Many2one('hotel.configuration.amenity', string="Amenity", required=True)
    name = fields.Char(string="Amenity Name", related="amenity_id.name", readonly=True)
    quantity = fields.Integer(string="Quantity", default=1, required=True)
    price = fields.Float(string="Price", required=True)
    sub_total = fields.Float(string="Sub Total", compute='_compute_sub_total', store=True)

    @api.depends('quantity', 'price')
    def _compute_sub_total(self):
        for record in self:
            record.sub_total = record.quantity * record.price

    @api.onchange('amenity_id')
    def _onchange_amenity_id(self):
        """ Update the price based on the selected amenity """
        if self.amenity_id:
            self.price = self.amenity_id.product_id.list_price  # Fetch the sales price from the related product

    @api.onchange('price')
    def _onchange_price(self):
        """ Sync the price with the product's sales price """
        if self.amenity_id and self.price:
            self.amenity_id.product_id.list_price = self.price  