def pre_init_hook(cr):
    """Default all existing leaves for not being full day precreating both
    boolean columns.
    """
    cr.execute("ALTER TABLE hr_holidays ADD from_half_day BOOLEAN")
    cr.execute("ALTER TABLE hr_holidays ADD to_half_day BOOLEAN")
    cr.execute("ALTER TABLE hr_holidays ADD from_half_day_am_pm char")
    cr.execute("ALTER TABLE hr_holidays ADD to_half_day_am_pm char")
