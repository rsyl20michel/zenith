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

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    type_of_financing = fields.Selection([
        ('comptant', 'Comptant'),
        ('credit', 'Crédit'),
        ('eco_solidaire', 'Eco Solidaire'),
        ('defis_tertiaire', 'Défisc tertiaire'),
        ('other', 'Autre')
    ], string='Type de financement')

    type_of_prime = fields.Selection([
        ('edf_cdp', 'EDF CDP'),
        ('edf_agir_plus', 'EDF Agir +'),
        ('edf_tertiaire', 'EDF Tertiaire')
    ], string='Type de prime')

    type_of_opportunities = fields.Selection([
        ('ba', 'Brasseurs d\'air'),
        ('ces', 'Chauffe eau'),
        ('iso', 'Isolation'),
        ('pic', 'Programmateurs d\'intermittence climatisation'),
        ('led', 'Leds'),
        ('sav', 'SAV'),
        ('kit_psicine', 'Kit piscine'),
        ('kit_pv', 'Kit PV'),
        ('borne_elec', 'Borne électrique'),
        ('other', 'Autre')
    ], string='Type d\' opportunité')
    
    type_de_sav = fields.Selection([
        ('ba', 'Brasseurs d\'air'),
        ('ces', 'Chauffe eau'),
        ('iso', 'Isolation'),
        ('pic', 'Programmateurs d\'intermittence climatisation'),
        ('led', 'Leds'),
        ('kit_psicine', 'Kit piscine'),
        ('kit_pv', 'Kit PV'),
        ('borne_elec', 'Borne électrique'),
        ('other', 'Autre')
    ], string='Type de SAV', help="Type de produit concerné par le SAV")

    mobile_partner = fields.Char(related='partner_id.mobile', string="Mobile")
    
    formatted_address = fields.Text(
        string="Adresse",
        compute="_compute_formatted_address",
        store=False,
        readonly=True,
        help="Adresse complète du client formatée"
    )

    date_de_visite_technique = fields.Date(
        string="Date de visite technique",
        required=False,
        help="Date prévue pour la visite technique"
    )

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
    ], string='Résistance', default = 'no')

    ces_cuivre_supp = fields.Selection([
        ('no', 'Non'),
        ('yes_paye', 'Payé OUI'),
        ('yes_non_paye', 'Payé NON'),
    ], string='Cuivre supplémentaire', default = 'no')

    ces_cuivre_supp_nb_metre = fields.Integer(string='Nombre de mètres supplémentaire de cuivre')

    ces_rehausse = fields.Boolean(
        string='Réhausse',
        default=False)
    
    ces_type_bloc = fields.Selection([
        ('monobloc_plaque_tole', "Monobloc - Plaque tôle"),
        ('monobloc_tole_rehausse', "Monobloc - Tôle rehaussée"),
        ('monobloc_toiture_terrasse', "Monobloc - Toiture terrasse"),
        ('monobloc_au_sol', "Monobloc - Au sol"),
        ('dissocie_tole_verticale', "Dissocié - Tôle verticale"),
        ('dissocie_tole_horizontale', "Dissocié - Tôle horizontale"),
        ('dissocie_toiture_terrasse_vertical', "Dissocié - Toiture terrasse vertical"),
        ('dissocie_toiture_terrasse_horizontal', "Dissocié - Toiture terrasse horizontal"),
    ], string="Type de bloc")

    ces_pente_degre = fields.Float(
    string="Pente (degré)",
    help="Pente du toit en degrés"
    )

    ces_hauteur_m = fields.Float(
        string="Hauteur (en mètres)",
        help="Hauteur estimée de l'installation"
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
        ('maison', 'Maison'),
        ('veranda', 'Véranda'),
        ('garage', 'Garage'),
        ('sol', 'Sol')
    ], string="Installation sur")

    ces_raccordement_sur = fields.Selection([
        ('cuisine', 'Cuisine'),
        ('salle_de_bain', 'Salle de bain'),
        ('chauffe_eau_existant', 'Chauffe-eau existant'),
        ('cuivre_nu', 'Cuivre nu'),
        ('wicu', 'WICU'),
        ('polythylene', 'Polythylène'),
        ('autre', 'Autre')
    ], string="Raccordement sur")

    ces_raccordement_detail = fields.Char(
        string="Détail raccordement",
        help="Précisions sur le type de raccordement"
    )

    ces_charpente = fields.Selection([
        ('metallique', 'Métallique'),
        ('bois', 'Bois'),
        ('beton', 'Béton')
    ], string="Charpente")

    ces_type_tole = fields.Selection([
        ('ondulee', 'Ondulée'),
        ('onduline', 'Onduline'),
        ('1000p', '1000P'),
        ('carree', 'Carrée')
    ], string="Type de tôle")

    ces_attentes_prevues = fields.Selection([
        ('interieur', 'Intérieur'),
        ('exterieur', 'Extérieur'),
        ('aucune', 'Aucune')
    ], string="Attentes prévues")

    ces_distance_cuve_capteur = fields.Float(
        string="Distance cuve à capteur (m)",
        help="Distance estimée entre la cuve et les capteurs en mètres"
    )

    ces_chauffe_eau_existant = fields.Selection([
        ('gaz', 'Gaz'),
        ('electrique', 'Électrique'),
        ('solaire', 'Solaire'),
        ('non_existant', 'Non existant')
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
        string="Date du permis de construire"
    )

    suivi_dossier_task_id = fields.Many2one(
        'project.task',
        string="Suivi de dossier",
        help="Tâche automatiquement créée lors de la validation du devis."
    )

    type_of_opportunity_badge = fields.Html(
        string="Type d’opportunité",
        compute="_compute_type_badge",
        sanitize=False
    )

    type_of_opportunity_color = fields.Char(
        string="Couleur type d’opportunité",
        compute="_compute_type_badge",
        store=True
    )

    caracteristique_technique_id = fields.Many2one(
        'zenith.caracteristique.technique',
        string="Caractéristique technique",
        help="Caractéristique technique associée à cette opportunité"
    )

    def action_open_caracteristique_technique(self):
        """
        Méthode pour ouvrir le formulaire de caractéristique technique
        Si une caractéristique existe déjà, ouvre cette caractéristique en édition
        Sinon, ouvre un formulaire de création
        """
        self.ensure_one()
        if self.caracteristique_technique_id:
            # Si une caractéristique existe, ouvrir en mode édition
            return {
                'name': _('Caractéristique Technique'),
                'type': 'ir.actions.act_window',
                'res_model': 'zenith.caracteristique.technique',
                'view_mode': 'form',
                'res_id': self.caracteristique_technique_id.id,
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
                    'default_lead_id': self.id,
                }
            }

    def _compute_formatted_address(self):
        """Calcule l'adresse formatée du client"""
        for lead in self:
            address_parts = []
            partner = lead.partner_id
            
            # Ajout des différentes parties de l'adresse si elles existent
            if partner.street:
                address_parts.append(partner.street)
            if partner.street2:
                address_parts.append(partner.street2)
            if partner.zip or partner.city:
                zip_city = ' '.join(filter(None, [partner.zip, partner.city]))
                if zip_city:
                    address_parts.append(zip_city)
            if partner.state_id:
                address_parts.append(partner.state_id.name)
            if partner.country_id:
                address_parts.append(partner.country_id.name)
            
            # Formatage de l'adresse complète
            lead.formatted_address = '\n'.join(address_parts) if address_parts else ''
    
    def _compute_type_badge(self):
        color_map = {
            'ba': '#007bff',              # Brasseur d'air – Bleu
            'ces': '#ffc107',             # Chauffe eau – Jaune
            'led': '#28a745',             # Leds – Vert
            'iso': '#dc3545',             # Isolation – Rouge
            'sav': '#6c757d',             # SAV – Gris foncé
            'kit_pv': '#e83e8c',          # PV – Rose
            'kit_psicine': '#8B4513',     # Kit piscine – Marron
            'borne_elec': '#6f42c1',      # Borne électrique – Mauve
            'pic': '#17a2b8',             # Programmateur clim – Bleu clair
            'other': '#adb5bd',           # Autre – Gris clair
        }

        for lead in self:
            value = lead.type_of_opportunities
            selection = lead._fields['type_of_opportunities'].selection
            label = dict(selection).get(value, '')
            color = color_map.get(value, '#adb5bd')  # gris par défaut
            if value:
                lead.type_of_opportunity_color = color 
                lead.type_of_opportunity_badge = f"""
                    <span style="
                        background-color: {color};
                        color: white;
                        padding: 2px 8px;
                        border-radius: 10px;
                        font-size: 0.75rem;
                        display: inline-block;">
                        {label}
                    </span>
                """
            else:
                lead.type_of_opportunity_badge = ''