#!/usr/bin/env python3
"""
Advanced 3D Computational Architectural Generator & Multi-Format Compiler
Project: 2-Storey Specialty Coffee Shop in Burgos, Pakil, Laguna

Major Upgrades & Aesthetic Enhancements:
1. Zero Artificial Neon Green:
   - Eliminated all artificial green cylinders, green boxes, and awkward green blocks.
   - Clean architectural materials: warm golden oak, smoked walnut, fluted timber, Calacatta quartz,
     brushed stainless steel, rich cognac leather, architectural concrete, and limewash plaster.
2. Articulated Modern Architectural Facade (Zero Flat Solid Monoliths):
   - Vertical architectural timber battens / wood louvers on 2nd floor wings and West facade.
   - Cantilevered matte black steel entrance canopy with dual tie-rod stays.
   - Recessed warm ceiling pot lights under canopy illuminating the entrance.
   - 3D Backlit architectural cafe signage fascia ("BURGOS HIGHLANDS | SPECIALTY COFFEE").
   - 2nd Floor Balcony black steel pergola trellis with cross-beams and rafters.
3. Abundant, High-End Designer Furniture (Inside & Outside):
   - Ground Floor: 4.5m caramel leather banquette booth with vertical fluted back cushions,
     4 pedestal dining tables, 8 Scandinavian chairs, 4.2m solid oak window bar counter with
     5 bar stools, 3 central round cafe tables with 6 bentwood chairs, Scandinavian armchair lounge,
     and fully equipped commercial barista station with 3-group espresso machine, twin grinders,
     V60 pour-over drip station, illuminated pastry display case, and commercial refrigerators.
   - Second Floor: Large L-shaped modular sectional sofa, nesting trio coffee tables, 2 tub armchairs,
     3.5m solid oak communal work table with 8 ergonomic chairs, 2 private study booth pods with
     timber privacy screens and task lamps, 4.0m West panoramic window study counter with 4 bar stools,
     airy open Japandi display bookshelf, and double-height atrium void with frameless glass railing.
   - Balcony: 4 outdoor cafe dining tables with 10 stylish bistro chairs, black steel pergola,
     and glass balustrades with continuous metal top rail.
4. Visible 3D Light Fixtures & Multi-Source Interactive Illumination:
   - Visible 3D Light Fixtures: 3 brass cone pendant lamps over barista bar, 4 pendant lamps over
     dining tables, 14 warm festoon globe string lights suspended across the balcony pergola trellis,
     4 recessed downlights under canopy soffit, and desk lamps on study booths.
   - Linear warm LED underglow accent strips under the quartz waterfall counter edge, banquette plinth,
     and stair handrail.
   - Dynamic Three.js Interior Lighting with dedicated interior point lights and spot lights.
   - Interactive UI Dimmer slider (0% to 200%) and 3 Ambiance Presets: Daylight Studio, Golden Hour Sunset,
     and Evening / Night Cafe (where warm interior lights glow through glass curtain walls!).
"""

import os
import math
import json
import ezdxf
from ezdxf.render import forms


# ==============================================================================
# 3D MODEL DATA CONTAINER
# ==============================================================================

class Model3D:
    def __init__(self):
        self.boxes = []      # list of (x, y, z, w, d, h, layer, material)
        self.cylinders = []  # list of (cx, cy, z, r, h, layer, material)
        self.dimensions = [] # list of (p1, p2, text, subtext, axis)

    def add_box(self, x, y, z, w, d, h, layer="3D-DEFAULT", material="default"):
        """Adds an axis-aligned 3D box (coordinates in mm)."""
        self.boxes.append((float(x), float(y), float(z), float(w), float(d), float(h), layer, material))

    def add_cylinder(self, cx, cy, z, r, h, layer="3D-DEFAULT", material="default"):
        """Adds a vertical cylinder (coordinates in mm)."""
        self.cylinders.append((float(cx), float(cy), float(z), float(r), float(h), layer, material))

    def add_dimension(self, p1, p2, text, subtext="", axis="x"):
        """Adds a 3D architectural dimension chain measurement (coordinates in mm)."""
        self.dimensions.append((p1, p2, text, subtext, axis))


# ==============================================================================
# HIGH-END ARCHITECTURAL FURNITURE & FIXTURE BUILDERS
# ==============================================================================

def add_modern_chair(m: Model3D, cx, cy, z, angle_deg=0, seat_mat="leather", frame_mat="metal_dark"):
    """
    Builds a modern designer cafe chair with 4 slender tubular legs,
    upholstered seat cushion, rear uprights, and curved backrest rail.
    """
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    def rot(lx, ly):
        return cx + lx * cos_a - ly * sin_a, cy + lx * sin_a + ly * cos_a

    leg_off = 170
    for lx, ly in [(-leg_off, -leg_off), (leg_off, -leg_off), (-leg_off, leg_off), (leg_off, leg_off)]:
        px, py = rot(lx, ly)
        m.add_cylinder(px, py, z, 13, 430, "3D-FURNITURE", frame_mat)

    m.add_box(cx - 210, cy - 210, z + 410, 420, 420, 40, "3D-FURNITURE", seat_mat)

    p1x, p1y = rot(-160, 160)
    p2x, p2y = rot(160, 160)
    m.add_cylinder(p1x, p1y, z + 430, 12, 350, "3D-FURNITURE", frame_mat)
    m.add_cylinder(p2x, p2y, z + 430, 12, 350, "3D-FURNITURE", frame_mat)

    m.add_box(cx - 200, cy + 150, z + 700, 400, 35, 90, "3D-FURNITURE", seat_mat)


def add_pedestal_dining_table(m: Model3D, cx, cy, z, radius=375, height=730, top_mat="wood", base_mat="metal_dark"):
    """
    Builds a modern cafe dining table with solid circular oak/marble top
    and cast-iron tulip pedestal base.
    """
    m.add_cylinder(cx, cy, z, 230, 18, "3D-FURNITURE", base_mat)
    m.add_cylinder(cx, cy, z + 18, 35, height - 18 - 32, "3D-FURNITURE", base_mat)
    m.add_cylinder(cx, cy, z + height - 32, radius, 32, "3D-FURNITURE", top_mat)


def add_modern_bar_stool(m: Model3D, cx, cy, z, seat_mat="leather"):
    """
    Builds a minimalist modern bar stool with 4 slender tapered legs,
    circular footrest ring, and round leather seat disc.
    """
    leg_r = 130
    for ang in [0.78, 2.35, 3.92, 5.49]:
        lx = cx + math.cos(ang) * leg_r
        ly = cy + math.sin(ang) * leg_r
        m.add_cylinder(lx, ly, z, 11, 650, "3D-FURNITURE", "metal_dark")
    m.add_cylinder(cx, cy, z + 260, 150, 15, "3D-FURNITURE", "metal_dark")
    m.add_cylinder(cx, cy, z + 650, 180, 45, "3D-FURNITURE", seat_mat)


def add_lounge_armchair(m: Model3D, cx, cy, z, angle_deg=0):
    """
    Builds a Scandinavian low lounge tub armchair with angled wooden legs
    and plush rounded leather bucket upholstery.
    """
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    def rot(lx, ly):
        return cx + lx * cos_a - ly * sin_a, cy + lx * sin_a + ly * cos_a

    # 4 Angled wooden legs
    for lx, ly in [(-220, -220), (220, -220), (-220, 220), (220, 220)]:
        px, py = rot(lx, ly)
        m.add_cylinder(px, py, z, 16, 280, "3D-FURNITURE", "wood_dark")

    # Thick cushioned seat base (650 x 600 x 140)
    m.add_box(cx - 325, cy - 300, z + 260, 650, 600, 140, "3D-FURNITURE", "leather")
    # Low curved wraparound backrest
    m.add_box(cx - 340, cy + 180, z + 400, 680, 140, 280, "3D-FURNITURE", "leather")
    # Armrest sides
    m.add_box(cx - 340, cy - 250, z + 360, 120, 430, 220, "3D-FURNITURE", "leather")
    m.add_box(cx + 220, cy - 250, z + 360, 120, 430, 220, "3D-FURNITURE", "leather")


def add_pendant_light(m: Model3D, cx, cy, cz, cord_len=900, shade_r=130, shade_h=160):
    """
    Builds a visible modern suspended pendant light fixture:
    thin black suspension cord, brass/black conical shade, and glowing diffuser disc.
    cz is ceiling attachment height in mm.
    """
    # Ceiling rose canopy
    m.add_cylinder(cx, cy, cz - 20, 45, 20, "3D-LIGHTS", "metal_dark")
    # Slender electrical suspension cord
    m.add_cylinder(cx, cy, cz - cord_len, 4, cord_len - 20, "3D-LIGHTS", "metal_dark")
    # Brass conical shade body
    fixture_z = cz - cord_len - shade_h
    m.add_cylinder(cx, cy, fixture_z, shade_r, shade_h, "3D-LIGHTS", "metal_dark")
    # Glowing warm light diffuser bottom disc (self-illuminated light_glow!)
    m.add_cylinder(cx, cy, fixture_z + 8, shade_r - 12, 18, "3D-LIGHTS", "light_glow")


def add_commercial_refrigerator(m: Model3D, x, y, z):
    """
    Builds a commercial 2-door reach-in refrigerator with brushed stainless steel cabinet,
    dual thermal glass doors, interior wire shelves, and realistic beverage inventory.
    (ZERO artificial green cylinders or blocks!).
    """
    # Main stainless steel insulated cabinet (1250w x 750d x 1980h)
    m.add_box(x, y, z, 750, 1250, 1980, "3D-BARISTA-BAR", "appliance_steel")
    m.add_box(x + 20, y + 20, z, 710, 1210, 90, "3D-BARISTA-BAR", "metal_dark")
    m.add_box(x + 10, y + 20, z + 1820, 750, 1210, 140, "3D-BARISTA-BAR", "metal_dark")

    # Left & Right door stainless perimeter frames
    m.add_box(x + 740, y + 30, z + 100, 20, 580, 1700, "3D-BARISTA-BAR", "appliance_steel")
    m.add_box(x + 740, y + 640, z + 100, 20, 580, 1700, "3D-BARISTA-BAR", "appliance_steel")

    # Thermal glass viewing panels
    m.add_box(x + 745, y + 80, z + 160, 12, 480, 1580, "3D-BARISTA-BAR", "glass")
    m.add_box(x + 745, y + 690, z + 160, 12, 480, 1580, "3D-BARISTA-BAR", "glass")

    # 4 Interior stainless steel shelf racks with realistic beverage bottles & dairy cartons (No foliage!)
    for sz in [400, 750, 1100, 1450]:
        m.add_box(x + 80, y + 50, z + sz, 620, 1150, 20, "3D-BARISTA-BAR", "metal_dark")
        for by in [150, 450, 750, 1050]:
            # White barista milk cartons
            m.add_box(x + 200, y + by, z + sz + 20, 110, 85, 220, "3D-BARISTA-BAR", "fixture_white")
            # Cold brew bottled drinks (glass and steel caps)
            m.add_cylinder(x + 450, y + by + 40, z + sz + 20, 42, 210, "3D-BARISTA-BAR", "glass")

    # Vertical stainless tubular door handles
    m.add_box(x + 765, y + 570, z + 650, 25, 25, 750, "3D-BARISTA-BAR", "metal_dark")
    m.add_box(x + 765, y + 650, z + 650, 25, 25, 750, "3D-BARISTA-BAR", "metal_dark")
    # Digital LED temperature display
    m.add_box(x + 755, y + 590, z + 1870, 10, 70, 30, "3D-BARISTA-BAR", "light_glow")


def add_undercounter_cooler(m: Model3D, x, y, z):
    """Builds a backbar undercounter dual-glass door beverage refrigerator."""
    m.add_box(x, y, z, 550, 950, 840, "3D-BARISTA-BAR", "appliance_steel")
    m.add_box(x + 540, y + 30, z + 40, 15, 420, 760, "3D-BARISTA-BAR", "glass")
    m.add_box(x + 540, y + 500, z + 40, 15, 420, 760, "3D-BARISTA-BAR", "glass")
    m.add_box(x + 60, y + 40, z + 420, 460, 870, 15, "3D-BARISTA-BAR", "metal_dark")


def add_espresso_station(m: Model3D, x, y, z):
    """
    Builds a commercial 3-group espresso machine with cup warming tray,
    twin conical bean grinders, pour-over station, knock box, and tamp station.
    """
    # 3-Group Commercial Espresso Machine (920w x 540d x 440h)
    m.add_box(x, y, z, 520, 920, 440, "3D-BARISTA-BAR", "metal_dark")
    m.add_box(x + 510, y + 80, z + 80, 25, 760, 130, "3D-BARISTA-BAR", "appliance_steel")
    # 3 Walnut group handles protruding forward
    for gy in [200, 460, 720]:
        m.add_box(x + 520, y + gy, z + 150, 120, 40, 35, "3D-BARISTA-BAR", "wood_dark")
    # Top stainless cup warming tray with ceramic cups
    m.add_box(x + 30, y + 50, z + 440, 460, 820, 20, "3D-BARISTA-BAR", "appliance_steel")
    for cx in [x + 100, x + 250, x + 400]:
        for cy in [y + 120, y + 300, y + 480, y + 660]:
            m.add_cylinder(cx, cy, z + 460, 38, 55, "3D-BARISTA-BAR", "fixture_white")

    # Twin Mahlkönig Coffee Grinders
    for gy in [y - 320, y - 620]:
        m.add_box(x + 100, gy, z, 240, 240, 360, "3D-BARISTA-BAR", "metal_dark")
        m.add_cylinder(x + 220, gy + 120, z + 360, 95, 180, "3D-BARISTA-BAR", "glass")
        m.add_cylinder(x + 220, gy + 120, z + 370, 85, 120, "3D-BARISTA-BAR", "wood_dark")

    # V60 / Chemex Manual Pour-Over Drip Stand
    m.add_box(x + 80, y + 1020, z, 320, 480, 25, "3D-BARISTA-BAR", "wood_dark")
    m.add_box(x + 100, y + 1040, z + 25, 20, 440, 180, "3D-BARISTA-BAR", "metal_dark")
    m.add_box(x + 100, y + 1040, z + 185, 260, 440, 20, "3D-BARISTA-BAR", "metal_dark")
    for fy in [y + 1120, y + 1340]:
        m.add_cylinder(x + 230, fy, z + 205, 55, 75, "3D-BARISTA-BAR", "glass")


def add_pastry_showcase(m: Model3D, x, y, z):
    """
    Builds an illuminated frameless glass bakery display case
    with polished quartz base, tiered wooden pastry risers, and pastries.
    """
    m.add_box(x, y, z, 1200, 520, 40, "3D-BARISTA-BAR", "quartz")
    m.add_box(x, y, z + 40, 1200, 520, 480, "3D-BARISTA-BAR", "glass")
    m.add_box(x + 50, y + 40, z + 50, 1100, 440, 25, "3D-BARISTA-BAR", "wood")
    m.add_box(x + 80, y + 60, z + 260, 1040, 380, 20, "3D-BARISTA-BAR", "wood")
    # Modeled pastries on trays
    for px in [x + 180, x + 420, x + 660, x + 900]:
        m.add_box(px, y + 150, z + 75, 160, 120, 50, "3D-BARISTA-BAR", "wood_dark")
        m.add_box(px, y + 160, z + 280, 150, 110, 45, "3D-BARISTA-BAR", "wood_dark")
    # Warm internal LED strip glow in showcase
    m.add_box(x + 30, y + 480, z + 490, 1140, 20, 15, "3D-LIGHTS", "light_glow")


def add_open_japandi_shelf(m: Model3D, x, y, z, width=3200, height=2200):
    """
    Builds an open, airy Japandi display bookcase with slender matte black posts
    and floating oak shelves.
    """
    for px in [x, x + 1050, x + 2100, x + width - 30]:
        m.add_box(px, y, z, 30, 260, height, "3D-FURNITURE", "metal_dark")
        m.add_box(px, y + 230, z, 30, 30, height, "3D-FURNITURE", "metal_dark")

    for sz in [350, 800, 1250, 1700, 2150]:
        m.add_box(x, y, z + sz, width, 260, 25, "3D-FURNITURE", "wood")
        for bx in [x + 200, x + 800, x + 1400, x + 2000, x + 2600]:
            m.add_box(bx, y + 30, z + sz + 25, 140, 180, 180, "3D-FURNITURE", "quartz")
            m.add_cylinder(bx + 260, y + 120, z + sz + 25, 45, 140, "3D-FURNITURE", "wood_dark")


def add_modular_lounge_sofa(m: Model3D, x, y, z):
    """
    Builds a modern low-profile Japandi modular sofa with plush cushions,
    corner chaise, low wood plinth, and accent throw pillows.
    """
    m.add_box(x, y, z, 2400, 950, 80, "3D-FURNITURE", "wood_dark")
    m.add_box(x, y + 950, z, 950, 950, 80, "3D-FURNITURE", "wood_dark")

    for sx in [x + 30, x + 820, x + 1610]:
        m.add_box(sx, y + 30, z + 80, 760, 890, 340, "3D-FURNITURE", "leather")
    m.add_box(x + 30, y + 950, z + 80, 890, 920, 340, "3D-FURNITURE", "leather")

    m.add_box(x, y, z + 420, 2400, 220, 340, "3D-FURNITURE", "leather")
    m.add_box(x, y + 220, z + 420, 220, 1680, 340, "3D-FURNITURE", "leather")


