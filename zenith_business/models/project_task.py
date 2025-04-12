from odoo import models, fields, api, _
from odoo.exceptions import UserError

PROJECT_TASK_WRITABLE_FIELDS = {
    'partner_city',
    'partner_zip',
    'type_of_opportunity_badge',
}


class ProjectTask(models.Model):
    _inherit = 'project.task'

    opportunity_id = fields.Many2one(
        'crm.lead',
        string='Opportunité',
        help="L'opportunité liée à cette tâche (optionnel)."
    )

    type_of_opportunity = fields.Selection(
        related='opportunity_id.type_of_opportunities',
        string='Type d’opportunité',
        store=True,
        readonly=True
    )

    type_of_opportunity_badge = fields.Html(
        related='opportunity_id.type_of_opportunity_badge',
        string="Type d’opportunité",
        readonly=True,
        sanitize=False
    )

    type_of_opportunity_color = fields.Char(
        related='opportunity_id.type_of_opportunity_color',
        string="Couleur type d’opportunité",
        store=True,
        readonly=True
    )

    display_name_gantt = fields.Char(
        compute="_compute_display_name_gantt",
        store=True
    )

    partner_zip = fields.Char(related='partner_id.zip', store=True, readonly=False)
    partner_city = fields.Char(related='partner_id.city', store=True, readonly=False)

    @property
    def SELF_WRITABLE_FIELDS(self):
        return super().SELF_WRITABLE_FIELDS | PROJECT_TASK_WRITABLE_FIELDS

    @api.depends('name', 'type_of_opportunity')
    def _compute_display_name_gantt(self):
        selection_dict = dict(self.env['crm.lead']._fields['type_of_opportunities'].selection)
        for task in self:
            label = selection_dict.get(task.type_of_opportunity, '')
            task.display_name_gantt = label or "non défini"

    @api.model
    def create(self, vals):
        task = super().create(vals)

        if not task.opportunity_id and task.sale_order_id and task.sale_order_id.opportunity_id:
            task.opportunity_id = task.sale_order_id.opportunity_id.id

        if task.opportunity_id:
            task.opportunity_id.suivi_dossier_task_id = task

        return task

    def action_plan_site_service(self):
        for task in self:
            company = task.opportunity_id.company_id or self.env.company

            site_project = self.env['project.project'].search([
                ('name', 'ilike', 'Service sur site'),
                ('company_id', '=', company.id)
            ], limit=1)

            if not site_project:
                raise UserError(_("Le projet 'Service sur site' n'a pas été trouvé dans la société %s.") % company.name)

            new_task = self.env['project.task'].create({
                'name': f"Intervention - {task.partner_id.name or 'Sans client'}",
                'project_id': site_project.id,
                'partner_id': task.partner_id.id,
                'user_ids': [(6, 0, task.user_ids.ids)],
                'parent_id': task.id,
                'color': 5,
                'company_id': company.id,
                'opportunity_id': task.opportunity_id.id
            })

            new_task._compute_color_from_type()

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'project.task',
                'view_mode': 'form',
                'res_id': new_task.id,
                'target': 'current',
            }

    def action_send_report(self):
        self.ensure_one()

        # Vérifie que l'utilisateur est dans le groupe Service sur site / Administrateur
        if not self.env.user.has_group('industry_fsm.group_fsm_manager'):
            raise UserError(_("Vous n'êtes pas autorisé à envoyer le rapport."))

        # Appel de la logique existante (optionnel, à adapter si besoin)
        return super().action_send_report()

    def action_view_caracteristique_technique(self):
        """
        Méthode pour afficher la caractéristique technique associée à l'opportunité liée à cette tâche
        Si aucune opportunité n'est liée ou si l'opportunité n'a pas de caractéristique technique,
        affiche un message d'avertissement
        """
        self.ensure_one()

        # Vérifier si une opportunité est liée à cette tâche
        if not self.opportunity_id:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Aucune opportunité liée'),
                    'message': _('Cette tâche n\'est liée à aucune opportunité. Rapprochez-vous d\'un responsable.'),
                    'type': 'warning',
                    'sticky': False,
                }
            }

        # Vérifier si l'opportunité a une caractéristique technique
        if not self.opportunity_id.caracteristique_technique_id:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Aucune caractéristique technique'),
                    'message': _(
                        'Aucune caractéristique technique n\'existe pour cette opportunité. Rapprochez-vous d\'un responsable.'),
                    'type': 'warning',
                    'sticky': False,
                }
            }

        # Si une caractéristique technique existe, l'afficher
        return {
            'name': _('Caractéristique Technique'),
            'type': 'ir.actions.act_window',
            'res_model': 'zenith.caracteristique.technique',
            'view_mode': 'form',
            'res_id': self.opportunity_id.caracteristique_technique_id.id,
            'target': 'current',
            'context': {'form_view_ref': 'zenith_business.view_zenith_caracteristique_technique_form'}
        }

    @api.depends('type_of_opportunity')
    def _compute_color_from_type(self):
        color_map = {
            'ba': 4,  # Bleu
            'ces': 3,  # Jaune
            'led': 10,  # Vert
            'iso': 1,  # Rouge
            'sav': 0,  # Gris foncé
            'kit_pv': 9,  # Rose
            'kit_psicine': 2,  # Marron
            'borne_elec': 9,  # Violet
            'pic': 7,  # Cyan clair
            'other': 5,  # Mauve
        }
        for task in self:
            task.color = color_map.get(task.type_of_opportunity, 0)
