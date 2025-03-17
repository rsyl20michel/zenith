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

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    city_id = fields.Many2one("res.city", string='Contact City')
    firstname = fields.Char(string='Firstname', tracking=True)
    lastname = fields.Char(string='Lastname', tracking=True)

    @api.onchange('firstname', 'lastname')
    def set_name(self):
        for record in self:
            record.name = "%s %s" % (record.firstname if record.firstname else '',
                                     record.lastname if record.lastname else '')

    @api.onchange('city_id')
    def _onchange_city_id(self):
        for rec in self:
            if rec.city_id:
                rec.city = rec.city_id.name
                rec.zip = rec.city_id.zip
                rec.country_id = rec.city_id.country_id

    @api.model_create_multi
    def create(self, vals_list):
        self = self.sudo()
        partners = super(ResPartner, self).create(vals_list)
        for res in partners:
            if res.company_type != 'company' and (not res.firstname or not res.lastname):
                name_parts = res.name.split()

                if len(name_parts) > 1:
                    res.firstname = name_parts[0]  # First word as first name
                    res.lastname = " ".join(name_parts[1:])  # The rest as a name
                else:
                    res.lastname = name_parts[0]  # If only one word, assign it to the name
        return partners