def add_private_study_booth(m: Model3D, x, y, z):
    """
    Builds an acoustic focus work booth on 2nd floor with timber privacy screens,
    upholstered bench seat, work desk, and brass task lamp.
    """
    w, d, h = 1100.0, 950.0, 1800.0
    # Left & Right acoustic oak slatted divider screens
    m.add_box(x, y, z, 30, d, h, "3D-FURNITURE", "wood")
    m.add_box(x + w - 30, y, z, 30, d, h, "3D-FURNITURE", "wood")
    # Back acoustic wall panel
    m.add_box(x + 30, y, z, w - 60, 30, h, "3D-FURNITURE", "wood_dark")
    # Padded bench seat (height 450mm)
    m.add_box(x + 30, y + 30, z, w - 60, 480, 450, "3D-FURNITURE", "leather")
    # Study work desk (height 740mm)
    m.add_box(x + 30, y + 490, z + 710, w - 60, 440, 35, "3D-FURNITURE", "wood")
    # Modern brass task lamp
    m.add_cylinder(x + w - 150, y + 800, z + 745, 45, 12, "3D-LIGHTS", "metal_dark")
    m.add_cylinder(x + w - 150, y + 800, z + 757, 8, 320, "3D-LIGHTS", "metal_dark")
    m.add_cylinder(x + w - 180, y + 760, z + 1070, 35, 70, "3D-LIGHTS", "light_glow")


def add_balcony_pergola_with_lights(m: Model3D, z_balc=3950.0, z_pergola=6900.0):
    """
    Builds a contemporary architectural steel pergola trellis over the 2.5m cantilevered balcony,
    complete with 14 warm glowing festoon globe string lights suspended across the rafters.
    """
    # 4 Vertical black steel posts (80 x 80mm)
    post_coords = [(200, 12400), (3400, 12400), (6600, 12400), (9800, 12400)]
    for px, py in post_coords:
        m.add_box(px, py, z_balc, 80, 80, z_pergola - z_balc, "3D-PERGOLA", "metal_dark")

    # Front main header beam spanning 10 meters (80 x 180mm)
    m.add_box(0, 12400, z_pergola - 180, 10000, 80, 180, "3D-PERGOLA", "metal_dark")
    # Rear wall ledger beam (80 x 180mm)
    m.add_box(0, 10000, z_pergola - 180, 10000, 80, 180, "3D-PERGOLA", "metal_dark")

    # 9 Transverse pergola louver rafters spanning 2.5m (60 x 120mm)
    for i in range(9):
        rx = 400.0 + i * 1150.0
        m.add_box(rx, 10000, z_pergola - 120, 60, 2480, 120, "3D-PERGOLA", "metal_dark")

    # 14 Suspended Warm Festoon Globe Lights (glowing bulbs under pergola rafters!)
    for i in range(7):
        lx = 800.0 + i * 1400.0
        for ly in [10800.0, 11800.0]:
            # Slender black drop cable
            m.add_cylinder(lx, ly, z_pergola - 350, 3, 230, "3D-LIGHTS", "metal_dark")
            # Glowing warm spherical bulb
            m.add_cylinder(lx, ly, z_pergola - 390, 36, 40, "3D-LIGHTS", "light_glow")


def add_entrance_canopy_and_signage(m: Model3D, z_level=3400.0):
    """
    Builds a cantilevered black steel entrance canopy over the North storefront entrance,
    with dual structural tie-rod stays, recessed downlights, and 3D backlit cafe signage.
    """
    canopy_x = 1600.0
    canopy_y = 10000.0
    canopy_w = 3400.0
    canopy_d = 1600.0
    canopy_h = 130.0

    # Cantilevered steel awning structure
    m.add_box(canopy_x, canopy_y, z_level, canopy_w, canopy_d, canopy_h, "3D-CANOPY", "metal_dark")
    # Fascia edge trim in dark bronze
    m.add_box(canopy_x - 20, canopy_y, z_level, canopy_w + 40, canopy_d + 30, 25, "3D-CANOPY", "metal_dark")

    # 2 Structural steel tie-rod support cables from upper 2F beam down to canopy corners
    m.add_cylinder(canopy_x + 80, canopy_y + canopy_d - 60, z_level + canopy_h, 16, 500, "3D-CANOPY", "metal_dark")
    m.add_cylinder(canopy_x + canopy_w - 80, canopy_y + canopy_d - 60, z_level + canopy_h, 16, 500, "3D-CANOPY", "metal_dark")

    # 4 Recessed Ceiling Pot Downlights under canopy soffit (illuminating the steps & double doors!)
    for dx in [canopy_x + 600, canopy_x + 1300, canopy_x + 2100, canopy_x + 2800]:
        m.add_cylinder(dx, canopy_y + 800, z_level - 10, 75, 12, "3D-LIGHTS", "light_glow")

    # Backlit 3D Architectural Cafe Signage Fascia
    sign_w = 3200.0
    sign_h = 420.0
    m.add_box(canopy_x + 100, canopy_y + canopy_d + 10, z_level - 60, sign_w, 40, sign_h, "3D-CANOPY", "metal_dark")
    # Glowing backlit letter/logo accent band
    m.add_box(canopy_x + 180, canopy_y + canopy_d + 45, z_level + 40, sign_w - 160, 15, 220, "3D-LIGHTS", "light_glow")



def add_coffee_shop_exterior_architecture(m: Model3D):
    """
    Builds rich, multi-layered Coffee Shop Exterior Architecture:
    1. Continuous roasted basalt plinth base band with projecting drip sill ledge.
    2. Continuous horizontal dark bronze & caramel wood inter-floor belt frieze with warm LED underglow.
    3. South Elevation:
       - Central vertical roasted timber feature tower with vertical fluted battens.
       - Large 3D illuminated Roastery Signboard ("BURGOS SPECIALTY COFFEE ROASTERY") with glowing cup logo.
       - Cantilevered espresso window box hoods and timber sunshade canopies over GF & 2F windows.
       - Vertical warm caramel timber battens flanking the window bays.
       - Built-in planter troughs under GF windows with lush coffee shrubs.
       - Architectural exterior cylinder up/down sconce lights on columns.
    4. West Elevation:
       - Cantilevered box hoods and horizontal timber sunshades over panoramic windows.
       - Vertical timber battens flanking window bays.
       - Backlit circular coffee medallion signboard.
       - Planter boxes and sconce lights.
    5. North Elevation:
       - Vertical timber battens on 2F wings and GF accent screens.
    6. Roof Parapet:
       - Dark bronze parapet cap coping and warm timber horizontal frieze board.
    """
    # 1. CONTINUOUS LOWER PLINTH BAND (DARK ESPRESSO BASALT) & DRIP SILL
    m.add_box(0, -35, 0, 10000, 35, 600, "3D-WALLS-EXTR", "wood_dark")
    m.add_box(-50, -60, 570, 10100, 60, 40, "3D-WALLS-EXTR", "metal_dark")
    m.add_box(-35, 0, 0, 35, 10000, 600, "3D-WALLS-EXTR", "wood_dark")
    m.add_box(-60, -50, 570, 60, 10100, 40, "3D-WALLS-EXTR", "metal_dark")
    m.add_box(10000, 0, 0, 35, 10000, 600, "3D-WALLS-EXTR", "wood_dark")
    m.add_box(10000, -50, 570, 60, 10100, 40, "3D-WALLS-EXTR", "metal_dark")

    # 2. CONTINUOUS HORIZONTAL INTER-FLOOR BELT FRIEZE & UNDERGLOW (Z = 3700 to 3950)
    m.add_box(0, -80, 3700, 10000, 80, 250, "3D-CANOPY", "metal_dark")
    m.add_box(0, -95, 3750, 10000, 15, 150, "3D-CANOPY", "wood")
    m.add_box(0, -85, 3690, 10000, 20, 15, "3D-LIGHTS", "light_glow")
    m.add_box(-80, 0, 3700, 80, 10000, 250, "3D-CANOPY", "metal_dark")
    m.add_box(-95, 0, 3750, 15, 10000, 150, "3D-CANOPY", "wood")
    m.add_box(-85, 0, 3690, 20, 10000, 15, "3D-LIGHTS", "light_glow")
    m.add_box(10000, 0, 3700, 80, 10000, 250, "3D-CANOPY", "metal_dark")
    m.add_box(10080, 0, 3750, 15, 10000, 150, "3D-CANOPY", "wood")
    m.add_box(10065, 0, 3690, 20, 10000, 15, "3D-LIGHTS", "light_glow")

    # 3. SOUTH FACADE - CENTRAL VERTICAL TIMBER FEATURE TOWER & 3D ROASTERY SIGN
    m.add_box(4200, -40, 600, 1600, 40, 7200, "3D-LOUVERS", "wood_dark")
    for x in range(4220, 5800, 80):
        m.add_box(x, -80, 600, 40, 40, 7200, "3D-LOUVERS", "wood")

    sign_w, sign_h = 1440.0, 960.0
    sign_x, sign_y, sign_z = 4280.0, -130.0, 4200.0
    m.add_box(sign_x, sign_y, sign_z, sign_w, 50, sign_h, "3D-CANOPY", "metal_dark")
    m.add_box(sign_x + 20, sign_y - 10, sign_z + 20, sign_w - 40, 10, sign_h - 40, "3D-CANOPY", "wood_dark")
    m.add_box(sign_x + 30, sign_y - 15, sign_z + 30, sign_w - 60, 5, sign_h - 60, "3D-CANOPY", "wood")
    
    # Backlit 3D Coffee Cup Emblem
    cup_x = sign_x + sign_w / 2.0 - 90
    cup_z = sign_z + sign_h - 260
    m.add_box(cup_x, sign_y - 30, cup_z, 180, 15, 150, "3D-LIGHTS", "light_glow")
    m.add_box(cup_x + 180, sign_y - 30, cup_z + 35, 45, 15, 80, "3D-LIGHTS", "light_glow")
    m.add_box(cup_x - 20, sign_y - 30, cup_z - 20, 220, 15, 20, "3D-LIGHTS", "light_glow")
    m.add_box(cup_x + 30, sign_y - 30, cup_z + 165, 18, 15, 60, "3D-LIGHTS", "light_glow")
    m.add_box(cup_x + 80, sign_y - 30, cup_z + 175, 18, 15, 75, "3D-LIGHTS", "light_glow")
    m.add_box(cup_x + 130, sign_y - 30, cup_z + 165, 18, 15, 60, "3D-LIGHTS", "light_glow")

    # Glowing Sign Letter Bands
    m.add_box(sign_x + 120, sign_y - 30, sign_z + 460, sign_w - 240, 15, 130, "3D-LIGHTS", "light_glow")
    m.add_box(sign_x + 160, sign_y - 30, sign_z + 300, sign_w - 320, 15, 90, "3D-LIGHTS", "light_glow")
    m.add_box(sign_x + 240, sign_y - 30, sign_z + 170, sign_w - 480, 15, 60, "3D-LIGHTS", "light_glow")
    # Top lamp hood
    m.add_box(sign_x - 30, sign_y - 80, sign_z + sign_h, sign_w + 60, 120, 45, "3D-CANOPY", "metal_dark")
    m.add_box(sign_x, sign_y - 70, sign_z + sign_h - 15, sign_w, 80, 15, "3D-LIGHTS", "light_glow")

    # 4. SOUTH FACADE - CANTILEVERED WINDOW HOODS, CANOPIES & PLANTERS
    for wx1, wx2 in [(1200, 4200), (5800, 8800)]:
        ww = wx2 - wx1
        m.add_box(wx1, -160, 600, ww, 160, 50, "3D-WALLS-EXTR", "metal_dark")
        m.add_box(wx1, -220, 3250, ww, 220, 60, "3D-WALLS-EXTR", "metal_dark")
        m.add_box(wx1 - 50, -160, 600, 50, 160, 2700, "3D-WALLS-EXTR", "metal_dark")
        m.add_box(wx2, -160, 600, 50, 160, 2700, "3D-WALLS-EXTR", "metal_dark")
        
        awn_w = ww + 200
        m.add_box(wx1 - 100, -500, 3310, awn_w, 500, 45, "3D-CANOPY", "metal_dark")
        for ay in [-440, -340, -240, -140]:
            m.add_box(wx1 - 90, ay, 3320, awn_w - 20, 65, 30, "3D-CANOPY", "wood")
        m.add_cylinder(wx1 - 60, -460, 3350, 10, 320, "3D-CANOPY", "metal_dark")
        m.add_cylinder(wx2 + 60, -460, 3350, 10, 320, "3D-CANOPY", "metal_dark")

        m.add_box(wx1 + 100, -280, 600, ww - 200, 260, 320, "3D-WALLS-EXTR", "metal_dark")
        m.add_box(wx1 + 120, -270, 620, ww - 240, 240, 280, "3D-WALLS-EXTR", "wood_dark")
        m.add_box(wx1 + 130, -260, 900, ww - 260, 220, 200, "3D-FURNITURE", "wood_dark")

    for wx1, wx2 in [(1500, 4500), (5500, 8500)]:
        ww = wx2 - wx1
        m.add_box(wx1, -160, 4000, ww, 160, 50, "3D-WALLS-EXTR", "metal_dark")
        m.add_box(wx1, -220, 6450, ww, 220, 60, "3D-WALLS-EXTR", "metal_dark")
        m.add_box(wx1 - 50, -160, 4000, 50, 160, 2500, "3D-WALLS-EXTR", "metal_dark")
        m.add_box(wx2, -160, 4000, 50, 160, 2500, "3D-WALLS-EXTR", "metal_dark")

        awn_w = ww + 200
        m.add_box(wx1 - 100, -500, 6510, awn_w, 500, 45, "3D-CANOPY", "metal_dark")
        for ay in [-440, -340, -240, -140]:
            m.add_box(wx1 - 90, ay, 6520, awn_w - 20, 65, 30, "3D-CANOPY", "wood")
        m.add_cylinder(wx1 - 60, -460, 6550, 10, 320, "3D-CANOPY", "metal_dark")
        m.add_cylinder(wx2 + 60, -460, 6550, 10, 320, "3D-CANOPY", "metal_dark")

    for x in range(200, 1150, 100):
        m.add_box(x, -55, 600, 40, 45, 3100, "3D-LOUVERS", "wood")
        m.add_box(x, -55, 4000, 40, 45, 3000, "3D-LOUVERS", "wood")
    for x in range(8850, 9800, 100):
        m.add_box(x, -55, 600, 40, 45, 3100, "3D-LOUVERS", "wood")
        m.add_box(x, -55, 4000, 40, 45, 3000, "3D-LOUVERS", "wood")

    # 5. WEST FACADE - CANTILEVERED HOODS, ROASTERY MEDALLION & LOUVERS
    for wy1, wy2 in [(1200, 4200), (7600, 9400)]:
        wh = wy2 - wy1
        m.add_box(-160, wy1, 600, 160, wh, 50, "3D-WALLS-EXTR", "metal_dark")
        m.add_box(-220, wy1, 3250, 220, wh, 60, "3D-WALLS-EXTR", "metal_dark")
        m.add_box(-160, wy1 - 50, 600, 160, 50, 2700, "3D-WALLS-EXTR", "metal_dark")
        m.add_box(-160, wy2, 600, 160, 50, 2700, "3D-WALLS-EXTR", "metal_dark")
        
        m.add_box(-500, wy1 - 80, 3310, 500, wh + 160, 45, "3D-CANOPY", "metal_dark")
        for ax in [-440, -340, -240, -140]:
            m.add_box(ax, wy1 - 70, 3320, 65, wh + 140, 30, "3D-CANOPY", "wood")

    m.add_box(-160, 2000, 4000, 160, 6000, 50, "3D-WALLS-EXTR", "metal_dark")
    m.add_box(-240, 2000, 6450, 240, 6000, 60, "3D-WALLS-EXTR", "metal_dark")
    m.add_box(-160, 1950, 4000, 160, 50, 2500, "3D-WALLS-EXTR", "metal_dark")
    m.add_box(-160, 8000, 4000, 160, 50, 2500, "3D-WALLS-EXTR", "metal_dark")
    m.add_box(-520, 1900, 6510, 520, 6200, 50, "3D-CANOPY", "metal_dark")
    for ax in [-460, -360, -260, -160]:
        m.add_box(ax, 1920, 6520, 65, 6160, 30, "3D-CANOPY", "wood")

    for y in range(200, 1150, 100):
        m.add_box(-55, y, 600, 45, 40, 3100, "3D-LOUVERS", "wood")
        m.add_box(-55, y, 4000, 45, 40, 3000, "3D-LOUVERS", "wood")
    for y in range(8050, 9800, 100):
        m.add_box(-55, y, 600, 45, 40, 3100, "3D-LOUVERS", "wood")
        m.add_box(-55, y, 4000, 45, 40, 3000, "3D-LOUVERS", "wood")

    # Round Coffee Medallion
    m.add_cylinder(-80, 5000, 4800, 450, 40, "3D-CANOPY", "metal_dark")
    m.add_cylinder(-100, 5000, 4810, 390, 20, "3D-LIGHTS", "light_glow")
    m.add_cylinder(-110, 5000, 4815, 280, 15, "3D-CANOPY", "wood_dark")
    m.add_cylinder(-115, 5000, 4820, 150, 15, "3D-LIGHTS", "light_glow")

    # 6. NORTH FACADE - LOUVERS
    for x in range(240, 2400, 120):
        m.add_box(x, 10010, 4000, 40, 70, 2800, "3D-LOUVERS", "wood")
    for x in range(7600, 9760, 120):
        m.add_box(x, 10010, 4000, 40, 70, 2800, "3D-LOUVERS", "wood")
    for x in range(4050, 5200, 120):
        m.add_box(x, 10010, 600, 40, 70, 3000, "3D-LOUVERS", "wood")

    # 7. PARAPET CAP & ROOF FRIEZE
    m.add_box(-40, -40, 7780, 10080, 280, 50, "3D-ROOF", "metal_dark")
    m.add_box(-40, 9760, 7780, 10080, 280, 50, "3D-ROOF", "metal_dark")
    m.add_box(-40, -40, 7780, 280, 10080, 50, "3D-ROOF", "metal_dark")
    m.add_box(9760, -40, 7780, 280, 10080, 50, "3D-ROOF", "metal_dark")
    m.add_box(0, -50, 7200, 10000, 40, 220, "3D-ROOF", "wood")
    m.add_box(-50, 0, 7200, 40, 10000, 220, "3D-ROOF", "wood")
    m.add_box(10010, 0, 7200, 40, 10000, 220, "3D-ROOF", "wood")

    # 8. EXTERIOR WALL SCONCES
    for sx in [200, 4100, 5900, 9800]:
        for sz in [2300, 5600]:
            m.add_cylinder(sx, -70, sz, 32, 140, "3D-LIGHTS", "metal_dark")
            m.add_cylinder(sx, -70, sz + 135, 36, 20, "3D-LIGHTS", "light_glow")
            m.add_cylinder(sx, -70, sz - 15, 36, 20, "3D-LIGHTS", "light_glow")
    for sy in [200, 4100, 7600, 9800]:
        for sz in [2300, 5600]:
            m.add_cylinder(-70, sy, sz, 32, 140, "3D-LIGHTS", "metal_dark")
            m.add_cylinder(-70, sy, sz + 135, 36, 20, "3D-LIGHTS", "light_glow")
            m.add_cylinder(-70, sy, sz - 15, 36, 20, "3D-LIGHTS", "light_glow")

