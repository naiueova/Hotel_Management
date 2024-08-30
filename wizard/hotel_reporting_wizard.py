from odoo import models, fields, api

class RoomBookingReportWizard(models.TransientModel):
    _name = 'hotel.reporting.wizard'
    _description = 'Room Booking Report Wizard'

    checkin_date = fields.Date('Check-in', required=True)
    checkout_date = fields.Date('Check-out', required=True)
    room_id = fields.Many2one('hotel.configuration.room', string='Room')

    def action_print_report(self):
        domain = [
            ('room_detail_ids.checkin_date', '>=', self.checkin_date),
            ('room_detail_ids.room_id', '=', self.room_id.id),
        ]
        
        if self.checkout_date:
            domain.append('|')
            domain.append(('room_detail_ids.checkout_date', '<=', self.checkout_date))
            domain.append(('room_detail_ids.checkout_date', '=', False))
        
        reservations = self.env['hotel.reservation'].search(domain)
        
        return self.env.ref('hotel_management.action_hotel_reporting').report_action(reservations)
