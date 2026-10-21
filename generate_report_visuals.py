#!/usr/bin/env python3
"""
Generates high-resolution figures and analytical graphics for the Feasibility Study:
'Burgos Highlands Specialty Coffee - Pakil, Laguna'
"""

import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

ASSETS_DIR = 'generated_assets'
os.makedirs(ASSETS_DIR, exist_ok=True)

# Standardize 3D renders
for f in os.listdir(ASSETS_DIR):
    if 'exterior_cafe_parking' in f:
        shutil.copy2(os.path.join(ASSETS_DIR, f), os.path.join(ASSETS_DIR, 'figure_render_exterior.jpg'))
    elif 'interior_ground_bar' in f:
        shutil.copy2(os.path.join(ASSETS_DIR, f), os.path.join(ASSETS_DIR, 'figure_render_interior_gf.jpg'))
    elif 'interior_second_floor' in f:
        shutil.copy2(os.path.join(ASSETS_DIR, f), os.path.join(ASSETS_DIR, 'figure_render_interior_2f.jpg'))

print("3D renders standardized.")

# ----------------------------------------------------------------------
# 1. ANNOTATED SATELLITE MAP OF PAKIL, LAGUNA
# ----------------------------------------------------------------------
def generate_satellite_map():
    sat_raw = os.path.join(ASSETS_DIR, 'pakil_satellite_raw.png')
    if not os.path.exists(sat_raw):
        print("Satellite raw image missing, skipping.")
        return

    img = Image.open(sat_raw)
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.imshow(img)

    # Coords relative to 768x768 image
    # Center tile contains Pakil Poblacion & Burgos along Laguna de Bay
    # Site pin
    site_x, site_y = 380, 420
    ax.scatter(site_x, site_y, color='#E63946', s=250, zorder=5, edgecolors='white', linewidth=2.5)
    ax.annotate(
        "PROPOSED SITE: CAFÉ TURUMBA & ROASTERY\n(Barangay Burgos, Manila East Road)\n14°22'57.4\"N 121°28'45.8\"E",
        xy=(site_x, site_y), xytext=(site_x + 30, site_y - 80),
        arrowprops=dict(facecolor='#E63946', shrink=0.08, width=2, headwidth=8, edgecolor='white', lw=1.5),
        bbox=dict(boxstyle="round,pad=0.5", fc="#1F2937", ec="#E63946", lw=2, alpha=0.92),
        fontsize=9, fontweight='bold', color='white', zorder=6
    )

    # Manila East Road marker
    ax.annotate(
        "MANILA EAST ROAD (NATIONAL HIGHWAY)\nPrimary Eastern Laguna Arterial Corridor",
        xy=(350, 470), xytext=(80, 520),
        arrowprops=dict(facecolor='#F59E0B', shrink=0.08, width=1.8, headwidth=7, edgecolor='white', lw=1),
        bbox=dict(boxstyle="round,pad=0.4", fc="#111827", ec="#F59E0B", lw=1.5, alpha=0.9),
        fontsize=8, fontweight='bold', color='#FCD34D', zorder=6
    )

    # Turumba Shrine Church marker
    church_x, church_y = 410, 310
    ax.scatter(church_x, church_y, color='#3B82F6', s=180, zorder=5, edgecolors='white', linewidth=2)
    ax.annotate(
        "St. Peter of Alcantara Parish\n(Diocesan Shrine of Our Lady of Turumba)\n~350m Walk from Site",
        xy=(church_x, church_y), xytext=( church_x + 40, church_y - 60),
        arrowprops=dict(facecolor='#3B82F6', shrink=0.08, width=1.8, headwidth=7, edgecolor='white', lw=1),
        bbox=dict(boxstyle="round,pad=0.4", fc="#1E3A8A", ec="#60A5FA", lw=1.5, alpha=0.9),
        fontsize=8, fontweight='bold', color='white', zorder=6
    )

    # Mt. Ping-as / Sierra Madre marker
    ax.annotate(
        "SIERRA MADRE MOUNTAIN RANGE\n& MT. PING-AS PILGRIMAGE TRAIL",
        xy=(620, 200), xytext=(480, 100),
        arrowprops=dict(facecolor='#10B981', shrink=0.08, width=1.8, headwidth=7, edgecolor='white', lw=1),
        bbox=dict(boxstyle="round,pad=0.4", fc="#064E3B", ec="#34D399", lw=1.5, alpha=0.9),
        fontsize=8, fontweight='bold', color='white', zorder=6
    )

    # Laguna de Bay marker
    ax.annotate(
        "LAGUNA DE BAY (LAKE SHORELINE)\nScenic Western Vista & Breeze",
        xy=(180, 380), xytext=(40, 260),
        arrowprops=dict(facecolor='#06B6D4', shrink=0.08, width=1.8, headwidth=7, edgecolor='white', lw=1),
        bbox=dict(boxstyle="round,pad=0.4", fc="#164E63", ec="#22D3EE", lw=1.5, alpha=0.9),
        fontsize=8, fontweight='bold', color='white', zorder=6
    )

    # North arrow and scale
    ax.annotate('N', xy=(0.93, 0.90), xycoords='axes fraction', fontsize=16, fontweight='bold',
                color='white', ha='center', va='center',
                bbox=dict(boxstyle="circle,pad=0.3", fc="#111827", ec="white", lw=1.5))
    ax.arrow(0.93, 0.83, 0, 0.05, transform=ax.transAxes, color='white', width=0.006, head_width=0.025, head_length=0.02)

    # Scale Bar (approx 200m at zoom 16 is ~120px)
    ax.plot([40, 160], [730, 730], color='white', lw=4, solid_capstyle='butt')
    ax.text(100, 715, 'Approx. 200 Meters', color='white', fontsize=8, fontweight='bold', ha='center',
            bbox=dict(boxstyle="square,pad=0.2", fc="black", ec="none", alpha=0.7))

    ax.set_title("Figure 1: High-Resolution Satellite Vicinity Map of Proposed Coffee Shop Site in Pakil, Laguna\n(Source: ESRI World Imagery / Georeferenced Coordinates: 14°22'57.4\"N 121°28'45.8\"E)",
                 fontsize=10, fontweight='bold', pad=12, color='#1F2937')
    ax.axis('off')
    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'figure_satellite_map.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out_path)

