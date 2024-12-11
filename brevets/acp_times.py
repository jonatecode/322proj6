"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/pages/rulesForRiders
and the calculator at https://rusa.jkassen.org/time/
"""

import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  docstrings.

# The upper brevet distance and the min/max speeds for each segment
# (distance km: min kmh/h, max kmh/h)
MIN_MAX_SPEEDS = {
    200: (15, 34),
    300: (15, 32),
    400: (15, 32),
    600: (15, 30),
    1000: (11.428, 28),
    1300: (13.333, 26),
}


def validate_distance(dist: float):
    """Validates distance values."""
    if dist < 0:
        raise ValueError(f"Negative control distance (km): {dist})")


def validate_brevet(dist: float):
    """Validates brevet distances."""
    if dist not in MIN_MAX_SPEEDS:
        raise ValueError(f"Invalid brevet distance: {dist}")


def validate_date_time(tm: str):
    """Validates date-time strings."""
    try:
        arrow.get(tm)
    except arrow.parser.ParserError:
        raise ValueError(f"Invalid time format: {tm}")


def compute_elapsed_time(control_dist_km: int, speed_type: str) -> float:
    """Computes the elapsed time based on segment speeds."""
    cumulative_dist: int = 0
    elapsed_hours: float = 0

    for max_dist, (min_speed, max_speed) in MIN_MAX_SPEEDS.items():
        speed = max_speed if speed_type == "open" else min_speed
        segment_dist = min(
            max_dist - cumulative_dist, control_dist_km - cumulative_dist
        )
        if segment_dist > 0:
            elapsed_hours += segment_dist / speed
            cumulative_dist += segment_dist
        else:
            break

        if cumulative_dist >= control_dist_km:
            break

    return elapsed_hours


def open_time(
    control_dist_km_f: float, brevet_dist_km: float, brevet_start_time: str
) -> str:
    """Computes the open time for a control and returns it in ISO 8601 format.
    Args:
       control_dist_km: the control distance in kilometers
       brevet_dist_km: the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    validate_distance(control_dist_km_f)
    validate_brevet(brevet_dist_km)
    validate_date_time(brevet_start_time)

    start_time: arrow.Arrow = arrow.get(brevet_start_time)

    # Ensure the control distance does not exceed the brevet distance
    control_dist_km: int = int(min(control_dist_km_f, brevet_dist_km))

    # Compute the elapsed time in hours using the compute_elapsed_time method
    elapsed_hours = compute_elapsed_time(control_dist_km, "open")

    open_time = start_time.shift(minutes=round(elapsed_hours * 60))
    return open_time.isoformat()


def close_time(control_dist_km: float, brevet_dist_km: float, brevet_start_time: str):
    """Computes the close time for a control and returns it in ISO 8601 format.
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    validate_distance(control_dist_km)
    validate_brevet(brevet_dist_km)
    validate_date_time(brevet_start_time)

    start_time: arrow.Arrow = arrow.get(brevet_start_time)
    total_hours: float = 0

    # Special cases handling (see rules at https://rusa.org/pages/rulesForRiders)
    if control_dist_km == 0:
        total_hours += 1
    if brevet_dist_km == 200 and control_dist_km >= 200:
        total_hours += 10.0 / 60
    if brevet_dist_km == 400 and control_dist_km >= 400:
        total_hours += 20.0 / 60

    # Cap control distance at brevet distance
    control_dist_km = int(min(control_dist_km, brevet_dist_km))
    total_hours += compute_elapsed_time(control_dist_km, "close")

    close_time = start_time.shift(minutes=round(total_hours * 60))
    return close_time.isoformat()