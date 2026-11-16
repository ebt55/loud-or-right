"""Easing and tween helpers. Times are in seconds, local to a scene."""


def clamp(x, lo=0.0, hi=1.0):
    return lo if x < lo else hi if x > hi else x


def linear(x):
    return clamp(x)


def in_out_cubic(x):
    x = clamp(x)
    return 4 * x * x * x if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def out_cubic(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def in_cubic(x):
    x = clamp(x)
    return x * x * x


def out_back(x, s=1.4):
    """Small overshoot, for pops (badges, ticks)."""
    x = clamp(x)
    c3 = s + 1
    return 1 + c3 * (x - 1) ** 3 + s * (x - 1) ** 2


def prog(t, t0, dur, ease=in_out_cubic):
    """Eased progress 0..1 of a tween starting at t0 lasting dur."""
    if dur <= 0:
        return 1.0 if t >= t0 else 0.0
    return ease((t - t0) / dur)


def lerp(a, b, p):
    return a + (b - a) * p


def lerp2(a, b, p):
    return (a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p)


def lerp_color(a, b, p):
    return tuple(int(round(a[i] + (b[i] - a[i]) * p)) for i in range(len(a)))


def window(t, t_in, t_out=None, fade_in=0.5, fade_out=0.4, ease=in_out_cubic):
    """Visibility 0..1: fades in from t_in, holds, fades out ending at t_out (None = stays)."""
    a = prog(t, t_in, fade_in, ease)
    if t_out is not None:
        a = min(a, 1.0 - prog(t, t_out - fade_out, fade_out, ease))
    return a


def enter(t, t_in, dur=0.55, dist=40, direction=(0, 1), ease=out_cubic):
    """(alpha, dx, dy) for a fade-and-slide entrance: the element slides in from `direction` * dist."""
    p = prog(t, t_in, dur, ease)
    return p, direction[0] * dist * (1 - p), direction[1] * dist * (1 - p)
