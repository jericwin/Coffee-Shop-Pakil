#!/usr/bin/env python3
"""
Adds the Dedicated Parking Facility (Cars, PWD, Motorcycles, Bicycles, Driveway, Streetlights)
and updates branding to 'Café Turumba & Coffee Roasters' in generate_coffee_shop_3d.py.
"""

import re
import os

with open("generate_coffee_shop_3d.py", "r", encoding="utf-8") as f:
    code = f.read()

# ----------------------------------------------------------------------
# 1. ADD PARKING FACILITY FUNCTION TO 3D GENERATOR
# ----------------------------------------------------------------------
parking_code = '''
# ==============================================================================
# DEDICATED PARKING FACILITY & SITE GROUNDS (PAKIL, LAGUNA)
# ==============================================================================

def add_dedicated_parking_facility(m: Model3D):
    """
    Constructs the comprehensive 240 sq.m. Dedicated Off-Street Parking Facility:
    - 8 Standard Car Parking Stalls (2.5m x 5.0m) with white striping & wheel stops
    - 3D Modern Parked Vehicles (Pearl White SUV, Silver Sedan, Navy Crossover)
    - 1 PWD Accessible Parking Stall (3.7m x 5.0m, BP-344 compliant) with blue epoxy pad,
      wheelchair symbol, yellow hatched access aisle, curb ramp, and PWD post sign
    - 6 Dedicated Motorcycle / Scooter Stalls with parked motorbikes
    - Covered Bicycle Parking Station (4 inverted-U racks, 2 road bikes, repair pump)
    - 6.0m Two-Way Central Circulation Drive Aisle with directional white road arrows
    - Manila East Road highway asphalt strip in front with yellow dashed centerline
    - Solar LED streetlamp poles (6m) illuminating the parking area
    - Concrete perimeter curbs and lush tropical palm tree landscaping
    """
    # 1. SITE GROUND PAVEMENT SLAB (Asphalt & Interlocking Eco-Pavers)
    # Extends in front of the building (Y = 9900 to 25500, X = -3000 to 13000)
    m.add_box(-3000, 9900, -30, 16000, 15600, 30, "3D-SITE", "asphalt")
    
    # Concrete curbs enclosing parking property boundary
    m.add_box(-3000, 9900, 0, 200, 15600, 160, "3D-SITE", "concrete")
    m.add_box(12800, 9900, 0, 200, 15600, 160, "3D-SITE", "concrete")
    m.add_box(-3000, 9900, 0, 16000, 200, 160, "3D-SITE", "concrete")

    # Front sidewalk / pedestrian buffer (Y = 24800 to 25500)
    m.add_box(-3000, 24800, 0, 3500, 700, 150, "3D-SITE", "concrete")
    m.add_box(6500, 24800, 0, 6500, 700, 150, "3D-SITE", "concrete")

    # 2. MANILA EAST ROAD (NATIONAL HIGHWAY) SECTION IN FRONT
    # Road strip: Y = 25500 to 32500, X = -8000 to 18000
    m.add_box(-8000, 25500, -40, 26000, 7000, 40, "3D-SITE", "asphalt")

    # Yellow dashed highway center line (at Y = 29000)
    for rx in range(-8000, 17000, 3500):
        m.add_box(rx, 28925, 2, 2000, 150, 8, "3D-SITE", "paint_yellow")
    # White highway shoulder solid lines
    m.add_box(-8000, 25600, 2, 26000, 120, 8, "3D-SITE", "paint_white")
    m.add_box(-8000, 32380, 2, 26000, 120, 8, "3D-SITE", "paint_white")

    # 6.0m Two-Way Ingress / Egress Apron Drop (X = 500 to 6500, Y = 24800 to 25500)
    m.add_box(500, 24800, 0, 6000, 700, 50, "3D-SITE", "asphalt")

    # 3. 6.0M TWO-WAY CENTRAL CIRCULATION DRIVE AISLE
    # White Directional Traffic Arrows on pavement
    # Ingress entry arrow (pointing South toward cafe: Y = 23000, X = 2000)
    m.add_box(1950, 22200, 2, 100, 800, 6, "3D-SITE", "paint_white")
    m.add_box(1850, 22200, 2, 300, 100, 6, "3D-SITE", "paint_white")
    m.add_box(1750, 22300, 2, 500, 100, 6, "3D-SITE", "paint_white")

    # Egress exit arrow (pointing North toward highway: Y = 16000, X = 5000)
    m.add_box(4950, 16000, 2, 100, 800, 6, "3D-SITE", "paint_white")
    m.add_box(4850, 16700, 2, 300, 100, 6, "3D-SITE", "paint_white")
    m.add_box(4750, 16600, 2, 500, 100, 6, "3D-SITE", "paint_white")

    # 4. EAST PARKING BAYS (STANDARD CAR STALLS & PWD STALL)
    # Stalls depth: 5.0m (X = 6800 to 11800)
    # Stalls 1 to 4: Y = 11200 to 21200 (4 stalls x 2.5m = 10.0m)
    car_y_coords = [11200, 13700, 16200, 18700]

    for idx, sy in enumerate(car_y_coords):
        # White boundary line (100mm wide x 5000mm length)
        m.add_box(6800, sy, 2, 5000, 100, 8, "3D-SITE", "paint_white")
        # Heavy-duty rubber wheel stop (car bumper: 1800mm x 150mm x 100mm) at back (X = 11400)
        m.add_box(11400, sy + 350, 0, 150, 1800, 100, "3D-SITE", "metal_dark")
        # Yellow safety reflector caps on wheel stop
        m.add_box(11390, sy + 500, 40, 15, 300, 40, "3D-SITE", "paint_yellow")
        m.add_box(11390, sy + 1500, 40, 15, 300, 40, "3D-SITE", "paint_yellow")

    # Final boundary stripe for stall 4
    m.add_box(6800, 21200, 2, 5000, 100, 8, "3D-SITE", "paint_white")

    # 3D PARKED VEHICLE #1: PEARL WHITE LUXURY SUV (Stall 1: Y = 11200)
    car1_x, car1_y = 7200, 11500
    m.add_box(car1_x, car1_y, 200, 4200, 1900, 750, "3D-VEHICLES", "fixture_white") # Chassis
    m.add_box(car1_x + 600, car1_y + 50, 950, 2500, 1800, 680, "3D-VEHICLES", "fixture_white") # Cabin
    m.add_box(car1_x + 580, car1_y + 60, 960, 2540, 1780, 650, "3D-VEHICLES", "glass") # Tinted Windows
    m.add_box(car1_x - 30, car1_y + 200, 400, 30, 1500, 180, "3D-VEHICLES", "metal_dark") # Grille
    m.add_box(car1_x - 20, car1_y + 150, 450, 20, 250, 120, "3D-LIGHTS", "light_glow") # Headlight L
    m.add_box(car1_x - 20, car1_y + 1500, 450, 20, 250, 120, "3D-LIGHTS", "light_glow") # Headlight R
    m.add_box(car1_x + 4200, car1_y + 150, 500, 20, 250, 100, "3D-VEHICLES", "car_paint_red") # Taillight L
    m.add_box(car1_x + 4200, car1_y + 1500, 500, 20, 250, 100, "3D-VEHICLES", "car_paint_red") # Taillight R
    # 4 Wheels
    for wx, wy in [(car1_x + 750, car1_y - 40), (car1_x + 3300, car1_y - 40),
                   (car1_x + 750, car1_y + 1720), (car1_x + 3300, car1_y + 1720)]:
        m.add_cylinder(wx, wy + 110, 0, 330, 220, "3D-VEHICLES", "metal_dark")
        m.add_cylinder(wx, wy + 110, 80, 180, 60, "3D-VEHICLES", "appliance_steel") # Silver Hubcap

    # 3D PARKED VEHICLE #2: METALLIC SILVER COMPACT SEDAN (Stall 2: Y = 13700)
    car2_x, car2_y = 7300, 14000
    m.add_box(car2_x, car2_y, 180, 4200, 1800, 600, "3D-VEHICLES", "car_paint_silver")
    m.add_box(car2_x + 800, car2_y + 50, 780, 2200, 1700, 580, "3D-VEHICLES", "car_paint_silver")
    m.add_box(car2_x + 780, car2_y + 60, 790, 2240, 1680, 550, "3D-VEHICLES", "glass")
    m.add_box(car2_x - 20, car2_y + 150, 350, 20, 220, 100, "3D-LIGHTS", "light_glow")
    m.add_box(car2_x - 20, car2_y + 1430, 350, 20, 220, 100, "3D-LIGHTS", "light_glow")
    m.add_box(car2_x + 4200, car2_y + 150, 400, 20, 220, 90, "3D-VEHICLES", "car_paint_red")
    m.add_box(car2_x + 4200, car2_y + 1430, 400, 20, 220, 90, "3D-VEHICLES", "car_paint_red")
    for wx, wy in [(car2_x + 700, car2_y - 40), (car2_x + 3200, car2_y - 40),
                   (car2_x + 700, car2_y + 1620), (car2_x + 3200, car2_y + 1620)]:
        m.add_cylinder(wx, wy + 110, 0, 300, 200, "3D-VEHICLES", "metal_dark")
        m.add_cylinder(wx, wy + 110, 70, 160, 60, "3D-VEHICLES", "appliance_steel")

    # 3D PARKED VEHICLE #3: MIDNIGHT BLUE CROSSOVER (Stall 3: Y = 16200)
    car3_x, car3_y = 7250, 16500
    m.add_box(car3_x, car3_y, 190, 4150, 1850, 700, "3D-VEHICLES", "car_paint_blue")
    m.add_box(car3_x + 650, car3_y + 50, 890, 2450, 1750, 640, "3D-VEHICLES", "car_paint_blue")
    m.add_box(car3_x + 630, car3_y + 60, 900, 2490, 1730, 610, "3D-VEHICLES", "glass")
    m.add_box(car3_x - 20, car3_y + 150, 400, 20, 220, 100, "3D-LIGHTS", "light_glow")
    m.add_box(car3_x - 20, car3_y + 1480, 400, 20, 220, 100, "3D-LIGHTS", "light_glow")
    for wx, wy in [(car3_x + 700, car3_y - 40), (car3_x + 3250, car3_y - 40),
                   (car3_x + 700, car3_y + 1670), (car3_x + 3250, car3_y + 1670)]:
        m.add_cylinder(wx, wy + 110, 0, 310, 210, "3D-VEHICLES", "metal_dark")

    # 5. PWD ACCESSIBLE PARKING STALL (BP 344 COMPLIANT)
    # Size: 3.70m wide x 5.0m deep (X = 6800 to 11800, Y = 21200 to 24900)
    pwd_x, pwd_y = 6800, 21200
    pwd_w, pwd_d = 5000, 3700

    # Blue-painted epoxy ground pad
    m.add_box(pwd_x, pwd_y, 2, pwd_w, pwd_d, 6, "3D-SITE", "paint_blue")
    # White perimeter border
    m.add_box(pwd_x, pwd_y + pwd_d - 100, 4, pwd_w, 100, 8, "3D-SITE", "paint_white")

    # Yellow diagonal hatched 1.2m transfer access aisle (Y = 21200 to 22400)
    for hx in range(pwd_x + 200, pwd_x + pwd_w - 400, 800):
        m.add_box(hx, pwd_y + 100, 4, 300, 1000, 6, "3D-SITE", "paint_yellow")

    # International Symbol of Access (Wheelchair Emblem in Center of Stall)
    # Center at (pwd_x + 2500, pwd_y + 2800)
    wc_x, wc_y = pwd_x + 2400, pwd_y + 2700
    m.add_box(wc_x, wc_y, 8, 200, 60, 8, "3D-SITE", "paint_white") # Head
    m.add_box(wc_x + 50, wc_y + 100, 8, 100, 350, 8, "3D-SITE", "paint_white") # Torso
    m.add_box(wc_x + 50, wc_y + 450, 8, 300, 80, 8, "3D-SITE", "paint_white") # Seat
    m.add_box(wc_x + 280, wc_y + 250, 8, 70, 200, 8, "3D-SITE", "paint_white") # Footrest
    m.add_cylinder(wc_x + 100, wc_y + 350, 8, 250, 8, "3D-SITE", "paint_white") # Wheel ring

    # PWD Wheel Stop
    m.add_box(pwd_x + pwd_w - 400, pwd_y + 1800, 0, 150, 1800, 100, "3D-SITE", "paint_blue")

    # PWD Reserved Post Sign
    m.add_cylinder(pwd_x + 200, pwd_y + pwd_d - 300, 0, 25, 2000, "3D-SITE", "metal_dark")
    m.add_box(pwd_x + 100, pwd_y + pwd_d - 350, 1400, 200, 30, 450, "3D-SITE", "paint_blue") # Signboard plate
    m.add_box(pwd_x + 120, pwd_y + pwd_d - 365, 1450, 160, 15, 350, "3D-SITE", "paint_white") # Emblem

    # PWD Direct Curb Ramp (1:12 slope) connecting to cafe entrance walkway
    m.add_box(6000, 23500, 0, 800, 1400, 150, "3D-SITE", "concrete")

    # 6. WEST PARKING BAYS (MOTORCYCLE BAY & COVERED BICYCLE STATION)
    # Stalls depth: 2.5m (X = -2200 to 300 mm)
    # Motorcycle Bay (6 Stalls): Y = 11200 to 18700 (6 stalls x 1.25m = 7.5m)
    for k in range(7):
        my = 11200 + k * 1250
        m.add_box(-2200, my, 2, 2500, 80, 8, "3D-SITE", "paint_white")

    # 3D Parked Motorcycle #1 (Red Sport Motorcycle in Stall 1: Y = 11500)
    moto1_x, moto1_y = -1800, 11700
    m.add_box(moto1_x, moto1_y, 250, 1600, 500, 550, "3D-VEHICLES", "car_paint_red") # Frame
    m.add_box(moto1_x + 400, moto1_y + 50, 650, 600, 400, 200, "3D-VEHICLES", "leather") # Seat
    m.add_cylinder(moto1_x + 150, moto1_y + 250, 0, 260, 100, "3D-VEHICLES", "metal_dark") # Front wheel
    m.add_cylinder(moto1_x + 1450, moto1_y + 250, 0, 260, 120, "3D-VEHICLES", "metal_dark") # Rear wheel
    m.add_box(moto1_x + 100, moto1_y + 100, 800, 80, 300, 40, "3D-VEHICLES", "metal_dark") # Handlebars
    m.add_box(moto1_x - 30, moto1_y + 200, 600, 30, 100, 100, "3D-LIGHTS", "light_glow") # Headlight

    # 3D Parked Motorcycle #2 (Charcoal Scooter in Stall 3: Y = 14000)
    moto2_x, moto2_y = -1750, 14200
    m.add_box(moto2_x, moto2_y, 220, 1500, 550, 500, "3D-VEHICLES", "metal_dark")
    m.add_box(moto2_x + 450, moto2_y + 50, 620, 650, 450, 180, "3D-VEHICLES", "leather")
    m.add_cylinder(moto2_x + 150, moto2_y + 275, 0, 240, 90, "3D-VEHICLES", "metal_dark")
    m.add_cylinder(moto2_x + 1350, moto2_y + 275, 0, 240, 100, "3D-VEHICLES", "metal_dark")

    # 7. COVERED BICYCLE PARKING STATION (LAGUNA LAKE LOOP PIT-STOP)
    # Size: 2.5m x 5.0m (X = -2200 to 300 mm, Y = 19200 to 24200)
    bike_x, bike_y = -2200, 19200
    bike_w, bike_d = 2500, 5000

    # 4 Steel Canopy Posts (Z = 0 to 2600mm)
    m.add_box(bike_x, bike_y, 0, 100, 100, 2600, "3D-CANOPY", "metal_dark")
    m.add_box(bike_x + bike_w - 100, bike_y, 0, 100, 100, 2600, "3D-CANOPY", "metal_dark")
    m.add_box(bike_x, bike_y + bike_d - 100, 0, 100, 100, 2600, "3D-CANOPY", "metal_dark")
    m.add_box(bike_x + bike_w - 100, bike_y + bike_d - 100, 0, 100, 100, 2600, "3D-CANOPY", "metal_dark")

    # Canopy Roof Shelter
    m.add_box(bike_x - 100, bike_y - 100, 2600, bike_w + 200, bike_d + 200, 60, "3D-CANOPY", "metal_dark")
    m.add_box(bike_x - 50, bike_y - 50, 2660, bike_w + 100, bike_d + 100, 20, "3D-CANOPY", "glass")

    # Inverted-U Stainless Steel Bike Racks (4 Bollards)
    for bx in [-1700, -1100, -500]:
        m.add_box(bx, bike_y + 800, 0, 60, 60, 900, "3D-FURNITURE", "appliance_steel")
        m.add_box(bx, bike_y + 2200, 0, 60, 60, 900, "3D-FURNITURE", "appliance_steel")
        m.add_box(bx, bike_y + 800, 840, 60, 1400, 60, "3D-FURNITURE", "appliance_steel")

    # 3D Parked Road Bicycle #1 (Red Frame)
    m.add_cylinder(-1600, bike_y + 1100, 0, 330, 40, "3D-VEHICLES", "metal_dark") # Front wheel
    m.add_cylinder(-1600, bike_y + 2100, 0, 330, 40, "3D-VEHICLES", "metal_dark") # Rear wheel
    m.add_box(-1610, bike_y + 1100, 320, 20, 1000, 30, "3D-VEHICLES", "car_paint_red") # Top tube
    m.add_box(-1610, bike_y + 1550, 320, 20, 40, 450, "3D-VEHICLES", "car_paint_red") # Seat tube
    m.add_box(-1630, bike_y + 1500, 770, 60, 140, 30, "3D-VEHICLES", "leather") # Saddle

    # Free Standing Bike Floor Pump & Repair Tool Stand
    m.add_cylinder(-300, bike_y + 1000, 0, 80, 700, "3D-FURNITURE", "paint_yellow") # Pump cylinder
    m.add_box(-450, bike_y + 980, 680, 300, 40, 30, "3D-FURNITURE", "metal_dark") # Pump handle
    m.add_box(-400, bike_y + 1500, 0, 120, 120, 1400, "3D-FURNITURE", "metal_dark") # Tool stand post

    # 8. SOLAR LED STREETLIGHT POLES (ILLUMINATING THE PARKING AREA)
    # Pole 1 (East boundary: X = 12500, Y = 17500)
    m.add_cylinder(12500, 17500, 0, 80, 5800, "3D-SITE", "metal_dark") # Mast
    m.add_box(12100, 17400, 5700, 400, 200, 80, "3D-SITE", "metal_dark") # Arm
    m.add_box(12000, 17350, 5800, 500, 400, 20, "3D-SITE", "metal_dark") # Solar panel
    m.add_box(12050, 17420, 5650, 300, 160, 40, "3D-LIGHTS", "light_glow") # Downlight lamp head

    # Pole 2 (West boundary: X = -2600, Y = 17500)
    m.add_cylinder(-2600, 17500, 0, 80, 5800, "3D-SITE", "metal_dark")
    m.add_box(-2600, 17400, 5700, 400, 200, 80, "3D-SITE", "metal_dark")
    m.add_box(-2500, 17350, 5800, 500, 400, 20, "3D-SITE", "metal_dark")
    m.add_box(-2450, 17420, 5650, 300, 160, 40, "3D-LIGHTS", "light_glow")

    # 9. TROPICAL PALM TREES & PERIMETER PLANTER BOXES
    palm_coords = [
        (-2700, 10500), (-2700, 24500),
        (12400, 10500), (12400, 24500)
    ]
    for px, py in palm_coords:
        # Planter Box Base
        m.add_box(px - 400, py - 400, 0, 800, 800, 450, "3D-SITE", "concrete")
        m.add_box(px - 350, py - 350, 450, 700, 700, 50, "3D-SITE", "wood_dark") # Soil
        # Palm trunk (slender curved height 4.5m)
        m.add_cylinder(px, py, 500, 120, 4000, "3D-SITE", "wood_dark")
        # Green palm frond crown
        m.add_box(px - 800, py - 800, 4400, 1600, 1600, 250, "3D-SITE", "greenery")
        m.add_box(px - 1100, py - 200, 4300, 2200, 400, 150, "3D-SITE", "greenery")
        m.add_box(px - 200, py - 1100, 4300, 400, 2200, 150, "3D-SITE", "greenery")
'''

