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
import io

from odoo import models, _, Command
from odoo.exceptions import UserError
from odoo.tools.pdf import PdfFileReader


class ResUsers(models.Model):
    _inherit = 'res.users'

    def generate_sign_template(self, reference, report_id, record_id):
        """
        Generate document PDF
        :return:
        """
        pdf = self.env['ir.actions.report'].sudo()._render_qweb_pdf(report_id, res_ids=record_id)

        # TODO: for now, PDF files without extension are recognized as application/octet-stream;base64
        try:
            file_pdf = PdfFileReader(io.BytesIO(pdf), strict=False, overwriteWarnings=False)
        except Exception as e:
            raise UserError(_("This file cannot be read. Is it a valid PDF?"))
        attachment = self.env['ir.attachment'].create(
            {'name': reference, 'datas': pdf, 'mimetype': 'application/pdf;base64'})
        template = self.env['sign.template'].create(
            {'attachment_id': attachment.id, 'favorited_ids': [(4, self.env.user.id)], 'active': True})
        return template

    def preview_document(self, template):
        """
        Preview document PDF
        :param template: Sign template record
        :return:
        """
        self.ensure_one()
        return {
            'name': "Template \"%(name)s\"" % {'name': template.attachment_id.name},
            'type': 'ir.actions.client',
            'tag': 'sign.Template',
            'params': {
                'id': template.id,
                'sign_directly_without_mail': False,
            },
        }

    def send_document(self, template, reference, subject, message, signers, record_id):
        """
        Send document PDF
        :param template: Sign template record
        :param name: Name of the document
        :param reference: Ref. of the document
        :param signers: List of signers e.g.: [{'partner_id': 7, 'role': 1}, {'partner_id': 2, 'role': 2}]
        :return:
        """
        # Send automatically an email to recipients
        template_id = template.id

        record_id.message_post(body=_("%s has been successfully sended.") % reference,
                               message_type='comment', subtype_xmlid='mail.mt_comment')

        sign_request = self.env['sign.request'].create({
            'template_id': template_id,
            'request_item_ids': [Command.create({
                'partner_id': signer['partner_id'],
                'role_id': signer['role_id'],
            }) for signer in signers],
            'reference': reference,
            'subject': subject,
            'message': message,
        })
        return sign_request
