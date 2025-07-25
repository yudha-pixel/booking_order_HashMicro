from odoo import models, fields

class ServiceTeam(models.Model):
    _name = 'service.team'
    _description = 'Service Team'

    name = fields.Char('Team Name', required=True)
    team_leader_id = fields.Many2one('res.users', 'Team Leader', required=True)
    team_members_ids = fields.Many2many('res.users', 'res_user_service_team_rel',
                                        'user_id', 'service_team_id', string='Team Members')