# Insert parking function before build_coffee_shop_3d_model
code = code.replace("def build_coffee_shop_3d_model():", parking_code + "\ndef build_coffee_shop_3d_model():")

# Call add_dedicated_parking_facility(m) inside build_coffee_shop_3d_model
build_hook = """    # 1. FOUNDATION, PLINTH & ENTRANCE STEPS"""
new_build_hook = """    # 0. DEDICATED PARKING FACILITY & SITE GROUNDS
    add_dedicated_parking_facility(m)

    # 1. FOUNDATION, PLINTH & ENTRANCE STEPS"""
code = code.replace(build_hook, new_build_hook)

# ----------------------------------------------------------------------
# 2. UPDATE SIGNBOARDS TO "CAFÉ TURUMBA" & "TURUMBA COFFEE ROASTERS"
# ----------------------------------------------------------------------
code = code.replace(
    'Backlit 3D Architectural Cafe Signage Fascia',
    'Backlit 3D Architectural Cafe Signage Fascia ("CAFÉ TURUMBA")'
)
code = code.replace(
    'Large 3D illuminated Roastery Signboard ("BURGOS SPECIALTY COFFEE ROASTERY")',
    'Large 3D illuminated Roastery Signboard ("TURUMBA COFFEE ROASTERS")'
)

