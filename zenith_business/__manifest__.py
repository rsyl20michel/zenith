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
{
    'name': "Zenith Business",
    'summary': 'Manage Zenith Business',
    'description': """
This module adds feature to manage Zenith business in Odoo
=====================
    """,
    'author': "IT-Solutions.mg",
    'website': "https://www.digitic.re",
    'category': 'Base',
    'version': '0.1',

    'depends': [
        'base',
        'web',
        'sale',
        'l10n_fr',
        'sign',
        'account',
        'contacts',
    ],

    'data': [
        # data

        # security
        'security/ir.model.access.csv',
        # views
        'views/res_city_views.xml',
        'views/res_partner_views.xml',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'views/res_config_settings_views.xml',
        # reports
        'reports/contrat_location_scooter.xml',
        # wizards

        # menus
        # 'views/menu_view.xml',

    ],
    'demo': [
    ],
    'qweb': [],
    'sequence': -10,
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
