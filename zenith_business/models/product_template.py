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

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    usage_type = fields.Selection([
        ('scooter_sale_loa', 'Scooter Sale LOA'),
    ], string="Usage Type")

    zen_location_id = fields.Many2one(
        'stock.location',
        string="Emplacement Zenith",
        help="Emplacement physique simplifié du produit (stock.location)",
    )