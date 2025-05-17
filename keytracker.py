import Quartz
import threading
import time
from AppKit import NSApp, NSApplication, NSWindow, NSBackingStoreBuffered, NSView, NSTextView, NSMakeRect, NSBorderlessWindowMask, NSTitledWindowMask, NSWindowStyleMaskBorderless, NSWindowStyleMaskTitled, NSFloatingWindowLevel, NSColor, NSTextField, NSFont
from Foundation import NSObject, NSAutoreleasePool

total_key_presses = 0
reset_timer = None
INACTIVITY_TIMEOUT = 2
window_ref = None

# Global reference to update label
label_ref = None

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
    global label_ref, total_key_presses, reset_timer, window_ref
    
    if event_type == Quartz.kCGEventKeyDown: 
        total_key_presses += 1
        if label_ref:
            label_ref.setStringValue_(f"{total_key_presses} HITS")
        if window_ref:
            flash_window(window_ref)

        # Reset the timer
        if reset_timer is not None:
            reset_timer.cancel()
        reset_timer = threading.Timer(INACTIVITY_TIMEOUT, reset_count)
        reset_timer.start()
        
    return event

def create_window():
    global label_ref, window_ref

    app = NSApplication.sharedApplication()

    # Window size and position
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(20, 600, 250, 50),
        NSWindowStyleMaskBorderless,
        NSBackingStoreBuffered,
        False
    )

    window.setLevel_(NSFloatingWindowLevel)
    window.setOpaque_(False)
    window.setBackgroundColor_(NSColor.clearColor())
    window.setIgnoresMouseEvents_(True)
    window.setAlphaValue_(0.8)

    # Text label
    label = NSTextField.alloc().initWithFrame_(NSMakeRect(10, 10, 230, 30))
    label.setStringValue_("Ready... Go!")
    label.setBezeled_(False)
    label.setDrawsBackground_(False)
    label.setEditable_(False)
    label.setSelectable_(False)
    label.setFont_(NSFont.systemFontOfSize_(18))
    label.setTextColor_(NSColor.whiteColor())

    window.contentView().addSubview_(label)
    window.orderFrontRegardless()

    label_ref = label
    window_ref = window
    return app


def hide_window():
    global window_ref
    if window_ref:
        window_ref.setAlphaValue_(0.0)


def main():
    event_mask = Quartz.CGEventMaskBit(Quartz.kCGEventKeyDown)
    event_tap=Quartz.CGEventTapCreate(
        Quartz.kCGSessionEventTap,
        Quartz.kCGHeadInsertEventTap,
        Quartz.kCGEventTapOptionDefault,
        event_mask,
        callback,
        None
    )
    run_loop_source = Quartz.CFMachPortCreateRunLoopSource(None,event_tap, 0)
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
