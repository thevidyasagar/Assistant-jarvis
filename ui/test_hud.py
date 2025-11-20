import time
from ui.hud import JarvisHUD

hud = JarvisHUD()
hud.start(blocking=False)

hud.show_listening()
time.sleep(1)

hud.show_thinking()
time.sleep(1)

hud.show_speaking("Done.")
time.sleep(2)

hud.show_ready()

# Keep window alive
while True:
    time.sleep(1)
