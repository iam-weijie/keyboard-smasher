import threading
import Quartz
from AppKit import (
    NSApplication, NSWindow, NSBackingStoreBuffered, NSMakeRect,
    NSWindowStyleMaskBorderless, NSFloatingWindowLevel, NSColor, NSTextField,
    NSFont
)

total_key_presses = 0
reset_timer = None
INACTIVITY_TIMEOUT = 2

# Global UI references
window_ref = None
count_label_ref = None
outline_count_label_ref = None  # Outline for number


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
    global total_key_presses, reset_timer, window_ref, count_label_ref, outline_count_label_ref

    if event_type == Quartz.kCGEventKeyDown:
        total_key_presses += 1

        if total_key_presses >= 2:
            if window_ref.alphaValue() < 0.8:
                window_ref.setAlphaValue_(0.8)

            # Update both main count label and outline label
            if count_label_ref:
                count_label_ref.setStringValue_(str(total_key_presses))
            if outline_count_label_ref:
                outline_count_label_ref.setStringValue_(str(total_key_presses))

            flash_window(window_ref)

            if reset_timer is not None:
                reset_timer.cancel()
            reset_timer = threading.Timer(INACTIVITY_TIMEOUT, reset_count)
            reset_timer.start()

    return event


def create_window():
    global window_ref, count_label_ref, outline_count_label_ref

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

    # Colors
    pink_color_hits = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.71, 0.0, 0.196, 1.0)  # #b50032
    pink_color_number = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.91, 0.49, 0.64, 1.0)  # #e781a3

    # Outline number label (slightly bigger)
    outline_count_label = NSTextField.alloc().initWithFrame_(NSMakeRect(0, 12, 130, 43))
    outline_count_label.setStringValue_("0")
    outline_count_label.setBezeled_(False)
    outline_count_label.setDrawsBackground_(False)
    outline_count_label.setEditable_(False)
    outline_count_label.setSelectable_(False)
    outline_count_label.setFont_(NSFont.boldSystemFontOfSize_(43))  # Slightly bigger for outline
    outline_count_label.setTextColor_(pink_color_number)
    outline_count_label.setAlignment_(2)

    # Main count label (on top)
    count_label = NSTextField.alloc().initWithFrame_(NSMakeRect(0, 12, 130, 40))
    count_label.setStringValue_("0")
    count_label.setBezeled_(False)
    count_label.setDrawsBackground_(False)
    count_label.setEditable_(False)
    count_label.setSelectable_(False)
    count_label.setFont_(NSFont.boldSystemFontOfSize_(40))
    count_label.setTextColor_(pink_color_hits)
    count_label.setAlignment_(2)

    # Outline "HITS" label (slightly bigger and bold)
    outline_label = NSTextField.alloc().initWithFrame_(NSMakeRect(128, 0, 110, 32))
    outline_label.setStringValue_("HITS")
    outline_label.setBezeled_(False)
    outline_label.setDrawsBackground_(False)
    outline_label.setEditable_(False)
    outline_label.setSelectable_(False)
    outline_label.setFont_(NSFont.boldSystemFontOfSize_(16))
    outline_label.setTextColor_(pink_color_hits)
    outline_label.setAlignment_(0)

    # Main "HITS" label (on top)
    hits_label = NSTextField.alloc().initWithFrame_(NSMakeRect(130, 0, 100, 30))
    hits_label.setStringValue_("HITS")
    hits_label.setBezeled_(False)
    hits_label.setDrawsBackground_(False)
    hits_label.setEditable_(False)
    hits_label.setSelectable_(False)
    hits_label.setFont_(NSFont.systemFontOfSize_(16))
    hits_label.setTextColor_(NSColor.whiteColor())
    hits_label.setAlignment_(0)

    # Add subviews in order: outline first, then main labels on top
    window.contentView().addSubview_(outline_count_label)
    window.contentView().addSubview_(count_label)
    window.contentView().addSubview_(outline_label)
    window.contentView().addSubview_(hits_label)
    window.orderFrontRegardless()

    window_ref = window
    count_label_ref = count_label
    outline_count_label_ref = outline_count_label

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
        print("Game Over")


if __name__ == '__main__':
    main()
