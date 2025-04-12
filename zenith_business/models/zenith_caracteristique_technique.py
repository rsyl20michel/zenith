# -*- coding: utf-8 -*-
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

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ZenithCaracteristiqueTechnique(models.Model):
    _name = 'zenith.caracteristique.technique'
    _description = 'Zenith Caractéristique Technique'
    
    # Champs généraux
    date_premier_passage = fields.Date(
        string="Date de premier passage",
        required=False,
        help="Date à laquelle le premier passage a été effectué"
    )
    
    date_controle = fields.Date(
        string="Date de contrôle",
        required=False,
        help="Date à laquelle le contrôle technique a été effectué"
    )
    
    detail_remarque = fields.Html(
        string="Détail et remarque",
        help="Détails et remarques concernant l'intervention"
    )
    
    lead_id = fields.Many2one(
        'crm.lead',
        string="Opportunité",
        required=True,
        ondelete='cascade',
        help="Opportunité associée à cette caractéristique technique"
    )
    
    type_of_opportunity_badge = fields.Html(
        related='lead_id.type_of_opportunity_badge',
        string="Type d'opportunité",
        readonly=True
    )
    
    type_of_opportunities = fields.Selection(
        related='lead_id.type_of_opportunities',
        string="Type d'opportunité",
        readonly=True,
        store=True
    )
    
    # Champs CES (Chauffe-eau solaire)
    ces_size_in_litre = fields.Selection([
        ('200', '200 L'),
        ('300', '300 L'),
        ('400', '400 L'),
        ('600', '600 L')
    ], string='Litrage')
    
    ces_nb_captor = fields.Integer(string='Nombre de capteur')
    
    ces_color = fields.Selection([
        ('gris_typhon', 'Gris Typhon'),
        ('blanc', 'Blanc')
    ], string='Couleur')
    
    ces_resistance = fields.Selection([
        ('no', 'Non'),
        ('a_raccorder', 'A raccorder'),
    ], string='Résistance', default='no')
    
    ces_cuivre_supp = fields.Selection([
        ('no', 'Non'),
        ('yes_paye', 'Payé OUI'),
        ('yes_non_paye', 'Payé NON'),
    ], string='Cuivre supplémentaire', default='no')
    
    ces_cuivre_supp_nb_metre = fields.Integer(string='Nombre de mètres supplémentaire de cuivre')
    
    ces_rehausse = fields.Boolean(
        string='Réhausse',
        default=False)
    
    ces_type_bloc = fields.Selection([
        ('monobloc_plaque_tole', "Monobloc - Plaque tôle"),
        ('monobloc_tole_rehausse', "Monobloc - Tôle rehaussée"),
        ('monobloc_toiture_terrasse', "Monobloc - Toiture terrasse"),
        ('monobloc_toiture_terrasse_rehausse', "Monobloc - Toiture terrasse rehaussée"),
        ('monobloc_tole_plate', "Monobloc - Tôle plate"),
        ('monobloc_tole_plate_rehausse', "Monobloc - Tôle plate rehaussée"),
        ('monobloc_tole_tuile', "Monobloc - Tôle tuile"),
        ('monobloc_tole_tuile_rehausse', "Monobloc - Tôle tuile rehaussée"),
        ('split_plaque_tole', "Split - Plaque tôle"),
        ('split_tole_rehausse', "Split - Tôle rehaussée"),
    ], string='Type de bloc')
    
    ces_pente_degre = fields.Float(
        string="Pente (degrés)",
        help="Pente du toit en degrés"
    )
    
    ces_hauteur_m = fields.Float(
        string="Hauteur (m)",
        help="Hauteur du toit en mètres"
    )
    
    ces_orientation_prevue = fields.Selection([
        ('nord', 'Nord'),
        ('nord_est', 'Nord-Est'),
        ('est', 'Est'),
        ('sud_est', 'Sud-Est'),
        ('sud', 'Sud'),
        ('sud_ouest', 'Sud-Ouest'),
        ('ouest', 'Ouest'),
        ('nord_ouest', 'Nord-Ouest')
    ], string="Orientation prévue")
    
    ces_installation_sur = fields.Selection([
        ('maison_principale', 'Maison principale'),
        ('dependance', 'Dépendance'),
        ('autre', 'Autre')
    ], string="Installation sur")
    
    ces_raccordement_sur = fields.Selection([
        ('cumulus_existant', 'Cumulus existant'),
        ('mitigeur_cuisine', 'Mitigeur cuisine'),
        ('mitigeur_sdb', 'Mitigeur SDB'),
        ('autre', 'Autre')
    ], string="Raccordement sur")
    
    ces_raccordement_detail = fields.Char(
        string="Détails du raccordement",
        help="Précisions sur le raccordement"
    )
    
    ces_charpente = fields.Selection([
        ('bois', 'Bois'),
        ('metallique', 'Métallique'),
        ('beton', 'Béton')
    ], string="Type de charpente")
    
    ces_type_tole = fields.Selection([
        ('tole_plate', 'Tôle plate'),
        ('tole_ondule', 'Tôle ondulée'),
        ('tole_bac', 'Tôle bac'),
        ('tole_tuile', 'Tôle tuile'),
        ('autre', 'Autre')
    ], string="Type de tôle")
    
    ces_attentes_prevues = fields.Selection([
        ('interieur', 'Intérieur'),
        ('exterieur', 'Extérieur'),
        ('aucune', 'Aucune')
    ], string="Attentes prévues")
    
    ces_distance_cuve_capteur = fields.Float(
        string="Distance cuve à capteur (m)",
        help="Distance estimée entre la cuve et le capteur en mètres"
    )
    
    ces_chauffe_eau_existant = fields.Selection([
        ('electrique', 'Électrique'),
        ('solaire', 'Solaire'),
        ('gaz', 'Gaz'),
        ('autre', 'Autre'),
        ('aucun', 'Aucun')
    ], string="Chauffe-eau existant")
    
    ces_chauffe_eau_conserver = fields.Selection([
        ('oui', 'Oui'),
        ('non', 'Non')
    ], string="Conserver le chauffe-eau existant")
    
    ces_maison_plus_deux_ans = fields.Selection([
        ('oui', 'Oui'),
        ('non', 'Non')
    ], string="Maison de plus de 2 ans")
    
    ces_date_permis_construire = fields.Date(
        string="Date du permis de construire",
        help="Date du permis de construire de la maison"
    )
    
    # Champs pour les photos
    photo_ids = fields.Many2many(
        'ir.attachment',
        'zenith_caracteristique_photo_rel',
        'caracteristique_id',
        'attachment_id',
        string="Photos",
        domain=[('mimetype', 'like', 'image')],
        context={'default_res_model': 'zenith.caracteristique.technique'}
    )
    
    @api.model
    def remove_photo(self, record_id, attachment_id):
        """Supprime une photo de la galerie"""
        record = self.browse(record_id)
        if not record:
            return False
            
        # Supprime la relation entre l'enregistrement et la pièce jointe
        record.write({
            'photo_ids': [(3, attachment_id)]
        })
        
        # Vérifie si la pièce jointe est utilisée ailleurs et la supprime si nécessaire
        attachment = self.env['ir.attachment'].browse(attachment_id)
        if attachment.exists() and not attachment.res_id:
            attachment.unlink()
            
        return True
        
    def action_view_image(self):
        """Ouvre le wizard d'affichage d'image"""
        self.ensure_one()
        context = self.env.context
        attachment_id = context.get('attachment_id')
        
        if not attachment_id:
            return False
            
        return {
            'type': 'ir.actions.act_window',
            'name': 'Visualiser l\'image',
            'res_model': 'zenith.image.viewer.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_attachment_id': attachment_id,
                'default_model': 'zenith.caracteristique.technique'
            }
        }
        
    # Cette méthode n'est plus utilisée, nous utilisons le widget many2many_binary à la place
    
    # Champs pour les pièces justificatives - Fichiers client
    cni_attachment_id = fields.Binary(
        string="CNI",
        attachment=True,
        help="Carte Nationale d'Identité au format PDF, JPG ou PNG"
    )
    cni_filename = fields.Char(string="Nom du fichier CNI")
    
    justificatif_adresse_attachment_id = fields.Binary(
        string="Justificatif d'adresse",
        attachment=True,
        help="Justificatif d'adresse au format PDF, JPG ou PNG"
    )
    justificatif_adresse_filename = fields.Char(string="Nom du fichier justificatif d'adresse")
    
    avis_impot_attachment_id = fields.Binary(
        string="Avis d'impôt",
        attachment=True,
        help="Avis d'impôt au format PDF, JPG ou PNG"
    )
    avis_impot_filename = fields.Char(string="Nom du fichier avis d'impôt")
    
    facture_edf_attachment_id = fields.Binary(
        string="Facture EDF",
        attachment=True,
        help="Facture EDF au format PDF, JPG ou PNG"
    )
    facture_edf_filename = fields.Char(string="Nom du fichier facture EDF")
    
    info_precontractuelle_attachment_id = fields.Binary(
        string="Information Pré-Contractuelle",
        attachment=True,
        help="Information Pré-Contractuelle au format PDF, JPG ou PNG"
    )
    info_precontractuelle_filename = fields.Char(string="Nom du fichier Information Pré-Contractuelle")
    
    # Champs pour les pièces justificatives - Fichiers chantier
    attestation_tva_reduite_attachment_id = fields.Binary(
        string="Attestation sur l'honneur TVA réduite",
        attachment=True,
        help="Attestation sur l'honneur TVA réduite au format PDF, JPG ou PNG"
    )
    attestation_tva_reduite_filename = fields.Char(string="Nom du fichier attestation TVA réduite")
    
    fiche_synthese_attachment_id = fields.Binary(
        string="Fiche synthèse",
        attachment=True,
        help="Fiche synthèse au format PDF, JPG ou PNG"
    )
    fiche_synthese_filename = fields.Char(string="Nom du fichier fiche synthèse")
    
    cadre_contribution_cee_attachment_id = fields.Binary(
        string="Cadre contribution CEE",
        attachment=True,
        help="Cadre contribution CEE au format PDF, JPG ou PNG"
    )
    cadre_contribution_cee_filename = fields.Char(string="Nom du fichier cadre contribution CEE")
    
    plan_cadastral_attachment_id = fields.Binary(
        string="Plan cadastral",
        attachment=True,
        help="Plan cadastral au format PDF, JPG ou PNG"
    )
    plan_cadastral_filename = fields.Char(string="Nom du fichier plan cadastral")
    
    autorisation_proprietaire_attachment_id = fields.Binary(
        string="Autorisation propriétaire",
        attachment=True,
        help="Autorisation propriétaire au format PDF, JPG ou PNG"
    )
    autorisation_proprietaire_filename = fields.Char(string="Nom du fichier autorisation propriétaire")
    
    bail_location_attachment_id = fields.Binary(
        string="Bail location",
        attachment=True,
        help="Bail location au format PDF, JPG ou PNG"
    )
    bail_location_filename = fields.Char(string="Nom du fichier bail location")
    
    # Champs photos BA (Brasseur d'air)
    img_ba_chambre1 = fields.Binary(string="BA - Chambre 1")
    img_ba_chambre1_filename = fields.Char(string="Nom fichier BA - Chambre 1")
    img_ba_chambre2 = fields.Binary(string="BA - Chambre 2")
    img_ba_chambre2_filename = fields.Char(string="Nom fichier BA - Chambre 2")
    img_ba_chambre3 = fields.Binary(string="BA - Chambre 3")
    img_ba_chambre3_filename = fields.Char(string="Nom fichier BA - Chambre 3")
    img_ba_chambre4 = fields.Binary(string="BA - Chambre 4")
    img_ba_chambre4_filename = fields.Char(string="Nom fichier BA - Chambre 4")
    img_ba_chambre5 = fields.Binary(string="BA - Chambre 5")
    img_ba_chambre5_filename = fields.Char(string="Nom fichier BA - Chambre 5")
    img_ba_salon1 = fields.Binary(string="BA - Salon 1")
    img_ba_salon1_filename = fields.Char(string="Nom fichier BA - Salon 1")
    img_ba_salon2 = fields.Binary(string="BA - Salon 2")
    img_ba_salon2_filename = fields.Char(string="Nom fichier BA - Salon 2")
    img_ba_salon3 = fields.Binary(string="BA - Salon 3")
    img_ba_salon3_filename = fields.Char(string="Nom fichier BA - Salon 3")
    img_ba_bureau = fields.Binary(string="BA - Bureau")
    img_ba_bureau_filename = fields.Char(string="Nom fichier BA - Bureau")
    img_ba_sejour = fields.Binary(string="BA - Séjour")
    img_ba_sejour_filename = fields.Char(string="Nom fichier BA - Séjour")
    
    # Champs photos CESI (Chauffe-eau solaire)
    img_ces_tableau_electrique = fields.Binary(string="CESI - Tableau électrique")
    img_ces_tableau_electrique_filename = fields.Char(string="Nom fichier CESI - Tableau électrique")
    img_ces_acces_maison = fields.Binary(string="CESI - Accès maison")
    img_ces_acces_maison_filename = fields.Char(string="Nom fichier CESI - Accès maison")
    img_ces_attente_electrique = fields.Binary(string="CESI - Attente électrique")
    img_ces_attente_electrique_filename = fields.Char(string="Nom fichier CESI - Attente électrique")
    img_ces_attentes_eaux = fields.Binary(string="CESI - Attentes eaux")
    img_ces_attentes_eaux_filename = fields.Char(string="Nom fichier CESI - Attentes eaux")
    img_ces_devanture_maison = fields.Binary(string="CESI - Devanture de maison")
    img_ces_devanture_maison_filename = fields.Char(string="Nom fichier CESI - Devanture de maison")
    img_ces_facade1 = fields.Binary(string="CESI - Façade 1")
    img_ces_facade1_filename = fields.Char(string="Nom fichier CESI - Façade 1")
    img_ces_facade2 = fields.Binary(string="CESI - Façade 2")
    img_ces_facade2_filename = fields.Char(string="Nom fichier CESI - Façade 2")
    
    # Champs pour les brasseurs d'air
    ba_nombre_salon = fields.Integer(string="Nombre salon", default=0)
    ba_nombre_salle_manger = fields.Integer(string="Nombre salle à manger", default=0)
    ba_nombre_chambre = fields.Integer(string="Nombre chambre", default=0)
    ba_nombre_bureau = fields.Integer(string="Nombre bureau", default=0)
    ba_nombre_terasse_fermee = fields.Integer(string="Nombre terrasse fermée", default=0)
    ba_nombre_autre = fields.Integer(string="Nombre autre", default=0)
    ba_motif_autre = fields.Char(string="Motif autre")

    def action_preview_document(self, doc_type):
        """
        Méthode générique pour prévisualiser un document dans une popup modale
        
        :param doc_type: Type de document ('cni', 'justificatif_adresse', etc.)
        :return: Action pour afficher le document ou une notification
        """
        # Définir les informations pour chaque type de document
        document_mapping = {
            'cni': {
                'field': 'cni_attachment_id',
                'filename_field': 'cni_filename',
                'default_name': 'CNI.pdf',
                'message': "Aucune CNI n'a été téléchargée."
            },
            'justificatif_adresse': {
                'field': 'justificatif_adresse_attachment_id',
                'filename_field': 'justificatif_adresse_filename',
                'default_name': 'Justificatif_Adresse.pdf',
                'message': "Aucun justificatif d'adresse n'a été téléchargé."
            },
            'avis_impot': {
                'field': 'avis_impot_attachment_id',
                'filename_field': 'avis_impot_filename',
                'default_name': 'Avis_Impot.pdf',
                'message': "Aucun avis d'impôt n'a été téléchargé."
            },
            'facture_edf': {
                'field': 'facture_edf_attachment_id',
                'filename_field': 'facture_edf_filename',
                'default_name': 'Facture_EDF.pdf',
                'message': "Aucune facture EDF n'a été téléchargée."
            },
            'info_precontractuelle': {
                'field': 'info_precontractuelle_attachment_id',
                'filename_field': 'info_precontractuelle_filename',
                'default_name': 'Information_Precontractuelle.pdf',
                'message': "Aucune information pré-contractuelle n'a été téléchargée."
            },
            'attestation_tva_reduite': {
                'field': 'attestation_tva_reduite_attachment_id',
                'filename_field': 'attestation_tva_reduite_filename',
                'default_name': 'Attestation_TVA_Reduite.pdf',
                'message': "Aucune attestation sur l'honneur TVA réduite n'a été téléchargée."
            },
            'fiche_synthese': {
                'field': 'fiche_synthese_attachment_id',
                'filename_field': 'fiche_synthese_filename',
                'default_name': 'Fiche_Synthese.pdf',
                'message': "Aucune fiche synthèse n'a été téléchargée."
            },
            'cadre_contribution_cee': {
                'field': 'cadre_contribution_cee_attachment_id',
                'filename_field': 'cadre_contribution_cee_filename',
                'default_name': 'Cadre_Contribution_CEE.pdf',
                'message': "Aucun cadre contribution CEE n'a été téléchargé."
            },
            'plan_cadastral': {
                'field': 'plan_cadastral_attachment_id',
                'filename_field': 'plan_cadastral_filename',
                'default_name': 'Plan_Cadastral.pdf',
                'message': "Aucun plan cadastral n'a été téléchargé."
            },
            'autorisation_proprietaire': {
                'field': 'autorisation_proprietaire_attachment_id',
                'filename_field': 'autorisation_proprietaire_filename',
                'default_name': 'Autorisation_Proprietaire.pdf',
                'message': "Aucune autorisation propriétaire n'a été téléchargée."
            },
            'bail_location': {
                'field': 'bail_location_attachment_id',
                'filename_field': 'bail_location_filename',
                'default_name': 'Bail_Location.pdf',
                'message': "Aucun bail location n'a été téléchargé."
            }
        }
        
        # Vérifier si le type de document est valide
        if doc_type not in document_mapping:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Erreur'),
                    'message': _("Type de document non reconnu."),
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        # Récupérer les informations du document
        doc_info = document_mapping[doc_type]
        doc_content = getattr(self, doc_info['field'])
        doc_filename = getattr(self, doc_info['filename_field'], False) or doc_info['default_name']
        
        # Vérifier si le document existe
        if not doc_content:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Aucun document'),
                    'message': _(doc_info['message']),
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        # Créer un attachement temporaire pour la prévisualisation
        attachment = self.env['ir.attachment'].create({
            'name': doc_filename,
            'datas': doc_content,
            'res_model': 'zenith.caracteristique.technique',
            'res_id': self.id,
        })
        
        # Utiliser l'action standard pour ouvrir le document dans une page tierce
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=false' % attachment.id,
            'target': 'new',
        }
    
    def action_preview_cni(self):
        """
        Prévisualiser la CNI dans une popup
        """
        return self.action_preview_document('cni')
    
    def action_preview_justificatif_adresse(self):
        """
        Prévisualiser le justificatif d'adresse dans une popup
        """
        return self.action_preview_document('justificatif_adresse')
        
    def action_preview_avis_impot(self):
        """
        Prévisualiser l'avis d'impôt dans une popup
        """
        return self.action_preview_document('avis_impot')
        
    def action_preview_facture_edf(self):
        """
        Prévisualiser la facture EDF dans une popup
        """
        return self.action_preview_document('facture_edf')
        
    def action_preview_info_precontractuelle(self):
        """
        Prévisualiser l'information précontractuelle dans une popup
        """
        return self.action_preview_document('info_precontractuelle')
        
    def action_preview_attestation_tva_reduite(self):
        """
        Prévisualiser l'attestation TVA réduite dans une popup
        """
        return self.action_preview_document('attestation_tva_reduite')
        
    def action_preview_fiche_synthese(self):
        """
        Prévisualiser la fiche synthèse dans une popup
        """
        return self.action_preview_document('fiche_synthese')
        
    def action_preview_cadre_contribution_cee(self):
        """
        Prévisualiser le cadre de contribution CEE dans une popup
        """
        return self.action_preview_document('cadre_contribution_cee')
        
    def action_preview_plan_cadastral(self):
        """
        Prévisualiser le plan cadastral dans une popup
        """
        return self.action_preview_document('plan_cadastral')
        
    def action_preview_autorisation_proprietaire(self):
        """
        Prévisualiser l'autorisation propriétaire dans une popup
        """
        return self.action_preview_document('autorisation_proprietaire')
        
    def action_preview_bail_location(self):
        """
        Prévisualiser le bail de location dans une popup
        """
        return self.action_preview_document('bail_location')
    
    @api.model
    def create_caracteristique_technique(self, lead_id):
        """
        Méthode pour créer ou éditer une caractéristique technique à partir d'une opportunité
        """
        # Vérifier si une caractéristique technique existe déjà pour ce lead
        lead = self.env['crm.lead'].browse(lead_id)
        if lead.caracteristique_technique_id:
            # Si une caractéristique existe, ouvrir en mode édition
            return {
                'name': _('Caractéristique Technique'),
                'type': 'ir.actions.act_window',
                'res_model': 'zenith.caracteristique.technique',
                'view_mode': 'form',
                'res_id': lead.caracteristique_technique_id.id,
                'target': 'current',
                'context': {'form_view_ref': 'zenith_business.view_zenith_caracteristique_technique_form'}
            }
        else:
            # Sinon, ouvrir en mode création
            return {
                'name': _('Caractéristique Technique'),
                'type': 'ir.actions.act_window',
                'res_model': 'zenith.caracteristique.technique',
                'view_mode': 'form',
                'target': 'current',
                'context': {
                    'default_lead_id': lead_id,
                }
            }
    
    def write(self, vals):
        """
        Surcharge de la méthode write pour mettre à jour l'opportunité
        """
        result = super(ZenithCaracteristiqueTechnique, self).write(vals)
        # Mettre à jour le champ dans le lead si ce n'est pas déjà fait
        for record in self:
            if record.lead_id and record.lead_id.caracteristique_technique_id.id != record.id:
                record.lead_id.write({
                    'caracteristique_technique_id': record.id
                })
            
            # Synchroniser les champs ces_ avec le lead associé
            ces_fields = {}
            for field in record._fields:
                if field.startswith('ces_'):
                    ces_fields[field] = record[field]
            
            if ces_fields and record.lead_id:
                record.lead_id.write(ces_fields)
                
        return result
    
    @api.model_create_multi
    def create(self, vals_list):
        """
        Surcharge de la méthode create pour mettre à jour l'opportunité
        """
        records = super(ZenithCaracteristiqueTechnique, self).create(vals_list)
        for record in records:
            if record.lead_id and record.lead_id.caracteristique_technique_id.id != record.id:
                record.lead_id.write({
                    'caracteristique_technique_id': record.id
                })
                
            # Synchroniser les champs ces_ avec le lead associé
            ces_fields = {}
            for field in record._fields:
                if field.startswith('ces_'):
                    ces_fields[field] = record[field]
            
            if ces_fields and record.lead_id:
                record.lead_id.write(ces_fields)
                
        return records
