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
import threading

from odoo import models, fields, _, api, http
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    professional_use = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Professional use')
    installation_type = fields.Selection([
        ('new', 'New'),
        ('old', 'Old')
    ], string='Installation type')
    allow_rental_contract = fields.Boolean(related='company_id.allow_rental_contract', readonly=False)

    # Signature
    rental_contract_template_id = fields.Many2one('sign.template', string="Rental contract",
                                                  help="Document that the tenant will have to sign.",
                                                  copy=False)
    document_sign_request_ids = fields.Many2many('sign.request', string='Signed Documents',
                                                 compute='_compute_document_sign_request_ids')
    rental_contract = fields.Binary(string='Rental contract', copy=False)
    rental_contract_filename = fields.Char(copy=False)
    is_signature_sent = fields.Boolean(string='Signature sent', default=False)
    signature_count = fields.Integer(string="# Signatures", compute='_compute_signature_count')
    request_item_ids = fields.One2many('sign.request.item', 'sign_request_id', string="Signers",
                                       compute='_compute_request_item_ids')

    def _compute_signature_count(self):
        for rec in self:
            rec.signature_count = self.env['sign.request'].sudo().search_count(
                [('template_id', '=', rec.rental_contract_template_id.id)])

    @api.depends('rental_contract_template_id')
    def _compute_request_item_ids(self):
        self = self.sudo()
        for rec in self:
            request_ids = self.env['sign.request'].sudo().search(
                [('template_id', 'in', [rec.rental_contract_template_id.id])])
            if any(request_id.state == 'signed' for request_id in request_ids):
                rec.request_item_ids = request_ids.filtered(lambda x: x.state == 'signed').mapped('request_item_ids')
            else:
                rec.request_item_ids = request_ids[-1:].mapped('request_item_ids')

    def get_registration(self):
        registration = ''
        sale_loa_id = self.picking_ids.filtered(lambda x: x.product_id.product_tmpl_id.usage_type == 'scooter_sale_loa')
        if sale_loa_id and sale_loa_id.mapped('move_ids') and sale_loa_id.mapped('move_ids.lot_ids'):
            last_display_name = sale_loa_id.mapped('move_ids.lot_ids.display_name')[-1]
            registration = last_display_name.split()[-1]
        return registration

    def generate_rental_contract(self):
        """
        Generate rental contract
        :return:
        """
        self.ensure_one()

        if len(self.order_line.filtered(lambda x: x.product_id.product_tmpl_id.usage_type == 'scooter_sale_loa')) > 1:
            raise UserError(
                _("Only one product of type 'Scooter Sale LOA' is allowed. Please correct your selection before generating the rental contract."))

        reference = _("Rental contract %s") % self.partner_id.name

        # Get default role
        ref = self.env.ref
        customer_id = ref('sign.sign_item_role_customer')

        template = self.env.user.generate_sign_template(reference, 'zenith_business.report_contract_rental',
                                                        self.id)

        # Set Contract template to the new document
        self.rental_contract_template_id = template.id

        # Set Contract to null
        self.rental_contract = False

        type_signature = ref('sign.sign_item_type_signature')
        type_date = ref('sign.sign_item_type_date')

        sign_item_values = [
            {'template_id': template.id, 'type_id': type_signature.id, 'required': True,
             'option_ids': [], 'responsible_id': customer_id.id,
             'page': 4,
             'posX': 0.160,
             'posY': 0.675,
             'width': 0.270,
             'height': 0.075},
            {'template_id': template.id, 'type_id': type_date.id, 'required': True,
             'option_ids': [], 'responsible_id': customer_id.id,
             'page': 4,
             'posX': 0.274,
             'posY': 0.836,
             'width': 0.150,
             'height': 0.015},
            # Signature optionnel pour le droit de rétractation
            {'template_id': template.id, 'type_id': type_signature.id, 'required': False,
             'option_ids': [], 'responsible_id': customer_id.id,
             'page': 5,
             'posX': 0.075,
             'posY': 0.488,
             'width': 0.270,
             'height': 0.075},
            {'template_id': template.id, 'type_id': type_date.id, 'required': False,
             'option_ids': [], 'responsible_id': customer_id.id,
             'page': 5,
             'posX': 0.191,
             'posY': 0.389,
             'width': 0.150,
             'height': 0.015}
        ]

        self.env['sign.item'].create(sign_item_values)

        self.message_post(body=_("%s has been successfully generated.") % reference, message_type='comment',
                          subtype_xmlid='mail.mt_comment')

        # Set signature sent to False
        self.is_signature_sent = False

    def preview_rental_contract(self):
        """
        Preview rental contract PDF
        :rtype: object
        """
        return self.env.user.preview_document(self.rental_contract_template_id)

    def send_rental_contract(self):
        """
        Send rental contract PDF
        :rtype: object
        """
        self.ensure_one()

        if self.is_signature_sent:
            return False

        # Get default role
        ref = self.env.ref
        customer_id = ref('sign.sign_item_role_customer')

        template = self.rental_contract_template_id
        reference = _("Rental contract %s") % self.name

        # Send automatically an email to Investor and Investis DOM
        signers = [{'partner_id': self.partner_id.id, 'role_id': customer_id.id}]
        name = _("Rental contract %s") % self.partner_id.name
        value = _("Signature Request - %s") % name

        # Set signature sent to True
        self.is_signature_sent = True

        return self.env.user.send_document(template, reference, value, value, signers, self)

    @api.depends('rental_contract_template_id')
    def _compute_document_sign_request_ids(self):
        for rec in self:
            # Reset signed document when computing new sign requests
            if not rec.rental_contract_template_id:
                rec.rental_contract = False
                rec.document_sign_request_ids = False
                continue

            # Find the latest signed request for this template
            request = self.env['sign.request'].sudo().search([
                ('template_id', '=', rec.rental_contract_template_id.id),
                ('state', '=', 'signed')
            ], limit=1, order='id desc')

            rec.document_sign_request_ids = request

            if rec.document_sign_request_ids and not rec.rental_contract:
                # Reservation contract
                contract_request = http.request.env['sign.request'].sudo().browse(
                    rec.document_sign_request_ids.filtered(
                        lambda x: x.template_id.id == rec.rental_contract_template_id.id).id)

                # Get the completed document and upload it automatically in the convention field
                if contract_request and not rec.rental_contract:
                    if not contract_request.completed_document:
                        t = threading.Thread(target=contract_request.generate_completed_document())
                        t.daemon = True
                        t.start()
                    resevation_document = contract_request.completed_document
                    extension = '.' + contract_request.template_id.attachment_id.mimetype.replace('application/',
                                                                                                  '').replace(
                        ';base64', '')
                    filename = contract_request.reference.replace(extension, '') + extension

                    rec.rental_contract = resevation_document
                    rec.rental_contract_filename = filename

    @api.onchange('sale_order_template_id', 'installation_type')
    def _onchange_sale_order_template_id(self):
        sale_order_template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)
        res = super()._onchange_sale_order_template_id()

        # Si un modèle est sélectionné et qu’il a une position fiscale
        if sale_order_template and sale_order_template.fiscal_position_id and self.installation_type:
            self.fiscal_position_id = sale_order_template.fiscal_position_id.id

        # Remplacements selon le type d'installation
        if self.installation_type and self.company_id.id == 3:
            if self.installation_type == 'old':
                self.fiscal_position_id = self.env['account.fiscal.position'].browse(13)
            elif self.installation_type == 'new':
                self.fiscal_position_id = self.env['account.fiscal.position'].browse(10)

        return res