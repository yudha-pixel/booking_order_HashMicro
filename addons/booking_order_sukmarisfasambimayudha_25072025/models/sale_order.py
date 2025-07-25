from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, Warning

class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_booking_order = fields.Boolean("Is Booking Order")
    service_team_id = fields.Many2one('service.team', 'Team')
    service_team_leader_id = fields.Many2one('res.users', "Team Leader")
    service_team_members_ids = fields.Many2many('res.users', 'res_user_sale_order_rel', 'user_id',
                                                'sale_order_id', string="Team Members")
    booking_start = fields.Datetime(string='Booking Start')
    booking_end = fields.Datetime(string='Booking End')
    work_order_id = fields.Many2one('work.order', string='Work Order')

    @api.onchange('service_team_id')
    def onchange_team_id(self):
        if self.service_team_id:
            self.service_team_leader_id = self.service_team_id.team_leader_id.id
            self.service_team_members_ids = [(6,0,[user.id for user in self.service_team_id.team_members_ids])]

    def _check_availability(self):
        self.ensure_one()
        domain = [
            ('team_id', '=', self.team_id.id),
            ('state', 'not in', ['cancel', 'done']),
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
            raise Warning(_('Team is available for booking'))

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

                work_order = self.env['work.order'].create({
                    'state': 'pending',
                    'planned_start': order.booking_start,
                    'planned_end': order.booking_end,
                    'team_id': order.team_id.id,
                    'team_leader_id': order.service_team_leader_id.id,
                    'team_members_ids': [(6, 0, order.service_team_members_ids.ids)],
                    'booking_order_reference_id': order.id,
                })
                order.write({'work_order_id': work_order.id})
                return res
        return super(SaleOrder, self).action_confirm()

    @api.multi
    def action_view_work_order(self):
        """ Open the work order form view """
        self.ensure_one()
        return {
            'name': _('Work Order'),
            'type': 'ir.actions.act_window',
            'res_model': 'work.order',
            'view_mode': 'form',
            'res_id': self.work_order_id.id,
            'target': 'current',
        }

    