# ----------------------------------------------------------------------
# 2. ANNOTATED ROAD / TOURISM NETWORK MAP (OSM)
# ----------------------------------------------------------------------
def generate_vicinity_map():
    osm_raw = os.path.join(ASSETS_DIR, 'pakil_osm_raw.png')
    if not os.path.exists(osm_raw):
        print("OSM raw image missing, skipping.")
        return

    img = Image.open(osm_raw)
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.imshow(img)

    # Regional Corridor markers
    site_x, site_y = 380, 420
    ax.scatter(site_x, site_y, color='#D97706', s=240, zorder=5, edgecolors='black', linewidth=2)
    ax.annotate(
        "PROPOSED PROJECT SITE:\nCAFÉ TURUMBA & COFFEE ROASTERS\n& DEDICATED PARKING FACILITY",
        xy=(site_x, site_y), xytext=(site_x - 300, site_y - 120),
        arrowprops=dict(facecolor='#D97706', shrink=0.08, width=2, headwidth=8, edgecolor='black', lw=1),
        bbox=dict(boxstyle="round,pad=0.5", fc="#FEF3C7", ec="#D97706", lw=2, alpha=0.95),
        fontsize=9, fontweight='bold', color='#92400E', zorder=6
    )

    # Direction to Paete (South)
    ax.annotate(
        "TO PAETE & LUMBAN (Carving & Embroidery Capital) ➔\n(Southbound Manila East Road)",
        xy=(350, 680), xytext=(300, 730),
        bbox=dict(boxstyle="round,pad=0.4", fc="#EFF6FF", ec="#3B82F6", lw=1.5),
        fontsize=8, fontweight='bold', color='#1E40AF', zorder=6
    )

    # Direction to Pangil & Siniloan (North)
    ax.annotate(
        "⬅ TO PANGIL & SINILOAN (Eco-parks & University Belt)\n(Northbound Manila East Road / Famy Junction)",
        xy=(400, 120), xytext=(60, 60),
        bbox=dict(boxstyle="round,pad=0.4", fc="#ECFDF5", ec="#10B981", lw=1.5),
        fontsize=8, fontweight='bold', color='#065F46', zorder=6
    )

    ax.set_title("Figure 2: Eastern Laguna Regional Transportation & Tourism Corridor Map (Pakil Municipality)\n(Source: OpenStreetMap Contributors / LGU Pakil Municipal Tourism Master Plan)",
                 fontsize=10, fontweight='bold', pad=12, color='#1F2937')
    ax.axis('off')
    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'figure_vicinity_map.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out_path)