# ----------------------------------------------------------------------
# 3. ADD NEW MATERIALS IN OBJ/MTL AND THREE.JS
# ----------------------------------------------------------------------
mtl_needle = """newmtl appliance_steel
Kd 0.82 0.84 0.87
Ka 0.30 0.30 0.30
Ks 0.90 0.92 0.95
Ns 80
d 1.0"""

mtl_addition = """newmtl appliance_steel
Kd 0.82 0.84 0.87
Ka 0.30 0.30 0.30
Ks 0.90 0.92 0.95
Ns 80
d 1.0

newmtl asphalt
Kd 0.22 0.24 0.27
Ka 0.10 0.10 0.10
Ks 0.05 0.05 0.05
Ns 5
d 1.0

newmtl paint_white
Kd 0.98 0.98 0.98
Ka 0.30 0.30 0.30
Ks 0.20 0.20 0.20
Ns 15
d 1.0

newmtl paint_yellow
Kd 0.96 0.75 0.15
Ka 0.25 0.20 0.05
Ks 0.10 0.10 0.10
Ns 10
d 1.0

newmtl paint_blue
Kd 0.12 0.35 0.85
Ka 0.10 0.20 0.40
Ks 0.30 0.35 0.45
Ns 25
d 1.0

newmtl car_paint_red
Kd 0.82 0.15 0.15
Ka 0.20 0.05 0.05
Ks 0.75 0.75 0.75
Ns 85
d 1.0

newmtl car_paint_silver
Kd 0.82 0.83 0.86
Ka 0.30 0.30 0.32
Ks 0.85 0.85 0.88
Ns 90
d 1.0

newmtl car_paint_blue
Kd 0.12 0.22 0.52
Ka 0.05 0.10 0.20
Ks 0.75 0.75 0.80
Ns 85
d 1.0

newmtl greenery
Kd 0.15 0.48 0.18
Ka 0.08 0.20 0.09
Ks 0.05 0.08 0.05
Ns 5
d 1.0"""
code = code.replace(mtl_needle, mtl_addition)

