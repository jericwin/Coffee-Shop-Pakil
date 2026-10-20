import re
import os
import shutil

print("Reading index.html to apply joystick and remove emojis...")
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove emojis
emoji_replacements = [
    ("<span>🏛️</span> 3D Model Mode", "3D Model Mode"),
    ("<span>🚶</span> Customer Walk Mode", "Customer Walk Mode"),
    ("🚪 Entrance", "Entrance"),
    ("☕ Barista Bar", "Barista Bar"),
    ("🚻 CR (Restroom)", "CR (Restroom)"),
    ("🪜 Umakyat sa 2F", "Umakyat sa 2F"),
    ("🛋️ Umupo sa 2F Sofa", "Umupo sa 2F Sofa"),
    ("🌿 Outdoor Balcony", "Outdoor Balcony"),
    ("🪑 Umupo sa Table", "Umupo sa Table"),
    ("🚻 Pumunta sa CR", "Pumunta sa CR"),
    ("🪜 Umakyat sa 2F", "Umakyat sa 2F"),
    ("🛋️ Umupo sa Sofa", "Umupo sa Sofa"),
    ("🌿 Balcony", "Balcony"),
    ('<span id="sit-icon">🪑</span> ', ''),
    ('<span id="cam-view-icon">🎥</span> ', ''),
    ("document.getElementById('sit-icon').textContent = '🧍';", "// sit icon removed"),
    ("document.getElementById('sit-icon').textContent = '🪑';", "// sit icon removed"),
    ("document.getElementById('cam-view-icon').textContent = (walkCameraView === 'third') ? '🎥' : '👁️';", "// cam icon removed")
]

for old, new in emoji_replacements:
    content = content.replace(old, new)

# 2. Replace .dpad-container CSS with Joystick CSS
old_dpad_css = """        /* Bottom Floating Virtual D-Pad (Touch & Click) */
        .dpad-container {
            position: absolute;
            bottom: 28px;
            left: 28px;
            width: 140px;
            height: 140px;
            z-index: 25;
            display: none;
            pointer-events: auto;
        }
        .dpad-btn {
            position: absolute;
            width: 44px;
            height: 44px;
            background: linear-gradient(135deg, rgba(30, 20, 15, 0.92) 0%, rgba(45, 30, 22, 0.88) 100%);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 12px;
            color: #ffffff;
            font-size: 16px;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 8px 18px rgba(0, 0, 0, 0.35);
            user-select: none;
            -webkit-user-select: none;
            touch-action: none;
        }
        .dpad-btn:active {
            background: #d97706;
            transform: scale(0.92);
        }
        .dpad-up    { top: 0; left: 48px; }
        .dpad-down  { bottom: 0; left: 48px; }
        .dpad-left  { top: 48px; left: 0; }
        .dpad-right { top: 48px; right: 0; }"""

new_joystick_css = """        /* Mobile & Phone Touch Virtual Analog Joystick */
        .joystick-container {
            position: absolute;
            bottom: 24px;
            left: 24px;
            width: 130px;
            height: 150px;
            z-index: 25;
            display: none;
            flex-direction: column;
            align-items: center;
            touch-action: none;
            user-select: none;
            -webkit-user-select: none;
            pointer-events: auto;
        }
        .joystick-base {
            position: relative;
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(32, 22, 16, 0.90) 0%, rgba(18, 12, 9, 0.97) 100%);
            border: 2px solid rgba(245, 158, 11, 0.5);
            box-shadow: 0 10px 26px rgba(0, 0, 0, 0.45), inset 0 2px 8px rgba(255, 255, 255, 0.12);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: grab;
        }
        .joystick-base:active {
            cursor: grabbing;
        }
        .joystick-center-marker {
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: rgba(245, 158, 11, 0.25);
            border: 1px dashed rgba(245, 158, 11, 0.6);
            pointer-events: none;
        }
        .joystick-stick {
            position: absolute;
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: radial-gradient(circle at 35% 35%, #fbbf24 0%, #d97706 60%, #92400e 100%);
            border: 2.5px solid #ffffff;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45), 0 0 14px rgba(245, 158, 11, 0.6);
            top: 36px;
            left: 36px;
            pointer-events: none;
            transform: translate(0px, 0px);
            transition: transform 0.08s ease-out;
        }
        .joystick-label {
            font-size: 9.5px;
            font-weight: 700;
            color: #fbbf24;
            letter-spacing: 0.8px;
            margin-top: 6px;
            pointer-events: none;
            text-shadow: 0 2px 6px rgba(0, 0, 0, 0.8);
        }"""

if old_dpad_css in content:
    content = content.replace(old_dpad_css, new_joystick_css)