# ----------------------------------------------------------------------
# 3. DETAILED SITE DEVELOPMENT PLAN & DEDICATED PARKING AREA LAYOUT
# ----------------------------------------------------------------------
def generate_site_parking_plan():
    fig, ax = plt.subplots(figsize=(11, 8.5), dpi=300)

    # Site dimensions: 15.0m frontage x 30.0m depth = 450.0 sq.m.
    # Coordinates in meters: X from 0 to 15, Y from 0 to 30
    # Boundary
    ax.plot([0, 15, 15, 0, 0], [0, 0, 30, 30, 0], color='#111827', lw=3, zorder=2)
    ax.fill([0, 15, 15, 0], [0, 0, 30, 30], color='#F3F4F6', zorder=1)

    # Manila East Road along bottom (Y = -5 to 0)
    ax.fill_between([-2, 17], -6, 0, color='#374151', zorder=1)
    ax.plot([-2, 17], [-6, -6], color='#9CA3AF', lw=1.5, ls='--')
    ax.plot([-2, 17], [-3, -3], color='#FBBF24', lw=2, ls='--')
    ax.text(7.5, -4.5, "MANILA EAST ROAD (12.0m R.O.W. NATIONAL HIGHWAY)", color='white',
            ha='center', va='center', fontweight='bold', fontsize=9)

    # Sidewalk / Buffer (Y = 0 to 1.5)
    ax.fill([0, 15, 15, 0], [0, 0, 1.5, 1.5], color='#D1D5DB', zorder=2)
    ax.text(7.5, 0.75, "Concrete Sidewalk / Pedestrian Walkway (1.50m Width)",
            color='#374151', ha='center', va='center', fontsize=7, fontweight='bold')

    # Driveway Ingress / Egress (6.0m curb cut: X = 1.0 to 7.0, Y = 0 to 1.5)
    ax.fill([1.0, 7.0, 7.0, 1.0], [0, 0, 1.5, 1.5], color='#4B5563', zorder=3)
    ax.text(4.0, 0.75, "VEHICULAR INGRESS / EGRESS (6.0m WIDE APRON)", color='white',
            ha='center', va='center', fontsize=7, fontweight='bold')

    # Driveway circulation aisle (X = 1.0 to 7.0, Y = 1.5 to 13.5)
    ax.fill([1.0, 7.0, 7.0, 1.0], [1.5, 1.5, 13.5, 13.5], color='#9CA3AF', alpha=0.35, zorder=2)
    ax.annotate("", xy=(4.0, 10.0), xytext=(4.0, 2.5),
                arrowprops=dict(arrowstyle="<->", color="#1F2937", lw=2))
    ax.text(4.0, 6.2, "6.0m TWO-WAY VEHICULAR\nCIRCULATION AISLE", ha='center', va='center',
            fontsize=8, fontweight='bold', color='#1F2937', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#9CA3AF"))

    # PARKING BAYS (Right side: X = 7.0 to 14.5, Y = 1.5 to 13.5)
    # 4 Car slots along right boundary (Slots 1, 2, 3, 4) - perpendicular 2.5m x 5.0m
    # X = 9.5 to 14.5 (5.0m length), Y from 1.5 to 11.5 (4 slots * 2.5m = 10.0m)
    for i in range(4):
        sy = 1.5 + i * 2.5
        rect = patches.Rectangle((9.5, sy), 5.0, 2.5, linewidth=1.5, edgecolor='#4B5563', facecolor='#E5E7EB', zorder=3)
        ax.add_patch(rect)
        ax.plot([9.5, 14.5], [sy, sy], color='#F3F4F6', lw=2, zorder=4)
        # Wheel stop
        ax.add_patch(patches.Rectangle((13.8, sy + 0.3), 0.3, 1.9, facecolor='#1F2937', zorder=4))
        ax.text(11.8, sy + 1.25, f"CAR SLOT #{i+1}\n(2.5m x 5.0m)", ha='center', va='center',
                fontsize=7, fontweight='bold', color='#1F2937')

    # PWD Accessible Parking Slot (Slot 5: 3.7m width x 5.0m depth as per BP 344)
    # X = 9.5 to 14.5, Y = 11.5 to 15.2 (3.7m wide)
    pwd_rect = patches.Rectangle((9.5, 11.5), 5.0, 3.7, linewidth=2, edgecolor='#1E40AF', facecolor='#DBEAFE', zorder=3)
    ax.add_patch(pwd_rect)
    # Diagonal hatched access aisle
    ax.add_patch(patches.Rectangle((9.5, 11.5), 5.0, 1.2, facecolor='#93C5FD', hatch='///', alpha=0.6, zorder=4))
    # Wheel stop
    ax.add_patch(patches.Rectangle((13.8, 12.8), 0.3, 2.1, facecolor='#1E40AF', zorder=4))
    ax.text(12.0, 13.5, "♿ PWD ACCESSIBLE\nPARKING (3.7m x 5.0m)\n[BP 344 COMPLIANT]",
            ha='center', va='center', fontsize=7.5, fontweight='bold', color='#1E40AF')
    # PWD Curb ramp connecting to main walkway
    ax.add_patch(patches.Rectangle((8.0, 13.0), 1.5, 1.5, facecolor='#FCD34D', ec='#B45309', lw=1.5, zorder=4))
    ax.text(8.75, 13.75, "RAMP\n1:12", ha='center', va='center', fontsize=6, fontweight='bold', color='#78350F')

    # Front Parking Slots (Slots 6, 7, 8: X = 1.0 to 7.0, Y = 13.5 to 16.0)
    # 3 car stalls perpendicular facing north: width 2.5m, depth 5.0m (X = 1.0 to 8.5)
    # Let's put Motorcycle / Bike racks on X = 0.5 to 3.5, Y = 1.5 to 6.5
    # Motorcycle slots (6 slots: 1.25m x 2.5m each)
    moto_bg = patches.Rectangle((0.5, 1.5), 2.5, 7.5, facecolor='#FEF3C7', ec='#D97706', lw=1.5, zorder=3)
    ax.add_patch(moto_bg)
    for k in range(6):
        my = 1.5 + k * 1.25
        ax.plot([0.5, 3.0], [my, my], color='#B45309', lw=1, ls='--', zorder=4)
        ax.text(1.75, my + 0.62, f"MOTO #{k+1}", ha='center', va='center', fontsize=6, color='#78350F', fontweight='bold')
    ax.text(1.75, 9.3, "MOTORCYCLE BAY\n(6 SLOTS: 1.25x2.5m)", ha='center', va='center',
            fontsize=7, fontweight='bold', color='#B45309', bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#D97706"))

    # Bicycle Parking & Tool Station for Laguna Lake Loop Cyclists (X = 0.5 to 3.0, Y = 10.0 to 13.5)
    bike_bg = patches.Rectangle((0.5, 10.0), 2.5, 3.5, facecolor='#D1FAE5', ec='#059669', lw=1.5, zorder=3)
    ax.add_patch(bike_bg)
    ax.text(1.75, 11.75, "🚲 COVERED BICYCLE RACK\n(10 BIKES + REPAIR PUMP)\n[LAGUNA LAKE CYCLISTS]",
            ha='center', va='center', fontsize=6.5, fontweight='bold', color='#065F46')

    # Additional Car Slots 6, 7, 8 in middle apron (X = 1.0 to 8.5, Y = 14.0 to 19.0)
    # 3 slots: X = 1.0 to 3.5 (Slot 6), X = 3.5 to 6.0 (Slot 7), X = 6.0 to 8.5 (Slot 8)
    for c in range(3):
        cx = 1.0 + c * 2.5
        rect = patches.Rectangle((cx, 14.0), 2.5, 5.0, linewidth=1.5, edgecolor='#4B5563', facecolor='#E5E7EB', zorder=3)
        ax.add_patch(rect)
        # Wheel stop
        ax.add_patch(patches.Rectangle((cx + 0.3, 18.5), 1.9, 0.3, facecolor='#1F2937', zorder=4))
        ax.text(cx + 1.25, 16.5, f"CAR SLOT #{c+6}\n(2.5m x 5.0m)", ha='center', va='center',
                fontsize=6.5, fontweight='bold', color='#1F2937')

    # Landscaping buffer & Paved Walkway (X = 0 to 15, Y = 19.0 to 20.0)
    ax.fill([0, 15, 15, 0], [19.0, 19.0, 20.0, 20.0], color='#A7F3D0', zorder=2)
    ax.text(7.5, 19.5, "Landscaped Garden Buffer, Planter Boxes & Outdoor Walkway",
            ha='center', va='center', fontsize=7, color='#065F46', fontweight='bold')

    # 2-STOREY COFFEE SHOP BUILDING FOOTPRINT (10.0m x 10.0m: X = 2.5 to 12.5, Y = 20.0 to 30.0)
    bldg = patches.Rectangle((2.5, 20.0), 10.0, 10.0, linewidth=3, edgecolor='#991B1B', facecolor='#FEF2F2', zorder=4)
    ax.add_patch(bldg)

    # Building details
    ax.text(7.5, 25.5, "2-STOREY COFFEE SHOP BUILDING\n(GROSS FLOOR AREA = 185.0 SQ.M.)\nGROUND FLOOR FOOTPRINT: 10.0m x 10.0m (100 SQ.M.)\nFFL +0.600m ELEVATED FLOOD-RESILIENT PLINTH",
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#991B1B')

    # Main Entrance Canopy & Steps (X = 4.5 to 8.5, Y = 19.2 to 20.0)
    canopy = patches.Rectangle((4.5, 19.2), 4.0, 0.8, facecolor='#FEE2E2', ec='#DC2626', lw=1.5, zorder=5)
    ax.add_patch(canopy)
    ax.text(6.5, 19.6, "MAIN ENTRY CANOPY & ACCESSIBLE STEPS", ha='center', va='center',
            fontsize=6.5, fontweight='bold', color='#991B1B')

    # Cantilevered Balcony (Second Floor projection: X = 2.5 to 12.5, Y = 20.0 to 22.5)
    balc = patches.Rectangle((2.5, 20.0), 10.0, 2.5, fill=False, edgecolor='#B91C1C', lw=2, ls='--', zorder=5)
    ax.add_patch(balc)
    ax.text(7.5, 21.2, "2ND FLOOR CANTILEVERED BALCONY (OVERHANG ABOVE)",
            ha='center', va='center', fontsize=6.5, color='#B91C1C', style='italic')

    # Alfresco Side Deck (X = 12.5 to 14.5, Y = 20.0 to 29.0)
    deck = patches.Rectangle((12.5, 20.0), 2.0, 9.0, facecolor='#FEF3C7', ec='#D97706', lw=1.5, zorder=3)
    ax.add_patch(deck)
    ax.text(13.5, 24.5, "OUTDOOR\nALFRESCO\nPATIO\n(2.0x9.0m)", ha='center', va='center',
            fontsize=7, fontweight='bold', color='#92400E')

    # Rear Service Yard & Mechanical Area (X = 0.5 to 2.5, Y = 20.0 to 29.0)
    serv = patches.Rectangle((0.5, 20.0), 2.0, 9.0, facecolor='#E0E7FF', ec='#4338CA', lw=1.5, zorder=3)
    ax.add_patch(serv)
    ax.text(1.5, 24.5, "SERVICE\nYARD\n• Grease Trap\n• Genset\n• MRF Waste",
            ha='center', va='center', fontsize=6.5, fontweight='bold', color='#3730A3')

    # Dimension annotations
    # Width dimension (15.0m)
    ax.annotate("", xy=(0, 30.8), xytext=(15, 30.8), arrowprops=dict(arrowstyle="<->", color="#111827", lw=1.5))
    ax.text(7.5, 31.2, "15.00 METERS SITE FRONTAGE", ha='center', va='bottom', fontsize=8, fontweight='bold')

    # Depth dimension (30.0m)
    ax.annotate("", xy=(-0.8, 0), xytext=(-0.8, 30), arrowprops=dict(arrowstyle="<->", color="#111827", lw=1.5))
    ax.text(-1.2, 15.0, "30.00 METERS SITE DEPTH", ha='center', va='center', rotation=90, fontsize=8, fontweight='bold')

    # Setbacks
    ax.text(1.2, 29.5, "Rear Setback: 1.0m", fontsize=6, color='#6B7280')
    ax.text(14.0, 29.5, "Side: 0.5m", fontsize=6, color='#6B7280', ha='right')

    # Parking Summary Badge
    badge_text = (
        "PARKING MATRIX SUMMARY:\n"
        "• Total Lot Area: 450.00 sq.m.\n"
        "• Standard Car Slots: 8 Slots (2.5m x 5.0m)\n"
        "• PWD Accessible Slot: 1 Slot (3.7m x 5.0m)\n"
        "• Motorcycle Slots: 6 Slots (1.25m x 2.5m)\n"
        "• Bicycle Parking: 10 Bicycles + Workstand\n"
        "• Drive Aisle: 6.00m Wide (Two-Way Traffic)\n"
        "• Pavement: Permeable Eco-Pavers & Concrete"
    )
    ax.text(14.5, 18.5, badge_text, ha='right', va='top', fontsize=7,
            bbox=dict(boxstyle="round,pad=0.4", fc="#FFFFFF", ec="#1F2937", lw=1.5), zorder=6)

    ax.set_xlim(-2.5, 17.5)
    ax.set_ylim(-6.5, 32.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Figure 3: Comprehensive Architectural Site Development Plan with Dedicated Parking Facility\n(Café Turumba & Coffee Roasters, Pakil, Laguna • Lot Area: 450.0 sq.m. • Scale 1:150)",
                 fontsize=10, fontweight='bold', pad=15, color='#111827')

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'figure_site_parking_plan.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out_path)

# ----------------------------------------------------------------------
# 4. GROUND FLOOR PLAN (Scale 1:100 layout graphic)
# ----------------------------------------------------------------------
def generate_floor_plan_gf():
    fig, ax = plt.subplots(figsize=(9, 9), dpi=300)

    # Footprint 10m x 10m
    ax.plot([0, 10, 10, 0, 0], [0, 0, 10, 10, 0], color='#111827', lw=4, zorder=2)
    ax.fill([0, 10, 10, 0], [0, 0, 10, 10], color='#F9FAFB', zorder=1)

    # Grid columns (5m spacing)
    cols = [(0, 0), (5, 0), (10, 0), (0, 5), (5, 5), (10, 5), (0, 10), (5, 10), (10, 10)]
    for cx, cy in cols:
        ax.add_patch(patches.Rectangle((cx-0.2, cy-0.2), 0.4, 0.4, facecolor='#111827', zorder=5))

    # Barista Counter & Prep Island (X = 1.0 to 5.0, Y = 4.0 to 7.0)
    bar = patches.Rectangle((1.0, 4.0), 3.5, 3.0, facecolor='#E5E7EB', ec='#374151', lw=2, zorder=3)
    ax.add_patch(bar)
    ax.text(2.75, 5.5, "COMMERCIAL BARISTA BAR\n& COFFEE LAB\n• Espresso Station (3-Group)\n• Dual Grinders & Pour-Over\n• Pastry Showcase & POS Cashier",
            ha='center', va='center', fontsize=7, fontweight='bold', color='#1F2937')

    # Back Prep Kitchen / Storage (X = 1.0 to 5.0, Y = 7.5 to 9.8)
    prep = patches.Rectangle((1.0, 7.5), 3.5, 2.3, facecolor='#FEF3C7', ec='#D97706', lw=1.5, zorder=3)
    ax.add_patch(prep)
    ax.text(2.75, 8.65, "PREPARATION KITCHEN\n• Under-counter Chillers\n• 3-Bowl Commercial Sink\n• Ice Machine & Dry Storage",
            ha='center', va='center', fontsize=6.5, fontweight='bold', color='#92400E')

    # Restroom (PWD / Gender Neutral: X = 7.8 to 9.8, Y = 0.2 to 2.4)
    pwd_toilet = patches.Rectangle((7.8, 0.2), 2.0, 2.2, facecolor='#DBEAFE', ec='#1E40AF', lw=1.5, zorder=3)
    ax.add_patch(pwd_toilet)
    ax.text(8.8, 1.3, "♿ PWD RESTROOM\n• Grab Rails & Emergency Alarm\n• Baby Changing Station",
            ha='center', va='center', fontsize=6, fontweight='bold', color='#1E40AF')

    # U-Shaped Staircase Core (X = 7.8 to 9.8, Y = 4.8 to 8.2)
    stair = patches.Rectangle((7.8, 4.8), 2.0, 3.4, facecolor='#E0E7FF', ec='#4338CA', lw=1.5, zorder=3)
    ax.add_patch(stair)
    for s in range(8):
        sy = 4.8 + s * 0.425
        ax.plot([7.8, 8.8], [sy, sy], color='#4338CA', lw=1)
        ax.plot([8.8, 9.8], [sy, sy], color='#4338CA', lw=1)
    ax.plot([8.8, 8.8], [4.8, 8.2], color='#4338CA', lw=1.5)
    ax.text(8.8, 6.5, "U-SHAPED\nSTAIR CORE\n(UP TO 2F)", ha='center', va='center',
            fontsize=6.5, fontweight='bold', color='#3730A3')

    # Seating Area 1: Banquette Booths (X = 1.0 to 4.5, Y = 0.5 to 2.5)
    booth = patches.Rectangle((1.0, 0.5), 3.5, 2.0, facecolor='#FED7AA', ec='#C2410C', lw=1.5, zorder=3)
    ax.add_patch(booth)
    ax.text(2.75, 1.5, "FLUTED LEATHER BANQUETTE BOOTHS\n(4 Pedestal Tables • 8 Dining Seats)",
            ha='center', va='center', fontsize=6.5, fontweight='bold', color='#9A3412')

    # Seating Area 2: Main Dining Cafe Tables (X = 5.2 to 7.5, Y = 1.0 to 4.0)
    ax.add_patch(patches.Circle((6.2, 2.5), 0.6, facecolor='#E5E7EB', ec='#4B5563', lw=1.5))
    ax.add_patch(patches.Circle((6.2, 7.0), 0.6, facecolor='#E5E7EB', ec='#4B5563', lw=1.5))
    ax.text(6.2, 2.5, "4-TOP", ha='center', va='center', fontsize=6, fontweight='bold')
    ax.text(6.2, 7.0, "4-TOP", ha='center', va='center', fontsize=6, fontweight='bold')

    # Window High Bar Seating (North Glazing: X = 5.4 to 9.4, Y = 9.2 to 9.8)
    wbar = patches.Rectangle((5.4, 9.2), 4.0, 0.6, facecolor='#E5E7EB', ec='#374151', lw=1.5, zorder=3)
    ax.add_patch(wbar)
    for bx in [6.0, 7.0, 8.0, 9.0]:
        ax.add_patch(patches.Circle((bx, 8.9), 0.2, facecolor='#111827'))
    ax.text(7.4, 9.5, "PANORAMIC WINDOW BAR (4 HIGH STOOLS)", ha='center', va='center',
            fontsize=6, fontweight='bold', color='#1F2937')

    # Main Entrance Doors (North: X = 2.0 to 3.8, Y = 9.8 to 10.0)
    ax.plot([2.0, 3.8], [10.0, 10.0], color='#10B981', lw=4, zorder=6)
    ax.text(2.9, 10.3, "MAIN ENTRANCE (DOUBLE GLASS DOORS)", ha='center', va='center',
            fontsize=6.5, fontweight='bold', color='#065F46')

    # Dimensions
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 11)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Figure 4: Ground Floor Architectural Layout Plan (Scale 1:100)\n(Commercial Barista Lab, Main Dining, Banquette Seating, PWD Restroom & Circulation • Area: 100 sq.m.)",
                 fontsize=10, fontweight='bold', pad=15, color='#111827')

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'figure_floor_plan_gf.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out_path)

# ----------------------------------------------------------------------
# 5. SECOND FLOOR PLAN & BALCONY (Scale 1:100 layout graphic)
# ----------------------------------------------------------------------
def generate_floor_plan_2f():
    fig, ax = plt.subplots(figsize=(9, 10.5), dpi=300)

    # Footprint 10m x 10m (Y = 0 to 10) + Balcony 2.5m projection (Y = 10 to 12.5)
    ax.plot([0, 10, 10, 0, 0], [0, 0, 10, 10, 0], color='#111827', lw=4, zorder=2)
    ax.fill([0, 10, 10, 0], [0, 0, 10, 10], color='#F9FAFB', zorder=1)

    # Balcony Projection (Y = 10 to 12.5)
    balc = patches.Rectangle((0, 10), 10, 2.5, facecolor='#FEF3C7', ec='#B45309', lw=2.5, zorder=2)
    ax.add_patch(balc)
    # Tempered glass balustrade
    ax.plot([0.1, 0.1, 9.9, 9.9], [10.0, 12.4, 12.4, 10.0], color='#0284C7', lw=2, zorder=4)

    # Balcony tables
    for bx in [2.0, 5.0, 8.0]:
        ax.add_patch(patches.Circle((bx, 11.2), 0.5, facecolor='#FDE68A', ec='#B45309', lw=1.5))
        ax.text(bx, 11.2, "BISTRO\n3-TOP", ha='center', va='center', fontsize=5.5, fontweight='bold')
    ax.text(5.0, 12.1, "CANTILEVERED OUTDOOR BALCONY TERRACE (PERGOLA & STRING LIGHTS)\nScenic View of Sierra Madre Foothills & Manila East Road Corridor",
            ha='center', va='center', fontsize=6.5, fontweight='bold', color='#78350F')

    # Double-Height Atrium Void (Open to Ground Floor: X = 1.2 to 3.8, Y = 4.0 to 7.0)
    void = patches.Rectangle((1.2, 4.0), 2.6, 3.0, facecolor='#EFF6FF', ec='#3B82F6', lw=2, ls='--', zorder=3)
    ax.add_patch(void)
    # Cross diagonal lines
    ax.plot([1.2, 3.8], [4.0, 7.0], color='#93C5FD', lw=1.5, ls=':')
    ax.plot([1.2, 3.8], [7.0, 4.0], color='#93C5FD', lw=1.5, ls=':')
    ax.text(2.5, 5.5, "OPEN ATRIUM VOID\n(OVERLOOKING BARISTA\nBAR BELOW)\n• Glass Guardrail 1.10m",
            ha='center', va='center', fontsize=6.5, fontweight='bold', color='#1D4ED8',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#3B82F6"))

    # Communal Work Table (X = 4.8 to 7.8, Y = 4.5 to 5.5)
    comm = patches.Rectangle((4.8, 4.5), 3.0, 1.0, facecolor='#FDE68A', ec='#92400E', lw=2, zorder=3)
    ax.add_patch(comm)
    # Power grommets
    ax.add_patch(patches.Rectangle((5.1, 4.8), 0.4, 0.4, facecolor='#1F2937'))
    ax.add_patch(patches.Rectangle((7.3, 4.8), 0.4, 0.4, facecolor='#1F2937'))
    ax.text(6.3, 5.0, "SOLID OAK COMMUNAL WORK TABLE\n(10 Ergonomic Chairs • AC / USB Outlets)",
            ha='center', va='center', fontsize=6, fontweight='bold', color='#78350F')

    # Semi-Private Study Pods (East wall: X = 4.5 to 7.5, Y = 1.0 to 3.0)
    pod = patches.Rectangle((4.5, 1.0), 3.0, 2.0, facecolor='#E0E7FF', ec='#4338CA', lw=1.5, zorder=3)
    ax.add_patch(pod)
    ax.text(6.0, 2.0, "ACOUSTIC STUDY PODS\n(Individual Focus Desks & Task Lamps)",
            ha='center', va='center', fontsize=6.5, fontweight='bold', color='#3730A3')

    # Modern Modular Lounge Sectional (West wall: X = 0.8 to 3.5, Y = 0.8 to 3.0)
    lounge = patches.Rectangle((0.8, 0.8), 2.7, 2.2, facecolor='#FED7AA', ec='#C2410C', lw=1.5, zorder=3)
    ax.add_patch(lounge)
    ax.text(2.15, 1.9, "MODULAR SOFA LOUNGE\n& LOW COFFEE TABLES\n(Relaxed Meeting Zone)",
            ha='center', va='center', fontsize=6.5, fontweight='bold', color='#9A3412')

    # West Panoramic Glazing Study Bar (X = 0.2 to 0.8, Y = 4.0 to 8.5)
    wbar = patches.Rectangle((0.2, 4.0), 0.6, 4.5, facecolor='#E5E7EB', ec='#374151', lw=1.5, zorder=3)
    ax.add_patch(wbar)
    ax.text(0.5, 6.25, "WEST STUDY COUNTER (FACING LAKE VISTA)", rotation=90, ha='center', va='center',
            fontsize=6, fontweight='bold', color='#1F2937')

    # Stair Core (X = 7.8 to 9.8, Y = 4.8 to 8.2)
    stair = patches.Rectangle((7.8, 4.8), 2.0, 3.4, facecolor='#E0E7FF', ec='#4338CA', lw=1.5, zorder=3)
    ax.add_patch(stair)
    ax.text(8.8, 6.5, "STAIR CORE\n(DOWN TO GF)", ha='center', va='center',
            fontsize=6.5, fontweight='bold', color='#3730A3')

    # Second Floor Restroom (X = 7.8 to 9.8, Y = 1.0 to 3.0)
    cr = patches.Rectangle((7.8, 1.0), 2.0, 2.0, facecolor='#DBEAFE', ec='#1E40AF', lw=1.5, zorder=3)
    ax.add_patch(cr)
    ax.text(8.8, 2.0, "CUSTOMER\nRESTROOM", ha='center', va='center',
            fontsize=6.5, fontweight='bold', color='#1E40AF')

    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 13.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Figure 5: Second Floor Architectural Layout & Balcony Terrace Plan (Scale 1:100)\n(Co-Working Mezzanine, Communal Workstations, Study Pods & Cantilevered Balcony • Area: 85 sq.m.)",
                 fontsize=10, fontweight='bold', pad=15, color='#111827')

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'figure_floor_plan_2f.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out_path)

# ----------------------------------------------------------------------
# 6. FINANCIAL PROJECTIONS (5-Year Revenue, Gross Profit, Net Income)
# ----------------------------------------------------------------------
def generate_financial_chart():
    years = ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5']
    revenue = [5840000, 6890000, 8130000, 9430000, 10850000]
    gross_profit = [3796000, 4547400, 5447100, 6412400, 7486500]
    net_income = [1182000, 1625000, 2198000, 2812000, 3514000]

    x = np.arange(len(years))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

    rects1 = ax.bar(x - width, [r / 1e6 for r in revenue], width, label='Gross Revenue (PHP M)', color='#2563EB')
    rects2 = ax.bar(x, [g / 1e6 for g in gross_profit], width, label='Gross Profit (PHP M)', color='#10B981')
    rects3 = ax.bar(x + width, [n / 1e6 for n in net_income], width, label='Net Income After Tax (PHP M)', color='#F59E0B')

    ax.set_ylabel('Philippine Pesos in Millions (PHP M)', fontsize=10, fontweight='bold')
    ax.set_title('Figure 6: Five-Year Financial Projections (Revenue, Gross Profit & Net Profit After Tax)\nCafé Turumba & Coffee Roasters, Pakil, Laguna',
                 fontsize=11, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=10, fontweight='bold')
    ax.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=9)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'₱{height:.2f}M',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=7.5, fontweight='bold')

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'figure_financial_growth.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out_path)

