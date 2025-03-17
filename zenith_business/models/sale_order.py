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

from odoo import models, fields, _, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    professional_use = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Professional use')

    # Signature
    rental_contract_template_id = fields.Many2one('sign.template', string="Rental contract",
                                                  help="Document that the tenant will have to sign.",
                                                  copy=False)
    document_sign_request_ids = fields.Many2many('sign.request', string='Signed Documents',
                                                 compute='_compute_document_sign_request_ids')
    rental_contract = fields.Binary(string='Rental contract', copy=False)
    rental_contract_filename = fields.Char(copy=False)
    is_signature_sent = fields.Boolean(string='Signature sent', default=False)

    def generate_rental_contract(self):
        """
        Generate rental contract
        :return:
        """
        self.ensure_one()

        reference = _("Rental contract %s") % self.partner_id.name

        # Get default role
        ref = self.env.ref
        customer_id = ref('sign.sign_item_role_customer')

        template = self.env.user.generate_sign_template(reference, 'zenith_business.rental_document',
                                                        self.id)

        # Set Contract template to the new document
        self.rental_contract_template_id = template.id

        # Set Contract to null
        self.rental_contract = False

        type_signature = ref('sign.sign_item_type_signature')

        sign_item_values = [
            {'template_id': template.id, 'type_id': type_signature.id, 'required': True,
             'option_ids': [], 'responsible_id': customer_id.id,
             'page': 1,
             'posX': 0.683,
             'posY': 0.776,
             'width': 0.270,
             'height': 0.075},
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
        company_id = ref('sign.sign_item_role_company')
        customer_id = ref('sign.sign_item_role_customer')
        spouse_id = ref('investisdom_defiscalisation.sign_item_role_spouse')

        template = self.rental_contract_template_id
        reference = _("rental contract %s") % self.name

        # Send automatically an email to Investor and Investis DOM
        signers = [{'partner_id': self.investor_id.id, 'role_id': customer_id.id},
                   {'partner_id': ref('base.main_partner').id, 'role_id': company_id.id}]
        if self.investor_id.marital_status in ['married_in_community', 'pacse_in_joint_possession']:
            if not self.investor_id.conjoint_partner_id.email:
                raise UserError(
                    _("The conjoint email is not yet set"))
            signers.append({'partner_id': self.investor_id.conjoint_partner_id.id, 'role_id': spouse_id.id}, )
        name = _("rental contract %s") % self.investor_id.name
        value = _("Signature Request - %s") % name

        # Set signature sent to True
        self.is_signature_sent = True

        return self.env.user.send_document(template, reference, value, value, signers, self)

    @api.depends('rental_contract_template_id')
    def _compute_document_sign_request_ids(self):
        for rec in self:
            # Reset signed document when computing new sign requests
            if not rec.rental_contract_template_id:
                rec.signed_delivery_note = False
                rec.document_sign_request_ids = False
                continue

            # Find the latest signed request for this template
            request = self.env['sign.request'].sudo().search([
                ('template_id', '=', rec.rental_contract_template_id.id),
                ('state', '=', 'signed')
            ], limit=1, order='id desc')

            rec.document_sign_request_ids = request

            # If we have a signed request and signatory info, and no signed document yet
            if request and rec.signatory_name and request.completed_document and not rec.signed_delivery_note:
                signatory_name = f"{rec.signatory_firstname or ''} {rec.signatory_name or ''}"
                rec.signed_delivery_note = request.completed_document
                rec.signed_delivery_note_filename = attachment_name = _('Signed_delivery_note_%s.pdf') % self.name

                # Create attachment and post message
                attachment = rec._create_signed_attachment(base64.b64decode(request.completed_document))
                if attachment:
                    rec._post_signature_message(attachment, signatory_name)
