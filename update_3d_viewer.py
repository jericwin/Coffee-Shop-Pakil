#!/usr/bin/env python3
"""
Comprehensive revision script for generate_coffee_shop_3d.py:
1. Adds Entrance Pylon Monument Sign at highway entrance ("CAFÉ TURUMBA").
2. Fixes missing PBR and stylistic materials for asphalt, paint_white, paint_yellow,
   paint_blue, car_paint_red, car_paint_silver, car_paint_blue, greenery.
3. Adds procedural dark asphalt texture with realistic micro-aggregate flecks.
4. Adds dedicated groupSite for 3D-SITE and 3D-VEHICLES so toggling and axonometric explode work seamlessly.
5. Adds Parking Lot & Vehicles toggle to the UI.
6. Adds all 8 Camera Presets (Parking & Facade [DEFAULT], North-West Iso, PWD Bay, Bicycle & Moto Station,
   North Entrance, Balcony & Pergola, Interior Barista Bar, Top Site Plan).
7. Sets default view to 'parking' showing the front facade and parking facility.
8. Re-executes generate_coffee_shop_3d.py to produce coffee_shop_3d_viewer.html and index.html.
"""

import sys
import os

with open("generate_coffee_shop_3d.py", "r", encoding="utf-8") as f:
    code = f.read()

# --------------------------------------------------------------------------
# 1. ADD ENTRANCE PYLON SIGN TO add_dedicated_parking_facility
# --------------------------------------------------------------------------
monument_needle = """    # 9. TROPICAL PALM TREES & PERIMETER PLANTER BOXES"""

monument_code = """    # 8B. HIGHWAY ENTRANCE PYLON MONUMENT SIGN ("CAFÉ TURUMBA")
    # Located at property front boundary along Manila East Road (X = -200, Y = 25000)
    pylon_x, pylon_y = -300, 24800
    # Concrete plinth footing
    m.add_box(pylon_x - 100, pylon_y, 0, 900, 500, 500, "3D-SITE", "concrete")
    # Matte black structural steel pylon totem
    m.add_box(pylon_x, pylon_y + 50, 500, 700, 400, 3200, "3D-SITE", "metal_dark")
    # Warm backlit signboard fascia (Facing North highway traffic)
    m.add_box(pylon_x + 50, pylon_y + 450, 1800, 600, 20, 1600, "3D-SITE", "metal_dark")
    # Glowing backlit panel with "CAFÉ TURUMBA"
    m.add_box(pylon_x + 70, pylon_y + 470, 2600, 560, 15, 600, "3D-LIGHTS", "light_glow")
    # Glowing coffee cup icon accent
    m.add_box(pylon_x + 250, pylon_y + 480, 2100, 200, 15, 380, "3D-LIGHTS", "light_glow")
    # Green LED "OPEN • FREE PARKING" bar
    m.add_box(pylon_x + 90, pylon_y + 470, 1200, 520, 15, 180, "3D-SITE", "paint_blue")

    # 9. TROPICAL PALM TREES & PERIMETER PLANTER BOXES"""

if monument_needle in code and "8B. HIGHWAY ENTRANCE PYLON" not in code:
    code = code.replace(monument_needle, monument_code)
    print("-> Added Highway Entrance Pylon Monument Sign.")

# --------------------------------------------------------------------------
# 2. ADD PROCEDURAL ASPHALT TEXTURE
# --------------------------------------------------------------------------
tex_needle = """        // 1. Scandinavian Hardwood Parquet Floor Texture"""

