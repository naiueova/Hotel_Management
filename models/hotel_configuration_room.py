from odoo import fields, models, api

class HotelRoom(models.Model):
    _name = 'hotel.configuration.room'
    _description = 'Hotel Room'

    name = fields.Char(string="Name", help="Name of the Room", required=True)
    status = fields.Selection([
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied')
    ], string="Status", default='available', required=True)
    is_room_avail = fields.Boolean(default=True, string="Status", help="Check if the room is available")
    list_price = fields.Float(string="Rent", digits="Product Price", required=True)
    room_image = fields.Image(string="Room Image", max_width=1920, max_height=1920)
    floor_id = fields.Many2one('hotel.configuration.floor', string="Floor", required=True)
    user_id = fields.Many2one('res.partner', string="Room Manager", required=True)
    room_type = fields.Selection([
        ('single', 'Single'),
        ('double', 'Double'),
        ('dormitory', 'Dormitory')
    ], string="Room Type", default='single', required=True)
    num_person = fields.Integer(string="Number of Persons", required=True)
    description = fields.Html(string="Description")
    room_amenities_ids = fields.One2many('hotel.room.amenities', 'room_id', string="Room Amenities")
    cost = fields.Float(string="Cost", compute='_compute_cost', store=True)

    @api.depends('room_amenities_ids.sub_total')
    def _compute_cost(self):
        for record in self:
            record.cost = sum(record.room_amenities_ids.mapped('sub_total'))