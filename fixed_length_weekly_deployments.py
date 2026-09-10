WEEK = 10080


def deployment_windows(
    utc_now: int,
    lead_time: int,
    min_duration: int,
    k: int,
    rules: list[tuple[str, int, int, int]],
) -> list[list[int]]:
    result = []
    allow_diff = [0] * (WEEK + 1)
    freeze_diff = [0] * (WEEK + 1)

    def add_interval(diff: list[int], start: int, duration: int):
        if duration == 0:
            return
        end = start + duration
        if end <= WEEK:
            diff[start] += 1
            diff[end] -= 1
        else:
            diff[start] += 1
            diff[WEEK] -= 1
            diff[0] += 1
            diff[end - WEEK] -= 1

    for kind, local_start, local_end, offset in rules:
        if local_start <= local_end:
            duration = local_end - local_start
        else:
            duration = WEEK - local_start + local_end

        utc_start = (local_start - offset) % WEEK
        diff = allow_diff if kind == "ALLOW" else freeze_diff
        add_interval(diff, utc_start, duration)

    deployable = [False] * WEEK
    allow_count = 0
    freeze_count = 0
    for i in range(WEEK):
        allow_count += allow_diff[i]
        freeze_count += freeze_diff[i]
        deployable[i] = allow_count > 0 and freeze_count == 0

    start = utc_now + lead_time
    horizon = start + 3 * WEEK
    result = []
    t = start
    while t < horizon and len(result) < k:
        while t < horizon and not deployable[t % WEEK]:
            t += 1
        span_start = t

        while t < horizon and deployable[t % WEEK]:
            t += 1

        span_end = t
        window_start = span_start
        while window_start + min_duration <= span_end and len(result) < k:
            result.append([window_start, window_start + min_duration])
            window_start += min_duration
    return result
