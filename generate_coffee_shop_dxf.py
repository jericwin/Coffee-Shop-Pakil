#!/usr/bin/env python3
"""
Architectural CAD Generator: 2-Storey Coffee Shop in Burgos, Pakil, Laguna
Author: Senior Computational Architectural Designer
Standards: Metric (1 unit = 1 mm), Strict Monochrome 2D Drafting (ACI 7)
"""

import math
import os
import ezdxf
from ezdxf import units


def setup_document():
    """Initializes DXF document with architectural standards and layers."""
    doc = ezdxf.new('R2010', setup=True)
    doc.units = units.MM
    doc.header['$INSUNITS'] = 4       # Millimeters
    doc.header['$MEASUREMENT'] = 1    # Metric
    doc.header['$LTSCALE'] = 100.0    # Linetype global scale factor

    # Ensure required layers (Strict Monochrome ACI 7)
    layers_def = [
        ('A-GRID', 'DASHED', 7),
        ('A-WALL-EXTR', 'Continuous', 7),
        ('A-WALL-INTR', 'Continuous', 7),
        ('A-DOOR', 'Continuous', 7),
        ('A-GLAZ', 'Continuous', 7),
        ('A-FURN-BAR', 'Continuous', 7),
        ('A-STAIR', 'Continuous', 7),
        ('A-DIMS', 'Continuous', 7),
        ('A-COLS', 'Continuous', 7),
        ('A-FURN', 'Continuous', 7),
        ('A-ANNO-TEXT', 'Continuous', 7),
        ('A-ANNO-SYMB', 'Continuous', 7),
    ]

    for name, linetype, color in layers_def:
        if name not in doc.layers:
            doc.layers.add(name, linetype=linetype, color=color)
        else:
            lyr = doc.layers.get(name)
            lyr.dxf.linetype = linetype
            lyr.dxf.color = color

    # Setup architectural dimension style
    if 'ARCH_DIM' not in doc.dimstyles:
        ds = doc.dimstyles.duplicate_entry('Standard', 'ARCH_DIM')
        ds.dxf.dimtxt = 220.0     # Text height 220mm
        ds.dxf.dimtsz = 140.0     # Architectural tick size (45° slash)
        ds.dxf.dimexe = 150.0     # Extension line overshoot
        ds.dxf.dimexo = 120.0     # Extension line origin offset
        ds.dxf.dimgap = 100.0     # Text gap from dimension line
        ds.dxf.dimtad = 1         # Text above dimension line
        ds.dxf.dimtih = 0         # Text inside aligns with dim line (never crosses vertical dim lines)
        ds.dxf.dimtoh = 0         # Text outside aligns with dim line
        ds.dxf.dimclrd = 7        # Dim line color ACI 7
        ds.dxf.dimclre = 7        # Ext line color ACI 7
        ds.dxf.dimclrt = 7        # Text color ACI 7
        ds.dxf.dimdec = 0         # 0 decimal places

    return doc


# ==============================================================================
# GEOMETRIC PRIMITIVES & DRAFTING UTILITIES
# ==============================================================================

def add_rect(msp, layer, x, y, w, h, closed=True):
    """Draws a rectangular polyline."""
    pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    return msp.add_lwpolyline(pts, close=closed, dxfattribs={'layer': layer, 'color': 7})


def add_line(msp, layer, p1, p2, linetype='ByLayer'):
    """Draws a line with specified layer and linetype."""
    attribs = {'layer': layer, 'color': 7}
    if linetype != 'ByLayer':
        attribs['linetype'] = linetype
    return msp.add_line(p1, p2, dxfattribs=attribs)


def add_text(msp, layer, text, insert, height=200, rotation=0, align='LEFT'):
    """Draws a single-line architectural text."""
    txt = msp.add_text(
        text,
        dxfattribs={
            'layer': layer,
            'color': 7,
            'height': height,
            'rotation': rotation
        }
    )
    if align == 'CENTER':
        txt.set_placement(insert, align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    elif align == 'MIDDLE_LEFT':
        txt.set_placement(insert, align=ezdxf.enums.TextEntityAlignment.MIDDLE_LEFT)
    elif align == 'MIDDLE_RIGHT':
        txt.set_placement(insert, align=ezdxf.enums.TextEntityAlignment.MIDDLE_RIGHT)
    else:
        txt.dxf.insert = insert
    return txt


def add_column(msp, cx, cy, size=400):
    """Draws a reinforced concrete structural column with centerline marker."""
    half = size / 2.0
    x0, y0 = cx - half, cy - half
    add_rect(msp, 'A-COLS', x0, y0, size, size)
    # Structural column diagonal cross
    add_line(msp, 'A-COLS', (x0, y0), (x0 + size, y0 + size))
    add_line(msp, 'A-COLS', (x0 + size, y0), (x0, y0 + size))


def add_window(msp, p1, p2, wall_thk=200, frame_thk=50):
    """
    Draws an architectural window assembly: outer & inner sills, 50mm side jambs,
    and twin 25mm spaced center glass panes.
    """
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)
    if length < 1e-4:
        return

    ux = dx / length
    uy = dy / length
    vx = -uy
    vy = ux

    # Corner points of wall aperture
    p1_in = (x1, y1)
    p2_in = (x2, y2)
    p1_out = (x1 + vx * wall_thk, y1 + vy * wall_thk)
    p2_out = (x2 + vx * wall_thk, y2 + vy * wall_thk)

    # Sill lines
    add_line(msp, 'A-GLAZ', p1_in, p2_in)
    add_line(msp, 'A-GLAZ', p1_out, p2_out)

    # Jamb end closures
    add_line(msp, 'A-GLAZ', p1_in, p1_out)
    add_line(msp, 'A-GLAZ', p2_in, p2_out)

    # 50mm frame profiles
    f1_in = (x1 + ux * frame_thk, y1 + uy * frame_thk)
    f1_out = (f1_in[0] + vx * wall_thk, f1_in[1] + vy * wall_thk)
    f2_in = (x2 - ux * frame_thk, y2 - uy * frame_thk)
    f2_out = (f2_in[0] + vx * wall_thk, f2_in[1] + vy * wall_thk)
    add_line(msp, 'A-GLAZ', f1_in, f1_out)
    add_line(msp, 'A-GLAZ', f2_in, f2_out)

    # Twin glass pane lines (offset +/- 15mm from centerline)
    mid_dist1 = wall_thk / 2.0 - 15.0
    mid_dist2 = wall_thk / 2.0 + 15.0
    g1_start = (f1_in[0] + vx * mid_dist1, f1_in[1] + vy * mid_dist1)
    g1_end = (f2_in[0] + vx * mid_dist1, f2_in[1] + vy * mid_dist1)
    g2_start = (f1_in[0] + vx * mid_dist2, f1_in[1] + vy * mid_dist2)
    g2_end = (f2_in[0] + vx * mid_dist2, f2_in[1] + vy * mid_dist2)
    add_line(msp, 'A-GLAZ', g1_start, g1_end)
    add_line(msp, 'A-GLAZ', g2_start, g2_end)


