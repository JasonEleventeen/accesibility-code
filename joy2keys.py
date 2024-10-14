import pygame
import time

KEY_REPEAT = 0.7
JS_THRESH = 0.5

KEY_MAP = {
    "axis0+": "RIGHT",
    "axis0-": "LEFT",
    "axis1-": "UP",
    "axis1+": "DOWN",
    "button0": "SELECT",
    "button1": "ESCAPE"
}

def get_key_code(code):
    return KEY_MAP.get(code, code)

# Initialize Pygame and joystick module
pygame.init()
pygame.joystick.init()

def get_joystick_state(joystick):
    pygame.event.pump()  # Process event queue
    states = {f'button{i}': joystick.get_button(i) for i in range(joystick.get_numbuttons())}
    states.update({f"axis{i}": joystick.get_axis(i) for i in range(2)})
    return states

state = {}
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

while pygame.joystick.get_count() > 0:

    event_state = get_joystick_state(joystick)

    for key, value in event_state.items():
        if abs(value) < 0.01:
            continue

        if key not in state:
            state[key] = {"time": time.time() - KEY_REPEAT, "value": value}

        state[key]["value"] = value

    # merge the state
    state = {key: val for key, val in state.items() if key in event_state and abs(event_state[key]) >= 0.01}

    for key, val in state.items():
        if time.time() - val["time"] >= KEY_REPEAT:
            key_code = get_key_code(key)
            value = val["value"]

            if key.startswith("axis"):
                if abs(value) >= JS_THRESH:
                    key_code = get_key_code(f"{key}{'+' if value > 0 else '-'}")
                else:
                    continue

            print(key, key_code)
            state[key]["time"] = time.time()


    time.sleep(0.01)

pygame.quit()