asphalt_tex_code = """        // 0. Highway & Parking Lot Heavy-Duty Asphalt Texture
        function createAsphaltTexture() {
            const canvas = document.createElement('canvas');
            canvas.width = 512;
            canvas.height = 512;
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = '#262c35';
            ctx.fillRect(0, 0, 512, 512);

            // Realistic speckled micro-aggregates & gravel flecks
            for (let i = 0; i < 3500; i++) {
                const rx = pseudoRandom(i, 1.2) * 512;
                const ry = pseudoRandom(i, 4.7) * 512;
                const size = pseudoRandom(i, 8.1) * 2.5 + 0.8;
                const shade = Math.floor(pseudoRandom(i, 9.3) * 50) + 25;
                ctx.fillStyle = `rgb(${shade}, ${shade + 2}, ${shade + 4})`;
                ctx.fillRect(rx, ry, size, size);
            }
            const tex = new THREE.CanvasTexture(canvas);
            tex.wrapS = THREE.RepeatWrapping;
            tex.wrapT = THREE.RepeatWrapping;
            tex.repeat.set(12, 12);
            return tex;
        }
        const texAsphalt = createAsphaltTexture();

        // 1. Scandinavian Hardwood Parquet Floor Texture"""

if tex_needle in code and "createAsphaltTexture" not in code:
    code = code.replace(tex_needle, asphalt_tex_code)
    print("-> Added Procedural Asphalt Texture Generator.")

# --------------------------------------------------------------------------
# 3. ADD MISSING MATERIALS TO ALL MAT_STYLES PALETTES
# --------------------------------------------------------------------------
pbr_needle = """                fixture_white: new THREE.MeshStandardMaterial({
                    map: texMarble,
                    roughness: 0.15,
                    metalness: 0.08
                }),
                light_glow: new THREE.MeshBasicMaterial({
                    color: 0xffe29a
                })"""

pbr_replacement = """                fixture_white: new THREE.MeshStandardMaterial({
                    map: texMarble,
                    roughness: 0.15,
                    metalness: 0.08
                }),
                light_glow: new THREE.MeshBasicMaterial({
                    color: 0xffe29a
                }),
                asphalt: new THREE.MeshStandardMaterial({
                    map: texAsphalt,
                    roughness: 0.88,
                    metalness: 0.08
                }),
                paint_white: new THREE.MeshStandardMaterial({
                    color: 0xffffff,
                    roughness: 0.35,
                    metalness: 0.05
                }),
                paint_yellow: new THREE.MeshStandardMaterial({
                    color: 0xf59e0b,
                    roughness: 0.35,
                    metalness: 0.05
                }),
                paint_blue: new THREE.MeshStandardMaterial({
                    color: 0x2563eb,
                    roughness: 0.30,
                    metalness: 0.08
                }),
                car_paint_red: new THREE.MeshStandardMaterial({
                    color: 0xdc2626,
                    roughness: 0.18,
                    metalness: 0.75
                }),
                car_paint_silver: new THREE.MeshStandardMaterial({
                    color: 0xcbd5e1,
                    roughness: 0.20,
                    metalness: 0.85
                }),
                car_paint_blue: new THREE.MeshStandardMaterial({
                    color: 0x1d4ed8,
                    roughness: 0.20,
                    metalness: 0.75
                }),
                greenery: new THREE.MeshStandardMaterial({
                    color: 0x15803d,
                    roughness: 0.65,
                    metalness: 0.02
                })"""

if pbr_needle in code:
    code = code.replace(pbr_needle, pbr_replacement)
    print("-> Updated PBR materials with asphalt, cars, PWD, and greenery.")

cad_needle = """                fixture_white: new THREE.MeshBasicMaterial({ color: 0xffffff }),
                light_glow: new THREE.MeshBasicMaterial({ color: 0xfef08a })"""

cad_replacement = """                fixture_white: new THREE.MeshBasicMaterial({ color: 0xffffff }),
                light_glow: new THREE.MeshBasicMaterial({ color: 0xfef08a }),
                asphalt: new THREE.MeshBasicMaterial({ color: 0x64748b }),
                paint_white: new THREE.MeshBasicMaterial({ color: 0xffffff }),
                paint_yellow: new THREE.MeshBasicMaterial({ color: 0xfde047 }),
                paint_blue: new THREE.MeshBasicMaterial({ color: 0x3b82f6 }),
                car_paint_red: new THREE.MeshBasicMaterial({ color: 0xef4444 }),
                car_paint_silver: new THREE.MeshBasicMaterial({ color: 0xe2e8f0 }),
                car_paint_blue: new THREE.MeshBasicMaterial({ color: 0x60a5fa }),
                greenery: new THREE.MeshBasicMaterial({ color: 0x22c55e })"""