def add_single_door(msp, hinge_pt, width, wall_thk, direction='N', hand='right', inward=True):
    """
    Draws a single swing door with 50mm jambs, 40mm door leaf, and 90-degree swing arc.
    """
    hx, hy = hinge_pt
    jamb_w = 50.0

    # Draw jambs
    if direction == 'N':  # Door along horizontal wall, wall is north of opening or opening is in north wall
        # Jamb at hinge
        add_rect(msp, 'A-DOOR', hx - jamb_w, hy, jamb_w, wall_thk)
        # Jamb at strike
        add_rect(msp, 'A-DOOR', hx + width, hy, jamb_w, wall_thk)

        # Leaf & Swing
        if hand == 'left':  # hinge on left, swings inward (-Y)
            leaf_end = (hx, hy - width)
            add_line(msp, 'A-DOOR', (hx, hy), leaf_end)
            msp.add_arc((hx, hy), width, 270, 360, dxfattribs={'layer': 'A-DOOR', 'color': 7})
        else:  # hinge on right, swings inward
            # hinge is at hx + width
            rx = hx + width
            leaf_end = (rx, hy - width)
            add_line(msp, 'A-DOOR', (rx, hy), leaf_end)
            msp.add_arc((rx, hy), width, 180, 270, dxfattribs={'layer': 'A-DOOR', 'color': 7})

    elif direction == 'W':  # Door along vertical wall (West partition)
        add_rect(msp, 'A-DOOR', hx, hy - jamb_w, wall_thk, jamb_w)
        add_rect(msp, 'A-DOOR', hx, hy + width, wall_thk, jamb_w)
        if inward:
            # Swings east (+X)
            leaf_end = (hx + width, hy)
            add_line(msp, 'A-DOOR', (hx, hy), leaf_end)
            msp.add_arc((hx, hy), width, 0, 90, dxfattribs={'layer': 'A-DOOR', 'color': 7})


def add_double_swing_door(msp, center_x, wall_y, total_width=1800, wall_thk=200):
    """
    Draws North entry 1800mm double-swing door (two 900mm leaves swinging inward).
    """
    half = total_width / 2.0
    x_left = center_x - half
    x_right = center_x + half
    jamb = 50.0
    leaf_w = half

    # Door jamb frames
    add_rect(msp, 'A-DOOR', x_left - jamb, wall_y, jamb, wall_thk)
    add_rect(msp, 'A-DOOR', x_right, wall_y, jamb, wall_thk)

    # Left Door Leaf: hinge at (x_left, wall_y), open position swinging inward to (x_left, wall_y - leaf_w)
    add_line(msp, 'A-DOOR', (x_left, wall_y), (x_left, wall_y - leaf_w))
    msp.add_arc((x_left, wall_y), leaf_w, 270, 360, dxfattribs={'layer': 'A-DOOR', 'color': 7})

    # Right Door Leaf: hinge at (x_right, wall_y), open position swinging inward to (x_right, wall_y - leaf_w)
    add_line(msp, 'A-DOOR', (x_right, wall_y), (x_right, wall_y - leaf_w))
    msp.add_arc((x_right, wall_y), leaf_w, 180, 270, dxfattribs={'layer': 'A-DOOR', 'color': 7})

    # Threshold line
    add_line(msp, 'A-DOOR', (x_left, wall_y + wall_thk), (x_right, wall_y + wall_thk))


def add_dimension_string(msp, points, base_y, is_horizontal=True, base_coord=None):
    """
    Generates precision linear architectural dimensions along an alignment chain.
    """
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]
        dist = abs(p2[0] - p1[0]) if is_horizontal else abs(p2[1] - p1[1])
        if dist < 1.0:
            continue

        if is_horizontal:
            base_pt = (p1[0], base_coord)
            dim = msp.add_linear_dim(
                base=base_pt,
                p1=p1,
                p2=p2,
                dimstyle='ARCH_DIM',
                dxfattribs={'layer': 'A-DIMS', 'color': 7}
            )
        else:
            base_pt = (base_coord, p1[1])
            dim = msp.add_linear_dim(
                base=base_pt,
                p1=p1,
                p2=p2,
                angle=90,
                dimstyle='ARCH_DIM',
                dxfattribs={'layer': 'A-DIMS', 'color': 7}
            )
        dim.render()


# ==============================================================================
# SPECIALIZED ARCHITECTURAL ASSEMBLIES
# ==============================================================================

def draw_grid_system(msp, x_offset=0, suffix=''):
    """Draws 3x3 structural column grid lines with dashed centerlines and labeled bubbles."""
    x_coords = [0.0 + x_offset, 5000.0 + x_offset, 10000.0 + x_offset]
    y_coords = [0.0, 5000.0, 10000.0]
    x_labels = ['A', 'B', 'C']
    y_labels = ['1', '2', '3']

    ext = 1600.0
    bubble_r = 350.0

    # Vertical Grids (A, B, C)
    for x, lbl in zip(x_coords, x_labels):
        # Dashed centerline
        add_line(msp, 'A-GRID', (x, -ext), (x, 10000.0 + ext), linetype='DASHED')
        # Bubbles Top & Bottom
        for by, txt_lbl in [(-ext - bubble_r, f"{lbl}{suffix}"), (10000.0 + ext + bubble_r, f"{lbl}{suffix}")]:
            msp.add_circle((x, by), bubble_r, dxfattribs={'layer': 'A-GRID', 'color': 7})
            add_text(msp, 'A-GRID', txt_lbl, (x, by), height=280, align='CENTER')

    # Horizontal Grids (1, 2, 3)
    for y, lbl in zip(y_coords, y_labels):
        # Dashed centerline
        add_line(msp, 'A-GRID', (x_offset - ext, y), (x_offset + 10000.0 + ext, y), linetype='DASHED')
        # Bubbles Left & Right
        for bx, txt_lbl in [(x_offset - ext - bubble_r, f"{lbl}{suffix}"), (x_offset + 10000.0 + ext + bubble_r, f"{lbl}{suffix}")]:
            msp.add_circle((bx, y), bubble_r, dxfattribs={'layer': 'A-GRID', 'color': 7})
            add_text(msp, 'A-GRID', txt_lbl, (bx, y), height=280, align='CENTER')


def draw_columns(msp, x_offset=0):
    """Places 400x400 reinforced concrete columns at 9 structural grid nodes."""
    for x in [0.0, 5000.0, 10000.0]:
        for y in [0.0, 5000.0, 10000.0]:
            add_column(msp, x + x_offset, y, size=400)


