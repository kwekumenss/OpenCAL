import threading

from opencal.gui import LCDGui
from hardware_controller import HardwareController
from print_controller import PrintController

def main():

    # Pass print_controller to the GUI
    gui = LCDGui()
    hardware = HardwareController()
    printer = PrintController()

    # Start GUI in separate thread
    gui_thread = threading.Thread(target=gui.run, daemon=True)
    gui_thread.start()
    gui_thread.join()

    # Assuming 'selected_option' comes from your rotary encoder logic
    if selected_option == "EJECT_USB":
        handle_safe_eject(printer, hardware)

def handle_safe_eject(print_controller, hardware):
    """Orchestrates the safety checks and unmounting process."""
    lcd = hardware.lcd
    usb = hardware.usb_device
    
    # 1. Update UI
    lcd.clear()
    lcd.write_message("Ejecting USB...", row=1)
    
    # 2. Safety: Stop all hardware processes that might be using the USB
    if print_controller.running:
        # This stops the projector, stepper, and LEDs
        print_controller.stop()
    else:
        # If no print is active, ensure the projector specifically is closed
        # to release any file handles on the MP4
        hardware.projector.stop_video()
    
    # 3. Attempt the system unmount
    # (Requires the safe_eject method we discussed adding to MP4Driver)
    success = usb.safe_eject() 
    
    # 4. Final Feedback
    lcd.clear()
    if success:
        lcd.write_message("Safe to Remove", row=1)
        lcd.write_message("USB Drive", row=2)
    else:
        lcd.write_message("Eject Failed!", row=1)
        lcd.write_message("Drive Busy", row=2)


if __name__ == "__main__":
    main()
