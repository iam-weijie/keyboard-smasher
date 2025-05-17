import Quartz
from AppKit import NSApp, NSApplication, NSWindow, NSBackingStoreBuffered, NSView, NSTextView, NSMakeRect, NSBorderlessWindowMask, NSTitledWindowMask
from AppKit import NSWindowStyleMaskBorderless, NSWindowStyleMaskTitled, NSFloatingWindowLevel
from AppKit import NSColor, NSTextField, NSFont
from Foundation import NSObject, NSAutoreleasePool

total_key_presses = 0

# Global reference to update label
label_ref = None

def callback(proxy, event_type, event, refcon):
    global label_ref, total_key_presses
    if event_type == Quartz.kCGEventKeyDown:
        keycode = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)
        total_key_presses += 1

        if label_ref:
            text = f"{total_key_presses} HITS"
            label_ref.setStringValue_(text)
    return event

def create_window():
    global label_ref

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
    return app

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