def draw_u_stairs(msp, x_base, y_base, is_second_floor=False):
    """
    Draws a U-shaped staircase:
    - Width: 2000mm (2 flights of 1000mm width)
    - Depth: 2500mm
    - Treads: 280mm run
    - Landing: 820mm depth at the turn
    - Zero-collision drafting: Arrow lines and diagonal void crosses break cleanly around all annotations.
    """
    flight_w = 1000.0
    landing_depth = 820.0
    run = 280.0
    tread_count = 6  # 6 treads * 280 = 1680mm + 820mm landing = 2500mm

    # Stairwell boundary enclosure
    add_rect(msp, 'A-WALL-INTR', x_base, y_base, 2000.0, 2500.0)

    # Flight divider / handrail centerline
    center_x = x_base + flight_w
    add_line(msp, 'A-STAIR', (center_x, y_base), (center_x, y_base + 2500.0 - landing_depth))

    # Intermediate Landing
    landing_y = y_base + 2500.0 - landing_depth
    add_line(msp, 'A-STAIR', (x_base, landing_y), (x_base + 2000.0, landing_y))
    add_text(msp, 'A-STAIR', 'LANDING', (x_base + 1000.0, landing_y + landing_depth / 2.0), height=140, align='CENTER')

    if not is_second_floor:
        # Ground Floor: Upward flight (West side) & Downward flight (East side)
        for i in range(tread_count):
            ty = y_base + i * run
            if i <= 3:
                add_line(msp, 'A-STAIR', (x_base, ty), (center_x, ty))
                add_text(msp, 'A-STAIR', str(i + 1), (x_base + 150.0, ty + 140.0), height=110, align='CENTER')
            else:
                add_line(msp, 'A-STAIR', (x_base, ty), (center_x, ty), linetype='DASHED')

            # Flight 2 (Overhead East Flight - dashed above break)
            add_line(msp, 'A-STAIR', (center_x, ty), (x_base + 2000.0, ty), linetype='DASHED')

        # Architectural Stair Break Line
        break_y = y_base + 3.8 * run
        break_pts = [
            (x_base - 50.0, break_y - 80.0),
            (center_x - 300.0, break_y - 80.0),
            (center_x - 200.0, break_y + 120.0),
            (center_x - 100.0, break_y - 120.0),
            (center_x + 100.0, break_y + 120.0),
            (center_x + 200.0, break_y - 80.0),
            (x_base + 2050.0, break_y - 80.0),
        ]
        msp.add_lwpolyline(break_pts, dxfattribs={'layer': 'A-STAIR', 'color': 7})

        # Directional "UP" Arrow with ZERO line-text collision
        arrow_start = (x_base + 500.0, y_base + 150.0)
        arrow_mid = (x_base + 500.0, landing_y - 150.0)
        msp.add_circle(arrow_start, 60.0, dxfattribs={'layer': 'A-STAIR', 'color': 7})

        # Segment 1: start up to text
        add_line(msp, 'A-STAIR', arrow_start, (x_base + 500.0, y_base + 480.0))
        # Clear gap for text "UP (18 RISERS)"
        add_text(msp, 'A-STAIR', 'UP (18 RISERS)', (x_base + 500.0, y_base + 750.0), height=130, rotation=90, align='CENTER')
        # Segment 2: text up to landing
        add_line(msp, 'A-STAIR', (x_base + 500.0, y_base + 1050.0), arrow_mid)

        # Arrowhead
        ah1 = (arrow_mid[0] - 80.0, arrow_mid[1] - 120.0)
        ah2 = (arrow_mid[0] + 80.0, arrow_mid[1] - 120.0)
        add_line(msp, 'A-STAIR', arrow_mid, ah1)
        add_line(msp, 'A-STAIR', arrow_mid, ah2)

    else:
        # Second Floor: Full descent treads and void opening with ZERO line collision
        for i in range(tread_count):
            ty = y_base + i * run
            add_line(msp, 'A-STAIR', (center_x, ty), (x_base + 2000.0, ty))
            add_text(msp, 'A-STAIR', str(18 - i), (x_base + 1850.0, ty + 140.0), height=110, align='CENTER')

        # Stair Void Label Box (boundary protects text from any lines or clutter)
        vbx1, vbx2 = x_base + 120.0, center_x - 120.0
        vby1, vby2 = y_base + 680.0, y_base + 1020.0
        add_rect(msp, 'A-STAIR', vbx1, vby1, vbx2 - vbx1, vby2 - vby1)

        # Void diagonal crossing arms terminate cleanly at label box corners
        add_line(msp, 'A-STAIR', (x_base, y_base), (vbx1, vby1), linetype='DASHED')
        add_line(msp, 'A-STAIR', (center_x, y_base), (vbx2, vby1), linetype='DASHED')
        add_line(msp, 'A-STAIR', (x_base, landing_y), (vbx1, vby2), linetype='DASHED')
        add_line(msp, 'A-STAIR', (center_x, landing_y), (vbx2, vby2), linetype='DASHED')

        add_text(msp, 'A-STAIR', 'STAIR VOID', (x_base + 500.0, y_base + 890.0), height=140, align='CENTER')
        add_text(msp, 'A-STAIR', 'OPEN TO BELOW', (x_base + 500.0, y_base + 760.0), height=105, align='CENTER')

        # Guardrails along stairwell edge
        add_line(msp, 'A-STAIR', (x_base, y_base), (center_x, y_base))
        add_line(msp, 'A-STAIR', (center_x, y_base), (center_x, landing_y))

        # "DN" Arrow with clean break around text
        arrow_start = (x_base + 1500.0, y_base + 150.0)
        arrow_mid = (x_base + 1500.0, landing_y - 150.0)
        msp.add_circle(arrow_mid, 60.0, dxfattribs={'layer': 'A-STAIR', 'color': 7})

        # Segment 1: from top down to text
        add_line(msp, 'A-STAIR', arrow_mid, (x_base + 1500.0, y_base + 850.0))
        # Clear gap for "DN"
        add_text(msp, 'A-STAIR', 'DN', (x_base + 1500.0, y_base + 700.0), height=140, rotation=90, align='CENTER')
        # Segment 2: from text down to arrowhead
        add_line(msp, 'A-STAIR', (x_base + 1500.0, y_base + 550.0), arrow_start)

        ah1 = (arrow_start[0] - 80.0, arrow_start[1] + 120.0)
        ah2 = (arrow_start[0] + 80.0, arrow_start[1] + 120.0)
        add_line(msp, 'A-STAIR', arrow_start, ah1)
        add_line(msp, 'A-STAIR', arrow_start, ah2)


