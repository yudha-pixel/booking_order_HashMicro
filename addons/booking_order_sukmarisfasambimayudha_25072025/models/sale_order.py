from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _is_wo(self):
        wo_obj = self.env['work.order']

        for i in self:
            domain = [('booking_order_reference_id', '=', i.id)]
        return False
    
    is_booking_order = fields.Boolean("Is Booking Order")
    service_team_id = fields.Many2one('service.team', 'Team')
    service_team_leader_id = fields.Many2one('res.users', "Team Leader")
    service_team_members_ids = fields.Many2many('res.users', 'res_user_sale_order_rel', 'user_id',
                                        'sale_order_id', string="Team Members")
    booking_start = fields.Datetime(string='Booking Start')
    booking_end = fields.Datetime(string='Booking End')
    is_work_order = fields.Boolean("Is Work Order", compute=_is_wo)

    @api.onchange('team_id')
    def onchange_team_id(self):
        if self.team_id:
            self.team_leader_id = self.service_team_id.team_leader_id.id
            self.team_members_ids = [(6,0,[user.id for user in self.service_team_id.team_members_ids])]

    def _check_availability(self):
        self.ensure_one()
        domain = [
            ('team_id', '=', self.team_id.id),
            ('state', '!=', 'cancelled'),
            ('planned_start', '<=', self.booking_end),
            ('planned_end', '>=', self.booking_start),
        ]
        overlapping_wo = self.env['work.order'].search(domain, limit=1)
        return overlapping_wo

    @api.multi
    def action_check_availability(self):
        overlapping_wo = self._check_availability()
        if overlapping_wo:
            message = (_("Team already has work order during that period on %s") %
                       overlapping_wo.booking_order_reference_id.name)
            raise ValidationError(message)
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Availability Check'),
                    'message': 'Team is available for booking',
                    'sticky': False,
                }
            }

    @api.multi
    def action_confirm(self):
        for order in self:
            if order.is_booking_order:
                overlapping_wo = order._check_availability()
                if overlapping_wo:
                    message = _(
                        "Team is not available during this period, already booked on %s. Please book on another date.") % (
                                  overlapping_wo.booking_order_reference_id.name)
                    raise ValidationError(message)

                res = super(SaleOrder, self).action_confirm()

                self.env['work.order'].create({
                    'state': 'pending',
                    'date_start': order.booking_start,
                    'date_end': order.booking_end,
                    'team_id': order.team_id.id,
                    'team_leader_id': order.service_team_leader_id.id,
                    'team_members_ids': [(6, 0, order.service_team_members_ids.ids)],
                    'booking_order_reference_id': order.id,
                })
                return res
        return super(SaleOrder, self).action_confirm()

    @api.multi
    def action_view_work_order(self):
        wo_ids = self.env['work.order'].search([('sale_order_id', '=', self.id)])
        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object('booking_order_muhardiansyah_300822.action_view_work_order')
        list_view_id = imd.xmlid_to_res_id('booking_order_muhardiansyah_300822.work_order_tree')
        form_view_id = imd.xmlid_to_res_id('booking_order_muhardiansyah_300822.work_order_form')

        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [(form_view_id, 'form')],
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
            'res_id' : wo_ids[0].id,
            'view_type' : 'form',
            'view_mode' : 'form',
            'view_id' : form_view_id,
        }
        
        return result
        
    