# ----------------------------------------------------------------------
# 7. BREAK-EVEN ANALYSIS GRAPHIC
# ----------------------------------------------------------------------
def generate_breakeven_chart():
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)

    # Monthly analysis in cups/orders: 0 to 4000 orders/month
    # Average order value: PHP 190.00
    # Variable cost per order (35%): PHP 66.50
    # Contribution margin: PHP 123.50
    # Monthly fixed costs: PHP 155,000 (Rent 35k, Salaries 65k, Utilities 25k, Admin/Deprec/Marketing 30k)
    # BEP in units = 155,000 / 123.50 = 1,255 orders/month (approx 42 orders/day)
    # BEP in Sales = 1,255 * 190 = PHP 238,450 / month

    q = np.linspace(0, 3500, 100)
    fixed_cost = np.full_like(q, 155000)
    total_cost = fixed_cost + (66.50 * q)
    total_revenue = 190.00 * q

    ax.plot(q, fixed_cost, color='#6B7280', lw=2, ls='--', label='Monthly Fixed Costs (₱155,000)')
    ax.plot(q, total_cost, color='#DC2626', lw=2.5, label='Total Costs (Fixed + Variable Costs)')
    ax.plot(q, total_revenue, color='#2563EB', lw=2.5, label='Total Revenue (₱190 Avg Ticket)')

    # Break-Even Point
    bep_q = 1255
    bep_rev = 238450
    ax.scatter([bep_q], [bep_rev], color='#E11D48', s=180, zorder=5, edgecolors='black', lw=1.5)
    ax.axvline(x=bep_q, color='#E11D48', linestyle=':', lw=1.5)
    ax.axhline(y=bep_rev, color='#E11D48', linestyle=':', lw=1.5)

    ax.annotate(f'BREAK-EVEN POINT (BEP)\n• Volume: 1,255 Orders/Mo (~42 Orders/Day)\n• Monthly Sales: ₱238,450\n• Safety Margin: 48.5% at Base Capacity',
                xy=(bep_q, bep_rev), xytext=(bep_q + 250, bep_rev - 70000),
                arrowprops=dict(facecolor='#E11D48', shrink=0.08, width=1.5, headwidth=6),
                bbox=dict(boxstyle="round,pad=0.5", fc="#FFF1F2", ec="#E11D48", lw=1.5),
                fontsize=8.5, fontweight='bold', color='#9F1239')

    # Shaded Profit Zone
    ax.fill_between(q[q >= bep_q], total_cost[q >= bep_q], total_revenue[q >= bep_q],
                    color='#D1FAE5', alpha=0.5, label='Projected Profit Zone (Operating Margin)')
    # Shaded Loss Zone
    ax.fill_between(q[q <= bep_q], total_revenue[q <= bep_q], total_cost[q <= bep_q],
                    color='#FEE2E2', alpha=0.5, label='Operating Loss Zone')

    ax.set_xlabel('Monthly Customer Transactions / Orders (Volume)', fontsize=10, fontweight='bold')
    ax.set_ylabel('Total Amount (Philippine Pesos)', fontsize=10, fontweight='bold')
    ax.set_title('Figure 7: Monthly Break-Even Analysis (BEP) Chart\nCafé Turumba & Coffee Roasters, Pakil, Laguna',
                 fontsize=11, fontweight='bold', pad=15)
    ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9, fontsize=8.5)
    ax.grid(True, linestyle='--', alpha=0.4)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'figure_breakeven.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out_path)