def draw_pwd_restroom(msp, x_base=7800.0, y_base=200.0):
    """
    Draws a PWD-compliant Restroom in the Southeast corner:
    - 2000mm x 2000mm clear internal dimensions
    - 100mm partition walls
    - 900mm clear accessible door with outward safety swing
    - PWD water closet, grab bars, accessible sink, and 1500mm turning circle
    - Zero line-text overlap: annotations placed in open clearance spaces.
    """
    # 100mm Internal Partition Walls
    add_rect(msp, 'A-WALL-INTR', 7700.0, 2200.0, 2100.0, 100.0)
    add_rect(msp, 'A-WALL-INTR', 7700.0, 200.0, 100.0, 700.0)
    add_rect(msp, 'A-WALL-INTR', 7700.0, 1800.0, 100.0, 500.0)

    # 900mm PWD Accessible Outward-Swinging Door
    door_w = 900.0
    add_rect(msp, 'A-DOOR', 7700.0, 850.0, 100.0, 50.0)
    add_rect(msp, 'A-DOOR', 7700.0, 1800.0, 100.0, 50.0)
    leaf_end = (7700.0 - door_w, 900.0)
    add_line(msp, 'A-DOOR', (7700.0, 900.0), leaf_end)
    msp.add_arc((7700.0, 900.0), door_w, 90, 180, dxfattribs={'layer': 'A-DOOR', 'color': 7})

    # PWD Water Closet (WC)
    wc_x, wc_y = 9300.0, 600.0
    add_rect(msp, 'A-FURN', wc_x - 250.0, wc_y - 200.0, 500.0, 200.0)
    add_rect(msp, 'A-FURN', wc_x - 190.0, wc_y, 380.0, 480.0)
    msp.add_arc((wc_x, wc_y + 240.0), 190.0, 0, 180, dxfattribs={'layer': 'A-FURN', 'color': 7})

    # Grab Bars
    add_line(msp, 'A-FURN', (wc_x - 450.0, 250.0), (wc_x - 450.0, 1050.0))
    add_line(msp, 'A-FURN', (wc_x - 300.0, 250.0), (wc_x + 300.0, 250.0))

    # Accessible Wash Basin
    sink_x, sink_y = 8000.0, 1750.0
    add_rect(msp, 'A-FURN', sink_x, sink_y, 600.0, 400.0)
    msp.add_circle((sink_x + 300.0, sink_y + 200.0), 120.0, dxfattribs={'layer': 'A-FURN', 'color': 7})

    # 1500mm PWD Turning Radius Clearance Circle (Dashed)
    msp.add_circle((8800.0, 1200.0), 750.0, dxfattribs={'layer': 'A-FURN', 'linetype': 'DASHED', 'color': 7})

    # Stacked room annotations in the clear center of the turning radius
    add_text(msp, 'A-ANNO-TEXT', 'PWD TOILET', (8800.0, 1420.0), height=150, align='CENTER')
    add_text(msp, 'A-ANNO-TEXT', 'FFL +0.580m', (8800.0, 1200.0), height=115, align='CENTER')
    add_text(msp, 'A-FURN', 'Ø1500 TURNING CLEARANCE', (8800.0, 980.0), height=95, align='CENTER')


def draw_barista_counter(msp):
    """
    Draws the Main L-shaped Barista Counter (3500mm x 2500mm) and Prep Zone along West Wall:
    - 600mm counter depth
    - 1200mm clear barista aisle behind counter
    - Zero-collision drafting: diagonal equipment crosses break cleanly around all labels.
    """
    # Back Prep Counter (against West Wall, X = 200 to 800, Y = 3500 to 7000)
    add_rect(msp, 'A-FURN-BAR', 200.0, 3500.0, 600.0, 3500.0)

    # Double-compartment prep sink (800x450mm)
    add_rect(msp, 'A-FURN-BAR', 250.0, 3700.0, 500.0, 800.0)
    add_rect(msp, 'A-FURN-BAR', 280.0, 3730.0, 440.0, 350.0)
    add_rect(msp, 'A-FURN-BAR', 280.0, 4120.0, 440.0, 350.0)
    add_text(msp, 'A-FURN-BAR', 'PREP SINK', (500.0, 4100.0), height=100, rotation=90, align='CENTER')

    # Undercounter Refrigerator / Ice Machine with broken diagonals (leaves center clear for text)
    add_rect(msp, 'A-FURN-BAR', 220.0, 4700.0, 560.0, 1000.0)
    add_line(msp, 'A-FURN-BAR', (220.0, 4700.0), (360.0, 4950.0), linetype='DASHED')
    add_line(msp, 'A-FURN-BAR', (640.0, 5450.0), (780.0, 5700.0), linetype='DASHED')
    add_line(msp, 'A-FURN-BAR', (220.0, 5700.0), (360.0, 5450.0), linetype='DASHED')
    add_line(msp, 'A-FURN-BAR', (640.0, 4950.0), (780.0, 4700.0), linetype='DASHED')
    add_text(msp, 'A-FURN-BAR', 'UNDERCOUNTER REF / ICE', (500.0, 5200.0), height=95, rotation=90, align='CENTER')

    # Handwash Sink
    add_rect(msp, 'A-FURN-BAR', 250.0, 6200.0, 500.0, 450.0)
    msp.add_circle((500.0, 6425.0), 120.0, dxfattribs={'layer': 'A-FURN-BAR', 'color': 7})

    # Main Front Service Counter (L-Shape)
    pts_l_counter = [
        (2000.0, 7000.0),
        (2600.0, 7000.0),
        (2600.0, 4100.0),
        (4500.0, 4100.0),
        (4500.0, 3500.0),
        (2000.0, 3500.0)
    ]
    msp.add_lwpolyline(pts_l_counter, close=True, dxfattribs={'layer': 'A-FURN-BAR', 'color': 7})

    # Commercial 3-Group Espresso Machine
    add_rect(msp, 'A-FURN-BAR', 2025.0, 5700.0, 550.0, 900.0)
    for gy in [5900.0, 6150.0, 6400.0]:
        msp.add_circle((2300.0, gy), 45.0, dxfattribs={'layer': 'A-FURN-BAR', 'color': 7})
    add_text(msp, 'A-FURN-BAR', 'ESPRESSO MACHINE', (2300.0, 6150.0), height=90, rotation=90, align='CENTER')

    # Dual Coffee Grinders
    add_rect(msp, 'A-FURN-BAR', 2050.0, 5350.0, 240.0, 240.0)
    msp.add_circle((2170.0, 5470.0), 90.0, dxfattribs={'layer': 'A-FURN-BAR', 'color': 7})
    add_rect(msp, 'A-FURN-BAR', 2050.0, 5050.0, 240.0, 240.0)
    msp.add_circle((2170.0, 5170.0), 90.0, dxfattribs={'layer': 'A-FURN-BAR', 'color': 7})
    add_text(msp, 'A-FURN-BAR', 'GRINDERS', (2170.0, 4950.0), height=85, rotation=90, align='CENTER')

    # POS Terminal
    add_rect(msp, 'A-FURN-BAR', 2100.0, 4300.0, 400.0, 400.0)
    add_text(msp, 'A-FURN-BAR', 'POS', (2300.0, 4500.0), height=110, align='CENTER')

    # Pastry Display Case
    add_rect(msp, 'A-FURN-BAR', 2900.0, 3550.0, 1200.0, 500.0)
    add_line(msp, 'A-FURN-BAR', (2900.0, 3800.0), (4100.0, 3800.0))
    add_text(msp, 'A-FURN-BAR', 'PASTRY DISPLAY CASE', (3500.0, 3800.0), height=95, align='CENTER')

    add_text(msp, 'A-FURN-BAR', 'ORDER / PICK-UP', (2300.0, 6800.0), height=100, rotation=90, align='CENTER')

    # Clear Barista Aisle Annotations (placed in open floor aisle with zero line intersections)
    add_text(msp, 'A-ANNO-TEXT', 'BARISTA STATION', (1400.0, 5600.0), height=150, rotation=90, align='CENTER')
    add_text(msp, 'A-ANNO-TEXT', 'PREP ZONE (1200mm AISLE)', (1400.0, 4300.0), height=120, rotation=90, align='CENTER')

    # Bar Stools along L-Counter return
    for bx in [2800.0, 3400.0, 4000.0]:
        msp.add_circle((bx, 3050.0), 180.0, dxfattribs={'layer': 'A-FURN', 'color': 7})
        msp.add_circle((bx, 3050.0), 60.0, dxfattribs={'layer': 'A-FURN', 'color': 7})