def add_vertical_facade_louvers_old(m: Model3D):
    """
    Adds Japanese / Scandinavian vertical timber battens (wood louvers) to the exterior facade,
    giving rhythmic shadow depth, texture, and architectural warmth (NO flat solid monoliths!).
    """
    z_start = 4000.0
    slat_h = 2800.0
    slat_w = 40.0
    slat_d = 70.0
    pitch = 120.0

    # 2nd Floor North Facade - Left Wing (X = 200 to 2400, Y = 10020)
    for x in range(240, 2400, int(pitch)):
        m.add_box(x, 10010, z_start, slat_w, slat_d, slat_h, "3D-LOUVERS", "wood")

    # 2nd Floor North Facade - Right Wing (X = 7600 to 9760, Y = 10020)
    for x in range(7600, 9760, int(pitch)):
        m.add_box(x, 10010, z_start, slat_w, slat_d, slat_h, "3D-LOUVERS", "wood")

    # Ground Floor North Entrance Accent Screen (X = 4000 to 5200, Y = 10010, Z = 600 to 3600)
    for x in range(4050, 5200, int(pitch)):
        m.add_box(x, 10010, 600, slat_w, slat_d, 3000, "3D-LOUVERS", "wood")


# ==============================================================================
# 3D ARCHITECTURAL ASSEMBLIES BUILDER
# ==============================================================================

