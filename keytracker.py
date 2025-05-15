import Quartz
from collections import defaultdict

key_count = defaultdict(int)

def callback(proxy, event_type, event, refcon):
    if event_type == Quartz.kCGEventKeyDown:
        keycode = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)
        key_count[keycode] += 1
        total = sum(key_count.values())
        print(f"Keycode {keycode} pressed. Total keys pressed: {total}")
    return event

def main():
    # Create an event tap to capture key down events
    event_mask = Quartz.CGEventMaskBit(Quartz.kCGEventKeyDown)
    event_tap = Quartz.CGEventTapCreate(
        Quartz.kCGHIDEventTap,  # tap at the point where HID events enter the system
        Quartz.kCGHeadInsertEventTap,
        Quartz.kCGEventTapOptionDefault,
        event_mask,
        callback,
        None
    )

    if not event_tap:
        print("Failed to create event tap. Must run with accessibility permissions.")
        exit(1)

    # Create a run loop source and add it to the current run loop
    run_loop_source = Quartz.CFMachPortCreateRunLoopSource(None, event_tap, 0)
    Quartz.CFRunLoopAddSource(
        Quartz.CFRunLoopGetCurrent(),
        run_loop_source,
        Quartz.kCFRunLoopCommonModes
    )

    # Enable the event tap
    Quartz.CGEventTapEnable(event_tap, True)

    print("Starting key press listener... Press Ctrl+C to quit.")
    Quartz.CFRunLoopRun()

if __name__ == "__main__":
    main()
