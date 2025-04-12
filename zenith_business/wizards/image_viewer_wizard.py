# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ImageViewerWizard(models.TransientModel):
    _name = 'zenith.image.viewer.wizard'
    _description = 'Image Viewer Wizard'

    attachment_id = fields.Many2one(
        'ir.attachment', 
        string='Image', 
        readonly=True
    )
    image = fields.Binary(
        string='Image', 
        related='attachment_id.datas', 
        readonly=True
    )
    model = fields.Char(string='Model')

    def action_delete_image(self):
        """Supprime l'image sélectionnée"""
        self.ensure_one()
        if self.model == 'zenith.caracteristique.technique':
            # Recherche des enregistrements liés à cette pièce jointe
            attachment = self.attachment_id
            if attachment.res_model == 'zenith.caracteristique.technique' and attachment.res_id:
                # Si l'attachement est directement lié à un enregistrement
                record_id = attachment.res_id
                self.env['zenith.caracteristique.technique'].remove_photo(record_id, attachment.id)
            else:
                # Recherche des enregistrements qui référencent cette pièce jointe
                records = self.env['zenith.caracteristique.technique'].search([])
                for record in records:
                    if attachment.id in record.photo_ids.ids:
                        self.env['zenith.caracteristique.technique'].remove_photo(record.id, attachment.id)
                        break
        return {'type': 'ir.actions.act_window_close'}
