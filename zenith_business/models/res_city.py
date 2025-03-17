# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2025 IT-Solutions.mg. All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api
from odoo.osv import expression


class ResCity(models.Model):
    _name = 'res.city'
    _description = 'City'
    _inherit = ['mail.thread']
    _order = 'name, create_date desc'

    sequence = fields.Integer('Sequence', default=0)
    name = fields.Char(string="Name", index=True, translate=True)
    active = fields.Boolean(string="Active", default=True)
    zip = fields.Char(string='ZIP Code')
    country_id = fields.Many2one('res.country', string='Country', required=True)

    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
        domain = domain or []
        if self.env.context.get('country_id'):
            domain = expression.AND([domain, [('country_id', '=', self.env.context.get('country_id'))]])

        if operator == 'ilike' and not (name or '').strip():
            domain1 = []
            domain2 = []
        else:
            domain1 = [('zip', '=ilike', name)]
            domain2 = [('name', operator, name)]

        first_state_ids = []
        if domain1:
            first_state_ids = list(self._search(
                expression.AND([domain1, domain]), limit=limit, order=order,
            ))
        return first_state_ids + [
            state_id
            for state_id in self._search(expression.AND([domain2, domain]),
                                         limit=limit, order=order)
            if state_id not in first_state_ids
        ]

    @api.depends('zip')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.name} ({record.zip})"