else:
    print("Warning: old_dpad_css not matched exactly, replacing by regex")
    content = re.sub(r'/\* Bottom Floating Virtual D-Pad .*?\.dpad-right \{ top: 48px; right: 0; \}', new_joystick_css, content, flags=re.DOTALL)

# 3. Replace D-pad HTML with Joystick HTML
old_dpad_html = """    <!-- Mobile / On-screen Virtual D-Pad -->
    <div class="dpad-container" id="dpad-container">
        <button class="dpad-btn dpad-up" id="dpad-up">▲</button>
        <button class="dpad-btn dpad-left" id="dpad-left">◀</button>
        <button class="dpad-btn dpad-down" id="dpad-down">▼</button>
        <button class="dpad-btn dpad-right" id="dpad-right">▶</button>
    </div>"""

new_joystick_html = """    <!-- Mobile & Touch Virtual Analog Joystick for Phone -->
    <div class="joystick-container" id="joystick-container">
        <div class="joystick-base" id="joystick-base">
            <div class="joystick-center-marker"></div>
            <div class="joystick-stick" id="joystick-stick"></div>
        </div>
        <div class="joystick-label">TOUCH JOYSTICK</div>
    </div>"""

content = content.replace(old_dpad_html, new_joystick_html)

# 4. Replace setDPad and setupDPad in JavaScript with Joystick logic
old_dpad_js = """        function setDPad(dir, active) {
            if (dir === 'up') keysPressed['KeyW'] = active;
            if (dir === 'down') keysPressed['KeyS'] = active;
            if (dir === 'left') keysPressed['KeyA'] = active;
            if (dir === 'right') keysPressed['KeyD'] = active;
        }

        // D-Pad Touch Listeners
        function setupDPad() {
            const binds = [
                ['dpad-up', 'up'],
                ['dpad-down', 'down'],
                ['dpad-left', 'left'],
                ['dpad-right', 'right']
            ];
            binds.forEach(([id, dir]) => {
                const el = document.getElementById(id);
                if (el) {
                    const down = (e) => { e.preventDefault(); setDPad(dir, true); };
                    const up = (e) => { e.preventDefault(); setDPad(dir, false); };
                    el.addEventListener('mousedown', down);
                    el.addEventListener('mouseup', up);
                    el.addEventListener('mouseleave', up);
                    el.addEventListener('touchstart', down);
                    el.addEventListener('touchend', up);
                }
            });
        }
        setupDPad();"""

new_joystick_js = """        // Virtual Analog Joystick Controller for Mobile / Phone & Desktop
        let joystickActive = false;
        let joystickInput = { x: 0, y: 0 };
        const joystickBase = document.getElementById('joystick-base');
        const joystickStick = document.getElementById('joystick-stick');
        const maxJoystickDist = 36;

        function updateJoystickFromPos(clientX, clientY) {
            const rect = joystickBase.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;

            const dx = clientX - centerX;
            const dy = clientY - centerY;
            const dist = Math.hypot(dx, dy);
            const clampedDist = Math.min(dist, maxJoystickDist);
            const angle = Math.atan2(dy, dx);

            const stickX = Math.cos(angle) * clampedDist;
            const stickY = Math.sin(angle) * clampedDist;

            joystickStick.style.transform = `translate(${stickX}px, ${stickY}px)`;
            joystickStick.style.transition = 'none';

            // Normalized inputs:
            joystickInput.x = stickX / maxJoystickDist; // -1 (left) to +1 (right)
            joystickInput.y = stickY / maxJoystickDist; // -1 (up) to +1 (down)
        }

        function resetJoystick() {
            joystickActive = false;
            joystickInput.x = 0;
            joystickInput.y = 0;
            joystickStick.style.transition = 'transform 0.16s cubic-bezier(0.16, 1, 0.3, 1)';
            joystickStick.style.transform = 'translate(0px, 0px)';
        }

        if (joystickBase) {
            joystickBase.addEventListener('mousedown', (e) => {
                e.preventDefault();
                joystickActive = true;
                updateJoystickFromPos(e.clientX, e.clientY);
            });

            window.addEventListener('mousemove', (e) => {
                if (joystickActive) {
                    updateJoystickFromPos(e.clientX, e.clientY);
                }
            });

            window.addEventListener('mouseup', () => {
                if (joystickActive) resetJoystick();
            });

            // Touch support for phones and tablets
            joystickBase.addEventListener('touchstart', (e) => {
                e.preventDefault();
                joystickActive = true;
                const touch = e.targetTouches[0];
                updateJoystickFromPos(touch.clientX, touch.clientY);
            }, { passive: false });

            window.addEventListener('touchmove', (e) => {
                if (!joystickActive) return;
                for (let i = 0; i < e.touches.length; i++) {
                    const touch = e.touches[i];
                    const rect = joystickBase.getBoundingClientRect();
                    if (Math.hypot(touch.clientX - (rect.left + rect.width / 2), touch.clientY - (rect.top + rect.height / 2)) < 110) {
                        updateJoystickFromPos(touch.clientX, touch.clientY);
                        break;
                    }
                }
            }, { passive: false });

            window.addEventListener('touchend', () => {
                if (joystickActive) resetJoystick();
            });
            window.addEventListener('touchcancel', () => {
                if (joystickActive) resetJoystick();
            });
        }"""