def build_coffee_shop_3d_model():
    """Builds the complete 3D architectural geometry and interior of the Coffee Shop."""
    m = Model3D()

    # Elevation datum heights (in mm)
    Z_GRADE = 0.0
    Z_FFL_GF = 600.0       # Ground floor finish floor (+600mm)
    Z_SLAB_2F = 3800.0     # 2nd floor slab bottom
    Z_FFL_2F = 4000.0      # 2nd floor finish floor (+4000mm)
    Z_BALC_FFL = 3950.0    # Balcony finish floor (+3950mm, 50mm weather drop)
    Z_ROOF = 7000.0        # Roof slab bottom
    Z_ROOF_TOP = 7200.0    # Roof slab top
    Z_PARAPET = 7800.0     # Roof parapet top (+7800mm)

    # --------------------------------------------------------------------------
    # 1. FOUNDATION, PLINTH & ENTRANCE STEPS
    # --------------------------------------------------------------------------
    # Main Foundation Plinth (10,000mm x 10,000mm)
    m.add_box(0, 0, Z_GRADE, 10000, 10000, Z_FFL_GF, "3D-SLABS", "concrete")

    # North Entrance Plinth Steps (3 steps = +600mm level change, risers 200mm, treads 300mm)
    step_w = 2600.0
    sx0 = 1600.0
    m.add_box(sx0, 10600, Z_GRADE, step_w, 300, 200, "3D-STAIRS", "concrete")
    m.add_box(sx0, 10300, Z_GRADE, step_w, 300, 400, "3D-STAIRS", "concrete")
    m.add_box(sx0, 10000, Z_GRADE, step_w, 300, 600, "3D-STAIRS", "concrete")

    # Entrance Architectural Dark Charcoal Planter Trough (No Neon Foliage!)
    m.add_box(4300, 10100, Z_GRADE, 1000, 550, 500, "3D-WALLS-EXTR", "metal_dark")
    m.add_box(4340, 10140, 500, 920, 470, 80, "3D-FURNITURE", "wood_dark")

    # Hardwood Parquet Finish Floors (Rich Scandinavian Parquet Texture)
    m.add_box(200, 200, Z_FFL_GF - 10, 9600, 9600, 10, "3D-FINISH", "floor")
    m.add_box(200, 200, Z_FFL_2F - 10, 9600, 9600, 10, "3D-FINISH", "floor")

    # --------------------------------------------------------------------------
    # 2. REINFORCED CONCRETE STRUCTURAL COLUMNS (400x400) & BEAMS
    # --------------------------------------------------------------------------
    col_coords = [
        (0, 0), (9600, 0), (0, 9600), (9600, 9600),
        (4800, 0), (4800, 9600), (0, 4800), (9600, 4800),
        (4800, 4800)
    ]
    for cx, cy in col_coords:
        m.add_box(cx, cy, Z_GRADE, 400, 400, Z_PARAPET, "3D-COLUMNS", "concrete")

    # Structural Beams connecting columns
    for y in [0, 4800, 9600]:
        m.add_box(0, y, 3600, 10000, 400, 200, "3D-COLUMNS", "concrete")
    for x in [0, 4800, 9600]:
        m.add_box(x, 0, 3600, 400, 10000, 200, "3D-COLUMNS", "concrete")

    # --------------------------------------------------------------------------
    # 3. GROUND FLOOR EXTERIOR WALLS & STOREFRONT GLAZING
    # --------------------------------------------------------------------------
    H_GF_WALL = 3200.0

    # SOUTH WALL (Y = 0 to 200)
    m.add_box(0, 0, Z_FFL_GF, 1200, 200, H_GF_WALL, "3D-WALLS-EXTR", "wall")
    m.add_box(4200, 0, Z_FFL_GF, 1600, 200, H_GF_WALL, "3D-WALLS-EXTR", "wall")
    m.add_box(8800, 0, Z_FFL_GF, 1200, 200, H_GF_WALL, "3D-WALLS-EXTR", "wall")
    for wx1, wx2 in [(1200, 4200), (5800, 8800)]:
        ww = wx2 - wx1
        m.add_box(wx1, 0, Z_FFL_GF, ww, 200, 900, "3D-WALLS-EXTR", "wall")
        m.add_box(wx1 + 40, 80, Z_FFL_GF + 900, ww - 80, 40, 1800, "3D-GLAZING", "glass")
        m.add_box(wx1, 0, Z_FFL_GF + 2700, ww, 200, 500, "3D-WALLS-EXTR", "wall")

    # WEST WALL (X = 0 to 200)
    m.add_box(0, 0, Z_FFL_GF, 200, 1200, H_GF_WALL, "3D-WALLS-EXTR", "wall")
    m.add_box(0, 4200, Z_FFL_GF, 200, 3400, H_GF_WALL, "3D-WALLS-EXTR", "wall")
    m.add_box(0, 9400, Z_FFL_GF, 200, 600, H_GF_WALL, "3D-WALLS-EXTR", "wall")
    for wy1, wy2 in [(1200, 4200), (7600, 9400)]:
        wh = wy2 - wy1
        m.add_box(0, wy1, Z_FFL_GF, 200, wh, 900, "3D-WALLS-EXTR", "wall")
        m.add_box(80, wy1 + 40, Z_FFL_GF + 900, 40, wh - 80, 1800, "3D-GLAZING", "glass")
        m.add_box(0, wy1, Z_FFL_GF + 2700, 200, wh, 500, "3D-WALLS-EXTR", "wall")

    # EAST WALL (X = 9800 to 10000)
    m.add_box(9800, 0, Z_FFL_GF, 200, 2200, H_GF_WALL, "3D-WALLS-EXTR", "wall")
    m.add_box(9800, 5000, Z_FFL_GF, 200, 2500, H_GF_WALL, "3D-WALLS-EXTR", "wall")
    m.add_box(9800, 8800, Z_FFL_GF, 200, 1200, H_GF_WALL, "3D-WALLS-EXTR", "wall")
    for wy1, wy2 in [(2200, 5000), (7500, 8800)]:
        wh = wy2 - wy1
        m.add_box(9800, wy1, Z_FFL_GF, 200, wh, 900, "3D-WALLS-EXTR", "wall")
        m.add_box(9880, wy1 + 40, Z_FFL_GF + 900, 40, wh - 80, 1800, "3D-GLAZING", "glass")
        m.add_box(9800, wy1, Z_FFL_GF + 2700, 200, wh, 500, "3D-WALLS-EXTR", "wall")

    # NORTH FACADE & STOREFRONT (Y = 9800 to 10000)
    m.add_box(0, 9800, Z_FFL_GF, 2000, 200, H_GF_WALL, "3D-WALLS-EXTR", "wall")
    m.add_box(3800, 9800, Z_FFL_GF, 1400, 200, H_GF_WALL, "3D-WALLS-EXTR", "wall")
    m.add_box(9400, 9800, Z_FFL_GF, 600, 200, H_GF_WALL, "3D-WALLS-EXTR", "wall")

    # North 1800mm Commercial Double Door Opening
    m.add_box(2000, 9800, Z_FFL_GF + 2400, 1800, 200, 800, "3D-WALLS-EXTR", "wall")
    m.add_box(2030, 9860, Z_FFL_GF, 840, 50, 2360, "3D-DOORS", "metal_dark")
    m.add_box(2930, 9860, Z_FFL_GF, 840, 50, 2360, "3D-DOORS", "metal_dark")
    m.add_box(2110, 9875, Z_FFL_GF + 100, 680, 20, 2160, "3D-GLAZING", "glass")
    m.add_box(3010, 9875, Z_FFL_GF + 100, 680, 20, 2160, "3D-GLAZING", "glass")

    # North Storefront Glazing Curtain Wall
    m.add_box(5200, 9800, Z_FFL_GF, 4200, 200, 150, "3D-WALLS-EXTR", "wall")
    m.add_box(5200, 9800, Z_FFL_GF + 3000, 4200, 200, 200, "3D-WALLS-EXTR", "wall")
    m.add_box(5250, 9880, Z_FFL_GF + 150, 4100, 40, 2850, "3D-GLAZING", "glass")
    # Black Aluminum Storefront Mullions
    for mx in [5200, 6600, 8000, 9360]:
        m.add_box(mx, 9860, Z_FFL_GF + 150, 50, 70, 2850, "3D-GLAZING", "metal_dark")

    # Cantilevered Entrance Canopy, Recessed Downlights & Backlit Signage
    add_entrance_canopy_and_signage(m, z_level=3400.0)

    # --------------------------------------------------------------------------
    # 4. GROUND FLOOR PWD RESTROOM
    # --------------------------------------------------------------------------
    m.add_box(7700, 2200, Z_FFL_GF, 2100, 100, 2800, "3D-WALLS-INTR", "wall")
    m.add_box(7700, 200, Z_FFL_GF, 100, 700, 2800, "3D-WALLS-INTR", "wall")
    m.add_box(7700, 1800, Z_FFL_GF, 100, 500, 2800, "3D-WALLS-INTR", "wall")
    m.add_box(7700, 900, Z_FFL_GF + 2100, 100, 900, 700, "3D-WALLS-INTR", "wall")
    m.add_box(7720, 920, Z_FFL_GF, 50, 860, 2050, "3D-DOORS", "wood")

    # Restroom Vanity & Fixtures
    m.add_box(8000, 1400, Z_FFL_GF + 750, 1200, 500, 60, "3D-FURNITURE", "quartz")
    m.add_box(8300, 1450, Z_FFL_GF + 700, 500, 380, 150, "3D-FURNITURE", "quartz")
    m.add_box(8500, 1420, Z_FFL_GF + 850, 40, 60, 220, "3D-FURNITURE", "metal_dark")
    m.add_box(8200, 1950, Z_FFL_GF + 1100, 700, 20, 800, "3D-FURNITURE", "glass")
    m.add_box(9200, 450, Z_FFL_GF, 500, 200, 800, "3D-FURNITURE", "fixture_white")
    m.add_box(9260, 650, Z_FFL_GF, 380, 450, 450, "3D-FURNITURE", "fixture_white")

    # --------------------------------------------------------------------------
    # 5. U-SHAPED STAIRCASE TO SECOND FLOOR
    # --------------------------------------------------------------------------
    run_d = 280.0
    for i in range(8):
        sy = 5000.0 + i * run_d
        sh = (i + 1) * 188.0
        m.add_box(7800, sy, Z_FFL_GF, 1000, run_d, sh, "3D-STAIRS", "wood")

    # Intermediate Landing
    m.add_box(7800, 7240, Z_FFL_GF, 2000, 1000, 1700, "3D-STAIRS", "wood")

    # Flight 2
    for i in range(8):
        sy = 7240.0 - (i + 1) * run_d
        sh = 1700.0 + (i + 1) * 188.0
        m.add_box(8800, sy, Z_FFL_GF, 1000, run_d, sh, "3D-STAIRS", "wood")

    # Japandi Vertical Slatted Balustrade Screen
    for y_slat in range(5000, 7500, 120):
        m.add_box(7760, y_slat, Z_FFL_GF, 30, 40, 3350, "3D-STAIRS", "metal_dark")
    m.add_box(7750, 5000, Z_FFL_GF, 50, 2500, 40, "3D-STAIRS", "metal_dark")
    m.add_box(7750, 5000, Z_FFL_GF + 3310, 50, 2500, 40, "3D-STAIRS", "metal_dark")

    # --------------------------------------------------------------------------
    # 6. HIGH-END BARISTA BAR & REFRIGERATORS (RELEBOOK ARCHVIZ)
    # --------------------------------------------------------------------------
    # Back Prep Counter Base & Worktop
    m.add_box(200, 3500, Z_FFL_GF, 600, 3500, 850, "3D-BARISTA-BAR", "metal_dark")
    m.add_box(180, 3480, Z_FFL_GF + 850, 640, 3540, 40, "3D-BARISTA-BAR", "quartz")

    # Commercial Upright Double-Door Refrigerator ("Ref") - No Foliage!
    add_commercial_refrigerator(m, 200, 7100, Z_FFL_GF)

    # Undercounter Glass Beverage Cooler
    add_undercounter_cooler(m, 2000, 4000, Z_FFL_GF)

    # Commercial Ice Machine & Prep Sink
    m.add_box(200, 2700, Z_FFL_GF, 650, 700, 920, "3D-BARISTA-BAR", "appliance_steel")
    m.add_box(200, 2300, Z_FFL_GF, 600, 400, 850, "3D-BARISTA-BAR", "metal_dark")
    m.add_box(300, 2400, Z_FFL_GF + 850, 400, 280, 20, "3D-BARISTA-BAR", "appliance_steel")
    m.add_cylinder(480, 2540, Z_FFL_GF + 870, 14, 240, "3D-BARISTA-BAR", "metal_dark")

    # Front Service L-Counter with Fluted Slat Wood & Calacatta Quartz Countertop
    m.add_box(2000, 3500, Z_FFL_GF, 600, 3500, 860, "3D-BARISTA-BAR", "wood_fluted")
    m.add_box(1960, 3460, Z_FFL_GF + 860, 680, 3580, 50, "3D-BARISTA-BAR", "quartz")
    m.add_box(2600, 3500, Z_FFL_GF, 1900, 600, 860, "3D-BARISTA-BAR", "wood_fluted")
    m.add_box(2600, 3460, Z_FFL_GF + 860, 1940, 680, 50, "3D-BARISTA-BAR", "quartz")

    # Linear Warm LED Under-Counter Lip Strip Light
    m.add_box(2600, 3450, Z_FFL_GF + 850, 1940, 15, 12, "3D-LIGHTS", "light_glow")
    m.add_box(1950, 3460, Z_FFL_GF + 850, 15, 3580, 12, "3D-LIGHTS", "light_glow")

    # 3-Group Commercial Espresso Machine & Coffee Grinders
    add_espresso_station(m, 2050, 5600, Z_FFL_GF + 910)

    # POS Touchscreen & Payment Station
    m.add_box(2150, 4350, Z_FFL_GF + 910, 320, 320, 180, "3D-BARISTA-BAR", "metal_dark")
    m.add_box(2200, 4380, Z_FFL_GF + 1090, 220, 260, 20, "3D-BARISTA-BAR", "light_glow")

    # Illuminated Pastry Showcase with Tiered Wooden Pastry Trays
    add_pastry_showcase(m, 2850, 3550, Z_FFL_GF + 910)

    # Wall Slat Feature & Open Shelves behind Bar
    m.add_box(200, 3500, Z_FFL_GF + 900, 30, 3500, 2500, "3D-WALLS-INTR", "wood_dark")
    for sy in [1200, 1650, 2100]:
        m.add_box(230, 3700, Z_FFL_GF + sy, 220, 3000, 30, "3D-BARISTA-BAR", "wood")
        for bx in [3900, 4500, 5100, 5700, 6300]:
            m.add_box(250, bx, Z_FFL_GF + sy + 30, 120, 140, 180, "3D-BARISTA-BAR", "fixture_white")

    # Flush-mounted Back Wall Menu Board
    m.add_box(230, 4200, Z_FFL_GF + 2350, 20, 2200, 550, "3D-BARISTA-BAR", "metal_dark")

    # 3 Warm Overhead Brass Cone Pendant Lights over Barista Bar (with glowing diffusers!)
    for py in [4200, 5200, 6200]:
        add_pendant_light(m, 2300, py, Z_FFL_GF + 3200, cord_len=1000, shade_r=130, shade_h=160)

    # Minimalist Modern Bar Stools along return counter
    for bx in [2900, 3500, 4100]:
        add_modern_bar_stool(m, bx, 3050, Z_FFL_GF, seat_mat="leather")

    # --------------------------------------------------------------------------
    # 7. GROUND FLOOR ABUNDANT DINING & LOUNGE SEATING
    # --------------------------------------------------------------------------
    # 4.5m Upholstered Caramel Leather Banquette Booth Bench along South Wall
    banq_x = 1400.0
    banq_w = 4400.0
    m.add_box(banq_x, 220, Z_FFL_GF, banq_w, 550, 440, "3D-FURNITURE", "leather")
    m.add_box(banq_x, 220, Z_FFL_GF + 440, banq_w, 130, 480, "3D-FURNITURE", "leather")
    m.add_box(banq_x, 200, Z_FFL_GF, banq_w, 20, 920, "3D-FURNITURE", "wood_dark")
    # Warm LED strip reveal beneath banquette plinth
    m.add_box(banq_x, 760, Z_FFL_GF + 20, banq_w, 15, 12, "3D-LIGHTS", "light_glow")

    # 4 Dining Tables with Pedestal Bases & 8 Scandinavian Bentwood Chairs
    for i, tx in enumerate([1800, 2900, 4000, 5100]):
        add_pedestal_dining_table(m, tx, 1350, Z_FFL_GF, radius=375, height=730, top_mat="wood", base_mat="metal_dark")
        # 2 Chairs per table (one facing banquette, one angled)
        add_modern_chair(m, tx, 1950, Z_FFL_GF, angle_deg=180, seat_mat="leather", frame_mat="metal_dark")
        add_modern_chair(m, tx - 400, 1350, Z_FFL_GF, angle_deg=90, seat_mat="leather", frame_mat="metal_dark")
        # Overhead pendant lamp above each dining table!
        add_pendant_light(m, tx, 1350, Z_FFL_GF + 3200, cord_len=1100, shade_r=110, shade_h=140)

    # Storefront Window Bar Counter & 5 Bar Stools
    m.add_box(5300, 9400, Z_FFL_GF + 860, 4000, 450, 45, "3D-FURNITURE", "wood")
    m.add_box(5350, 9400, Z_FFL_GF, 50, 450, 860, "3D-FURNITURE", "metal_dark")
    m.add_box(9250, 9400, Z_FFL_GF, 50, 450, 860, "3D-FURNITURE", "metal_dark")
    for sx in [5700, 6500, 7300, 8100, 8900]:
        add_modern_bar_stool(m, sx, 8900, Z_FFL_GF, seat_mat="leather")

    # Central Round Bistro Tables & Bentwood Chairs
    for cx, cy in [(6200, 1600), (6600, 3200), (5200, 3100)]:
        add_pedestal_dining_table(m, cx, cy, Z_FFL_GF, radius=420, height=730, top_mat="quartz", base_mat="metal_dark")
        for ang in [0.3, 3.4]:
            px = cx + math.cos(ang) * 650
            py = cy + math.sin(ang) * 650
            add_modern_chair(m, px, py, Z_FFL_GF, angle_deg=math.degrees(ang) + 180, seat_mat="leather", frame_mat="metal_dark")

    # Scandinavian Armchair Lounge Corner
    add_lounge_armchair(m, 5800, 4700, Z_FFL_GF, angle_deg=45)
    add_lounge_armchair(m, 6800, 4700, Z_FFL_GF, angle_deg=-45)
    m.add_cylinder(6300, 4700, Z_FFL_GF, 280, 420, "3D-FURNITURE", "wood")

    # Self-Serve Water & Condiment Credenza
    m.add_box(5600, 250, Z_FFL_GF, 1000, 450, 850, "3D-FURNITURE", "wood_dark")
    m.add_cylinder(5900, 450, Z_FFL_GF + 850, 100, 280, "3D-FURNITURE", "glass")

    # --------------------------------------------------------------------------
    # 8. SECOND FLOOR SLAB & CANTILEVERED BALCONY (2.5M PROJECTION)
    # --------------------------------------------------------------------------
    SLAB_THK = 200.0

    m.add_box(0, 0, Z_SLAB_2F, 10000, 4000, SLAB_THK, "3D-SLABS", "concrete")
    m.add_box(0, 7500, Z_SLAB_2F, 10000, 2500, SLAB_THK, "3D-SLABS", "concrete")
    m.add_box(3800, 4000, Z_SLAB_2F, 4000, 3500, SLAB_THK, "3D-SLABS", "concrete")
    m.add_box(0, 4000, Z_SLAB_2F, 1200, 3500, SLAB_THK, "3D-SLABS", "concrete")
    m.add_box(9800, 4000, Z_SLAB_2F, 200, 3500, SLAB_THK, "3D-SLABS", "concrete")
    m.add_box(7800, 4000, Z_SLAB_2F, 2000, 1000, SLAB_THK, "3D-SLABS", "concrete")

    # Cantilevered Balcony Slab (2.5m projection)
    m.add_box(0, 10000, Z_SLAB_2F, 10000, 2500, 150, "3D-SLABS", "concrete")

    # Balcony Glass Balustrade & Metal Handrails
    m.add_box(50, 12450, Z_BALC_FFL, 9900, 30, 1080, "3D-GLAZING", "glass")
    m.add_box(0, 12430, Z_BALC_FFL + 1080, 10000, 70, 40, "3D-GLAZING", "metal_dark")
    m.add_box(50, 10000, Z_BALC_FFL, 30, 2450, 1080, "3D-GLAZING", "glass")
    m.add_box(30, 10000, Z_BALC_FFL + 1080, 70, 2470, 40, "3D-GLAZING", "metal_dark")
    m.add_box(9920, 10000, Z_BALC_FFL, 30, 2450, 1080, "3D-GLAZING", "glass")
    m.add_box(9900, 10000, Z_BALC_FFL + 1080, 70, 2470, 40, "3D-GLAZING", "metal_dark")

    # Balcony Architectural Black Steel Pergola Trellis with 14 Festoon Lights!
    add_balcony_pergola_with_lights(m, z_balc=Z_BALC_FFL, z_pergola=6900.0)

    # Balcony Outdoor Bistro Dining Tables & Chairs (4 Sets)
    for bx in [1600, 4000, 6400, 8600]:
        add_pedestal_dining_table(m, bx, 11200, Z_BALC_FFL, radius=350, height=720, top_mat="metal_dark", base_mat="metal_dark")
        add_modern_chair(m, bx - 480, 11200, Z_BALC_FFL, angle_deg=90, seat_mat="metal_dark", frame_mat="metal_dark")
        add_modern_chair(m, bx + 480, 11200, Z_BALC_FFL, angle_deg=270, seat_mat="metal_dark", frame_mat="metal_dark")

    # Low Architectural Planters on Balcony (Dark Charcoal, No Neon Green!)
    m.add_box(200, 12200, Z_BALC_FFL, 1600, 220, 350, "3D-WALLS-EXTR", "metal_dark")
    m.add_box(8200, 12200, Z_BALC_FFL, 1600, 220, 350, "3D-WALLS-EXTR", "metal_dark")

    # Void Edge Glass Railing (Atrium overlooking GF)
    m.add_box(1200, 4000, Z_FFL_2F, 2600, 40, 1100, "3D-GLAZING", "glass")
    m.add_box(1200, 6960, Z_FFL_2F, 2600, 40, 1100, "3D-GLAZING", "glass")
    m.add_box(3760, 4000, Z_FFL_2F, 40, 3000, 1100, "3D-GLAZING", "glass")

    # --------------------------------------------------------------------------
    # 9. SECOND FLOOR WALLS, LOUVERS & PANORAMIC WINDOWS
    # --------------------------------------------------------------------------
    H_2F_WALL = 3000.0

    # SOUTH WALL
    m.add_box(0, 0, Z_FFL_2F, 1500, 200, H_2F_WALL, "3D-WALLS-EXTR", "wall")
    m.add_box(4500, 0, Z_FFL_2F, 1000, 200, H_2F_WALL, "3D-WALLS-EXTR", "wall")
    m.add_box(8500, 0, Z_FFL_2F, 1500, 200, H_2F_WALL, "3D-WALLS-EXTR", "wall")
    for wx1, wx2 in [(1500, 4500), (5500, 8500)]:
        ww = wx2 - wx1
        m.add_box(wx1, 0, Z_FFL_2F, ww, 200, 800, "3D-WALLS-EXTR", "wall")
        m.add_box(wx1 + 40, 80, Z_FFL_2F + 800, ww - 80, 40, 1700, "3D-GLAZING", "glass")
        m.add_box(wx1, 0, Z_FFL_2F + 2500, ww, 200, 500, "3D-WALLS-EXTR", "wall")

    # WEST WALL
    m.add_box(0, 0, Z_FFL_2F, 200, 2000, H_2F_WALL, "3D-WALLS-EXTR", "wall")
    m.add_box(0, 8000, Z_FFL_2F, 200, 2000, H_2F_WALL, "3D-WALLS-EXTR", "wall")
    m.add_box(0, 2000, Z_FFL_2F, 200, 6000, 700, "3D-WALLS-EXTR", "wall")
    m.add_box(80, 2050, Z_FFL_2F + 700, 40, 5900, 1800, "3D-GLAZING", "glass")
    m.add_box(0, 2000, Z_FFL_2F + 2500, 200, 6000, 500, "3D-WALLS-EXTR", "wall")

    # EAST WALL
    m.add_box(9800, 0, Z_FFL_2F, 200, 2200, H_2F_WALL, "3D-WALLS-EXTR", "wall")
    m.add_box(9800, 5000, Z_FFL_2F, 200, 2500, H_2F_WALL, "3D-WALLS-EXTR", "wall")
    m.add_box(9800, 8500, Z_FFL_2F, 200, 1500, H_2F_WALL, "3D-WALLS-EXTR", "wall")
    for wy1, wy2 in [(2200, 5000), (7500, 8500)]:
        wh = wy2 - wy1
        m.add_box(9800, wy1, Z_FFL_2F, 200, wh, 800, "3D-WALLS-EXTR", "wall")
        m.add_box(9880, wy1 + 40, Z_FFL_2F + 800, 40, wh - 80, 1700, "3D-GLAZING", "glass")
        m.add_box(9800, wy1, Z_FFL_2F + 2500, 200, wh, 500, "3D-WALLS-EXTR", "wall")

    # NORTH FACADE & SLIDING BALCONY PORTAL
    m.add_box(0, 9800, Z_FFL_2F, 2500, 200, H_2F_WALL, "3D-WALLS-EXTR", "wall")
    m.add_box(7500, 9800, Z_FFL_2F, 2500, 200, H_2F_WALL, "3D-WALLS-EXTR", "wall")
    m.add_box(2500, 9800, Z_FFL_2F + 2500, 5000, 200, 500, "3D-WALLS-EXTR", "wall")
    m.add_box(2550, 9880, Z_FFL_2F, 4900, 40, 2480, "3D-GLAZING", "glass")
    for fx in [2500, 3750, 5000, 6250, 7450]:
        m.add_box(fx, 9860, Z_FFL_2F, 50, 80, 2500, "3D-DOORS", "metal_dark")

    # Add Vertical Architectural Timber Battens (Wood Louvers on Facade)
    add_coffee_shop_exterior_architecture(m)

    # --------------------------------------------------------------------------
    # 10. SECOND FLOOR LOUNGE, CO-WORKING & PRIVATE STUDY BOOTHS
    # --------------------------------------------------------------------------
    # Modular Low-Slung Designer Sectional Sofa (Cognac Leather)
    add_modular_lounge_sofa(m, 1600, 500, Z_FFL_2F)

    # Round Nesting Trio Coffee Tables (Smoked Oak + Calacatta Quartz)
    m.add_cylinder(2700, 1800, Z_FFL_2F + 340, 350, 32, "3D-FURNITURE", "wood_dark")
    m.add_cylinder(2700, 1800, Z_FFL_2F, 28, 340, "3D-FURNITURE", "metal_dark")
    m.add_cylinder(3200, 1550, Z_FFL_2F + 400, 260, 30, "3D-FURNITURE", "quartz")
    m.add_cylinder(3200, 1550, Z_FFL_2F, 25, 400, "3D-FURNITURE", "metal_dark")

    # Scandinavian Accent Lounge Tub Chairs
    for ax, ay in [(1800, 4800), (2800, 4800)]:
        add_modern_chair(m, ax + 375, ay + 375, Z_FFL_2F, angle_deg=0, seat_mat="leather", frame_mat="wood_dark")

    # Communal Co-working Oak Table with Trestle Legs (3.5m x 1.0m)
    tbl_x, tbl_y = 4600.0, 4500.0
    tbl_w = 3400.0
    m.add_box(tbl_x, tbl_y, Z_FFL_2F + 710, tbl_w, 1000, 50, "3D-FURNITURE", "wood")
    m.add_box(tbl_x + 300, tbl_y + 460, Z_FFL_2F + 755, tbl_w - 600, 80, 10, "3D-FURNITURE", "metal_dark")
    m.add_box(tbl_x + 200, tbl_y + 100, Z_FFL_2F, 80, 800, 710, "3D-FURNITURE", "metal_dark")
    m.add_box(tbl_x + tbl_w - 280, tbl_y + 100, Z_FFL_2F, 80, 800, 710, "3D-FURNITURE", "metal_dark")

    # Linear Suspended Pendant Task Light over Communal Desk
    m.add_box(tbl_x + 400, tbl_y + 485, Z_FFL_2F + 1900, tbl_w - 800, 30, 25, "3D-LIGHTS", "metal_dark")
    m.add_box(tbl_x + 400, tbl_y + 490, Z_FFL_2F + 1890, tbl_w - 800, 20, 10, "3D-LIGHTS", "light_glow")
    # Suspension wires
    m.add_cylinder(tbl_x + 600, tbl_y + 500, Z_FFL_2F + 1925, 3, 1000, "3D-LIGHTS", "metal_dark")
    m.add_cylinder(tbl_x + tbl_w - 600, tbl_y + 500, Z_FFL_2F + 1925, 3, 1000, "3D-LIGHTS", "metal_dark")

    # 8 Ergonomic Modern Work Chairs
    for i in range(4):
        cx = tbl_x + 425.0 + i * 850.0
        add_modern_chair(m, cx, tbl_y + 1250, Z_FFL_2F, angle_deg=180, seat_mat="leather", frame_mat="metal_dark")
        add_modern_chair(m, cx, tbl_y - 250, Z_FFL_2F, angle_deg=0, seat_mat="leather", frame_mat="metal_dark")

    # 2 Private Focus / Study Booth Pods along East partition (with timber screens & lamps)
    add_private_study_booth(m, 8400, 2500, Z_FFL_2F)
    add_private_study_booth(m, 8400, 3600, Z_FFL_2F)

    # 2nd Floor West Window Study Bar Counter & 4 Bar Stools
    m.add_box(250, 2200, Z_FFL_2F + 710, 400, 3800, 45, "3D-FURNITURE", "wood")
    for wy in [2600, 3400, 4200, 5000]:
        add_modern_bar_stool(m, 780, wy, Z_FFL_2F, seat_mat="leather")

    # Open Japandi Slatted Display Shelf
    add_open_japandi_shelf(m, 4500, 220, Z_FFL_2F, width=3200, height=2200)

    # Large Modern Framed Wall Canvas
    m.add_box(1800, 220, Z_FFL_2F + 1200, 1800, 30, 1100, "3D-FURNITURE", "wood_dark")

    # --------------------------------------------------------------------------
    # 11. ROOF SLAB & PARAPET
    # --------------------------------------------------------------------------
    m.add_box(0, 0, Z_ROOF, 10000, 10000, 200, "3D-ROOF", "concrete")
    m.add_box(0, 0, Z_ROOF_TOP, 10000, 200, 600, "3D-ROOF", "wall")
    m.add_box(0, 9800, Z_ROOF_TOP, 10000, 200, 600, "3D-ROOF", "wall")
    m.add_box(0, 200, Z_ROOF_TOP, 200, 9600, 600, "3D-ROOF", "wall")
    m.add_box(9800, 200, Z_ROOF_TOP, 200, 9600, 600, "3D-ROOF", "wall")

    # --------------------------------------------------------------------------
    # 12. ACCURATE 3D ARCHITECTURAL DIMENSION CHAINS (Sukat)
    # --------------------------------------------------------------------------
    m.add_dimension((0, -600, 0), (10000, -600, 0), "10.00 m", "OVERALL WIDTH", "x")
    m.add_dimension((-600, 0, 0), (-600, 10000, 0), "10.00 m", "OVERALL LENGTH", "y")
    m.add_dimension((10600, 10000, 3950), (10600, 12500, 3950), "2.50 m", "BALCONY PROJECTION", "y")
    m.add_dimension((-600, 10000, 0), (-600, 10000, 7800), "7.80 m", "PARAPET HEIGHT", "z")
    m.add_dimension((0, 12800, 4000), (10000, 12800, 4000), "10.00 m", "BALCONY WIDTH", "x")
    m.add_dimension((-500, 10000, 0), (-500, 10000, 600), "0.60 m", "PLINTH FFL", "z")
    m.add_dimension((-500, 10000, 600), (-500, 10000, 4000), "3.40 m", "STORY 1 HEIGHT", "z")
    m.add_dimension((2000, 7150, 1600), (2000, 3500, 1600), "3.50 m", "BARISTA LENGTH", "y")
    m.add_dimension((2000, 3350, 1600), (4500, 3350, 1600), "2.50 m", "BARISTA RETURN", "x")
    m.add_dimension((4600, 4350, 4800), (8000, 4350, 4800), "3.40 m", "COMMUNAL TABLE", "x")

    return m


# ==============================================================================
# EXPORT 1: TRUE 3D DXF GENERATOR (AutoCAD / SketchUp / Rhino)
# ==============================================================================

