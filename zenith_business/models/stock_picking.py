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

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    verification_technique_faite = fields.Boolean(
        string="Vérification technique faite",
        default=False,
        help="Indique si la vérification technique a été effectuée",
        tracking=True
    )
    date_validation_technique = fields.Datetime(
        string="Date de validation technique",
        help="Date à laquelle la vérification technique a été validée",
        tracking=True
    )
    equipe_de_pose = fields.Many2one(
        'res.users',
        string="Équipe de pose",
        help="Livreur assigné manuellement pour la livraison",
        tracking=True
    )

    def action_validation_technique(self):
        """
        Action appelée lors du clic sur le bouton 'Validation technique OK'
        - Met à jour le champ verification_technique_faite à True
        - Enregistre la date de validation
        - Assigne le responsable du BL
        """
        self.ensure_one()
        
        # Récupération du paramètre système pour l'ID du responsable BL
        bl_manager_id = self.env['ir.config_parameter'].sudo().get_param('zenith_business.bl_manager_id')
        
        if not bl_manager_id:
            raise UserError(_("Aucun responsable BL n'a été configuré. Veuillez configurer le paramètre système 'zenith_business.bl_manager_id'."))
        
        # Mise à jour des champs
        self.write({
            'verification_technique_faite': True,
            'date_validation_technique': fields.Datetime.now(),
        })
        
        # Assignation du responsable BL
        try:
            bl_manager = self.env['res.users'].browse(int(bl_manager_id))
            if bl_manager.exists():
                self.write({'user_id': bl_manager.id})
            else:
                raise UserError(_("Le responsable BL configuré n'existe pas."))
        except (ValueError, TypeError):
            raise UserError(_("L'ID du responsable BL configuré n'est pas valide."))
        