content = content.replace(old_dpad_js, new_joystick_js)

# 5. In setViewerMode, update display of joystick
content = content.replace(
    "document.getElementById('dpad-container').style.display = isWalk ? 'block' : 'none';",
    "document.getElementById('joystick-container').style.display = isWalk ? 'flex' : 'none';"
)

# 6. In animate(), add joystick analog input blending
old_move_code = """                    let moveForward = 0;
                    let turnAngle = 0;

                    if (keysPressed['KeyW'] || keysPressed['ArrowUp']) moveForward += 1;
                    if (keysPressed['KeyS'] || keysPressed['ArrowDown']) moveForward -= 1;
                    if (keysPressed['KeyA'] || keysPressed['ArrowLeft']) turnAngle += 1;
                    if (keysPressed['KeyD'] || keysPressed['ArrowRight']) turnAngle -= 1;

                    if (turnAngle !== 0) {
                        avatar.root.rotation.y += turnAngle * 2.6 * delta;
                    }

                    if (moveForward !== 0) {
                        if (isSitting) standUp();
                        isWalking = true;
                        const speed = (keysPressed['ShiftLeft'] || keysPressed['ShiftRight']) ? 4.2 : 2.6;
                        const angle = avatar.root.rotation.y;
                        const dx = Math.sin(angle) * moveForward * speed * delta;
                        const dz = Math.cos(angle) * moveForward * speed * delta;

                        // Bounds checking
                        const nextX = Math.max(0.4, Math.min(9.6, avatar.root.position.x + dx));
                        const nextZ = Math.max(-12.4, Math.min(0.2, avatar.root.position.z + dz));

                        avatar.root.position.x = nextX;
                        avatar.root.position.z = nextZ;
                        avatar.root.position.y = getElevationAt(avatar.root.position.x, avatar.root.position.z, avatar.root.position.y);
                    }"""

new_move_code = """                    let moveForward = 0;
                    let turnAngle = 0;

                    if (keysPressed['KeyW'] || keysPressed['ArrowUp']) moveForward += 1;
                    if (keysPressed['KeyS'] || keysPressed['ArrowDown']) moveForward -= 1;
                    if (keysPressed['KeyA'] || keysPressed['ArrowLeft']) turnAngle += 1;
                    if (keysPressed['KeyD'] || keysPressed['ArrowRight']) turnAngle -= 1;

                    // Blend with Analog Touch Joystick input (for Phone/Mobile)
                    if (joystickActive) {
                        moveForward -= joystickInput.y; // Pushing stick up moves forward
                        turnAngle -= joystickInput.x;   // Pushing stick left/right turns
                    }

                    if (turnAngle !== 0) {
                        avatar.root.rotation.y += turnAngle * 2.8 * delta;
                    }

                    if (Math.abs(moveForward) > 0.05) {
                        if (isSitting) standUp();
                        isWalking = true;
                        const baseSpeed = (keysPressed['ShiftLeft'] || keysPressed['ShiftRight']) ? 4.2 : 2.7;
                        const speed = baseSpeed * Math.min(1.0, Math.abs(moveForward));
                        const angle = avatar.root.rotation.y;
                        const dirSign = Math.sign(moveForward);

                        const dx = Math.sin(angle) * dirSign * speed * delta;
                        const dz = Math.cos(angle) * dirSign * speed * delta;

                        // Bounds checking
                        const nextX = Math.max(0.4, Math.min(9.6, avatar.root.position.x + dx));
                        const nextZ = Math.max(-12.4, Math.min(0.2, avatar.root.position.z + dz));

                        avatar.root.position.x = nextX;
                        avatar.root.position.z = nextZ;
                        avatar.root.position.y = getElevationAt(avatar.root.position.x, avatar.root.position.z, avatar.root.position.y);
                    }"""

content = content.replace(old_move_code, new_move_code)

# Write to index.html and coffee_shop_3d_viewer.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

with open("coffee_shop_3d_viewer.html", "w", encoding="utf-8") as f:
    f.write(content)

print("index.html and coffee_shop_3d_viewer.html successfully updated with Joystick and no emojis.")