if cad_needle in code:
    code = code.replace(cad_needle, cad_replacement)
    print("-> Updated CAD materials.")

nurbs_needle = """                fixture_white: new THREE.MeshStandardMaterial({ color: 0xf0efe8, roughness: 0.4, metalness: 0.1 }),
                light_glow: new THREE.MeshBasicMaterial({ color: 0xfff8db })"""

nurbs_replacement = """                fixture_white: new THREE.MeshStandardMaterial({ color: 0xf0efe8, roughness: 0.4, metalness: 0.1 }),
                light_glow: new THREE.MeshBasicMaterial({ color: 0xfff8db }),
                asphalt: new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.6, metalness: 0.1 }),
                paint_white: new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.4, metalness: 0.1 }),
                paint_yellow: new THREE.MeshStandardMaterial({ color: 0xfcd34d, roughness: 0.4, metalness: 0.1 }),
                paint_blue: new THREE.MeshStandardMaterial({ color: 0x93c5fd, roughness: 0.4, metalness: 0.1 }),
                car_paint_red: new THREE.MeshStandardMaterial({ color: 0xfca5a5, roughness: 0.3, metalness: 0.3 }),
                car_paint_silver: new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.3, metalness: 0.4 }),
                car_paint_blue: new THREE.MeshStandardMaterial({ color: 0xbfdbfe, roughness: 0.3, metalness: 0.3 }),
                greenery: new THREE.MeshStandardMaterial({ color: 0x86efac, roughness: 0.5, metalness: 0.05 })"""

if nurbs_needle in code:
    code = code.replace(nurbs_needle, nurbs_replacement)
    print("-> Updated NURBS materials.")

xray_needle = """                fixture_white: new THREE.MeshPhysicalMaterial({ color: 0x7dd3fc, transparent: true, opacity: 0.3, roughness: 0.1 }),
                light_glow: new THREE.MeshBasicMaterial({ color: 0xfef08a, transparent: true, opacity: 0.85 })"""

xray_replacement = """                fixture_white: new THREE.MeshPhysicalMaterial({ color: 0x7dd3fc, transparent: true, opacity: 0.3, roughness: 0.1 }),
                light_glow: new THREE.MeshBasicMaterial({ color: 0xfef08a, transparent: true, opacity: 0.85 }),
                asphalt: new THREE.MeshPhysicalMaterial({ color: 0x0284c7, transparent: true, opacity: 0.25, roughness: 0.1 }),
                paint_white: new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: 0.4, roughness: 0.1 }),
                paint_yellow: new THREE.MeshPhysicalMaterial({ color: 0xfacc15, transparent: true, opacity: 0.4, roughness: 0.1 }),
                paint_blue: new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.4, roughness: 0.1 }),
                car_paint_red: new THREE.MeshPhysicalMaterial({ color: 0xf87171, transparent: true, opacity: 0.45, roughness: 0.1 }),
                car_paint_silver: new THREE.MeshPhysicalMaterial({ color: 0xe2e8f0, transparent: true, opacity: 0.45, roughness: 0.1 }),
                car_paint_blue: new THREE.MeshPhysicalMaterial({ color: 0x60a5fa, transparent: true, opacity: 0.45, roughness: 0.1 }),
                greenery: new THREE.MeshPhysicalMaterial({ color: 0x4ade80, transparent: true, opacity: 0.3, roughness: 0.1 })"""

if xray_needle in code:
    code = code.replace(xray_needle, xray_replacement)
    print("-> Updated X-Ray materials.")