def export_dxf_3d(model: Model3D, output_path="coffee_shop_3d.dxf"):
    """Exports model into a clean 3D DXF file with 3DFACE entities on distinct layers."""
    print(f"-> Generating 3D DXF: '{output_path}'...")
    doc = ezdxf.new('R2010', setup=True)
    doc.units = ezdxf.units.MM
    doc.header['$INSUNITS'] = 4
    doc.header['$MEASUREMENT'] = 1
    msp = doc.modelspace()

    layers_needed = sorted(list(set(box[6] for box in model.boxes) | set(cyl[5] for cyl in model.cylinders)))
    for lyr in layers_needed:
        if lyr not in doc.layers:
            doc.layers.add(lyr, color=7)

    for x, y, z, w, d, h, layer, mat in model.boxes:
        cube = forms.cube(center=False)
        cube.scale(w, d, h)
        cube.translate(x, y, z)
        cube.render_3dfaces(msp, dxfattribs={'layer': layer, 'color': 7})

    segments = 16
    for cx, cy, z, r, h, layer, mat in model.cylinders:
        pts_bottom = []
        pts_top = []
        for i in range(segments):
            ang = 2 * math.pi * i / segments
            px = cx + r * math.cos(ang)
            py = cy + r * math.sin(ang)
            pts_bottom.append((px, py, z))
            pts_top.append((px, py, z + h))

        for i in range(segments):
            next_i = (i + 1) % segments
            msp.add_3dface([pts_bottom[i], pts_bottom[next_i], pts_top[next_i], pts_top[i]], dxfattribs={'layer': layer, 'color': 7})
            msp.add_3dface([(cx, cy, z + h), pts_top[i], pts_top[next_i], (cx, cy, z + h)], dxfattribs={'layer': layer, 'color': 7})
            msp.add_3dface([(cx, cy, z), pts_bottom[next_i], pts_bottom[i], (cx, cy, z)], dxfattribs={'layer': layer, 'color': 7})

    doc.saveas(output_path)
    file_size_kb = os.path.getsize(output_path) / 1024.0
    print(f"SUCCESS: 3D DXF compiled successfully: '{output_path}' ({file_size_kb:.2f} KB).")


# ==============================================================================
# EXPORT 2: UNIVERSAL 3D OBJ & MTL GENERATOR (Blender / Rhino / 3D Viewer)
# ==============================================================================

def export_obj_3d(model: Model3D, obj_path="coffee_shop_3d.obj", mtl_path="coffee_shop_3d.mtl"):
    """Exports model to Wavefront OBJ + MTL format with architectural materials."""
    print(f"-> Generating 3D OBJ/MTL: '{obj_path}'...")

    mtl_content = """# Architectural Materials for 2-Storey Coffee Shop (Pakil, Laguna)
newmtl concrete
Kd 0.84 0.84 0.82
Ka 0.22 0.22 0.22
Ks 0.12 0.12 0.12
Ns 12
d 1.0

newmtl wall
Kd 0.95 0.94 0.91
Ka 0.25 0.25 0.25
Ks 0.06 0.06 0.06
Ns 6
d 1.0

newmtl wood
Kd 0.72 0.48 0.27
Ka 0.20 0.14 0.09
Ks 0.22 0.18 0.14
Ns 25
d 1.0

newmtl wood_dark
Kd 0.36 0.23 0.15
Ka 0.10 0.08 0.05
Ks 0.15 0.15 0.15
Ns 20
d 1.0

newmtl wood_fluted
Kd 0.68 0.45 0.25
Ka 0.18 0.12 0.08
Ks 0.20 0.16 0.12
Ns 22
d 1.0

newmtl floor
Kd 0.75 0.52 0.30
Ka 0.22 0.16 0.10
Ks 0.25 0.20 0.15
Ns 30
d 1.0

newmtl quartz
Kd 0.96 0.96 0.97
Ka 0.30 0.30 0.30
Ks 0.70 0.70 0.72
Ns 70
d 1.0

newmtl glass
Kd 0.65 0.82 0.92
Ka 0.30 0.40 0.45
Ks 0.92 0.95 0.98
Ns 90
d 0.35

newmtl metal_dark
Kd 0.18 0.19 0.21
Ka 0.10 0.10 0.10
Ks 0.55 0.55 0.60
Ns 60
d 1.0

newmtl appliance_steel
Kd 0.82 0.84 0.87
Ka 0.30 0.30 0.30
Ks 0.85 0.85 0.85
Ns 80
d 1.0

newmtl leather
Kd 0.61 0.37 0.21
Ka 0.20 0.12 0.07
Ks 0.12 0.12 0.12
Ns 15
d 1.0

newmtl fixture_white
Kd 0.96 0.96 0.96
Ka 0.30 0.30 0.30
Ks 0.40 0.40 0.40
Ns 40
d 1.0

newmtl light_glow
Kd 1.00 0.92 0.68
Ka 1.00 0.92 0.68
Ke 1.00 0.85 0.50
Ks 0.10 0.10 0.10
Ns 10
d 1.0
"""
    with open(mtl_path, 'w', encoding='utf-8') as f:
        f.write(mtl_content)

    vertices = []
    normals = [
        (0, 0, -1),
        (0, 0, 1),
        (0, -1, 0),
        (1, 0, 0),
        (0, 1, 0),
        (-1, 0, 0),
    ]

    mat_faces = {}

    for x, y, z, w, d, h, layer, mat in model.boxes:
        base = len(vertices) + 1
        v = [
            (x, y, z), (x + w, y, z), (x + w, y + d, z), (x, y + d, z),
            (x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)
        ]
        vertices.extend(v)
        quads = [
            [(base, 1), (base + 3, 1), (base + 2, 1), (base + 1, 1)],
            [(base + 4, 2), (base + 5, 2), (base + 6, 2), (base + 7, 2)],
            [(base, 3), (base + 1, 3), (base + 5, 3), (base + 4, 3)],
            [(base + 1, 4), (base + 2, 4), (base + 6, 4), (base + 5, 4)],
            [(base + 2, 5), (base + 3, 5), (base + 7, 5), (base + 6, 5)],
            [(base + 3, 6), (base, 6), (base + 4, 6), (base + 7, 6)]
        ]
        if mat not in mat_faces:
            mat_faces[mat] = []
        mat_faces[mat].extend(quads)

    # Export cylinders into polygonal geometry (16 sides)
    segs = 16
    for cx, cy, z, r, h, layer, mat in model.cylinders:
        base = len(vertices) + 1
        top_center_idx = base
        bot_center_idx = base + 1
        vertices.append((cx, cy, z + h))
        vertices.append((cx, cy, z))

        for i in range(segs):
            ang = 2 * math.pi * i / segs
            px = cx + r * math.cos(ang)
            py = cy + r * math.sin(ang)
            vertices.append((px, py, z + h))
            vertices.append((px, py, z))

        cyl_faces = []
        for i in range(segs):
            next_i = (i + 1) % segs
            t_curr = base + 2 + i * 2
            b_curr = base + 3 + i * 2
            t_next = base + 2 + next_i * 2
            b_next = base + 3 + next_i * 2

            cyl_faces.append([(b_curr, 4), (b_next, 4), (t_next, 4), (t_curr, 4)])
            cyl_faces.append([(top_center_idx, 2), (t_curr, 2), (t_next, 2)])
            cyl_faces.append([(bot_center_idx, 1), (b_next, 1), (b_curr, 1)])

        if mat not in mat_faces:
            mat_faces[mat] = []
        mat_faces[mat].extend(cyl_faces)

    with open(obj_path, 'w', encoding='utf-8') as f:
        f.write("# Wavefront OBJ File: 2-Storey Coffee Shop in Pakil, Laguna\n")
        f.write(f"mtllib {os.path.basename(mtl_path)}\n\n")

        for vx, vy, vz in vertices:
            f.write(f"v {vx/1000.0:.4f} {vz/1000.0:.4f} {-vy/1000.0:.4f}\n")

        for nx, ny, nz in normals:
            f.write(f"vn {nx:.2f} {nz:.2f} {-ny:.2f}\n")

        for mat, faces in mat_faces.items():
            f.write(f"\nusemtl {mat}\n")
            f.write(f"g {mat}\n")
            for face in faces:
                f.write(f"f {' '.join(f'{vi}//{ni}' for vi, ni in face)}\n")

    file_size_kb = os.path.getsize(obj_path) / 1024.0
    print(f"SUCCESS: 3D OBJ compiled successfully: '{obj_path}' ({file_size_kb:.2f} KB).")


# ==============================================================================
# EXPORT 3: STANDALONE WEBGL VIEWER (PROCEDURAL TEXTURES & AESTHETIC GRADIENTS)
# ==============================================================================