def draw_table_4top(msp, cx, cy):
    """Draws a 4-person dining table (800x1200mm) with 4 chairs."""
    # Table
    add_rect(msp, 'A-FURN', cx - 600.0, cy - 400.0, 1200.0, 800.0)
    # 2 North Chairs
    for ox in [-300.0, 300.0]:
        add_rect(msp, 'A-FURN', cx + ox - 200.0, cy + 450.0, 400.0, 350.0)
    # 2 South Chairs
    for ox in [-300.0, 300.0]:
        add_rect(msp, 'A-FURN', cx + ox - 200.0, cy - 800.0, 400.0, 350.0)


def draw_round_table_3top(msp, cx, cy, radius=400.0):
    """Draws a round cafe table with 3 radially arranged chairs."""
    msp.add_circle((cx, cy), radius, dxfattribs={'layer': 'A-FURN', 'color': 7})
    for angle_deg in [30, 150, 270]:
        rad = math.radians(angle_deg)
        ch_x = cx + math.cos(rad) * (radius + 240.0)
        ch_y = cy + math.sin(rad) * (radius + 240.0)
        msp.add_circle((ch_x, ch_y), 180.0, dxfattribs={'layer': 'A-FURN', 'color': 7})


# ==============================================================================
# FLOOR PLAN BUILDERS
# ==============================================================================

def build_ground_floor(msp):
    """Constructs the complete Ground Floor architectural plan."""
    # 1. Structural Grid & Columns
    draw_grid_system(msp, x_offset=0, suffix='')
    draw_columns(msp, x_offset=0)

    # 2. Exterior Perimeter Walls (200mm thick, overall footprint 10000x10000)
    # Outer boundaries: (0,0) to (10000, 10000)
    # Inner boundaries: (200, 200) to (9800, 9800)

    # NORTH FACADE (Y = 9800 to 10000)
    # Wall piers: 0-2000 (corner/west), 3800-5400 (mid column), 9400-10000 (east corner)
    add_rect(msp, 'A-WALL-EXTR', 0.0, 9800.0, 2000.0, 200.0)
    add_rect(msp, 'A-WALL-EXTR', 3800.0, 9800.0, 1600.0, 200.0)
    add_rect(msp, 'A-WALL-EXTR', 9400.0, 9800.0, 600.0, 200.0)

    # North Entry: 1800mm Double-Swing Door (X = 2000 to 3800)
    add_double_swing_door(msp, center_x=2900.0, wall_y=9800.0, total_width=1800.0, wall_thk=200.0)
    # North Storefront Window: 4000mm Glazing (X = 5400 to 9400)
    add_window(msp, (5400.0, 9800.0), (9400.0, 9800.0), wall_thk=200.0)

    # Entrance Plinth Steps (3 steps = +600mm level change, risers 200mm, treads 300mm)
    # Projecting out into North plaza (Y = 10000 to 10900, X = 1700 to 4100)
    step_w = 2400.0
    sx0 = 1700.0
    for i, sy in enumerate([10000.0, 10300.0, 10600.0, 10900.0]):
        add_line(msp, 'A-STAIR', (sx0, sy), (sx0 + step_w, sy))
    add_line(msp, 'A-STAIR', (sx0, 10000.0), (sx0, 10900.0))
    add_line(msp, 'A-STAIR', (sx0 + step_w, 10000.0), (sx0 + step_w, 10900.0))
    # Text positioned cleanly outside the step edges
    add_text(msp, 'A-STAIR', 'ENTRANCE PLINTH (3 STEPS +600mm)', (2900.0, 11150.0), height=120, align='CENTER')

    # SOUTH FACADE (Y = 0 to 200)
    # Wall piers: 0-1200, 4200-5800, 8800-10000
    add_rect(msp, 'A-WALL-EXTR', 0.0, 0.0, 1200.0, 200.0)
    add_rect(msp, 'A-WALL-EXTR', 4200.0, 0.0, 1600.0, 200.0)
    add_rect(msp, 'A-WALL-EXTR', 8800.0, 0.0, 1200.0, 200.0)
    # South Windows: (1200 to 4200: 3000mm) & (5800 to 8800: 3000mm)
    add_window(msp, (1200.0, 0.0), (4200.0, 0.0), wall_thk=200.0)
    add_window(msp, (5800.0, 0.0), (8800.0, 0.0), wall_thk=200.0)

    # WEST FACADE (X = 0 to 200)
    # Wall piers: 0-1200 (south corner), 4200-7600 (prep zone solid wall), 9400-10000 (north corner)
    add_rect(msp, 'A-WALL-EXTR', 0.0, 0.0, 200.0, 1200.0)
    add_rect(msp, 'A-WALL-EXTR', 0.0, 4200.0, 200.0, 3400.0)
    add_rect(msp, 'A-WALL-EXTR', 0.0, 9400.0, 200.0, 600.0)
    # West Windows: (1200 to 4200: 3000mm dining window) & (7600 to 9400: 1800mm lounge window)
    add_window(msp, (0.0, 1200.0), (0.0, 4200.0), wall_thk=200.0)
    add_window(msp, (0.0, 7600.0), (0.0, 9400.0), wall_thk=200.0)

    # EAST FACADE (X = 9800 to 10000)
    # Wall piers: 0-2200 (restroom), 5000-7500 (stair core solid backing), 8800-10000 (north corner)
    add_rect(msp, 'A-WALL-EXTR', 9800.0, 0.0, 200.0, 2200.0)
    add_rect(msp, 'A-WALL-EXTR', 9800.0, 5000.0, 200.0, 2500.0)
    add_rect(msp, 'A-WALL-EXTR', 9800.0, 8800.0, 200.0, 1200.0)
    # East Windows: (2200 to 5000: 2800mm dining window) & (7500 to 8800: 1300mm window)
    add_window(msp, (9800.0, 2200.0), (9800.0, 5000.0), wall_thk=200.0)
    add_window(msp, (9800.0, 7500.0), (9800.0, 8800.0), wall_thk=200.0)

    # 3. Barista Counter & Prep Zone
    draw_barista_counter(msp)

    # 4. PWD Restroom (Southeast Corner)
    draw_pwd_restroom(msp, x_base=7800.0, y_base=200.0)

    # 5. U-Shaped Staircase Core (East Wall)
    draw_u_stairs(msp, x_base=7800.0, y_base=5000.0, is_second_floor=False)

    # 6. Seating Furniture Blocks
    # South Dining Zone
    draw_table_4top(msp, cx=2700.0, cy=1400.0)
    draw_table_4top(msp, cx=5800.0, cy=1400.0)
    # East Lounge / Dining Zone
    draw_round_table_3top(msp, cx=6500.0, cy=3500.0, radius=400.0)
    # Window Counter Seating along North Storefront (X = 5800 to 9000, Y = 9400)
    add_rect(msp, 'A-FURN', 5800.0, 9400.0, 3200.0, 400.0)
    for sx in [6200.0, 7000.0, 7800.0, 8600.0]:
        msp.add_circle((sx, 9150.0), 160.0, dxfattribs={'layer': 'A-FURN', 'color': 7})
    # Label placed in open walkway clear of counter and stool lines
    add_text(msp, 'A-FURN', 'WINDOW WORK BAR (HIGH STOOLS)', (7400.0, 8850.0), height=120, align='CENTER')

    # 7. Annotations & Room Tags (positioned with generous clearances from all lines)
    add_text(msp, 'A-ANNO-TEXT', 'MAIN DINING & SEATING', (5000.0, 2400.0), height=200, align='CENTER')
    add_text(msp, 'A-ANNO-TEXT', 'MAIN ENTRY AIRLOCK', (2900.0, 8100.0), height=140, align='CENTER')
    add_text(msp, 'A-ANNO-TEXT', 'GROUND FLOOR PLAN', (5000.0, -2100.0), height=320, align='CENTER')
    add_text(msp, 'A-ANNO-TEXT', 'FFL +0.600m  |  SCALE 1:100', (5000.0, -2450.0), height=180, align='CENTER')

    # 8. Linear Dimension Chains along Perimeter
    # South String Dims (Bay to Bay)
    add_dimension_string(msp, [(0.0, 0.0), (5000.0, 0.0), (10000.0, 0.0)], base_y=0, is_horizontal=True, base_coord=-800.0)
    # South Overall Dim
    add_dimension_string(msp, [(0.0, 0.0), (10000.0, 0.0)], base_y=0, is_horizontal=True, base_coord=-1400.0)

    # West String Dims
    add_dimension_string(msp, [(0.0, 0.0), (0.0, 5000.0), (0.0, 10000.0)], base_y=0, is_horizontal=False, base_coord=-800.0)
    # West Overall Dim
    add_dimension_string(msp, [(0.0, 0.0), (0.0, 10000.0)], base_y=0, is_horizontal=False, base_coord=-1400.0)

    # East String Dims
    add_dimension_string(msp, [(10000.0, 0.0), (10000.0, 5000.0), (10000.0, 10000.0)], base_y=0, is_horizontal=False, base_coord=10800.0)
    add_dimension_string(msp, [(10000.0, 0.0), (10000.0, 10000.0)], base_y=0, is_horizontal=False, base_coord=11400.0)

    # North Dims (Openings)
    n_pts = [(0.0, 10000.0), (2000.0, 10000.0), (3800.0, 10000.0), (5400.0, 10000.0), (9400.0, 10000.0), (10000.0, 10000.0)]
    add_dimension_string(msp, n_pts, base_y=0, is_horizontal=True, base_coord=11500.0)
    add_dimension_string(msp, [(0.0, 10000.0), (10000.0, 10000.0)], base_y=0, is_horizontal=True, base_coord=12100.0)