blueprint_needle = """                fixture_white: new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.7 }),
                light_glow: new THREE.MeshBasicMaterial({ color: 0x38bdf8 })"""

blueprint_replacement = """                fixture_white: new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.7 }),
                light_glow: new THREE.MeshBasicMaterial({ color: 0x38bdf8 }),
                asphalt: new THREE.MeshBasicMaterial({ color: 0x0f2b5c, transparent: true, opacity: 0.6 }),
                paint_white: new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.8 }),
                paint_yellow: new THREE.MeshBasicMaterial({ color: 0xfef08a, transparent: true, opacity: 0.8 }),
                paint_blue: new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.8 }),
                car_paint_red: new THREE.MeshBasicMaterial({ color: 0x225aa8, transparent: true, opacity: 0.7 }),
                car_paint_silver: new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.7 }),
                car_paint_blue: new THREE.MeshBasicMaterial({ color: 0x1d4ed8, transparent: true, opacity: 0.7 }),
                greenery: new THREE.MeshBasicMaterial({ color: 0x14532d, transparent: true, opacity: 0.6 })"""

if blueprint_needle in code:
    code = code.replace(blueprint_needle, blueprint_replacement)
    print("-> Updated Blueprint materials.")

# --------------------------------------------------------------------------
# 4. ADD groupSite AND INTEGRATE SITE / PARKING TOGGLE
# --------------------------------------------------------------------------
groups_needle = """        // Building Component Groups
        const groupGF = new THREE.Group();
        const group2F = new THREE.Group();
        const groupRoof = new THREE.Group();
        const groupDims = new THREE.Group();

        scene.add(groupGF);
        scene.add(group2F);
        scene.add(groupRoof);
        scene.add(groupDims);"""

groups_replacement = """        // Building Component Groups
        const groupSite = new THREE.Group();
        const groupGF = new THREE.Group();
        const group2F = new THREE.Group();
        const groupRoof = new THREE.Group();
        const groupDims = new THREE.Group();

        scene.add(groupSite);
        scene.add(groupGF);
        scene.add(group2F);
        scene.add(groupRoof);
        scene.add(groupDims);"""

if groups_needle in code:
    code = code.replace(groups_needle, groups_replacement)
    print("-> Added groupSite definition.")

boxes_layer_needle = """            if (b.layer === '3D-ROOF') {
                groupRoof.add(mesh);
            } else if (b.z >= 3.7) {
                group2F.add(mesh);
            } else {
                groupGF.add(mesh);
            }"""

boxes_layer_replacement = """            if (b.layer === '3D-SITE' || b.layer === '3D-VEHICLES') {
                groupSite.add(mesh);
            } else if (b.layer === '3D-ROOF') {
                groupRoof.add(mesh);
            } else if (b.z >= 3.7) {
                group2F.add(mesh);
            } else {
                groupGF.add(mesh);
            }"""

if boxes_layer_needle in code:
    code = code.replace(boxes_layer_needle, boxes_layer_replacement)
    print("-> Partitioned boxes into groupSite.")

cylinders_layer_needle = """            if (c.layer === '3D-ROOF') {
                groupRoof.add(mesh);
            } else if (c.z >= 3.7) {
                group2F.add(mesh);
            } else {
                groupGF.add(mesh);
            }"""

cylinders_layer_replacement = """            if (c.layer === '3D-SITE' || c.layer === '3D-VEHICLES') {
                groupSite.add(mesh);
            } else if (c.layer === '3D-ROOF') {
                groupRoof.add(mesh);
            } else if (c.z >= 3.7) {
                group2F.add(mesh);
            } else {
                groupGF.add(mesh);
            }"""

if cylinders_layer_needle in code:
    code = code.replace(cylinders_layer_needle, cylinders_layer_replacement)
    print("-> Partitioned cylinders into groupSite.")

