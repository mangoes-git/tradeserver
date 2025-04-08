from datetime import datetime, time


TIME_4AM = time(4, 0, 0)
TIME_4PM = time(16, 0, 0)


def is_time_between(begin_time=TIME_4AM, end_time=TIME_4PM, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        # daytime trading
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time
