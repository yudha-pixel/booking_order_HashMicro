from odoo import models, fields, api, _

class WorkOrder(models.Model):
    _name = 'work.order'
    _description = 'Work Order'

    name = fields.Char(string='WO Number', readonly=True, index=True, default=lambda self: 'New')
    booking_order_reference_id = fields.Many2one('sale.order', string='Booking Order Reference', readonly=True)
    team_id = fields.Many2one('service.team',string='Team', required=True)
    team_leader_id = fields.Many2one('res.users', string="Team Leader", required=True)
    team_members_ids = fields.Many2many('res.users', 'res_user_work_order_rel', 'user_id',
                                        'work_order_id', string="Team Members")
    planned_start = fields.Datetime(string='Planned Start', required=True)
    planned_end = fields.Datetime(string='Planned End', required=True)
    date_start = fields.Datetime(string='Date Start', readonly=True)
    date_end = fields.Datetime(string='Date End', readonly=True)
    state = fields.Selection([
        ('pending', 'Pending'), ('in_progress', 'In Progress'), ('done', 'Done'), ('cancel', 'Cancelled')],
        string='Status', default='pending')
    notes = fields.Text(string='Notes')
    
    @api.model
    def create(self, vals):
        if not vals.get('wo_number', False):
            vals['wo_number'] = self.env['ir.sequence'].next_by_code('work.order') or 'New'
        result = super(WorkOrder, self).create(vals)
        return result
    
    
    @api.multi
    def action_end_work(self):
        self.state = 'done'
        self.date_end = fields.Datetime.now()
        
    @api.multi
    def action_reset(self):
        self.state = 'pending'
        self.date_start = False
        
        
    
    @api.multi
    def action_start_work(self):
        self.state = 'in_progress'
        self.date_start = fields.Datetime.now()
    
        
    @api.multi
    def action_cancel(self):
        context = self._context.get('active_id')
        return {
            'name': _('Cancellation'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'cancel.work.order',
            'context': context,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': False,
        }
        
            
    