# --------------------------------------------------------------------------
# 5. EXPAND SUNLIGHT SHADOW BOUNDS TO COVER THE ENTIRE PROPERTY & HIGHWAY
# --------------------------------------------------------------------------
shadow_needle = """        sunLight.shadow.camera.left = -22;
        sunLight.shadow.camera.right = 22;
        sunLight.shadow.camera.top = 22;
        sunLight.shadow.camera.bottom = -22;"""

shadow_replacement = """        sunLight.shadow.camera.near = 0.5;
        sunLight.shadow.camera.far = 140;
        sunLight.shadow.camera.left = -32;
        sunLight.shadow.camera.right = 32;
        sunLight.shadow.camera.top = 35;
        sunLight.shadow.camera.bottom = -35;"""

if shadow_needle in code:
    code = code.replace(shadow_needle, shadow_replacement)
    print("-> Expanded Directional Sunlight shadow frustum.")

# --------------------------------------------------------------------------
# 6. UPDATE CAMERA PRESET BUTTONS AND TOGGLE LIST IN HTML CONTROL PANEL
# --------------------------------------------------------------------------
cam_btn_needle = """        <!-- Camera Presets -->
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
        </div>"""

cam_btn_replacement = """        <!-- Camera Presets -->
        <div class="feature-card">
            <div class="panel-section-title">
                <span>Camera Presets</span>
            </div>
            <div class="btn-grid-2">
                <button class="btn active" id="cam-parking" onclick="setCamera('parking')">Parking &amp; Facade</button>
                <button class="btn" id="cam-iso" onclick="setCamera('iso')">North-West Iso</button>
                <button class="btn" id="cam-pwd" onclick="setCamera('pwd')">PWD Accessible Bay</button>
                <button class="btn" id="cam-bikes" onclick="setCamera('bikes')">Bicycle &amp; Moto Station</button>
                <button class="btn" id="cam-front" onclick="setCamera('front')">North Entrance</button>
                <button class="btn" id="cam-balcony" onclick="setCamera('balcony')">Balcony &amp; Pergola</button>
                <button class="btn" id="cam-interior" onclick="setCamera('interior')">Interior Barista Bar</button>
                <button class="btn" id="cam-top" onclick="setCamera('top')">Top Site Plan</button>
            </div>
        </div>"""

if cam_btn_needle in code:
    code = code.replace(cam_btn_needle, cam_btn_replacement)
    print("-> Updated Camera Presets UI Grid.")

# Building Elements Toggle for Parking
toggles_needle = """        <!-- Building Elements Toggles -->
        <div class="feature-card">
            <div class="panel-section-title">
                <span>Building Elements</span>
            </div>
            <div class="toggle-list">
                <label class="toggle-item">
                    <span>Roof Slab & Parapet</span>
                    <input type="checkbox" id="chk-roof" checked onchange="toggleLayer('3D-ROOF', this.checked)">
                </label>"""

toggles_replacement = """        <!-- Building Elements Toggles -->
        <div class="feature-card">
            <div class="panel-section-title">
                <span>Building Elements</span>
            </div>
            <div class="toggle-list">
                <label class="toggle-item">
                    <span style="font-weight: 700; color: #60a5fa;">Dedicated Parking &amp; Vehicles</span>
                    <input type="checkbox" id="chk-site" checked onchange="toggleSite(this.checked)">
                </label>
                <label class="toggle-item">
                    <span>Roof Slab & Parapet</span>
                    <input type="checkbox" id="chk-roof" checked onchange="toggleLayer('3D-ROOF', this.checked)">
                </label>"""

if toggles_needle in code:
    code = code.replace(toggles_needle, toggles_replacement)
    print("-> Added Parking & Vehicles toggle to Building Elements.")

# --------------------------------------------------------------------------
# 7. UPDATE JS toggleSite AND setCamera LOGIC
# --------------------------------------------------------------------------
toggle_func_needle = """        function toggleFloor(floorNum, visible) {
            if (floorNum === 1) groupGF.visible = visible;
            if (floorNum === 2) group2F.visible = visible;
        }"""

