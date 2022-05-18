from odoo import api, fields, models


class Skill(models.Model):
    _inherit = "hr.skill"

    parent_id = fields.Many2one("hr.skill")
    childs_ids = fields.One2many(
        "hr.skill", ondelete="cascade", inverse_name="parent_id"
    )


class EmployeeSkill(models.Model):
    _inherit = "hr.employee.skill"

    name = fields.Char(related="skill_id.name")
    notes = fields.Html(string="Notes")
    level_progress = fields.Integer(store=True, group_operator="avg")


class SkillType(models.Model):
    _inherit = "hr.skill.type"

    def create_default_skill_level(self):
        for rec in self:
            self.env["hr.skill.level"].create(
                {
                    "skill_type_id": rec.id,
                    "name": "To learn",
                    "level_progress": 0,
                }
            )

    @api.model
    def create(self, vals):
        record = super(SkillType, self).create(vals)
        record.create_default_skill_level()
        return record