# Three.js PBR materials injection
pbr_needle = """                light_glow: new THREE.MeshBasicMaterial({
                    color: 0xffe29a
                })
            },"""

pbr_addition = """                light_glow: new THREE.MeshBasicMaterial({
                    color: 0xffe29a
                }),
                asphalt: new THREE.MeshStandardMaterial({
                    color: 0x242831,
                    roughness: 0.88,
                    metalness: 0.05
                }),
                paint_white: new THREE.MeshBasicMaterial({
                    color: 0xffffff
                }),
                paint_yellow: new THREE.MeshBasicMaterial({
                    color: 0xf59e0b
                }),
                paint_blue: new THREE.MeshStandardMaterial({
                    color: 0x1d4ed8,
                    roughness: 0.40,
                    metalness: 0.05
                }),
                car_paint_red: new THREE.MeshStandardMaterial({
                    color: 0xb91c1c,
                    roughness: 0.20,
                    metalness: 0.75
                }),
                car_paint_silver: new THREE.MeshStandardMaterial({
                    color: 0xd1d5db,
                    roughness: 0.25,
                    metalness: 0.85
                }),
                car_paint_blue: new THREE.MeshStandardMaterial({
                    color: 0x1e3a8a,
                    roughness: 0.20,
                    metalness: 0.80
                }),
                greenery: new THREE.MeshStandardMaterial({
                    color: 0x15803d,
                    roughness: 0.65,
                    metalness: 0.05
                })
            },"""