def build_second_floor(msp, x_offset=15000.0):
    """
    Constructs the Second Floor architectural plan:
    - Same boundary footprint (10000x10000mm) offset by X = +15,000mm
    - Cantilevered Balcony (2500mm projection on North facade)
    - Stair opening void with non-intersecting diagonal cross lines
    - Double-height acoustic void with protected label badge
    - Communal table (3000mm x 1000mm) at center
    - Perimeter work counters and lounge seating
    """
    xo = x_offset

    # 1. Structural Grid & Columns
    draw_grid_system(msp, x_offset=xo, suffix="'")
    draw_columns(msp, x_offset=xo)

    # 2. Exterior Perimeter Walls (200mm thick)
    # SOUTH FACADE (Y = 0 to 200)
    add_rect(msp, 'A-WALL-EXTR', xo + 0.0, 0.0, 1500.0, 200.0)
    add_rect(msp, 'A-WALL-EXTR', xo + 4500.0, 0.0, 1000.0, 200.0)
    add_rect(msp, 'A-WALL-EXTR', xo + 8500.0, 0.0, 1500.0, 200.0)
    add_window(msp, (xo + 1500.0, 0.0), (xo + 4500.0, 0.0), wall_thk=200.0)
    add_window(msp, (xo + 5500.0, 0.0), (xo + 8500.0, 0.0), wall_thk=200.0)

    # WEST FACADE (X = xo + 0 to xo + 200)
    add_rect(msp, 'A-WALL-EXTR', xo + 0.0, 0.0, 200.0, 2000.0)
    add_rect(msp, 'A-WALL-EXTR', xo + 0.0, 8000.0, 200.0, 2000.0)
    add_window(msp, (xo + 0.0, 2000.0), (xo + 0.0, 8000.0), wall_thk=200.0)  # 6m panoramic west window

    # EAST FACADE (X = xo + 9800 to xo + 10000)
    add_rect(msp, 'A-WALL-EXTR', xo + 9800.0, 0.0, 200.0, 2200.0)
    add_rect(msp, 'A-WALL-EXTR', xo + 9800.0, 5000.0, 200.0, 2500.0)
    add_rect(msp, 'A-WALL-EXTR', xo + 9800.0, 8500.0, 200.0, 1500.0)
    add_window(msp, (xo + 9800.0, 2200.0), (xo + 9800.0, 5000.0), wall_thk=200.0)
    add_window(msp, (xo + 9800.0, 7500.0), (xo + 9800.0, 8500.0), wall_thk=200.0)

    # NORTH FACADE & BALCONY CONNECTION (Y = 9800 to 10000)
    add_rect(msp, 'A-WALL-EXTR', xo + 0.0, 9800.0, 2500.0, 200.0)
    add_rect(msp, 'A-WALL-EXTR', xo + 7500.0, 9800.0, 2500.0, 200.0)
    # 5000mm Sliding Glass Balcony Portal (X = xo + 2500 to xo + 7500)
    add_window(msp, (xo + 2500.0, 9800.0), (xo + 7500.0, 9800.0), wall_thk=200.0)
    # Portal label placed in open room area (clear of window frame lines)
    add_text(msp, 'A-DOOR', 'SLIDING GLASS BALCONY ACCESS', (xo + 5000.0, 9450.0), height=130, align='CENTER')

    # 3. CANTILEVERED BALCONY (2500mm Projection on North Facade: Y = 10000 to 12500)
    balc_pts = [
        (xo + 0.0, 10000.0),
        (xo + 0.0, 12500.0),
        (xo + 10000.0, 12500.0),
        (xo + 10000.0, 10000.0)
    ]
    msp.add_lwpolyline(balc_pts, close=False, dxfattribs={'layer': 'A-WALL-EXTR', 'color': 7})

    # Glass Balustrade / Perimeter Railing (100mm offset)
    balustrade_pts = [
        (xo + 50.0, 10000.0),
        (xo + 50.0, 12450.0),
        (xo + 9950.0, 12450.0),
        (xo + 9950.0, 10000.0)
    ]
    msp.add_lwpolyline(balustrade_pts, close=False, dxfattribs={'layer': 'A-GLAZ', 'color': 7})
    add_text(msp, 'A-WALL-EXTR', '1100mm TEMPERED GLASS BALUSTRADE', (xo + 5000.0, 12050.0), height=110, align='CENTER')

    # Balcony Cafe Seating: 3 Round Tables (Ø700mm)
    for bx in [xo + 2000.0, xo + 5000.0, xo + 8000.0]:
        draw_round_table_3top(msp, cx=bx, cy=11200.0, radius=350.0)
    add_text(msp, 'A-ANNO-TEXT', 'CANTILEVERED OUTDOOR BALCONY', (xo + 5000.0, 11700.0), height=180, align='CENTER')
    add_text(msp, 'A-ANNO-TEXT', 'BALCONY FFL +3.950m', (xo + 5000.0, 10600.0), height=130, align='CENTER')

    # 4. Stair Core & Opening Void (Second Floor)
    draw_u_stairs(msp, x_base=xo + 7800.0, y_base=5000.0, is_second_floor=True)

    # 5. Central Double-Height Acoustic Void above Barista Counter with Protected Badge
    void_pts = [
        (xo + 1200.0, 4000.0),
        (xo + 3800.0, 4000.0),
        (xo + 3800.0, 7000.0),
        (xo + 1200.0, 7000.0)
    ]
    msp.add_lwpolyline(void_pts, close=True, dxfattribs={'layer': 'A-WALL-INTR', 'color': 7})
    # Guardrail around void (100mm offset)
    add_rect(msp, 'A-GLAZ', xo + 1300.0, 4100.0, 2400.0, 2800.0)

    # Central Void Label Box (boundary stops all diagonal cross lines so text is NEVER covered)
    abx1, abx2 = xo + 1500.0, xo + 3500.0
    aby1, aby2 = 5175.0, 5825.0
    add_rect(msp, 'A-WALL-INTR', abx1, aby1, abx2 - abx1, aby2 - aby1)

    # Diagonal void crossing lines terminating cleanly at label badge box
    add_line(msp, 'A-WALL-INTR', (xo + 1200.0, 4000.0), (abx1, aby1), linetype='DASHED')
    add_line(msp, 'A-WALL-INTR', (xo + 3800.0, 4000.0), (abx2, aby1), linetype='DASHED')
    add_line(msp, 'A-WALL-INTR', (xo + 1200.0, 7000.0), (abx1, aby2), linetype='DASHED')
    add_line(msp, 'A-WALL-INTR', (xo + 3800.0, 7000.0), (abx2, aby2), linetype='DASHED')

    add_text(msp, 'A-ANNO-TEXT', 'DOUBLE-HEIGHT ATRIUM VOID', (xo + 2500.0, 5580.0), height=150, align='CENTER')
    add_text(msp, 'A-ANNO-TEXT', 'OPEN TO GROUND FLOOR BAR', (xo + 2500.0, 5350.0), height=120, align='CENTER')

    # 6. COMMUNAL TABLE (3000mm x 1000mm) AT CENTER (Clean middle area for text)
    tbl_x, tbl_y = xo + 4800.0, 4500.0
    tbl_w, tbl_h = 3000.0, 1000.0
    add_rect(msp, 'A-FURN', tbl_x, tbl_y, tbl_w, tbl_h)

    # Dual power grommet modules flanking clear center label area
    add_rect(msp, 'A-FURN', tbl_x + 350.0, tbl_y + 420.0, 500.0, 160.0)
    add_rect(msp, 'A-FURN', tbl_x + 2150.0, tbl_y + 420.0, 500.0, 160.0)
    add_text(msp, 'A-FURN', 'POWER', (tbl_x + 600.0, tbl_y + 500.0), height=75, align='CENTER')
    add_text(msp, 'A-FURN', 'POWER', (tbl_x + 2400.0, tbl_y + 500.0), height=75, align='CENTER')

    # 10 Ergonomic Chairs around Communal Table
    for i in range(4):
        cx = tbl_x + 375.0 + i * 750.0
        add_rect(msp, 'A-FURN', cx - 225.0, tbl_y + tbl_h + 80.0, 450.0, 400.0)
        add_rect(msp, 'A-FURN', cx - 225.0, tbl_y - 480.0, 450.0, 400.0)
    add_rect(msp, 'A-FURN', tbl_x - 480.0, tbl_y + 275.0, 400.0, 450.0)
    add_rect(msp, 'A-FURN', tbl_x + tbl_w + 80.0, tbl_y + 275.0, 400.0, 450.0)

    # Communal Table Annotation placed in clear center of table
    add_text(msp, 'A-ANNO-TEXT', 'COMMUNAL WORK TABLE', (tbl_x + 1500.0, tbl_y + 580.0), height=130, align='CENTER')
    add_text(msp, 'A-ANNO-TEXT', '10-SEATER | INTEGRATED POWER', (tbl_x + 1500.0, tbl_y + 380.0), height=105, align='CENTER')

    # 7. Perimeter Workstation Counters & Lounge Furniture
    add_rect(msp, 'A-FURN', xo + 200.0, 2000.0, 500.0, 1800.0)
    for sy in [2400.0, 3200.0]:
        msp.add_circle((xo + 900.0, sy), 170.0, dxfattribs={'layer': 'A-FURN', 'color': 7})
    add_text(msp, 'A-FURN', 'INDIVIDUAL STUDY BAR', (xo + 1350.0, 2900.0), height=110, rotation=90, align='CENTER')

    # South Lounge Area
    add_rect(msp, 'A-FURN', xo + 1800.0, 500.0, 1800.0, 850.0)
    add_rect(msp, 'A-FURN', xo + 2100.0, 1550.0, 1200.0, 500.0)
    add_text(msp, 'A-FURN', 'LOUNGE SOFA', (xo + 2700.0, 925.0), height=120, align='CENTER')

    # Second Floor Executive Restroom (Stacked)
    add_rect(msp, 'A-WALL-INTR', xo + 7700.0, 200.0, 100.0, 2100.0)
    add_rect(msp, 'A-WALL-INTR', xo + 7700.0, 2200.0, 2100.0, 100.0)
    add_single_door(msp, (xo + 7700.0, 900.0), width=900.0, wall_thk=100.0, direction='W', inward=True)
    add_rect(msp, 'A-FURN', xo + 9200.0, 450.0, 500.0, 200.0)
    add_rect(msp, 'A-FURN', xo + 9260.0, 650.0, 380.0, 450.0)
    add_rect(msp, 'A-FURN', xo + 8000.0, 1750.0, 550.0, 400.0)
    msp.add_circle((xo + 8275.0, 1950.0), 110.0, dxfattribs={'layer': 'A-FURN', 'color': 7})
    add_text(msp, 'A-ANNO-TEXT', 'RESTROOM', (xo + 8800.0, 1400.0), height=150, align='CENTER')

    # 8. Annotations & Room Tags
    add_text(msp, 'A-ANNO-TEXT', 'SECOND FLOOR PLAN', (xo + 5000.0, -2100.0), height=320, align='CENTER')
    add_text(msp, 'A-ANNO-TEXT', 'FFL +4.000m  |  SCALE 1:100', (xo + 5000.0, -2450.0), height=180, align='CENTER')

    # 9. Dimension Chains for Second Floor
    add_dimension_string(msp, [(xo + 0.0, 0.0), (xo + 5000.0, 0.0), (xo + 10000.0, 0.0)], base_y=0, is_horizontal=True, base_coord=-800.0)
    add_dimension_string(msp, [(xo + 0.0, 0.0), (xo + 10000.0, 0.0)], base_y=0, is_horizontal=True, base_coord=-1400.0)
    add_dimension_string(msp, [(xo + 10000.0, 0.0), (xo + 10000.0, 5000.0), (xo + 10000.0, 10000.0)], base_y=0, is_horizontal=False, base_coord=xo + 10800.0)
    add_dimension_string(msp, [(xo + 10000.0, 0.0), (xo + 10000.0, 10000.0)], base_y=0, is_horizontal=False, base_coord=xo + 11400.0)

    balc_dim_pts = [(xo + 0.0, 10000.0), (xo + 0.0, 12500.0)]
    add_dimension_string(msp, balc_dim_pts, base_y=0, is_horizontal=False, base_coord=xo - 800.0)
    add_dimension_string(msp, [(xo + 0.0, 12500.0), (xo + 10000.0, 12500.0)], base_y=0, is_horizontal=True, base_coord=13300.0)


