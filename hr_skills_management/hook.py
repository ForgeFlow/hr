from odoo import SUPERUSER_ID
from odoo.api import Environment


def post_init_hook(cr, _):
    env = Environment(cr, SUPERUSER_ID, {})

    # Add 'To learn' level to hr.skill.types that don't have
    hr_skill_types = env["hr.skill.type"].search([])
    for hr_skill_type in hr_skill_types:
        level_to_learn = env["hr.skill.level"].search(
            [("skill_type_id", "=", hr_skill_type.id), ("name", "=", "To learn")]
        )
        if not level_to_learn:
            env["hr.skill.level"].create(
                {
                    "skill_type_id": hr_skill_type.id,
                    "name": "To learn",
                    "level_progress": 0,
                }
            )
