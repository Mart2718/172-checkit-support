"""Shared drawing code for angles in standard position (TR1, TR2, TR5): axes, the initial side on the positive x-axis,
the terminal side, a turn arc with an arrowhead, and optionally guide rays, a unit circle and a labeled point.
Import it from a make_<code>.py script."""
import math, os
TEAL, ORANGE, BLUE, GRAY, INK = '#1a6b6b', '#a84d16', '#1f4e9c', '#6b6b6b', '#1a1a2e'
S, C = 360, 180          # viewBox size and center
R = 140                  # length of the sides (and unit-circle radius)


def pt(r, deg):
    a = math.radians(deg)
    return C + r * math.cos(a), C - r * math.sin(a)


def draw(path, deg, label=None, clockwise=False, guides=None, unit_circle=False, point=None, point_label=None,
         arc_r=34, extra_arcs=0):
    """deg: where the terminal side points (0 to 360); clockwise draws the turn the other way (deg - 360).
    guides: step in degrees for faint guide rays. extra_arcs: full turns added to the arc (for coterminal angles)."""
    o = [f'<svg viewBox="0 0 {S} {S}" font-family="Arial, Helvetica, sans-serif" font-size="18">',
         f'<rect x="0" y="0" width="{S}" height="{S}" fill="#fcfcfc"/>']
    if guides:
        o.append('<g stroke="#d9d9d9" stroke-width="1.2">')
        for g in range(0, 360, guides):
            x, y = pt(R + 12, g)
            o.append(f'<line x1="{C}" y1="{C}" x2="{x:.1f}" y2="{y:.1f}"/>')
        o.append('</g>')
    if unit_circle:
        o.append(f'<circle cx="{C}" cy="{C}" r="{R}" fill="none" stroke="{GRAY}" stroke-width="1.6"/>')
    o.append(f'<g stroke="{GRAY}" stroke-width="1.8"><line x1="12" y1="{C}" x2="{S-12}" y2="{C}"/><line x1="{C}" y1="12" x2="{C}" y2="{S-12}"/></g>')
    o.append(f'<text x="{S-16}" y="{C-8}" text-anchor="end" fill="#333" font-style="italic">x</text>')
    o.append(f'<text x="{C+8}" y="24" fill="#333" font-style="italic">y</text>')
    x, y = pt(R, 0)
    o.append(f'<line x1="{C}" y1="{C}" x2="{x:.1f}" y2="{y:.1f}" stroke="{TEAL}" stroke-width="4"/>')
    x, y = pt(R, deg)
    o.append(f'<line x1="{C}" y1="{C}" x2="{x:.1f}" y2="{y:.1f}" stroke="{TEAL}" stroke-width="4"/>')
    # turn arc as a polyline spiral (so extra full turns stay visible), with an arrowhead at the end
    sweep = (deg - 360 if deg > 0 else deg) if clockwise else deg
    sweep += (360 * extra_arcs) * (1 if sweep >= 0 else -1)
    n = max(24, int(abs(sweep) / 4))
    pts = []
    for i in range(n + 1):
        t = i / n
        a = sweep * t
        r = arc_r + 9 * abs(a) / 360
        pts.append(pt(r, a))
    o.append('<polyline points="' + ' '.join(f'{px:.1f},{py:.1f}' for px, py in pts) + f'" fill="none" stroke="{ORANGE}" stroke-width="2.6"/>')
    (x1, y1), (x2, y2) = pts[-3], pts[-1]
    ang = math.atan2(y2 - y1, x2 - x1)
    h = 11
    a1 = (x2 - h * math.cos(ang - 0.45), y2 - h * math.sin(ang - 0.45))
    a2 = (x2 - h * math.cos(ang + 0.45), y2 - h * math.sin(ang + 0.45))
    o.append(f'<polygon points="{x2:.1f},{y2:.1f} {a1[0]:.1f},{a1[1]:.1f} {a2[0]:.1f},{a2[1]:.1f}" fill="{ORANGE}"/>')
    if label:
        mid = sweep / 2 if abs(sweep) <= 360 else (sweep % 360) / 2
        lx, ly = pt(arc_r + 40, mid)
        o.append(f'<text x="{lx:.1f}" y="{ly+6:.1f}" text-anchor="middle" fill="{ORANGE}" font-weight="bold">{label}</text>')
    if point is not None:
        px, py = pt(R, deg)
        o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="{BLUE}" stroke="#fff" stroke-width="1.5"/>')
        if point_label:
            lx, ly = pt(R + 26, deg)
            anc = 'start' if math.cos(math.radians(deg)) > 0.2 else ('end' if math.cos(math.radians(deg)) < -0.2 else 'middle')
            o.append(f'<text x="{lx:.1f}" y="{ly+6:.1f}" text-anchor="{anc}" fill="{BLUE}">{point_label}</text>')
    o.append('</svg>')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write('\n'.join(o) + '\n')