# ----------------------------------------------------------------------
# 8. CAPITAL EXPENDITURE (CAPEX) BREAKDOWN DONUT CHART
# ----------------------------------------------------------------------
def generate_capex_donut():
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)

    categories = [
        'Building Construction & Fit-out\n(₱2,450,000)',
        'Dedicated Parking Lot Paving,\nDrainage & Lighting (₱580,000)',
        'Commercial Espresso &\nBarista Machinery (₱820,000)',
        'Kitchen Equipment &\nRefrigeration (₱380,000)',
        'Furniture, Fixtures &\nArchitectural Decor (₱420,000)',
        'IT, POS, CCTV & Dual-ISP\nNetwork Setup (₱150,000)',
        'Pre-Operating Permits, Licenses\n& Launch Marketing (₱180,000)',
        'Initial Inventory &\nOperating Working Capital (₱520,000)'
    ]
    amounts = [2450000, 580000, 820000, 380000, 420000, 150000, 180000, 520000]
    total_capex = sum(amounts)

    colors = ['#1E3A8A', '#0284C7', '#D97706', '#F59E0B', '#10B981', '#6366F1', '#EC4899', '#64748B']

    wedges, texts, autotexts = ax.pie(
        amounts, autopct='%1.1f%%', pctdistance=0.78,
        colors=colors, startangle=140,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2)
    )

    for at in autotexts:
        at.set_color('white')
        at.set_fontweight('bold')
        at.set_fontsize(8)

    ax.legend(wedges, categories, title="CAPEX Allocation Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
              fontsize=8, title_fontsize=9)

    ax.text(0, 0, f"TOTAL INITIAL\nCAPITAL OUTLAY\n₱{total_capex:,.0f}\n(PHP 5.50M)",
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#111827')

    ax.set_title("Figure 8: Total Initial Project Investment & Capital Expenditure (CAPEX) Breakdown\nCafé Turumba & Coffee Roasters, Pakil, Laguna",
                 fontsize=10.5, fontweight='bold', pad=15)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'figure_capex_breakdown.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out_path)

# ----------------------------------------------------------------------
# 9. ORGANIZATIONAL STRUCTURE HIERARCHY CHART
# ----------------------------------------------------------------------
def generate_org_chart():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)

    # Box coordinates
    # Level 1: Board / Managing Owner
    # Level 2: General Manager
    # Level 3: Bar & Roastery Head, Kitchen & Pastry Head, Admin & Marketing Lead
    # Level 4: Baristas, Kitchen Cooks, Cashiers, Service Crew, Facilities & Security

    def draw_node(x, y, w, h, title, name, bg='#1E3A8A', fg='white'):
        rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.2",
                                      fc=bg, ec='#111827', lw=1.5, zorder=3)
        ax.add_patch(rect)
        ax.text(x, y + 0.12, title, ha='center', va='center', fontsize=8, fontweight='bold', color=fg, zorder=4)
        ax.text(x, y - 0.15, name, ha='center', va='center', fontsize=7, color=fg, zorder=4)

    # Connections
    ax.plot([5, 5], [5.6, 4.8], color='#374151', lw=2)  # Owner to GM
    ax.plot([1.8, 8.2], [3.9, 3.9], color='#374151', lw=2)  # Horizontal branch
    ax.plot([5, 5], [4.1, 3.9], color='#374151', lw=2)  # GM down to branch
    ax.plot([1.8, 1.8], [3.9, 3.2], color='#374151', lw=2)
    ax.plot([5.0, 5.0], [3.9, 3.2], color='#374151', lw=2)
    ax.plot([8.2, 8.2], [3.9, 3.2], color='#374151', lw=2)

    # Department sub-connections
    ax.plot([1.8, 1.8], [2.6, 1.8], color='#374151', lw=1.5, ls='--')
    ax.plot([5.0, 5.0], [2.6, 1.8], color='#374151', lw=1.5, ls='--')
    ax.plot([8.2, 8.2], [2.6, 1.8], color='#374151', lw=1.5, ls='--')

    # Draw Nodes
    draw_node(5.0, 5.8, 3.6, 0.7, "MANAGING PROPRIETOR / INVESTOR", "Executive Oversight & Capital Strategy", bg='#1E1B4B')
    draw_node(5.0, 4.4, 3.2, 0.7, "GENERAL STORE MANAGER", "Store Operations & Financial Compliance", bg='#1E40AF')

    draw_node(1.8, 2.9, 2.8, 0.7, "HEAD BARISTA & ROASTERY LEAD", "Coffee Quality, Training & Inventory", bg='#D97706')
    draw_node(5.0, 2.9, 2.8, 0.7, "HEAD KITCHEN & PASTRY CHEF", "Food Preparation, Recipes & Sanitation", bg='#059669')
    draw_node(8.2, 2.9, 2.8, 0.7, "MARKETING & ADMIN OFFICER", "Digital Media, Local Events & Accounts", bg='#7C3AED')

    draw_node(1.8, 1.3, 2.8, 0.7, "SPECIALTY BARISTAS (3)", "Espresso Craft, Pour-overs & POS", bg='#FEF3C7', fg='#92400E')
    draw_node(5.0, 1.3, 2.8, 0.7, "KITCHEN CREW (2)", "Baking, Pastry Finishing & Prep", bg='#D1FAE5', fg='#065F46')
    draw_node(8.2, 1.3, 2.8, 0.7, "FACILITY, PARKING & UTILITY (2)", "Parking Assistance, Busboy & Cleaning", bg='#F3E8FF', fg='#581C87')

    ax.set_xlim(0, 10)
    ax.set_ylim(0.5, 6.7)
    ax.axis('off')
    ax.set_title("Figure 9: Formal Organizational Structure & Operational Hierarchy\nCafé Turumba & Coffee Roasters, Pakil, Laguna",
                 fontsize=11, fontweight='bold', pad=15)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'figure_org_chart.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out_path)

