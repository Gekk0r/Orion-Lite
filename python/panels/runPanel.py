import manage.popup as popup
import wx
import manage.task_manager as tsk


class runPanel(wx.Panel):
    def __init__(self, parent, *a, **k):
        wx.Panel.__init__(self, parent, *a, **k)

        self.parent = parent

        # layout init
        self.panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.topSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.botSizer = wx.BoxSizer(wx.HORIZONTAL)

        # label
        self.title = wx.StaticText(self, style=wx.ALIGN_CENTER, label="Execute Settings")

        self.txt_status = wx.StaticText(self, label="Program Stopped", pos=(4, 155))

        # widget
        self.btn_run = wx.Button(self, label="Run acquisition", pos=(4, 105), size=(120, 45))
        self.btn_stop = wx.Button(self, label="Stop", pos=(127, 105), size=(100, 45))
        self.btn_single_shot = wx.Button(self, label="Single Shot", pos=(230, 105), size=(100, 45))

        self.progress_bar = wx.Gauge(self, -1, 100, pos=(4, 175), size=(320, 10), style=wx.GA_SMOOTH & wx.GA_HORIZONTAL)

        # Events
        self.btn_run.Bind(wx.EVT_BUTTON, self.acquisition)
        self.btn_stop.Bind(wx.EVT_BUTTON, self.stop_program)
        self.btn_single_shot.Bind(wx.EVT_BUTTON, self.single_shot)

        self.SetSizer(self.panelSizer)
        self.Fit()

    def increase_progress_bar(self):
        if (self.progress_bar.GetValue() != self.progress_bar.GetRange()):
            self.progress_bar.SetValue(self.progress_bar.GetValue() + 1)
        return

    def decrease_progress_bar(self):
        if (self.progress_bar.GetValue() > 0):
            self.progress_bar.SetValue(self.progress_bar.GetValue() - 1)
        return

    def set_range_progress_bar(self, max):
        self.progress_bar.SetRange(max)
        self.progress_bar.SetValue(0)
        return

    def reset_progress_bar(self):
        self.progress_bar.SetValue(0)
        return

    def acquisition(self, event):
        if self.parent.run_status == "Stop":
            self.btn_run.SetLabelText("Pause")
            self.parent.run_status = "Start"
            tsk.thread_run_manager(self.parent)
        elif self.parent.run_status == "Start":
            self.parent.run_status = "Pause"
            self.btn_run.SetLabelText("Continue")
        elif self.parent.run_status == "Pause":
            self.parent.run_status = "Start"
            self.btn_run.SetLabelText("Pause")
        return

    def stop_program(self, event):
        print("Stopping program")
        self.parent.run_status = "Stop"
        return

    def show_camera_config(self, event):
        extraPan = self.parent.additionalPan

        extraPan.cmb_shots_delay.Hide()
        extraPan.cmb_number_of_shots.Hide()
        extraPan.btn_set_camera_option.Hide()
        extraPan.txt_number_of_shots.Hide()
        extraPan.txt_shots_delay.Hide()

    def single_shot(self, event):
        popup.shoot_at_window(self.parent)
        # popup.file_name_preferences(self.parent)