def export_webgl_viewer(model: Model3D, output_path="coffee_shop_3d_viewer.html"):
    """
    Generates an interactive 3D architectural viewer in pure HTML/JS.
    Features:
    - Procedural Canvas Textures & Gradients (Parquet Hardwood, Fluted Slat Wood, Calacatta Quartz, Limewash, Concrete, Leather, Brushed Steel)
    - Studio HDR Reflection Environment Map (IBL reflections on stainless steel, glass, and quartz)
    - Pure Infinite Studio White Background (#ffffff) with invisible shadow-catching plane
    - High-End Archviz Furniture with smooth PBR shading (no wireframe cages on furniture)
    - Visible 3D Light Fixtures & Dynamic Warm Multi-Source Illumination (with Dimmer & Ambiance Presets)
    - Aesthetic Frosted Glassmorphism UI (Layered gradients, single cohesive royal blue accent, zero emojis)
    """
    print(f"-> Generating Advanced Interactive 3D Viewer: '{output_path}'...")

    boxes_data = []
    for x, y, z, w, d, h, layer, mat in model.boxes:
        boxes_data.append({
            "x": x / 1000.0,
            "y": y / 1000.0,
            "z": z / 1000.0,
            "w": w / 1000.0,
            "d": d / 1000.0,
            "h": h / 1000.0,
            "layer": layer,
            "mat": mat
        })

    cylinders_data = []
    for cx, cy, z, r, h, layer, mat in model.cylinders:
        cylinders_data.append({
            "cx": cx / 1000.0,
            "cy": cy / 1000.0,
            "z": z / 1000.0,
            "r": r / 1000.0,
            "h": h / 1000.0,
            "layer": layer,
            "mat": mat
        })

    dims_data = []
    for p1, p2, text, subtext, axis in model.dimensions:
        dims_data.append({
            "x1": p1[0] / 1000.0,
            "y1": p1[1] / 1000.0,
            "z1": p1[2] / 1000.0,
            "x2": p2[0] / 1000.0,
            "y2": p2[1] / 1000.0,
            "z2": p2[2] / 1000.0,
            "text": text,
            "subtext": subtext,
            "axis": axis
        })

    boxes_json = json.dumps(boxes_data)
    cylinders_json = json.dumps(cylinders_data)
    dims_json = json.dumps(dims_data)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>3D Architectural Model | 2-Storey Coffee Shop (Pakil, Laguna)</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: #ffffff;
            color: #0f172a;
            overflow: hidden;
            width: 100vw;
            height: 100vh;
        }}
        #canvas-container {{
            width: 100%;
            height: 100%;
            display: block;
        }}

        /* HUD Header - Aesthetic Frosted Glassmorphism */
        .hud-header {{
            position: absolute;
            top: 20px;
            left: 24px;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.94) 0%, rgba(30, 41, 59, 0.90) 100%);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 14px;
            padding: 14px 20px;
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.22), inset 0 1px 0 rgba(255, 255, 255, 0.15);
            pointer-events: auto;
            z-index: 10;
            max-width: calc(100vw - 48px);
        }}
        .hud-header h1 {{
            font-size: 15px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}
        .hud-header .badge {{
            font-size: 10px;
            font-weight: 700;
            padding: 3px 9px;
            border-radius: 5px;
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4);
            color: #ffffff;
            letter-spacing: 0.6px;
            text-transform: uppercase;
        }}
        .hud-header p {{
            font-size: 11.5px;
            color: #94a3b8;
        }}

        /* Mobile Controls Toggle Button */
        #btn-toggle-ui {{
            position: absolute;
            top: 20px;
            right: 24px;
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #ffffff;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.6px;
            padding: 9px 18px;
            border-radius: 8px;
            cursor: pointer;
            z-index: 30;
            display: none;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
        }}

        /* Control Panel - Aesthetic Frosted Glassmorphism with Unified Accent */
        .control-panel {{
            position: absolute;
            top: 20px;
            right: 24px;
            width: 320px;
            max-height: calc(100vh - 40px);
            overflow-y: auto;
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.95) 0%, rgba(24, 34, 53, 0.92) 100%);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 20px 48px rgba(0, 0, 0, 0.28), inset 0 1px 0 rgba(255, 255, 255, 0.12);
            z-index: 20;
            display: flex;
            flex-direction: column;
            gap: 12px;
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s ease;
        }}
        .control-panel::-webkit-scrollbar {{
            width: 4px;
        }}
        .control-panel::-webkit-scrollbar-thumb {{
            background: rgba(255, 255, 255, 0.2);
            border-radius: 2px;
        }}
        .panel-section-title {{
            font-size: 10.5px;
            font-weight: 700;
            color: #ffffff;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .panel-section-title .subtitle {{
            font-size: 9.5px;
            color: #94a3b8;
            font-weight: 600;
        }}

        /* Feature Card - Subtle Gradient & Inner Shadow */
        .feature-card {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            padding: 10px 12px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }}

        /* Sliders with Gradient Track */
        .slider-group {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        .slider-label {{
            display: flex;
            justify-content: space-between;
            font-size: 11.5px;
            font-weight: 500;
            color: #cbd5e1;
        }}
        .slider-label .val {{
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            color: #93c5fd;
        }}
        .slider-group input[type="range"] {{
            width: 100%;
            height: 5px;
            border-radius: 3px;
            background: linear-gradient(90deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.08));
            outline: none;
            cursor: pointer;
            accent-color: #2563eb;
        }}

        /* Button Grids */
        .btn-grid-3 {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 5px;
        }}
        .btn-grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 5px;
        }}
        .btn {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.07) 0%, rgba(255, 255, 255, 0.03) 100%);
            border: 1px solid rgba(255, 255, 255, 0.10);
            color: #e2e8f0;
            padding: 8px 9px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            user-select: none;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }}
        .btn:hover {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.14) 0%, rgba(255, 255, 255, 0.06) 100%);
            color: #ffffff;
            border-color: rgba(255, 255, 255, 0.20);
        }}
        .btn.active {{
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            border-color: #60a5fa;
            color: #ffffff;
            font-weight: 700;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.25);
        }}

        /* Checkbox Toggles */
        .toggle-list {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        .toggle-item {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 11.5px;
            color: #cbd5e1;
            cursor: pointer;
            user-select: none;
        }}
        .toggle-item input {{
            cursor: pointer;
            accent-color: #2563eb;
            width: 15px;
            height: 15px;
        }}

        /* Navigation Help Overlay */
        .nav-help {{
            position: absolute;
            bottom: 20px;
            left: 24px;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.92) 0%, rgba(30, 41, 59, 0.88) 100%);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 8px;
            padding: 8px 14px;
            font-size: 11px;
            color: #94a3b8;
            display: flex;
            gap: 14px;
            z-index: 10;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
        }}
        .nav-help kbd {{
            background: rgba(255, 255, 255, 0.10);
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 2px 5px;
            border-radius: 4px;
            font-size: 10px;
            color: #f8fafc;
        }}

        /* Responsive Breakpoints */
        @media (max-width: 860px) {{
            #btn-toggle-ui {{
                display: block;
            }}
            .control-panel {{
                top: 64px;
                right: 16px;
                width: calc(100vw - 32px);
                max-width: 340px;
                max-height: calc(100vh - 84px);
                transform: translateX(115%);
            }}
            .control-panel.open {{
                transform: translateX(0);
            }}
            .hud-header {{
                top: 14px;
                left: 16px;
                padding: 10px 14px;
            }}
            .hud-header h1 {{
                font-size: 13.5px;
            }}
            .nav-help {{
                display: none;
            }}
        }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
    <div id="canvas-container"></div>

    <div class="hud-header">
        <h1>2-Storey Specialty Coffee Shop <span class="badge">Burgos, Pakil, Laguna</span></h1>
        <p>10m &times; 10m Footprint &bull; 2.5m Cantilever Balcony &bull; Studio Gallery Model</p>
    </div>

    <button id="btn-toggle-ui" onclick="toggleUIPanel()">Controls</button>

    <div class="control-panel" id="control-panel">
        <!-- ARCHITECTURAL & INTERIOR LIGHTING (NEW!) -->
        <div class="feature-card">
            <div class="panel-section-title">
                <span>Architectural & Interior Lighting</span>
                <span class="subtitle">WARM GLOW (2700K)</span>
            </div>
            <label class="toggle-item">
                <span style="font-weight: 600; color: #ffffff;">Interior Lights On</span>
                <input type="checkbox" id="chk-lights" checked onchange="toggleInteriorLights(this.checked)">
            </label>
            <div class="slider-group">
                <div class="slider-label">
                    <span>Interior Lights Dimmer</span>
                    <span class="val" id="dimmer-val">120%</span>
                </div>
                <input type="range" id="lights-dimmer-slider" min="0" max="2.5" step="0.1" value="1.2" oninput="updateInteriorDimmer(this.value)">
            </div>
            <div class="panel-section-title" style="margin-top: 4px;">
                <span>Atmospheric Ambiance Mode</span>
            </div>
            <div class="btn-grid-3">
                <button class="btn active" id="amb-day" onclick="setAmbiance('day')">Daylight</button>
                <button class="btn" id="amb-sunset" onclick="setAmbiance('sunset')">Golden Hour</button>
                <button class="btn" id="amb-night" onclick="setAmbiance('night')">Night Cafe</button>
            </div>
        </div>

        <!-- DOLLHOUSE SECTION CUTAWAY -->
        <div class="feature-card">
            <div class="panel-section-title">
                <span>Dollhouse Section Cut</span>
                <span class="subtitle">PERSPECTIVE SECTION</span>
            </div>
            <label class="toggle-item">
                <span style="font-weight: 600; color: #ffffff;">Enable Section Slice</span>
                <input type="checkbox" id="chk-cutaway" onchange="toggleCutaway(this.checked)">
            </label>
            <div class="slider-group">
                <div class="slider-label">
                    <span>Section Cut Depth</span>
                    <span class="val" id="cut-val">5.0m</span>
                </div>
                <input type="range" id="cut-slider" min="0.5" max="9.5" step="0.2" value="5.0" oninput="updateCutDepth(this.value)">
            </div>
            <div class="btn-grid-2">
                <button class="btn active" id="cut-axis-z" onclick="setCutAxis('z')">North Facade Cut</button>
                <button class="btn" id="cut-axis-x" onclick="setCutAxis('x')">West Side Cut</button>
            </div>
            <button class="btn" id="btn-dollhouse" onclick="triggerDollhousePreset()">
                Dollhouse Perspective Preset
            </button>
        </div>

        <!-- Render Style Selector -->
        <div class="feature-card">
            <div class="panel-section-title">
                <span>Shading Style</span>
                <span class="subtitle" id="current-style-tag">PBR REALISTIC</span>
            </div>
            <div class="btn-grid-3">
                <button class="btn active" id="style-pbr" onclick="setStyle('pbr')">PBR Real</button>
                <button class="btn" id="style-cad" onclick="setStyle('cad')">CAD Mode</button>
                <button class="btn" id="style-nurbs" onclick="setStyle('nurbs')">NURBS Clay</button>
            </div>
            <div class="btn-grid-2" style="margin-top: 4px;">
                <button class="btn" id="style-xray" onclick="setStyle('xray')">X-Ray Ghosted</button>
                <button class="btn" id="style-blueprint" onclick="setStyle('blueprint')">Blueprint</button>
            </div>
        </div>

        <!-- Solar Simulation & Time of Day -->
        <div class="feature-card">
            <div class="panel-section-title">
                <span>Solar & Lighting Simulator</span>
            </div>
            <div class="slider-group">
                <div class="slider-label">
                    <span>Time of Day (Sun Angle)</span>
                    <span class="val" id="time-val">14:00 (Noon)</span>
                </div>
                <input type="range" id="sun-time-slider" min="6" max="20" step="0.25" value="14">
            </div>
            <div class="slider-group" style="margin-top: 4px;">
                <div class="slider-label">
                    <span>Sun Compass Azimuth</span>
                    <span class="val" id="azim-val">220°</span>
                </div>
                <input type="range" id="sun-azim-slider" min="0" max="360" step="5" value="220">
            </div>
        </div>

        <!-- 3D Dimensions Toggle -->
        <div class="feature-card">
            <div class="panel-section-title">
                <span>Measurements (Sukat)</span>
            </div>
            <label class="toggle-item">
                <span style="font-weight: 600; color: #ffffff;">Show 3D Dimensions</span>
                <input type="checkbox" id="chk-dims" checked onchange="toggleDimensions(this.checked)">
            </label>
        </div>

        <!-- Exploded Axonometric Slider -->
        <div class="feature-card">
            <div class="panel-section-title">
                <span>Exploded Axonometric</span>
            </div>
            <div class="slider-group">
                <div class="slider-label">
                    <span>Floor Separation</span>
                    <span class="val" id="explode-val">0.0m</span>
                </div>
                <input type="range" id="explode-slider" min="0" max="6" step="0.1" value="0">
            </div>
        </div>

        <!-- Camera Presets -->
        <div class="feature-card">
            <div class="panel-section-title">
                <span>Camera Presets</span>
            </div>
            <div class="btn-grid-2">
                <button class="btn active" id="cam-iso" onclick="setCamera('iso')">North-West Iso</button>
                <button class="btn" id="cam-front" onclick="setCamera('front')">North Entrance</button>
                <button class="btn" id="cam-balcony" onclick="setCamera('balcony')">Balcony View</button>
                <button class="btn" id="cam-top" onclick="setCamera('top')">Top Cutaway</button>
            </div>
        </div>

        <!-- Building Elements Toggles -->
        <div class="feature-card">
            <div class="panel-section-title">
                <span>Building Elements</span>
            </div>
            <div class="toggle-list">
                <label class="toggle-item">
                    <span>Roof Slab & Parapet</span>
                    <input type="checkbox" id="chk-roof" checked onchange="toggleLayer('3D-ROOF', this.checked)">
                </label>
                <label class="toggle-item">
                    <span>Second Floor & Balcony</span>
                    <input type="checkbox" id="chk-2f" checked onchange="toggleFloor(2, this.checked)">
                </label>
                <label class="toggle-item">
                    <span>Ground Floor & Plinth</span>
                    <input type="checkbox" id="chk-gf" checked onchange="toggleFloor(1, this.checked)">
                </label>
                <label class="toggle-item">
                    <span>Exterior Louvers & Canopy</span>
                    <input type="checkbox" id="chk-louvers" checked onchange="toggleLouvers(this.checked)">
                </label>
                <label class="toggle-item">
                    <span>Lighting Fixtures & Glow</span>
                    <input type="checkbox" id="chk-light-fixtures" checked onchange="toggleLayer('3D-LIGHTS', this.checked)">
                </label>
                <label class="toggle-item">
                    <span>Glass & Balustrades</span>
                    <input type="checkbox" id="chk-glass" checked onchange="toggleLayer('3D-GLAZING', this.checked)">
                </label>
                <label class="toggle-item">
                    <span>Furniture & Refrigerator</span>
                    <input type="checkbox" id="chk-furn" checked onchange="toggleFurniture(this.checked)">
                </label>
            </div>
        </div>
    </div>

    <div class="nav-help">
        <span><kbd>Left Click + Drag</kbd> Orbit</span>
        <span><kbd>Right Click + Drag</kbd> Pan</span>
        <span><kbd>Scroll</kbd> Zoom</span>
    </div>

    <script>
        const BOXES_DATA = {boxes_json};
        const CYLINDERS_DATA = {cylinders_json};
        const DIMS_DATA = {dims_json};

        // ==============================================================================
        // PROCEDURAL ARCHITECTURAL TEXTURES & GRADIENT GENERATORS
        // ==============================================================================
        function pseudoRandom(x, y) {{
            const sin = Math.sin(x * 12.9898 + y * 78.233) * 43758.5453;
            return sin - Math.floor(sin);
        }}

        // 1. Scandinavian Hardwood Parquet Floor Texture
        function createParquetTexture() {{
            const canvas = document.createElement('canvas');
            canvas.width = 1024;
            canvas.height = 1024;
            const ctx = canvas.getContext('2d');

            ctx.fillStyle = '#b8854d';
            ctx.fillRect(0, 0, 1024, 1024);

            const rows = 16;
            const rowH = 1024 / rows;
            const cols = 5;
            const colW = 1024 / cols;

            for (let r = 0; r < rows; r++) {{
                const offset = (r % 2) * (colW / 2);
                for (let c = -1; c <= cols + 1; c++) {{
                    const x = c * colW + offset;
                    const y = r * rowH;

                    const shift = (pseudoRandom(r, c) - 0.5) * 36;
                    const rVal = Math.min(235, Math.max(145, 198 + shift));
                    const gVal = Math.min(195, Math.max(105, 144 + shift * 0.8));
                    const bVal = Math.min(145, Math.max(65, 90 + shift * 0.6));

                    const grad = ctx.createLinearGradient(x, y, x + colW, y + rowH);
                    grad.addColorStop(0, `rgb(${{rVal}}, ${{gVal}}, ${{bVal}})`);
                    grad.addColorStop(1, `rgb(${{rVal - 16}}, ${{gVal - 14}}, ${{bVal - 12}})`);
                    ctx.fillStyle = grad;
                    ctx.fillRect(x + 1, y + 1, colW - 2, rowH - 2);

                    ctx.strokeStyle = `rgba(${{rVal - 45}}, ${{gVal - 40}}, ${{bVal - 35}}, 0.28)`;
                    ctx.lineWidth = 1;
                    for (let gy = y + 5; gy < y + rowH - 3; gy += 6) {{
                        ctx.beginPath();
                        for (let gx = x; gx < x + colW; gx += 16) {{
                            const wave = Math.sin((gx - x) * 0.05 + gy * 0.1) * 2.5;
                            if (gx === x) ctx.moveTo(gx, gy + wave);
                            else ctx.lineTo(gx, gy + wave);
                        }}
                        ctx.stroke();
                    }}

                    ctx.strokeStyle = 'rgba(40, 24, 10, 0.40)';
                    ctx.lineWidth = 1.5;
                    ctx.strokeRect(x, y, colW, rowH);
                }}
            }}

            const tex = new THREE.CanvasTexture(canvas);
            tex.wrapS = THREE.RepeatWrapping;
            tex.wrapT = THREE.RepeatWrapping;
            tex.repeat.set(3, 3);
            return tex;
        }}

        function createParquetBumpMap() {{
            const canvas = document.createElement('canvas');
            canvas.width = 1024;
            canvas.height = 1024;
            const ctx = canvas.getContext('2d');

            ctx.fillStyle = '#808080';
            ctx.fillRect(0, 0, 1024, 1024);

            const rows = 16;
            const rowH = 1024 / rows;
            const cols = 5;
            const colW = 1024 / cols;

            for (let r = 0; r < rows; r++) {{
                const offset = (r % 2) * (colW / 2);
                for (let c = -1; c <= cols + 1; c++) {{
                    const x = c * colW + offset;
                    const y = r * rowH;

                    ctx.strokeStyle = '#222222';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(x, y, colW, rowH);

                    ctx.strokeStyle = '#999999';
                    ctx.lineWidth = 1;
                    for (let gy = y + 6; gy < y + rowH - 4; gy += 10) {{
                        ctx.beginPath();
                        ctx.moveTo(x + 2, gy);
                        ctx.lineTo(x + colW - 2, gy);
                        ctx.stroke();
                    }}
                }}
            }}

            const tex = new THREE.CanvasTexture(canvas);
            tex.wrapS = THREE.RepeatWrapping;
            tex.wrapT = THREE.RepeatWrapping;
            tex.repeat.set(3, 3);
            return tex;
        }}

        // 2. Fluted Timber Slat Counter Base Texture
        function createFlutedWoodTexture() {{
            const canvas = document.createElement('canvas');
            canvas.width = 512;
            canvas.height = 512;
            const ctx = canvas.getContext('2d');

            const slatW = 16;
            for (let x = 0; x < 512; x += slatW) {{
                const sGrad = ctx.createLinearGradient(x, 0, x + slatW, 0);
                sGrad.addColorStop(0.0, '#362112');
                sGrad.addColorStop(0.2, '#87562f');
                sGrad.addColorStop(0.5, '#c8955a');
                sGrad.addColorStop(0.8, '#87562f');
                sGrad.addColorStop(1.0, '#362112');
                ctx.fillStyle = sGrad;
                ctx.fillRect(x, 0, slatW, 512);

                ctx.fillStyle = 'rgba(50, 30, 15, 0.12)';
                for (let y = 0; y < 512; y += 12) {{
                    if (pseudoRandom(x, y) > 0.4) {{
                        ctx.fillRect(x, y, slatW, 4);
                    }}
                }}
            }}

            const tex = new THREE.CanvasTexture(canvas);
            tex.wrapS = THREE.RepeatWrapping;
            tex.wrapT = THREE.RepeatWrapping;
            tex.repeat.set(4, 2);
            return tex;
        }}

        // 3. Natural Golden Oak & Smoked Walnut Textures
        function createOakWoodTexture(isDark = false) {{
            const canvas = document.createElement('canvas');
            canvas.width = 512;
            canvas.height = 512;
            const ctx = canvas.getContext('2d');

            const baseCol = isDark ? '#422c1b' : '#c6955a';
            const midCol  = isDark ? '#331f12' : '#b07f43';
            const darkCol = isDark ? '#211309' : '#8c5d2b';

            const grad = ctx.createLinearGradient(0, 0, 512, 512);
            grad.addColorStop(0, baseCol);
            grad.addColorStop(0.5, midCol);
            grad.addColorStop(1, darkCol);
            ctx.fillStyle = grad;
            ctx.fillRect(0, 0, 512, 512);

            ctx.lineWidth = 1.3;
            ctx.strokeStyle = isDark ? 'rgba(15, 8, 4, 0.35)' : 'rgba(85, 50, 20, 0.32)';
            for (let y = -20; y < 530; y += 6) {{
                ctx.beginPath();
                for (let x = 0; x <= 512; x += 12) {{
                    const wave = Math.sin(x * 0.02 + y * 0.04) * 6 + Math.cos(x * 0.06) * 3;
                    if (x === 0) ctx.moveTo(x, y + wave);
                    else ctx.lineTo(x, y + wave);
                }}
                ctx.stroke();
            }}

            const imgData = ctx.getImageData(0, 0, 512, 512);
            const d = imgData.data;
            for (let i = 0; i < d.length; i += 4) {{
                const n = (Math.random() - 0.5) * 14;
                d[i]     = Math.min(255, Math.max(0, d[i] + n));
                d[i + 1] = Math.min(255, Math.max(0, d[i + 1] + n * 0.8));
                d[i + 2] = Math.min(255, Math.max(0, d[i + 2] + n * 0.6));
            }}
            ctx.putImageData(imgData, 0, 0);

            const tex = new THREE.CanvasTexture(canvas);
            tex.wrapS = THREE.RepeatWrapping;
            tex.wrapT = THREE.RepeatWrapping;
            return tex;
        }}

        // 4. Roman Clay / Limewash Plaster Wall Texture
        function createLimewashWallTexture() {{
            const canvas = document.createElement('canvas');
            canvas.width = 512;
            canvas.height = 512;
            const ctx = canvas.getContext('2d');

            ctx.fillStyle = '#f5f3ef';
            ctx.fillRect(0, 0, 512, 512);

            for (let i = 0; i < 40; i++) {{
                const cx = Math.random() * 512;
                const cy = Math.random() * 512;
                const rad = 60 + Math.random() * 120;
                const grad = ctx.createRadialGradient(cx, cy, 10, cx, cy, rad);
                const shade = 230 + Math.floor(Math.random() * 20);
                grad.addColorStop(0, `rgba(${{shade}}, ${{shade - 2}}, ${{shade - 6}}, 0.35)`);
                grad.addColorStop(1, 'rgba(245, 243, 239, 0)');
                ctx.fillStyle = grad;
                ctx.beginPath();
                ctx.arc(cx, cy, rad, 0, Math.PI * 2);
                ctx.fill();
            }}

            const imgData = ctx.getImageData(0, 0, 512, 512);
            const d = imgData.data;
            for (let i = 0; i < d.length; i += 4) {{
                const noise = (Math.random() - 0.5) * 8;
                d[i]     = Math.min(255, Math.max(0, d[i] + noise));
                d[i + 1] = Math.min(255, Math.max(0, d[i + 1] + noise));
                d[i + 2] = Math.min(255, Math.max(0, d[i + 2] + noise));
            }}
            ctx.putImageData(imgData, 0, 0);

            const tex = new THREE.CanvasTexture(canvas);
            tex.wrapS = THREE.RepeatWrapping;
            tex.wrapT = THREE.RepeatWrapping;
            tex.repeat.set(2, 2);
            return tex;
        }}

        // 5. Board-Formed Architectural Concrete Texture
        function createConcreteTexture() {{
            const canvas = document.createElement('canvas');
            canvas.width = 512;
            canvas.height = 512;
            const ctx = canvas.getContext('2d');

            ctx.fillStyle = '#d7d6d2';
            ctx.fillRect(0, 0, 512, 512);

            const plankH = 512 / 8;
            for (let i = 0; i < 8; i++) {{
                const y = i * plankH;
                const diff = (pseudoRandom(i, 7) - 0.5) * 16;
                const g = Math.floor(214 + diff);
                ctx.fillStyle = `rgb(${{g}}, ${{g - 1}}, ${{g - 3}})`;
                ctx.fillRect(0, y + 1, 512, plankH - 2);

                ctx.strokeStyle = 'rgba(70, 70, 70, 0.35)';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(512, y);
                ctx.stroke();

                for (let tx of [80, 256, 432]) {{
                    ctx.fillStyle = 'rgba(60, 60, 60, 0.40)';
                    ctx.beginPath();
                    ctx.arc(tx, y + plankH / 2, 7, 0, Math.PI * 2);
                    ctx.fill();
                }}
            }}

            const tex = new THREE.CanvasTexture(canvas);
            tex.wrapS = THREE.RepeatWrapping;
            tex.wrapT = THREE.RepeatWrapping;
            return tex;
        }}

        // 6. Calacatta Gold White Marble / Quartz Texture
        function createMarbleTexture() {{
            const canvas = document.createElement('canvas');
            canvas.width = 1024;
            canvas.height = 1024;
            const ctx = canvas.getContext('2d');

            const bg = ctx.createLinearGradient(0, 0, 1024, 1024);
            bg.addColorStop(0.0, '#fafafc');
            bg.addColorStop(0.5, '#f4f5f8');
            bg.addColorStop(1.0, '#ffffff');
            ctx.fillStyle = bg;
            ctx.fillRect(0, 0, 1024, 1024);

            function drawVein(startX, startY, len, angle, col, width) {{
                ctx.strokeStyle = col;
                ctx.lineWidth = width;
                ctx.beginPath();
                let x = startX;
                let y = startY;
                ctx.moveTo(x, y);
                const steps = Math.floor(len / 18);
                for (let s = 0; s < steps; s++) {{
                    x += Math.cos(angle) * 18 + (pseudoRandom(s, x) - 0.5) * 14;
                    y += Math.sin(angle) * 18 + (pseudoRandom(y, s) - 0.5) * 14;
                    ctx.lineTo(x, y);
                }}
                ctx.stroke();
            }}

            drawVein(50, 200, 1200, 0.65, 'rgba(160, 165, 175, 0.22)', 3.5);
            drawVein(300, 100, 1100, 0.70, 'rgba(195, 165, 125, 0.18)', 2.5);
            drawVein(600, 50, 950, 0.60, 'rgba(170, 175, 185, 0.16)', 2.0);
            drawVein(100, 600, 1000, 0.68, 'rgba(190, 160, 120, 0.15)', 2.0);

            const tex = new THREE.CanvasTexture(canvas);
            tex.wrapS = THREE.RepeatWrapping;
            tex.wrapT = THREE.RepeatWrapping;
            return tex;
        }}

        // 7. Rich Cognac Saddle Leather Texture
        function createLeatherTexture() {{
            const canvas = document.createElement('canvas');
            canvas.width = 512;
            canvas.height = 512;
            const ctx = canvas.getContext('2d');

            const grad = ctx.createRadialGradient(256, 256, 40, 256, 256, 360);
            grad.addColorStop(0, '#a66538');
            grad.addColorStop(0.7, '#854b23');
            grad.addColorStop(1, '#5e3214');
            ctx.fillStyle = grad;
            ctx.fillRect(0, 0, 512, 512);

            ctx.fillStyle = 'rgba(40, 18, 5, 0.18)';
            for (let y = 0; y < 512; y += 8) {{
                for (let x = 0; x < 512; x += 8) {{
                    if (pseudoRandom(x, y) > 0.3) {{
                        ctx.beginPath();
                        ctx.arc(x + pseudoRandom(y, x) * 2, y + pseudoRandom(x, y) * 2, 1.3, 0, Math.PI * 2);
                        ctx.fill();
                    }}
                }}
            }}

            const tex = new THREE.CanvasTexture(canvas);
            tex.wrapS = THREE.RepeatWrapping;
            tex.wrapT = THREE.RepeatWrapping;
            tex.repeat.set(2, 2);
            return tex;
        }}

        // 8. Brushed Commercial Stainless Steel Texture
        function createBrushedSteelTexture() {{
            const canvas = document.createElement('canvas');
            canvas.width = 512;
            canvas.height = 512;
            const ctx = canvas.getContext('2d');

            const grad = ctx.createLinearGradient(0, 0, 512, 0);
            grad.addColorStop(0.0, '#e6ebf2');
            grad.addColorStop(0.25, '#d0d5dc');
            grad.addColorStop(0.50, '#f2f5f9');
            grad.addColorStop(0.75, '#c5cbd4');
            grad.addColorStop(1.0, '#e2e7ee');
            ctx.fillStyle = grad;
            ctx.fillRect(0, 0, 512, 512);

            ctx.strokeStyle = 'rgba(90, 100, 115, 0.18)';
            ctx.lineWidth = 1;
            for (let y = 0; y < 512; y += 2) {{
                if (Math.random() > 0.3) {{
                    ctx.beginPath();
                    ctx.moveTo(0, y);
                    ctx.lineTo(512, y);
                    ctx.stroke();
                }}
            }}

            const tex = new THREE.CanvasTexture(canvas);
            tex.wrapS = THREE.RepeatWrapping;
            tex.wrapT = THREE.RepeatWrapping;
            return tex;
        }}

        // 9. Procedural Studio HDR Reflection Environment Map
        function createStudioEnvironment() {{
            const canvas = document.createElement('canvas');
            canvas.width = 1024;
            canvas.height = 512;
            const ctx = canvas.getContext('2d');

            const grad = ctx.createLinearGradient(0, 0, 0, 512);
            grad.addColorStop(0.0, '#ffffff');
            grad.addColorStop(0.35, '#f0f4f8');
            grad.addColorStop(0.50, '#e2e8f0');
            grad.addColorStop(0.70, '#cbd5e1');
            grad.addColorStop(1.0, '#ffffff');
            ctx.fillStyle = grad;
            ctx.fillRect(0, 0, 1024, 512);

            const s1 = ctx.createRadialGradient(280, 120, 10, 280, 120, 200);
            s1.addColorStop(0, 'rgba(255, 255, 255, 0.95)');
            s1.addColorStop(1, 'rgba(255, 255, 255, 0)');
            ctx.fillStyle = s1;
            ctx.fillRect(0, 0, 1024, 512);

            const s2 = ctx.createRadialGradient(760, 160, 10, 760, 160, 220);
            s2.addColorStop(0, 'rgba(255, 250, 240, 0.85)');
            s2.addColorStop(1, 'rgba(255, 255, 255, 0)');
            ctx.fillStyle = s2;
            ctx.fillRect(0, 0, 1024, 512);

            const tex = new THREE.CanvasTexture(canvas);
            tex.mapping = THREE.EquirectangularReflectionMapping;
            return tex;
        }}

        // Instantiate Procedural Textures
        const texParquet = createParquetTexture();
        const bumpParquet = createParquetBumpMap();
        const texFlutedWood = createFlutedWoodTexture();
        const texOak = createOakWoodTexture(false);
        const texDarkOak = createOakWoodTexture(true);
        const texWall = createLimewashWallTexture();
        const texConcrete = createConcreteTexture();
        const texMarble = createMarbleTexture();
        const texLeather = createLeatherTexture();
        const texSteel = createBrushedSteelTexture();
        const studioEnv = createStudioEnvironment();

        // Material Palettes for Different Shading Styles
        const MAT_STYLES = {{
            pbr: {{
                concrete: new THREE.MeshStandardMaterial({{
                    map: texConcrete,
                    roughness: 0.78,
                    metalness: 0.08
                }}),
                wall: new THREE.MeshStandardMaterial({{
                    map: texWall,
                    roughness: 0.90,
                    metalness: 0.02
                }}),
                wood: new THREE.MeshStandardMaterial({{
                    map: texOak,
                    roughness: 0.40,
                    metalness: 0.04
                }}),
                wood_dark: new THREE.MeshStandardMaterial({{
                    map: texDarkOak,
                    roughness: 0.55,
                    metalness: 0.04
                }}),
                wood_fluted: new THREE.MeshStandardMaterial({{
                    map: texFlutedWood,
                    roughness: 0.45,
                    metalness: 0.04
                }}),
                floor: new THREE.MeshStandardMaterial({{
                    map: texParquet,
                    bumpMap: bumpParquet,
                    bumpScale: 0.035,
                    roughness: 0.38,
                    metalness: 0.05
                }}),
                quartz: new THREE.MeshStandardMaterial({{
                    map: texMarble,
                    roughness: 0.12,
                    metalness: 0.05
                }}),
                glass: new THREE.MeshPhysicalMaterial({{
                    color: 0xbae6fd,
                    transparent: true,
                    opacity: 0.30,
                    roughness: 0.04,
                    metalness: 0.1,
                    transmission: 0.92,
                    ior: 1.52
                }}),
                metal_dark: new THREE.MeshStandardMaterial({{
                    color: 0x1e242f,
                    roughness: 0.35,
                    metalness: 0.85
                }}),
                appliance_steel: new THREE.MeshStandardMaterial({{
                    map: texSteel,
                    roughness: 0.20,
                    metalness: 0.92
                }}),
                leather: new THREE.MeshStandardMaterial({{
                    map: texLeather,
                    roughness: 0.48,
                    metalness: 0.05
                }}),
                fixture_white: new THREE.MeshStandardMaterial({{
                    map: texMarble,
                    roughness: 0.15,
                    metalness: 0.08
                }}),
                light_glow: new THREE.MeshBasicMaterial({{
                    color: 0xffe29a
                }})
            }},
            cad: {{
                concrete: new THREE.MeshBasicMaterial({{ color: 0xffffff }}),
                wall: new THREE.MeshBasicMaterial({{ color: 0xf8fafc }}),
                wood: new THREE.MeshBasicMaterial({{ color: 0xe2e8f0 }}),
                wood_dark: new THREE.MeshBasicMaterial({{ color: 0xcbd5e1 }}),
                wood_fluted: new THREE.MeshBasicMaterial({{ color: 0xe2e8f0 }}),
                floor: new THREE.MeshBasicMaterial({{ color: 0xf1f5f9 }}),
                quartz: new THREE.MeshBasicMaterial({{ color: 0xffffff }}),
                glass: new THREE.MeshBasicMaterial({{ color: 0x93c5fd, transparent: true, opacity: 0.35 }}),
                metal_dark: new THREE.MeshBasicMaterial({{ color: 0x475569 }}),
                appliance_steel: new THREE.MeshBasicMaterial({{ color: 0xe2e8f0 }}),
                leather: new THREE.MeshBasicMaterial({{ color: 0xcbd5e1 }}),
                fixture_white: new THREE.MeshBasicMaterial({{ color: 0xffffff }}),
                light_glow: new THREE.MeshBasicMaterial({{ color: 0xfef08a }})
            }},
            nurbs: {{
                concrete: new THREE.MeshStandardMaterial({{ color: 0xdad9d5, roughness: 0.45, metalness: 0.15 }}),
                wall: new THREE.MeshStandardMaterial({{ color: 0xe5e4e0, roughness: 0.45, metalness: 0.15 }}),
                wood: new THREE.MeshStandardMaterial({{ color: 0xd5d4cf, roughness: 0.45, metalness: 0.15 }}),
                wood_dark: new THREE.MeshStandardMaterial({{ color: 0xc8c7c2, roughness: 0.45, metalness: 0.15 }}),
                wood_fluted: new THREE.MeshStandardMaterial({{ color: 0xd5d4cf, roughness: 0.45, metalness: 0.15 }}),
                floor: new THREE.MeshStandardMaterial({{ color: 0xd8d7d2, roughness: 0.45, metalness: 0.15 }}),
                quartz: new THREE.MeshStandardMaterial({{ color: 0xf0efe8, roughness: 0.20, metalness: 0.10 }}),
                glass: new THREE.MeshStandardMaterial({{ color: 0xbacdd9, transparent: true, opacity: 0.5, roughness: 0.1 }}),
                metal_dark: new THREE.MeshStandardMaterial({{ color: 0xa8a7a2, roughness: 0.45, metalness: 0.15 }}),
                appliance_steel: new THREE.MeshStandardMaterial({{ color: 0xc4c3be, roughness: 0.45, metalness: 0.15 }}),
                leather: new THREE.MeshStandardMaterial({{ color: 0xbdbcb6, roughness: 0.45, metalness: 0.15 }}),
                fixture_white: new THREE.MeshStandardMaterial({{ color: 0xf0efe8, roughness: 0.4, metalness: 0.1 }}),
                light_glow: new THREE.MeshBasicMaterial({{ color: 0xfff8db }})
            }},
            xray: {{
                concrete: new THREE.MeshPhysicalMaterial({{ color: 0x0284c7, transparent: true, opacity: 0.22, roughness: 0.1 }}),
                wall: new THREE.MeshPhysicalMaterial({{ color: 0x0ea5e9, transparent: true, opacity: 0.20, roughness: 0.1 }}),
                wood: new THREE.MeshPhysicalMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.35, roughness: 0.1 }}),
                wood_dark: new THREE.MeshPhysicalMaterial({{ color: 0x0369a1, transparent: true, opacity: 0.35, roughness: 0.1 }}),
                wood_fluted: new THREE.MeshPhysicalMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.35, roughness: 0.1 }}),
                floor: new THREE.MeshPhysicalMaterial({{ color: 0x0284c7, transparent: true, opacity: 0.25, roughness: 0.1 }}),
                quartz: new THREE.MeshPhysicalMaterial({{ color: 0xe0f2fe, transparent: true, opacity: 0.30, roughness: 0.05 }}),
                glass: new THREE.MeshPhysicalMaterial({{ color: 0xe0f2fe, transparent: true, opacity: 0.15, roughness: 0.05 }}),
                metal_dark: new THREE.MeshPhysicalMaterial({{ color: 0x0284c7, transparent: true, opacity: 0.45, roughness: 0.1 }}),
                appliance_steel: new THREE.MeshPhysicalMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.40, roughness: 0.1 }}),
                leather: new THREE.MeshPhysicalMaterial({{ color: 0x0284c7, transparent: true, opacity: 0.30, roughness: 0.1 }}),
                fixture_white: new THREE.MeshPhysicalMaterial({{ color: 0x7dd3fc, transparent: true, opacity: 0.3, roughness: 0.1 }}),
                light_glow: new THREE.MeshBasicMaterial({{ color: 0xfef08a, transparent: true, opacity: 0.85 }})
            }},
            blueprint: {{
                concrete: new THREE.MeshBasicMaterial({{ color: 0x0f2b5c, transparent: true, opacity: 0.7 }}),
                wall: new THREE.MeshBasicMaterial({{ color: 0x133873, transparent: true, opacity: 0.7 }}),
                wood: new THREE.MeshBasicMaterial({{ color: 0x1a4a96, transparent: true, opacity: 0.7 }}),
                wood_dark: new THREE.MeshBasicMaterial({{ color: 0x0d2247, transparent: true, opacity: 0.7 }}),
                wood_fluted: new THREE.MeshBasicMaterial({{ color: 0x1a4a96, transparent: true, opacity: 0.7 }}),
                floor: new THREE.MeshBasicMaterial({{ color: 0x112d5e, transparent: true, opacity: 0.7 }}),
                quartz: new THREE.MeshBasicMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.6 }}),
                glass: new THREE.MeshBasicMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.25 }}),
                metal_dark: new THREE.MeshBasicMaterial({{ color: 0x225aa8, transparent: true, opacity: 0.7 }}),
                appliance_steel: new THREE.MeshBasicMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.6 }}),
                leather: new THREE.MeshBasicMaterial({{ color: 0x1a4a96, transparent: true, opacity: 0.7 }}),
                fixture_white: new THREE.MeshBasicMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.7 }}),
                light_glow: new THREE.MeshBasicMaterial({{ color: 0x38bdf8 }})
            }}
        }};

        let currentStyle = 'pbr';

        // Scene, Camera, Renderer Setup - PURE INFINITE STUDIO WHITE
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xffffff);
        scene.environment = studioEnv;

        const camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: false }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.setClearColor(0xffffff, 1.0);
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.08;
        renderer.localClippingEnabled = true;
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.target.set(5.0, 3.5, -6.0);

        // Sunlight & Ambient Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.90);
        scene.add(ambientLight);

        const sunLight = new THREE.DirectionalLight(0xfff8ee, 1.25);
        sunLight.castShadow = true;
        sunLight.shadow.mapSize.width = 2048;
        sunLight.shadow.mapSize.height = 2048;
        sunLight.shadow.camera.near = 0.5;
        sunLight.shadow.camera.far = 100;
        sunLight.shadow.camera.left = -22;
        sunLight.shadow.camera.right = 22;
        sunLight.shadow.camera.top = 22;
        sunLight.shadow.camera.bottom = -22;
        sunLight.shadow.bias = -0.0003;
        scene.add(sunLight);

        const fillLight = new THREE.DirectionalLight(0xe8f0fe, 0.35);
        scene.add(fillLight);

        // ======================================================================
        // DYNAMIC MULTI-SOURCE WARM INTERIOR & ARCHITECTURAL LIGHTING
        // ======================================================================
        const interiorLightsGroup = new THREE.Group();
        const interiorLightSources = [];

        function addWarmPoint(x, y, z, colHex, baseIntensity, dist) {{
            const light = new THREE.PointLight(colHex, baseIntensity, dist);
            light.position.set(x, y, z);
            light.userData = {{ baseIntensity: baseIntensity }};
            interiorLightsGroup.add(light);
            interiorLightSources.push(light);
            return light;
        }}

        // 1. Barista Counter Warm Pendants
        const lightBarista = addWarmPoint(2.3, 2.5, -5.2, 0xffa840, 1.4, 9);
        // 2. GF Dining Banquette Lights
        const lightGFBanquette = addWarmPoint(3.5, 2.5, -1.8, 0xffb050, 1.3, 9);
        // 3. GF Storefront Window Bar Light
        const lightGFWindow = addWarmPoint(7.0, 2.5, -8.8, 0xffaa40, 1.2, 9);
        // 4. 2F Lounge Sectional Sofa Light
        const light2FLounge = addWarmPoint(2.5, 5.8, -1.8, 0xffb560, 1.3, 9);
        // 5. 2F Communal Co-working Hub
        const light2FCowork = addWarmPoint(6.3, 5.8, -5.0, 0xffb560, 1.5, 10);
        // 6. 2F Private Study Booths
        const light2FBooths = addWarmPoint(8.4, 5.5, -3.0, 0xffaa40, 1.2, 7);
        // 7. Balcony Pergola Festoon Lights (West & East Zones)
        const lightBalc1 = addWarmPoint(3.2, 5.8, -11.2, 0xff9944, 1.3, 9);
        const lightBalc2 = addWarmPoint(7.5, 5.8, -11.2, 0xff9944, 1.3, 9);

        // 8. North Entrance Canopy Downlight Spotlight
        const entranceSpot = new THREE.SpotLight(0xffe0a0, 2.0, 12, Math.PI / 4, 0.4);
        entranceSpot.position.set(3.3, 3.4, -10.5);
        entranceSpot.target.position.set(3.3, 0.6, -10.5);
        entranceSpot.userData = {{ baseIntensity: 2.0 }};
        scene.add(entranceSpot.target);
        interiorLightsGroup.add(entranceSpot);
        interiorLightSources.push(entranceSpot);

        scene.add(interiorLightsGroup);

        let interiorDimmerFactor = 1.2;
        let interiorLightsEnabled = true;

        function updateInteriorDimmer(val) {{
            interiorDimmerFactor = parseFloat(val);
            const pct = Math.round(interiorDimmerFactor * 100);
            document.getElementById('dimmer-val').textContent = pct + '%';
            applyInteriorLighting();
        }}

        function toggleInteriorLights(enabled) {{
            interiorLightsEnabled = enabled;
            interiorLightsGroup.visible = enabled;
        }}

        function applyInteriorLighting() {{
            interiorLightSources.forEach(l => {{
                l.intensity = l.userData.baseIntensity * interiorDimmerFactor;
            }});
        }}

        // Ambiance Presets: Daylight, Golden Hour Sunset, Evening/Night Cafe
        function setAmbiance(mode) {{
            document.querySelectorAll('.btn-grid-3 .btn').forEach(b => {{
                if (b.id && b.id.startsWith('amb-')) b.classList.remove('active');
            }});
            const btn = document.getElementById('amb-' + mode);
            if (btn) btn.classList.add('active');

            if (mode === 'day') {{
                scene.background.setHex(0xffffff);
                sunLight.color.setHex(0xfff8ee);
                sunLight.intensity = 1.25;
                ambientLight.color.setHex(0xffffff);
                ambientLight.intensity = 0.90;
                updateInteriorDimmer(1.0);
                document.getElementById('lights-dimmer-slider').value = 1.0;
                document.getElementById('sun-time-slider').value = 14;
            }} else if (mode === 'sunset') {{
                scene.background.setHex(0xfdf4ec);
                sunLight.color.setHex(0xff7722);
                sunLight.intensity = 1.4;
                ambientLight.color.setHex(0xffd5b0);
                ambientLight.intensity = 0.65;
                updateInteriorDimmer(1.5);
                document.getElementById('lights-dimmer-slider').value = 1.5;
                document.getElementById('sun-time-slider').value = 17.5;
            }} else if (mode === 'night') {{
                scene.background.setHex(0x0a1122);
                sunLight.color.setHex(0x3b5284);
                sunLight.intensity = 0.20;
                ambientLight.color.setHex(0x1a243d);
                ambientLight.intensity = 0.35;
                updateInteriorDimmer(2.2);
                document.getElementById('lights-dimmer-slider').value = 2.2;
                document.getElementById('sun-time-slider').value = 20;
            }}
            updateSolarLighting();
        }}

        // Invisible Shadow Catcher Ground Plane
        const shadowFloorGeo = new THREE.PlaneGeometry(400, 400);
        const shadowFloorMat = new THREE.ShadowMaterial({{ opacity: 0.12 }});
        const shadowFloor = new THREE.Mesh(shadowFloorGeo, shadowFloorMat);
        shadowFloor.rotation.x = -Math.PI / 2;
        shadowFloor.position.y = -0.01;
        shadowFloor.receiveShadow = true;
        scene.add(shadowFloor);

        // Building Component Groups
        const groupGF = new THREE.Group();
        const group2F = new THREE.Group();
        const groupRoof = new THREE.Group();
        const groupDims = new THREE.Group();

        scene.add(groupGF);
        scene.add(group2F);
        scene.add(groupRoof);
        scene.add(groupDims);

        const allMeshNodes = [];
        const allEdgeNodes = [];

        // DOLLHOUSE SECTION CUT CLIPPING PLANES
        const clipPlaneZ = new THREE.Plane(new THREE.Vector3(0, 0, 1), 5.0);
        const clipPlaneX = new THREE.Plane(new THREE.Vector3(1, 0, 0), -4.5);
        let activeClipPlane = clipPlaneZ;
        let isCutawayActive = false;

        function updateCutawayPlane() {{
            if (isCutawayActive) {{
                renderer.clippingPlanes = [activeClipPlane];
            }} else {{
                renderer.clippingPlanes = [];
            }}
        }}

        function toggleCutaway(enabled) {{
            isCutawayActive = enabled;
            updateCutawayPlane();
        }}

        function updateCutDepth(val) {{
            const depth = parseFloat(val);
            document.getElementById('cut-val').textContent = depth.toFixed(1) + 'm';
            if (activeClipPlane === clipPlaneZ) {{
                clipPlaneZ.constant = depth;
            }} else {{
                clipPlaneX.constant = -(10.0 - depth);
            }}
        }}

        function setCutAxis(axis) {{
            document.getElementById('cut-axis-z').classList.toggle('active', axis === 'z');
            document.getElementById('cut-axis-x').classList.toggle('active', axis === 'x');
            activeClipPlane = (axis === 'z') ? clipPlaneZ : clipPlaneX;
            updateCutawayPlane();
        }}

        function triggerDollhousePreset() {{
            document.getElementById('chk-cutaway').checked = true;
            toggleCutaway(true);
            setCutAxis('z');
            const chkDims = document.getElementById('chk-dims');
            if (chkDims) {{
                chkDims.checked = false;
                toggleDimensions(false);
            }}
            camera.position.set(-8.0, 7.5, -20.5);
            controls.target.set(5.0, 3.8, -5.0);
            controls.update();
        }}

        function toggleUIPanel() {{
            const p = document.getElementById('control-panel');
            p.classList.toggle('open');
        }}

        // BUILD ARCHITECTURAL BOX GEOMETRY
        BOXES_DATA.forEach(b => {{
            const geo = new THREE.BoxGeometry(b.w, b.h, b.d);
            const initialMat = MAT_STYLES.pbr[b.mat] || MAT_STYLES.pbr.wall;
            const mesh = new THREE.Mesh(geo, initialMat);

            const posX = b.x + b.w / 2.0;
            const posY = b.z + b.h / 2.0;
            const posZ = -(b.y + b.d / 2.0);

            mesh.position.set(posX, posY, posZ);
            mesh.castShadow = (b.mat !== 'glass' && b.mat !== 'light_glow');
            mesh.receiveShadow = true;
            mesh.userData = {{ layer: b.layer, matKey: b.mat, origY: posY, z_base: b.z }};

            const isStructural = b.layer.startsWith('3D-WALLS') || b.layer === '3D-COLUMNS' || b.layer === '3D-SLABS' || b.layer === '3D-ROOF';
            if (isStructural) {{
                const edges = new THREE.EdgesGeometry(geo, 24);
                const edgeMat = new THREE.LineBasicMaterial({{ color: 0x475569, linewidth: 1 }});
                const edgeLine = new THREE.LineSegments(edges, edgeMat);
                mesh.add(edgeLine);
                allEdgeNodes.push(edgeLine);
            }}

            if (b.layer === '3D-ROOF') {{
                groupRoof.add(mesh);
            }} else if (b.z >= 3.7) {{
                group2F.add(mesh);
            }} else {{
                groupGF.add(mesh);
            }}

            allMeshNodes.push(mesh);
        }});

        // BUILD ARCHITECTURAL CYLINDER GEOMETRY
        CYLINDERS_DATA.forEach(c => {{
            const geo = new THREE.CylinderGeometry(c.r, c.r, c.h, 24);
            const initialMat = MAT_STYLES.pbr[c.mat] || MAT_STYLES.pbr.metal_dark;
            const mesh = new THREE.Mesh(geo, initialMat);

            const posX = c.cx;
            const posY = c.z + c.h / 2.0;
            const posZ = -c.cy;

            mesh.position.set(posX, posY, posZ);
            mesh.castShadow = (c.mat !== 'glass' && c.mat !== 'light_glow');
            mesh.receiveShadow = true;
            mesh.userData = {{ layer: c.layer, matKey: c.mat, origY: posY, z_base: c.z }};

            if (c.layer === '3D-ROOF') {{
                groupRoof.add(mesh);
            }} else if (c.z >= 3.7) {{
                group2F.add(mesh);
            }} else {{
                groupGF.add(mesh);
            }}

            allMeshNodes.push(mesh);
        }});

        // 3D DIMENSION BADGES & LINES (Metric Sukat)
        function makeDimensionBadge(text, subtext) {{
            const canvas = document.createElement('canvas');
            canvas.width = 256;
            canvas.height = 128;
            const ctx = canvas.getContext('2d');

            ctx.fillStyle = 'rgba(15, 23, 42, 0.92)';
            if (ctx.roundRect) {{
                ctx.roundRect(8, 8, 240, 112, 16);
            }} else {{
                ctx.rect(8, 8, 240, 112);
            }}
            ctx.fill();

            ctx.strokeStyle = '#2563eb';
            ctx.lineWidth = 4;
            if (ctx.roundRect) {{
                ctx.roundRect(8, 8, 240, 112, 16);
            }} else {{
                ctx.rect(8, 8, 240, 112);
            }}
            ctx.stroke();

            ctx.font = 'bold 38px "JetBrains Mono", monospace';
            ctx.fillStyle = '#ffffff';
            ctx.textAlign = 'center';
            ctx.fillText(text, 128, 56);

            if (subtext) {{
                ctx.font = 'bold 20px "Plus Jakarta Sans", sans-serif';
                ctx.fillStyle = '#93c5fd';
                ctx.fillText(subtext, 128, 92);
            }}

            const tex = new THREE.CanvasTexture(canvas);
            const mat = new THREE.SpriteMaterial({{ map: tex, depthTest: false }});
            const sprite = new THREE.Sprite(mat);
            sprite.scale.set(1.4, 0.7, 1.0);
            return sprite;
        }}

        DIMS_DATA.forEach(d => {{
            const p1 = new THREE.Vector3(d.x1, d.z1, -d.y1);
            const p2 = new THREE.Vector3(d.x2, d.z2, -d.y2);

            const lineGeo = new THREE.BufferGeometry().setFromPoints([p1, p2]);
            const lineMat = new THREE.LineBasicMaterial({{ color: 0x2563eb, linewidth: 2, depthTest: false }});
            const line = new THREE.Line(lineGeo, lineMat);
            groupDims.add(line);

            const mid = new THREE.Vector3().addVectors(p1, p2).multiplyScalar(0.5);
            mid.y += 0.35;
            const badge = makeDimensionBadge(d.text, d.subtext);
            badge.position.copy(mid);
            groupDims.add(badge);
        }});

        // SOLAR SIMULATOR & LIGHTING UPDATES
        const sunTimeSlider = document.getElementById('sun-time-slider');
        const sunTimeVal = document.getElementById('time-val');
        const sunAzimSlider = document.getElementById('sun-azim-slider');
        const sunAzimVal = document.getElementById('azim-val');

        function updateSolarLighting() {{
            const hour = parseFloat(sunTimeSlider.value);
            const azimDeg = parseFloat(sunAzimSlider.value);

            const h = Math.floor(hour);
            const m = Math.floor((hour - h) * 60);
            const timeStr = String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0');

            let elevationDeg = 0;
            if (hour >= 6 && hour <= 18.5) {{
                elevationDeg = Math.sin(((hour - 6) / 12.5) * Math.PI) * 78.0;
            }}
            elevationDeg = Math.max(0.5, elevationDeg);

            sunTimeVal.textContent = `${{timeStr}} (${{elevationDeg.toFixed(0)}}° Sun)`;
            sunAzimVal.textContent = `${{azimDeg}}°`;

            const radAzim = (azimDeg * Math.PI) / 180.0;
            const radElev = (elevationDeg * Math.PI) / 180.0;
            const sunDist = 45.0;

            const sunX = 5.0 + sunDist * Math.cos(radElev) * Math.sin(radAzim);
            const sunY = sunDist * Math.sin(radElev);
            const sunZ = -5.0 - sunDist * Math.cos(radElev) * Math.cos(radAzim);

            sunLight.position.set(sunX, sunY, sunZ);
            fillLight.position.set(-sunX * 0.7, sunY * 0.5 + 5.0, -sunZ * 0.7);
        }}

        sunTimeSlider.addEventListener('input', updateSolarLighting);
        sunAzimSlider.addEventListener('input', updateSolarLighting);
        updateSolarLighting();
        applyInteriorLighting();

        // SHADING STYLES CONTROLLER
        function setStyle(styleKey) {{
            currentStyle = styleKey;
            document.querySelectorAll('.btn-grid-3 .btn, .btn-grid-2 .btn').forEach(b => {{
                if (b.id && b.id.startsWith('style-')) b.classList.remove('active');
            }});
            const btn = document.getElementById('style-' + styleKey);
            if (btn) btn.classList.add('active');

            const tag = document.getElementById('current-style-tag');
            tag.innerText = styleKey.toUpperCase();

            const palette = MAT_STYLES[styleKey] || MAT_STYLES.pbr;

            allMeshNodes.forEach(m => {{
                const k = m.userData.matKey;
                m.material = palette[k] || palette.wall;
            }});

            if (styleKey === 'cad') {{
                scene.background.setHex(0xffffff);
                allEdgeNodes.forEach(e => e.material.color.setHex(0x000000));
            }} else if (styleKey === 'blueprint') {{
                scene.background.setHex(0x0b162c);
                allEdgeNodes.forEach(e => e.material.color.setHex(0x38bdf8));
            }} else if (styleKey === 'xray') {{
                scene.background.setHex(0x060c18);
                allEdgeNodes.forEach(e => e.material.color.setHex(0x00e5ff));
            }} else if (styleKey === 'nurbs') {{
                scene.background.setHex(0x181a1f);
                allEdgeNodes.forEach(e => e.material.color.setHex(0x3a3c42));
            }} else {{
                scene.background.setHex(0xffffff);
                allEdgeNodes.forEach(e => e.material.color.setHex(0x475569));
            }}
        }}

        // EXPLODED AXONOMETRIC & VISIBILITY HANDLERS
        const explodeSlider = document.getElementById('explode-slider');
        const explodeVal = document.getElementById('explode-val');
        explodeSlider.addEventListener('input', (e) => {{
            const val = parseFloat(e.target.value);
            explodeVal.innerText = val.toFixed(1) + 'm';
            group2F.position.y = val * 0.75;
            groupRoof.position.y = val * 1.5;
            groupDims.position.y = val * 0.35;
        }});

        function toggleDimensions(visible) {{
            groupDims.visible = visible;
        }}

        function toggleLayer(layerName, visible) {{
            allMeshNodes.forEach(m => {{
                if (m.userData.layer === layerName) m.visible = visible;
            }});
        }}

        function toggleFloor(floorNum, visible) {{
            if (floorNum === 1) groupGF.visible = visible;
            if (floorNum === 2) group2F.visible = visible;
        }}

        function toggleLouvers(visible) {{
            allMeshNodes.forEach(m => {{
                if (m.userData.layer === '3D-LOUVERS' || m.userData.layer === '3D-CANOPY' || m.userData.layer === '3D-PERGOLA') {{
                    m.visible = visible;
                }}
            }});
        }}

        function toggleFurniture(visible) {{
            allMeshNodes.forEach(m => {{
                if (m.userData.layer === '3D-FURNITURE' || m.userData.layer === '3D-BARISTA-BAR') {{
                    m.visible = visible;
                }}
            }});
        }}

        // CAMERA PRESETS
        function setCamera(preset) {{
            document.querySelectorAll('.btn-grid-2 .btn').forEach(b => {{
                if (b.id && b.id.startsWith('cam-')) b.classList.remove('active');
            }});
            const btn = document.getElementById('cam-' + preset);
            if (btn) btn.classList.add('active');

            if (preset === 'iso') {{
                camera.position.set(-14, 16, -20);
                controls.target.set(5.0, 3.5, -6.0);
            }} else if (preset === 'front') {{
                camera.position.set(5.0, 3.8, -24.0);
                controls.target.set(5.0, 3.5, -6.0);
            }} else if (preset === 'balcony') {{
                camera.position.set(5.0, 7.0, -18.0);
                controls.target.set(5.0, 4.5, -11.0);
            }} else if (preset === 'top') {{
                camera.position.set(5.0, 26.0, -5.0);
                controls.target.set(5.0, 0.0, -5.0);
            }}
            controls.update();
        }}

        setCamera('iso');

        // Animation Loop & Responsive Resize
        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});

        function animate() {{
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }}
        animate();
    </script>