code = code.replace(pbr_needle, pbr_addition)

# Three.js CAD materials injection
cad_needle = """                fixture_white: new THREE.MeshStandardMaterial({ color: 0xf0efe8, roughness: 0.4, metalness: 0.1 }),"""
cad_addition = """                fixture_white: new THREE.MeshStandardMaterial({ color: 0xf0efe8, roughness: 0.4, metalness: 0.1 }),
                asphalt: new THREE.MeshBasicMaterial({ color: 0x94a3b8 }),
                paint_white: new THREE.MeshBasicMaterial({ color: 0xffffff }),
                paint_yellow: new THREE.MeshBasicMaterial({ color: 0xfde047 }),
                paint_blue: new THREE.MeshBasicMaterial({ color: 0x60a5fa }),
                car_paint_red: new THREE.MeshBasicMaterial({ color: 0xf87171 }),
                car_paint_silver: new THREE.MeshBasicMaterial({ color: 0xe2e8f0 }),
                car_paint_blue: new THREE.MeshBasicMaterial({ color: 0x93c5fd }),
                greenery: new THREE.MeshBasicMaterial({ color: 0x86efac }),"""
code = code.replace(cad_needle, cad_addition)

# ----------------------------------------------------------------------
# 4. UPDATE HTML HUD HEADER & AUTOPILOT BUTTONS
# ----------------------------------------------------------------------
code = code.replace(
    "<title>3D Architectural Model | 2-Storey Coffee Shop (Pakil, Laguna)</title>",
    "<title>3D Architectural Model | Café Turumba & Roastery (Pakil, Laguna)</title>"
)
code = code.replace(
    "<h1>2-Storey Specialty Coffee Shop <span class=\"badge\">Burgos, Pakil, Laguna</span></h1>",
    "<h1>Café Turumba & Coffee Roasters <span class=\"badge\">Pakil, Laguna</span> <span class=\"badge\" style=\"background:#10b981;color:#fff;\">Dedicated Parking</span></h1>"
)
code = code.replace(
    "<p>Pakil, Laguna • Contemporary 2-Storey Coffee Shop & Interactive Simulation</p>",
    "<p>Pakil, Laguna • Contemporary 2-Storey Specialty Cafe, Micro-Roastery & Dedicated Parking Facility</p>"
)
code = code.replace(
    "<span class=\"subtitle\">PAKIL COFFEE SHOP</span>",
    "<span class=\"subtitle\">CAFÉ TURUMBA • PAKIL, LAGUNA</span>"
)