def draw_title_block_and_symbols(msp):
    """Draws a professional architectural title block, project header, and true North arrow."""
    # North Arrow Symbol
    na_x, na_y = 5000.0, 13200.0
    msp.add_circle((na_x, na_y), 450.0, dxfattribs={'layer': 'A-ANNO-SYMB', 'color': 7})
    # Arrowhead
    arrow_pts = [(na_x, na_y + 430.0), (na_x - 120.0, na_y - 200.0), (na_x, na_y - 120.0)]
    msp.add_lwpolyline(arrow_pts, close=True, dxfattribs={'layer': 'A-ANNO-SYMB', 'color': 7})
    arrow_pts2 = [(na_x, na_y + 430.0), (na_x + 120.0, na_y - 200.0), (na_x, na_y - 120.0)]
    msp.add_lwpolyline(arrow_pts2, close=True, dxfattribs={'layer': 'A-ANNO-SYMB', 'color': 7})
    add_text(msp, 'A-ANNO-SYMB', 'N', (na_x, na_y + 550.0), height=260, align='CENTER')

    # Project Information Banner / Title Block (Bottom Border)
    bx0, by0 = -2000.0, -3200.0
    bw, bh = 29000.0, 700.0
    add_rect(msp, 'A-ANNO-TEXT', bx0, by0, bw, bh)
    add_line(msp, 'A-ANNO-TEXT', (bx0, by0 + 350.0), (bx0 + bw, by0 + 350.0))

    # Column partitions inside title block
    col_divs = [bx0 + 7000.0, bx0 + 15000.0, bx0 + 22000.0]
    for cdx in col_divs:
        add_line(msp, 'A-ANNO-TEXT', (cdx, by0), (cdx, by0 + bh))

    # Title Block Text
    add_text(msp, 'A-ANNO-TEXT', 'PROJECT: 2-STOREY SPECIALTY COFFEE SHOP', (bx0 + 200.0, by0 + 470.0), height=180)
    add_text(msp, 'A-ANNO-TEXT', 'LOCATION: BURGOS, PAKIL, LAGUNA, PHILIPPINES', (bx0 + 200.0, by0 + 130.0), height=140)

    add_text(msp, 'A-ANNO-TEXT', 'DRAWING TITLE: ARCHITECTURAL FLOOR PLANS', (bx0 + 7200.0, by0 + 470.0), height=180)
    add_text(msp, 'A-ANNO-TEXT', 'LEVELS: GROUND FLOOR (+0.600m) & SECOND FLOOR (+4.000m)', (bx0 + 7200.0, by0 + 130.0), height=140)

    add_text(msp, 'A-ANNO-TEXT', 'DISCIPLINE: COMPUTATIONAL ARCHITECTURE', (bx0 + 15200.0, by0 + 470.0), height=180)
    add_text(msp, 'A-ANNO-TEXT', 'UNITS: MILLIMETERS (MM) | CAD ACI COLOR 7 (MONOCHROME)', (bx0 + 15200.0, by0 + 130.0), height=140)

    add_text(msp, 'A-ANNO-TEXT', 'STATUS: SCHEMATIC DESIGN / CAD COMPILATION', (bx0 + 22200.0, by0 + 470.0), height=180)
    add_text(msp, 'A-ANNO-TEXT', 'SHEET: A-101 | SCALE 1:100 @ A3', (bx0 + 22200.0, by0 + 130.0), height=140)


