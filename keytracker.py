import threading
import time
import Quartz
from AppKit import (
    NSApp, NSApplication, NSWindow, NSBackingStoreBuffered, NSMakeRect,
    NSWindowStyleMaskBorderless, NSFloatingWindowLevel, NSColor, NSTextField,
    NSFont
)
from Foundation import NSObject

total_key_presses = 0
reset_timer = None
INACTIVITY_TIMEOUT = 2

# Global UI references
window_ref = None
count_label_ref = None


def reset_count():
    global total_key_presses
    total_key_presses = 0
    hide_window()


def flash_window(window):
    def fade_out():
        window.setAlphaValue_(0.0)
        threading.Timer(0.05, fade_in).start()

    def fade_in():
        window.setAlphaValue_(0.8)

    fade_out()


def callback(proxy, event_type, event, refcon):
    global total_key_presses, reset_timer, window_ref, count_label_ref

    if event_type == Quartz.kCGEventKeyDown:
        total_key_presses += 1

        if total_key_presses >= 2:
            if window_ref.alphaValue() < 0.8:
                window_ref.setAlphaValue_(0.8)

            # Update label
            if count_label_ref:
                count_label_ref.setStringValue_(str(total_key_presses))
            # Flash effect        
            flash_window(window_ref)
            # Reset the timer
            if reset_timer is not None:
                reset_timer.cancel()
            reset_timer = threading.Timer(INACTIVITY_TIMEOUT, reset_count)
            reset_timer.start()

    return event


def create_window():
    global window_ref, count_label_ref

    app = NSApplication.sharedApplication()

    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(20, 600, 300, 60),
        NSWindowStyleMaskBorderless,
        NSBackingStoreBuffered,
        False
    )
    window.setLevel_(NSFloatingWindowLevel)
    window.setOpaque_(False)
    window.setBackgroundColor_(NSColor.clearColor())
    window.setIgnoresMouseEvents_(True)
    window.setAlphaValue_(0.0)  # Start hidden

    # Combo number
    count_label = NSTextField.alloc().initWithFrame_(NSMakeRect(10, 10, 130, 40))
    count_label.setStringValue_("0")
    count_label.setBezeled_(False)
    count_label.setDrawsBackground_(False)
    count_label.setEditable_(False)
    count_label.setSelectable_(False)
    count_label.setFont_(NSFont.boldSystemFontOfSize_(36))
    count_label.setTextColor_(NSColor.redColor())
    count_label.setAlignment_(2)

    # "HITS" label, shifted right
    hits_label = NSTextField.alloc().initWithFrame_(NSMakeRect(140, 12, 100, 30))
    hits_label.setStringValue_("HITS")
    hits_label.setBezeled_(False)
    hits_label.setDrawsBackground_(False)
    hits_label.setEditable_(False)
    hits_label.setSelectable_(False)
    hits_label.setFont_(NSFont.systemFontOfSize_(20))
    hits_label.setTextColor_(NSColor.whiteColor())
    hits_label.setAlignment_(0)

    window.contentView().addSubview_(count_label)
    window.contentView().addSubview_(hits_label)
    window.orderFrontRegardless()

    window_ref = window
    count_label_ref = count_label

    return app


def hide_window():
    global window_ref
    if window_ref:
        window_ref.setAlphaValue_(0.0)


def main():
    event_mask = Quartz.CGEventMaskBit(Quartz.kCGEventKeyDown)
    event_tap = Quartz.CGEventTapCreate(
        Quartz.kCGSessionEventTap,
        Quartz.kCGHeadInsertEventTap,
        Quartz.kCGEventTapOptionDefault,
        event_mask,
        callback,
        None
    )

    run_loop_source = Quartz.CFMachPortCreateRunLoopSource(None, event_tap, 0)
    Quartz.CFRunLoopAddSource(
        Quartz.CFRunLoopGetCurrent(),
        run_loop_source,
        Quartz.kCFRunLoopDefaultMode
    )

    Quartz.CGEventTapEnable(event_tap, True)
    app = create_window()
    try:
        Quartz.CFRunLoopRun()
    except KeyboardInterrupt:
        print("Exiting.")


if __name__ == '__main__':
    main()
