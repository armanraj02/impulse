from datetime import datetime, timedelta


def get_previous_completed_week(report_date):
    """
    Returns the previous completed Monday-Sunday week.

    Example:
        report_date = Saturday, 2026-09-05

        returns:
        week_start = Monday, 2026-08-24
        week_end   = Sunday, 2026-08-30
    """

    # Monday = 0, Tuesday = 1, ..., Saturday = 5, Sunday = 6
    current_weekday = report_date.weekday()

    # Find Monday of the current week
    current_monday = report_date - timedelta(days=current_weekday)

    # Previous completed week
    week_start = current_monday - timedelta(days=7)
    week_end = current_monday - timedelta(days=1)

    return week_start, week_end


if __name__ == "__main__":

    # Test date
    test_date = datetime(2026, 7, 4)

    week_start, week_end = get_previous_completed_week(test_date)

    print("Report Date :", test_date.date())
    print("Week Start  :", week_start.date())
    print("Week End    :", week_end.date())