# Add Parking navigation destination pills
nav_needle = """        <button class="dest-pill" onclick="autopilotTo('entrance')">Entrance</button>"""
nav_addition = """        <button class="dest-pill" onclick="autopilotTo('parking')" style="background:#d97706;color:#fff;font-weight:700;">Parking Lot</button>
        <button class="dest-pill" onclick="autopilotTo('pwd_parking')" style="background:#2563eb;color:#fff;font-weight:700;">♿ PWD Parking</button>
        <button class="dest-pill" onclick="autopilotTo('bike_station')" style="background:#059669;color:#fff;font-weight:700;">🚲 Bike Station</button>
        <button class="dest-pill" onclick="autopilotTo('entrance')">Entrance</button>"""
code = code.replace(nav_needle, nav_addition)

# Add camera autopilot coordinates for parking
auto_needle = """            entrance: { pos: new THREE.Vector3(2.9, 1.2, 11.8), target: new THREE.Vector3(2.9, 1.2, 9.8) },"""
auto_addition = """            parking: { pos: new THREE.Vector3(5.0, 3.5, 24.0), target: new THREE.Vector3(5.0, 1.5, 12.0) },
            pwd_parking: { pos: new THREE.Vector3(9.5, 2.0, 23.5), target: new THREE.Vector3(9.5, 0.5, 18.0) },
            bike_station: { pos: new THREE.Vector3(-1.0, 2.0, 22.0), target: new THREE.Vector3(-1.0, 0.8, 17.0) },
            entrance: { pos: new THREE.Vector3(2.9, 1.2, 11.8), target: new THREE.Vector3(2.9, 1.2, 9.8) },"""
code = code.replace(auto_needle, auto_addition)

# Update default Orbit camera to show both the building and the parking lot
cam_needle = """        camera.position.set(14.0, 9.0, 15.0);
        camera.lookAt(5.0, 3.0, 5.0);
        controls.target.set(5.0, 3.0, 5.0);"""
cam_addition = """        camera.position.set(16.0, 14.0, 32.0);
        camera.lookAt(5.0, 2.5, 12.0);
        controls.target.set(5.0, 2.5, 12.0);"""
code = code.replace(cam_needle, cam_addition)

with open("generate_coffee_shop_3d.py", "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS: generate_coffee_shop_3d.py patched with Dedicated Parking & Café Turumba branding!")
