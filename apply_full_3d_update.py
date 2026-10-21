#!/usr/bin/env python3
import sys

with open("generate_coffee_shop_3d.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. PBR Palette addition
pbr_old = """                fixture_white: new THREE.MeshStandardMaterial({{
                    map: texMarble,
                    roughness: 0.15,
                    metalness: 0.08
                }}),
                light_glow: new THREE.MeshBasicMaterial({{
                    color: 0xffe29a
                }})
            }},"""

pbr_new = """                fixture_white: new THREE.MeshStandardMaterial({{
                    map: texMarble,
                    roughness: 0.15,
                    metalness: 0.08
                }}),
                light_glow: new THREE.MeshBasicMaterial({{
                    color: 0xffe29a
                }}),
                asphalt: new THREE.MeshStandardMaterial({{
                    map: texAsphalt,
                    roughness: 0.88,
                    metalness: 0.08
                }}),
                paint_white: new THREE.MeshStandardMaterial({{
                    color: 0xffffff,
                    roughness: 0.35,
                    metalness: 0.05
                }}),
                paint_yellow: new THREE.MeshStandardMaterial({{
                    color: 0xf59e0b,
                    roughness: 0.35,
                    metalness: 0.05
                }}),
                paint_blue: new THREE.MeshStandardMaterial({{
                    color: 0x2563eb,
                    roughness: 0.30,
                    metalness: 0.08
                }}),
                car_paint_red: new THREE.MeshStandardMaterial({{
                    color: 0xdc2626,
                    roughness: 0.18,
                    metalness: 0.75
                }}),
                car_paint_silver: new THREE.MeshStandardMaterial({{
                    color: 0xcbd5e1,
                    roughness: 0.20,
                    metalness: 0.85
                }}),
                car_paint_blue: new THREE.MeshStandardMaterial({{
                    color: 0x1d4ed8,
                    roughness: 0.20,
                    metalness: 0.75
                }}),
                greenery: new THREE.MeshStandardMaterial({{
                    color: 0x15803d,
                    roughness: 0.65,
                    metalness: 0.02
                }})
            }},"""

if pbr_old in text:
    text = text.replace(pbr_old, pbr_new)
    print("-> PBR Palette updated.")
else:
    print("WARN: pbr_old not found!")

# 2. CAD Palette addition
cad_old = """                fixture_white: new THREE.MeshBasicMaterial({{ color: 0xffffff }}),
                light_glow: new THREE.MeshBasicMaterial({{ color: 0xfef08a }})
            }},"""

cad_new = """                fixture_white: new THREE.MeshBasicMaterial({{ color: 0xffffff }}),
                light_glow: new THREE.MeshBasicMaterial({{ color: 0xfef08a }}),
                asphalt: new THREE.MeshBasicMaterial({{ color: 0x64748b }}),
                paint_white: new THREE.MeshBasicMaterial({{ color: 0xffffff }}),
                paint_yellow: new THREE.MeshBasicMaterial({{ color: 0xfde047 }}),
                paint_blue: new THREE.MeshBasicMaterial({{ color: 0x3b82f6 }}),
                car_paint_red: new THREE.MeshBasicMaterial({{ color: 0xef4444 }}),
                car_paint_silver: new THREE.MeshBasicMaterial({{ color: 0xe2e8f0 }}),
                car_paint_blue: new THREE.MeshBasicMaterial({{ color: 0x60a5fa }}),
                greenery: new THREE.MeshBasicMaterial({{ color: 0x22c55e }})
            }},"""

if cad_old in text:
    text = text.replace(cad_old, cad_new)
    print("-> CAD Palette updated.")
else:
    print("WARN: cad_old not found!")

# 3. NURBS Palette addition
nurbs_old = """                fixture_white: new THREE.MeshStandardMaterial({{ color: 0xf0efe8, roughness: 0.4, metalness: 0.1 }}),
                light_glow: new THREE.MeshBasicMaterial({{ color: 0xfff8db }})
            }},"""

nurbs_new = """                fixture_white: new THREE.MeshStandardMaterial({{ color: 0xf0efe8, roughness: 0.4, metalness: 0.1 }}),
                light_glow: new THREE.MeshBasicMaterial({{ color: 0xfff8db }}),
                asphalt: new THREE.MeshStandardMaterial({{ color: 0x94a3b8, roughness: 0.6, metalness: 0.1 }}),
                paint_white: new THREE.MeshStandardMaterial({{ color: 0xffffff, roughness: 0.4, metalness: 0.1 }}),
                paint_yellow: new THREE.MeshStandardMaterial({{ color: 0xfcd34d, roughness: 0.4, metalness: 0.1 }}),
                paint_blue: new THREE.MeshStandardMaterial({{ color: 0x93c5fd, roughness: 0.4, metalness: 0.1 }}),
                car_paint_red: new THREE.MeshStandardMaterial({{ color: 0xfca5a5, roughness: 0.3, metalness: 0.3 }}),
                car_paint_silver: new THREE.MeshStandardMaterial({{ color: 0xe2e8f0, roughness: 0.3, metalness: 0.4 }}),
                car_paint_blue: new THREE.MeshStandardMaterial({{ color: 0xbfdbfe, roughness: 0.3, metalness: 0.3 }}),
                greenery: new THREE.MeshStandardMaterial({{ color: 0x86efac, roughness: 0.5, metalness: 0.05 }}),
            }},"""

if nurbs_old in text:
    text = text.replace(nurbs_old, nurbs_new)
    print("-> NURBS Palette updated.")
else:
    print("WARN: nurbs_old not found!")

# 4. X-Ray Palette addition
xray_old = """                fixture_white: new THREE.MeshPhysicalMaterial({{ color: 0x7dd3fc, transparent: true, opacity: 0.3, roughness: 0.1 }}),
                light_glow: new THREE.MeshBasicMaterial({{ color: 0xfef08a, transparent: true, opacity: 0.85 }})
            }},"""

xray_new = """                fixture_white: new THREE.MeshPhysicalMaterial({{ color: 0x7dd3fc, transparent: true, opacity: 0.3, roughness: 0.1 }}),
                light_glow: new THREE.MeshBasicMaterial({{ color: 0xfef08a, transparent: true, opacity: 0.85 }}),
                asphalt: new THREE.MeshPhysicalMaterial({{ color: 0x0284c7, transparent: true, opacity: 0.25, roughness: 0.1 }}),
                paint_white: new THREE.MeshPhysicalMaterial({{ color: 0xffffff, transparent: true, opacity: 0.4, roughness: 0.1 }}),
                paint_yellow: new THREE.MeshPhysicalMaterial({{ color: 0xfacc15, transparent: true, opacity: 0.4, roughness: 0.1 }}),
                paint_blue: new THREE.MeshPhysicalMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.4, roughness: 0.1 }}),
                car_paint_red: new THREE.MeshPhysicalMaterial({{ color: 0xf87171, transparent: true, opacity: 0.45, roughness: 0.1 }}),
                car_paint_silver: new THREE.MeshPhysicalMaterial({{ color: 0xe2e8f0, transparent: true, opacity: 0.45, roughness: 0.1 }}),
                car_paint_blue: new THREE.MeshPhysicalMaterial({{ color: 0x60a5fa, transparent: true, opacity: 0.45, roughness: 0.1 }}),
                greenery: new THREE.MeshPhysicalMaterial({{ color: 0x4ade80, transparent: true, opacity: 0.3, roughness: 0.1 }})
            }},"""

if xray_old in text:
    text = text.replace(xray_old, xray_new)
    print("-> X-Ray Palette updated.")
else:
    print("WARN: xray_old not found!")

# 5. Blueprint Palette addition
blueprint_old = """                fixture_white: new THREE.MeshBasicMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.7 }}),
                light_glow: new THREE.MeshBasicMaterial({{ color: 0x38bdf8 }})
            }}
        }};"""

blueprint_new = """                fixture_white: new THREE.MeshBasicMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.7 }}),
                light_glow: new THREE.MeshBasicMaterial({{ color: 0x38bdf8 }}),
                asphalt: new THREE.MeshBasicMaterial({{ color: 0x0f2b5c, transparent: true, opacity: 0.6 }}),
                paint_white: new THREE.MeshBasicMaterial({{ color: 0xffffff, transparent: true, opacity: 0.8 }}),
                paint_yellow: new THREE.MeshBasicMaterial({{ color: 0xfef08a, transparent: true, opacity: 0.8 }}),
                paint_blue: new THREE.MeshBasicMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.8 }}),
                car_paint_red: new THREE.MeshBasicMaterial({{ color: 0x225aa8, transparent: true, opacity: 0.7 }}),
                car_paint_silver: new THREE.MeshBasicMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.7 }}),
                car_paint_blue: new THREE.MeshBasicMaterial({{ color: 0x1d4ed8, transparent: true, opacity: 0.7 }}),
                greenery: new THREE.MeshBasicMaterial({{ color: 0x14532d, transparent: true, opacity: 0.6 }})
            }}
        }};"""

if blueprint_old in text:
    text = text.replace(blueprint_old, blueprint_new)
    print("-> Blueprint Palette updated.")
else:
    print("WARN: blueprint_old not found!")

# 6. Boxes group routing to groupSite
boxes_old = """            if (b.layer === '3D-ROOF') {{
                groupRoof.add(mesh);
            }} else if (b.z >= 3.7) {{
                group2F.add(mesh);
            }} else {{
                groupGF.add(mesh);
            }}"""

boxes_new = """            if (b.layer === '3D-SITE' || b.layer === '3D-VEHICLES') {{
                groupSite.add(mesh);
            }} else if (b.layer === '3D-ROOF') {{
                groupRoof.add(mesh);
            }} else if (b.z >= 3.7) {{
                group2F.add(mesh);
            }} else {{
                groupGF.add(mesh);
            }}"""

if boxes_old in text:
    text = text.replace(boxes_old, boxes_new)
    print("-> Boxes routed to groupSite.")
else:
    print("WARN: boxes_old not found!")

# 7. Cylinders group routing to groupSite
cyl_old = """            if (c.layer === '3D-ROOF') {{
                groupRoof.add(mesh);
            }} else if (c.z >= 3.7) {{
                group2F.add(mesh);
            }} else {{
                groupGF.add(mesh);
            }}"""

cyl_new = """            if (c.layer === '3D-SITE' || c.layer === '3D-VEHICLES') {{
                groupSite.add(mesh);
            }} else if (c.layer === '3D-ROOF') {{
                groupRoof.add(mesh);
            }} else if (c.z >= 3.7) {{
                group2F.add(mesh);
            }} else {{
                groupGF.add(mesh);
            }}"""

if cyl_old in text:
    text = text.replace(cyl_old, cyl_new)
    print("-> Cylinders routed to groupSite.")
else:
    print("WARN: cyl_old not found!")

# 8. toggleFloor & toggleSite
toggle_old = """        function toggleFloor(floorNum, visible) {{
            if (floorNum === 1) groupGF.visible = visible;
            if (floorNum === 2) group2F.visible = visible;
        }}"""

toggle_new = """        function toggleSite(visible) {{
            groupSite.visible = visible;
        }}

        function toggleFloor(floorNum, visible) {{
            if (floorNum === 1) groupGF.visible = visible;
            if (floorNum === 2) group2F.visible = visible;
        }}"""

if toggle_old in text:
    text = text.replace(toggle_old, toggle_new)
    print("-> toggleSite function added.")
else:
    print("WARN: toggle_old not found!")

# 9. setCamera and default camera
cam_old = """        // CAMERA PRESETS
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

        setCamera('iso');"""

cam_new = """        // CAMERA PRESETS
        function setCamera(preset) {{
            document.querySelectorAll('.btn-grid-2 .btn').forEach(b => {{
                if (b.id && b.id.startsWith('cam-')) b.classList.remove('active');
            }});
            const btn = document.getElementById('cam-' + preset);
            if (btn) btn.classList.add('active');

            if (preset === 'parking') {{
                camera.position.set(5.0, 11.0, -33.0);
                controls.target.set(5.0, 2.5, -13.0);
            }} else if (preset === 'iso') {{
                camera.position.set(-16.0, 15.0, -28.0);
                controls.target.set(5.0, 2.5, -12.0);
            }} else if (preset === 'pwd') {{
                camera.position.set(12.5, 4.0, -26.0);
                controls.target.set(9.2, 0.8, -22.5);
            }} else if (preset === 'bikes') {{
                camera.position.set(-5.5, 4.0, -25.0);
                controls.target.set(-1.0, 1.5, -20.0);
            }} else if (preset === 'front') {{
                camera.position.set(3.5, 2.4, -16.0);
                controls.target.set(3.5, 2.0, -10.0);
            }} else if (preset === 'balcony') {{
                camera.position.set(5.0, 7.5, -18.0);
                controls.target.set(5.0, 5.0, -11.0);
            }} else if (preset === 'interior') {{
                camera.position.set(5.5, 2.2, -4.0);
                controls.target.set(2.5, 1.4, -5.5);
            }} else if (preset === 'top') {{
                camera.position.set(5.0, 36.0, -17.0);
                controls.target.set(5.0, 0.0, -17.0);
            }}
            controls.update();
        }}

        setCamera('parking');"""

if cam_old in text:
    text = text.replace(cam_old, cam_new)
    print("-> setCamera function updated with all 8 presets and set to 'parking' on start.")
else:
    print("WARN: cam_old not found!")

# Write file
with open("generate_coffee_shop_3d.py", "w", encoding="utf-8") as f:
    f.write(text)

print("SUCCESS: generate_coffee_shop_3d.py updated!")
