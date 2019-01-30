from threading import Thread
import time
import wx

import popup


def run_manager(main_window):
    print ("Run manager")
    check_rotation = main_window.runPan.rotationCb.Value
    time_delay = main_window.time_between_shots
    degree_rotation = main_window.degree
    num_patterns = len(main_window.pattern)

    number_of_shots = int(main_window.number_of_shots) if not check_rotation else 360 / degree_rotation

    wx.CallAfter(main_window.runPan.btn_single_shot.Disable)

    if not check_rotation:
        degree_rotation = 360 / int(number_of_shots)
    remaining_shots = 360 // degree_rotation
    wx.CallAfter(change_shoot_panel, main_window, num_patterns, remaining_shots)
    main_window.runPan.set_range_progress_bar(remaining_shots + 2)

    for i in range(len(main_window.usb_camera)):

        wx.CallAfter(write_shoot_panel, main_window, "Executing camera " + str(i) + " setup...")

        if main_window.run_status == "Stop":
            wx.CallAfter(write_shoot_panel, main_window, "Stopping program...")
            time.sleep(2)
            main_window.runPan.btn_run.SetLabelText("Run acquisition")
            wx.CallAfter(write_shoot_panel, main_window, "Program Stopped")
            return

    main_window.runPan.increase_progress_bar()
    wx.CallAfter(change_shoot_panel, main_window, num_patterns, remaining_shots)

    for i in range(0, 360, degree_rotation):
        while main_window.run_status == "Pause":
            wx.CallAfter(write_shoot_panel, main_window, "Program Paused")
            time.sleep(1)
            print(main_window.run_status)
            if main_window.run_status == "Stop":
                break
        if main_window.run_status == "Stop":
            wx.CallAfter(write_shoot_panel, main_window, "Stopping program...")
            break
        wx.CallAfter(change_shoot_panel, main_window, num_patterns, remaining_shots)
        if check_rotation:
            main_window.arduinoBoards.rotate_table(i)
            time.sleep(degree_rotation * 5.5 / 360 + 2)
            pos = i

        main_window.arduinoBoards.trigger_camera(0)
        time.sleep(2 if check_rotation else int(time_delay))

        main_window.runPan.increase_progress_bar()
        remaining_shots -= 1

    if check_rotation:
        main_window.arduinoBoards.rotate_table(0)
        # main_window.arduinoBoards.reset_serial(# )

    main_window.runPan.increase_progress_bar()
    wx.CallAfter(write_shoot_panel, main_window, "Done")
    time.sleep(1.5)
    wx.CallAfter(write_shoot_panel, main_window, "Program Stopped")
    main_window.runPan.btn_run.SetLabelText("Run acquisition")
    main_window.run_status = "Stop"
    for i in range(360 / degree_rotation + 2, -1, -1):
        main_window.runPan.decrease_progress_bar()
        time.sleep(0.2)
    wx.CallAfter(main_window.runPan.btn_single_shot.Enable)
    wx.CallAfter(popup.start_shoot_at_dialog, main_window)
    return


def thread_run_manager(main_window):
    print("Start thread run manager")
    if check_devices(main_window):
        Thread(target=run_manager, args=(main_window,)).start()
    else:
        main_window.runPan.btn_run.SetLabelText("Run acquisition")
        main_window.runPan.parent.run_status = "Stop"
    print("Done")
    return


def change_shoot_panel(main_window, num_patterns, index):
    main_window.runPan.txt_status.SetLabel(
        "Remaining shots:  " + str(index) + (("   ( x " + str(num_patterns) + "  panels)")))
    return


def write_shoot_panel(main_window, text):
    main_window.runPan.txt_status.SetLabel(text)
    return


def shoot_at(main_window, degree, pattern=-1, camera=0):
    camera = int(camera)
    degree = int(degree)
    main_window.arduinoBoards.rotate_table(degree)
    time.sleep(degree * 5.5 / 360 + 2)
    if pattern != -1:
        print "Projected " + str(pattern)

        wx.CallAfter(main_window.projector.project_pattern)
        wx.CallAfter(main_window.projector.change_pattern, pattern)
        time.sleep(1.5)
    main_window.arduinoBoards.trigger_camera(camera)
    time.sleep(1)
    main_window.arduinoBoards.rotate_table(0)
    if pattern != -1:
        wx.CallAfter(main_window.projector.project_pattern, False)

    print(len(main_window.usb_camera))
    time.sleep(2)
    if camera == 0:
        for i in range(len(main_window.usb_camera)):
            print 'Usb camera: '
            print main_window.usb_camera

    else:
        print "camera: " + str(camera - 1)
    return


def check_devices(main_window):
    if popup.check_devices_dialog(main_window):
        for i in range(len(main_window.usb_camera)):
            main_window.arduinoBoards.trigger_camera(i + 1)
            time.sleep(1.5)
        main_window.arduinoBoards.rotate_table(20)
        time.sleep(1)
        main_window.arduinoBoards.rotate_table(0)
        if not popup.check_devices_response_dialog(main_window):
            main_window.arduinoBoards.reset_serial(main_window.arduinoBoards.serial_table)
            main_window.arduinoBoards.reset_serial(main_window.arduinoBoards.serial_camera)
            return False
    return True
