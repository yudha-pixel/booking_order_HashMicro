from odoo import models, fields, api, _

class CancelWorkOrder(models.TransientModel):
    _name = "cancel.work.order"
    _description = "Cancel the work order"
    
    notes = fields.Text(string='Reason of Cancellation', required=True)
    
    @api.multi
    def process_cancel(self):
        for rec in self:
            wo_id = self.env['work.order'].browse(self._context.get('active_id'))
            if rec.notes:
                if wo_id:
                    wo_id.write({'notes': rec.notes, 'state': 'cancel'})
        return True
                
            