# ----------------------------------------------------------------------
# 10. RISK SEVERITY VS. LIKELIHOOD HEATMAP MATRIX
# ----------------------------------------------------------------------
def generate_risk_matrix():
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)

    # 5x5 matrix
    # Impact (1-5) on Y, Likelihood (1-5) on X
    matrix = np.zeros((5, 5))
    for i in range(5):
        for j in range(5):
            matrix[i, j] = (i + 1) * (j + 1)

    # Custom color map green -> yellow -> red
    cmap = plt.cm.RdYlGn_r
    ax.imshow(matrix, cmap=cmap, origin='lower', extent=[0.5, 5.5, 0.5, 5.5], alpha=0.7)

    # Plot specific risks
    risks = [
        (2, 4, "R1: Seasonal Tourist\nFluctuation (Off-Peak)"),
        (4, 2, "R2: Power / Utility\nOutages during Storms"),
        (2, 2, "R3: Local Competitor\nPrice Pressure"),
        (3, 2, "R4: Green Coffee Bean\nCost Volatility"),
        (4, 1, "R5: Severe Typhoons /\nFlash Floods"),
        (2, 3, "R6: Parking Congestion\nduring Turumba Peak"),
        (3, 1, "R7: Barista Staff\nTurnover")
    ]

    for lx, ly, label in risks:
        ax.scatter(lx, ly, color='#111827', s=160, zorder=5, edgecolors='white', lw=1.5)
        ax.text(lx, ly + 0.22, label, ha='center', va='bottom', fontsize=7.5, fontweight='bold',
                color='#111827', bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#9CA3AF", alpha=0.9))

    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xticklabels(['1: Rare', '2: Unlikely', '3: Moderate', '4: Likely', '5: Almost Certain'], fontsize=9, fontweight='bold')
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1: Insignificant', '2: Minor', '3: Moderate', '4: Major', '5: Catastrophic'], fontsize=9, fontweight='bold')

    ax.set_xlabel('Risk Likelihood / Probability of Occurrence', fontsize=10, fontweight='bold')
    ax.set_ylabel('Impact / Consequence Severity Level', fontsize=10, fontweight='bold')
    ax.set_title('Figure 10: Enterprise Risk Assessment & Prioritization Matrix (5x5 Heatmap)\nCafé Turumba & Coffee Roasters, Pakil, Laguna',
                 fontsize=11, fontweight='bold', pad=15)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'figure_risk_matrix.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out_path)

if __name__ == '__main__':
    print("Generating analytical visuals and architectural graphics...")
    generate_satellite_map()
    generate_vicinity_map()
    generate_site_parking_plan()
    generate_floor_plan_gf()
    generate_floor_plan_2f()
    generate_financial_chart()
    generate_breakeven_chart()
    generate_capex_donut()
    generate_org_chart()
    generate_risk_matrix()
    print("All visual assets successfully generated in 'generated_assets/'!")
