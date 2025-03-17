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
import base64
import logging
import threading
import time

from odoo import models

_logger = logging.getLogger(__name__)


class SignRequest(models.Model):
    _inherit = 'sign.request'

    def _send_completed_document(self):
        """ Override to update picking after document is signed without sending emails """
        self.ensure_one()
        if self.state != 'signed':
            return

        if not self.completed_document:
            self._generate_completed_document()

        # Get picking linked to the sign request
        picking = self.env['stock.picking'].sudo().search([
            ('rental_contract_template_id', '=', self.template_id.id)
        ], limit=1)

        if picking:
            # Update picking's signed document
            picking.with_context(no_recompute=True)._compute_document_sign_request_ids()