toggle_func_replacement = """        function toggleSite(visible) {
            groupSite.visible = visible;
        }

        function toggleFloor(floorNum, visible) {
            if (floorNum === 1) groupGF.visible = visible;
            if (floorNum === 2) group2F.visible = visible;
        }"""

if toggle_func_needle in code:
    code = code.replace(toggle_func_needle, toggle_func_replacement)
    print("-> Added toggleSite function in JavaScript.")

set_cam_needle = """        // CAMERA PRESETS
        function setCamera(preset) {
            document.querySelectorAll('.btn-grid-2 .btn').forEach(b => {
                if (b.id && b.id.startsWith('cam-')) b.classList.remove('active');
            });
            const btn = document.getElementById('cam-' + preset);
            if (btn) btn.classList.add('active');

            if (preset === 'iso') {
                camera.position.set(-14, 16, -20);
                controls.target.set(5.0, 3.5, -6.0);
            } else if (preset === 'front') {
                camera.position.set(5.0, 3.8, -24.0);
                controls.target.set(5.0, 3.5, -6.0);
            } else if (preset === 'balcony') {
                camera.position.set(5.0, 7.0, -18.0);
                controls.target.set(5.0, 4.5, -11.0);
            } else if (preset === 'top') {
                camera.position.set(5.0, 26.0, -5.0);
                controls.target.set(5.0, 0.0, -5.0);
            }
            controls.update();
        }

        setCamera('iso');"""

set_cam_replacement = """        // CAMERA PRESETS
        function setCamera(preset) {
            document.querySelectorAll('.btn-grid-2 .btn').forEach(b => {
                if (b.id && b.id.startsWith('cam-')) b.classList.remove('active');
            });
            const btn = document.getElementById('cam-' + preset);
            if (btn) btn.classList.add('active');

            if (preset === 'parking') {
                camera.position.set(5.0, 11.0, -33.0);
                controls.target.set(5.0, 2.5, -13.0);
            } else if (preset === 'iso') {
                camera.position.set(-16.0, 15.0, -28.0);
                controls.target.set(5.0, 2.5, -12.0);
            } else if (preset === 'pwd') {
                camera.position.set(12.5, 4.0, -26.0);
                controls.target.set(9.2, 0.8, -22.5);
            } else if (preset === 'bikes') {
                camera.position.set(-5.5, 4.0, -25.0);
                controls.target.set(-1.0, 1.5, -20.0);
            } else if (preset === 'front') {
                camera.position.set(3.5, 2.4, -16.0);
                controls.target.set(3.5, 2.0, -10.0);
            } else if (preset === 'balcony') {
                camera.position.set(5.0, 7.5, -18.0);
                controls.target.set(5.0, 5.0, -11.0);
            } else if (preset === 'interior') {
                camera.position.set(5.5, 2.2, -4.0);
                controls.target.set(2.5, 1.4, -5.5);
            } else if (preset === 'top') {
                camera.position.set(5.0, 36.0, -17.0);
                controls.target.set(5.0, 0.0, -17.0);
            }
            controls.update();
        }

        setCamera('parking');"""

if set_cam_needle in code:
    code = code.replace(set_cam_needle, set_cam_replacement)
    print("-> Updated setCamera function with parking, pwd, bikes, interior presets & default set to 'parking'.")

# Initial camera position and controls target
cam_init_needle = """        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.target.set(5.0, 3.5, -6.0);"""

cam_init_replacement = """        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.target.set(5.0, 2.5, -13.0);"""

if cam_init_needle in code:
    code = code.replace(cam_init_needle, cam_init_replacement)
    print("-> Updated initial controls target to center of property.")

# Save modified generator script
with open("generate_coffee_shop_3d.py", "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS: generate_coffee_shop_3d.py updated with all revisions.")
