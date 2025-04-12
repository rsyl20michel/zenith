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
{
    'name': "Zenith Business",
    'summary': 'Manage Zenith Business',
    'description': """
This module adds feature to manage Zenith business in Odoo
=====================
    """,
    'author': "Digitic",
    'website': "https://www.digitic.re",
    'category': 'Base',
    'version': '0.1',

    'depends': [
        'base',
        'web',
        'sale',
        'sale_management',
        'l10n_fr',
        'sign',
        'account',
        'contacts',
        'crm',
        'stock',
        'project',
        'planning',
    ],

    'data': [
        # data

        # security
        'security/ir.model.access.csv',
        'security/groups.xml',
        # views
        'views/res_city_views.xml',
        'views/res_partner_views.xml',
        'views/product_template_views.xml',
        'views/sale_order_template_views.xml',
        'views/sale_order_views.xml',
        'views/res_config_settings_views.xml',
        'views/crm_lead_views.xml',
        'views/project_task_views.xml',
        'views/stock_picking_views.xml',
        'views/calendar_views.xml',
        # reports
        'reports/contrat_location_scooter.xml',
        'reports/sale_order.xml',
        # wizards
        'wizards/image_viewer_wizard_views.xml',
        # models views
        'views/zenith_caracteristique_technique_views.xml',
        # menus
        # 'views/menu_view.xml',

    ],
    'demo': [
    ],
    'assets': {
        'web.assets_backend_lazy': [
            'zenith_business/static/src/views/planning_gantt_renderer.js',
        ],
        'web.assets_backend': [
            'zenith_business/static/src/views/attendee_calendar_common_renderer.js',
            'zenith_business/static/src/views/attendee_calendar_models.js',
            'zenith_business/static/src/views/task_gantt_renderer.xml',
            'zenith_business/static/src/views/attendee_calendar_common_renderer.xml',
            'zenith_business/static/src/gantt_view.scss',
        ],
    },
    'qweb': [],
    'sequence': -10,
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
#
##############################################################################