</body>
</html>
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    file_size_kb = os.path.getsize(output_path) / 1024.0
    print(f"SUCCESS: Advanced Interactive 3D WebGL Viewer generated: '{output_path}' ({file_size_kb:.2f} KB).")


# ==============================================================================
# PIPELINE EXECUTION
# ==============================================================================

def generate_all_3d_formats():
    print("=" * 70)
    print("3D COMPUTATIONAL ARCHITECTURAL MODELING ENGINE")
    print("Project: 2-Storey Coffee Shop in Burgos, Pakil, Laguna")
    print("Standards: Metric (mm), Multi-Format Export (DXF, OBJ, WebGL HTML)")
    print("=" * 70)

    # 1. Compile 3D Building Geometry & Dimension Chains
    print("[1/4] Assembling 3D architectural geometry & interior assets...")
    model = build_coffee_shop_3d_model()
    print(f"      Total 3D components compiled: {len(model.boxes)} boxes, {len(model.cylinders)} cylinders.")
    print(f"      Total 3D dimension chains compiled: {len(model.dimensions)} measurement tags.")

    # 2. Export 3D DXF
    print("[2/4] Compiling 3D DXF (AutoCAD, SketchUp, Rhino, Revit)...")
    export_dxf_3d(model, "coffee_shop_3d.dxf")

    # 3. Export 3D OBJ & MTL
    print("[3/4] Compiling Universal 3D OBJ & MTL with architectural materials...")
    export_obj_3d(model, "coffee_shop_3d.obj", "coffee_shop_3d.mtl")

    # 4. Export Standalone Interactive WebGL Viewer
    print("[4/4] Compiling Standalone Interactive 3D WebGL Viewer...")
    export_webgl_viewer(model, "coffee_shop_3d_viewer.html")

    print("=" * 70)
    import shutil
    shutil.copyfile("coffee_shop_3d_viewer.html", "index.html")
    print("ALL 3D ARCHITECTURAL ASSETS GENERATED SUCCESSFULLY!")
    print("Files created in your workspace:")
    print("  1. coffee_shop_3d.dxf        (For AutoCAD 3D, SketchUp, Rhino, Revit)")
    print("  2. coffee_shop_3d.obj        (For Blender, 3ds Max, Cinema4D, Windows 3D Viewer)")
    print("  3. coffee_shop_3d.mtl        (Material definition file for OBJ)")
    print("  4. coffee_shop_3d_viewer.html(Open directly in Chrome/Edge to explore in 3D!)")
    print("=" * 70)


if __name__ == "__main__":
    generate_all_3d_formats()
