from odoo import models, fields, api, _

class HotelReservation(models.Model):
    _name = 'hotel.reservation'
    _description = 'Hotel Reservation'

    name = fields.Char(string="Booking Reference", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    customer_id = fields.Many2one('res.partner', string="Customer", required=True)
    invoice_address_id = fields.Many2one('res.partner', string="Invoice Address", compute="_compute_invoice_address", store=True)
    order_date = fields.Datetime(string="Order Date", default=fields.Datetime.now, required=True)

    room_detail_ids = fields.One2many('hotel.reservation.room.detail', 'reservation_id', string="Room Details")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('checkin', 'Check In'),
        ('checkout', 'Check Out'),
        ('cancelled', 'Cancelled') 
    ], string="Status", default='draft', track_visibility='onchange')

    total = fields.Float(string="Total", compute="_compute_total", store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.user.company_id.currency_id)

    @api.depends('room_detail_ids')
    def _compute_total(self):
        for record in self:
            total_rent = sum(detail.sub_total for detail in record.room_detail_ids)
            record.total = total_rent

    @api.depends('customer_id')
    def _compute_invoice_address(self):
        for record in self:
            record.invoice_address_id = record.customer_id

    def action_confirm(self):
        self.write({'state': 'confirmed'})
        self._update_room_status('reserved')

    def action_checkin(self):
        for detail in self.room_detail_ids:
            if not detail.checkin_date:
                detail.checkin_date = fields.Datetime.now()
            detail._compute_duration()
        self.write({'state': 'checkin'})
        self._update_room_status('occupied')

    def action_checkout(self):
        for detail in self.room_detail_ids:
            if not detail.checkout_date:
                detail.checkout_date = fields.Datetime.now()
            detail._compute_duration()
        self.write({'state': 'checkout'})
        self._update_room_status('available')

    def action_cancel(self):
        self.write({'state': 'cancelled'})
        self._update_room_status('available')

    def _update_room_status(self, status):
        for detail in self.room_detail_ids:
            detail.room_id.status = status

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hotel.reservation') or _('New')
        return super(HotelReservation, self).create(vals)
           
class HotelReservationRoomDetail(models.Model):
    _name = 'hotel.reservation.room.detail'
    _description = 'Hotel Reservation Room Detail'

    reservation_id = fields.Many2one('hotel.reservation', string="Reservation", required=True, ondelete='cascade')
    room_id = fields.Many2one('hotel.configuration.room', string="Room", required=True)
    checkin_date = fields.Datetime(string="Check In")
    checkout_date = fields.Datetime(string="Check Out")
    duration = fields.Float(string="Duration", default=1, compute="_compute_duration", store=True)
    unit_of_measure = fields.Many2one('uom.uom', string="Unit of Measure", default=lambda self: self.env.ref('uom.product_uom_day'))
    rent = fields.Float(string="Rent", related="room_id.list_price", readonly=False)
    sub_total = fields.Float(string="Sub Total", compute="_compute_sub_total", store=True)

    @api.depends('checkin_date', 'checkout_date')
    def _compute_duration(self):
        for record in self:
            if record.checkin_date and record.checkout_date:
                record.duration = (record.checkout_date - record.checkin_date).days or 1
            else:
                record.duration = 1

    @api.depends('duration', 'rent')
    def _compute_sub_total(self):
        for record in self:
            record.sub_total = record.duration * record.rent