# ==============================================================================
# MAIN EXECUTION PIPELINE
# ==============================================================================

def export_to_svg(dxf_path, svg_path):
    """Exports DXF modelspace into high-precision, Figma-ready monochrome SVG."""
    from ezdxf.addons.drawing import Frontend, RenderContext, layout
    from ezdxf.addons.drawing.svg import SVGBackend
    from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy, ColorPolicy

    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    ctx = RenderContext(doc)
    cfg = Configuration(
        background_policy=BackgroundPolicy.WHITE,
        color_policy=ColorPolicy.BLACK
    )
    backend = SVGBackend()
    frontend = Frontend(ctx, backend, config=cfg)

    # Sort entities: Linework/geometry drawn first, all text annotations drawn LAST (on top)
    non_text = [e for e in msp if e.dxftype() not in ('TEXT', 'MTEXT')]
    text_entities = [e for e in msp if e.dxftype() in ('TEXT', 'MTEXT')]
    frontend.draw_entities(non_text + text_entities)

    page = layout.Page.from_dxf_layout(msp)
    settings = layout.Settings(fit_page=True)
    svg_str = backend.get_string(page, settings=settings)

    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_str)
    file_size_kb = os.path.getsize(svg_path) / 1024.0
    print(f"SUCCESS: Figma-ready SVG generated successfully: '{svg_path}' ({file_size_kb:.2f} KB).")


def generate_coffee_shop_dxf(output_path="coffee_shop_pakil_laguna.dxf"):
    """Orchestrates complete CAD document creation, drafting, and file export."""
    print("=" * 70)
    print("COMPUTATIONAL ARCHITECTURAL DRAFTING ENGINE")
    print("Project: 2-Storey Coffee Shop in Burgos, Pakil, Laguna")
    print("Target Standard: Strict Monochrome ACI 7, Metric (mm), 1:100 Scale")
    print("=" * 70)

    # 1. Initialize Document & Design Environment
    doc = setup_document()
    msp = doc.modelspace()

    # 2. Build Architectural Blocks
    print("[1/5] Drafting Ground Floor Plan...")
    build_ground_floor(msp)

    print("[2/5] Drafting Second Floor Plan (Offset X = +15,000mm)...")
    build_second_floor(msp, x_offset=15000.0)

    print("[3/5] Adding Title Block, Project Header & True North Arrow...")
    draw_title_block_and_symbols(msp)

    # 3. Export DXF
    print(f"[4/5] Compiling and saving DXF to '{output_path}'...")
    doc.saveas(output_path)
    file_size_kb = os.path.getsize(output_path) / 1024.0
    print(f"SUCCESS: DXF generated successfully ({file_size_kb:.2f} KB).")

    # 4. Export Figma-Ready SVG
    svg_output = output_path.replace(".dxf", ".svg")
    print(f"[5/5] Compiling Figma-ready vector SVG to '{svg_output}'...")
    export_to_svg(output_path, svg_output)
    print("=" * 70)
    return output_path


if __name__ == "__main__":
    generate_coffee_shop_dxf()
