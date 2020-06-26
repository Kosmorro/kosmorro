import os
from typing import Union

import wx
import wx.adv
import wx.grid
import wx.richtext
import wx.lib.newevent

from .positionwindow import PositionWindow

from ..data import Position, AsterEphemerides, Event, MoonPhase
from ..i18n import _, TIME_FORMAT, FULL_DATE_FORMAT
from datetime import date

FPB_HORIZONTAL = 0x4

ComputeButtonEvent, EVT_COMPUTE_BUTTON = wx.lib.newevent.NewEvent()

ExportButtonEvent, EVT_EXPORT_BUTTON = wx.lib.newevent.NewEvent()


class ConfigPanel(wx.Panel):
    activate_position: bool
    position: Union[None, Position]
    compute_date: date
    timezone: int

    def __init__(self, parent, activate_position: bool = False, position: Position = None,
                 compute_date: date = date.today(), timezone: int = 0):
        super(ConfigPanel, self).__init__(parent)
        self.activate_position = activate_position
        self.position = position
        self.compute_date = compute_date
        self.timezone = timezone

        self._position_checkbox = wx.CheckBox(self, label=_('Position:'))
        self._position_change_btn = wx.Button(self)
        self.update_position_btn_label()
        self._position_change_btn.SetToolTip(wx.ToolTip(_('Change the position')))
        self._position_checkbox.SetValue(activate_position)
        self._position_change_btn.Enable(activate_position)

        self.Bind(wx.EVT_CHECKBOX, self.on_position_checkbox, self._position_checkbox)
        self.Bind(wx.EVT_BUTTON, self.on_position_button, self._position_change_btn)

        date_lbl = wx.StaticText(self, label=_('Date:'))
        self._date_picker = wx.adv.DatePickerCtrl(self, dt=wx.DateTime(compute_date),
                                                  style=wx.adv.DP_DEFAULT)
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.date_changed, self._date_picker)

        timezone_lbl = wx.StaticText(self, label=_('Timezone:'))
        self._timezone_spin = wx.SpinCtrl(self, min=-23, max=23, value=str(timezone))
        self.Bind(wx.EVT_SPINCTRL, self.timezone_changed, self._timezone_spin)

        sizer = wx.FlexGridSizer(2, 5, 5)
        sizer.AddGrowableCol(1, 1)

        self._compute_button = wx.Button(self, label=_('&Compute'))
        self._export_button = wx.Button(self, label=_('E&xport PDF…'))

        self.Bind(wx.EVT_BUTTON, self.compute_button_clicked, self._compute_button)
        self.Bind(wx.EVT_BUTTON, self.export_button_clicked, self._export_button)

        sizer.AddMany([(self._position_checkbox, 0, wx.EXPAND),
                       (self._position_change_btn, 0, wx.EXPAND),
                       (date_lbl, 0, wx.EXPAND),
                       (self._date_picker, 0, wx.EXPAND),
                       (timezone_lbl, 0, wx.EXPAND),
                       (self._timezone_spin, 0, wx.EXPAND)])

        main_sizer = wx.FlexGridSizer(3, 5, 5)
        main_sizer.AddGrowableCol(0, 2)

        main_sizer.AddMany([(sizer, 0, wx.EXPAND),
                            (self._compute_button, 0, wx.EXPAND),
                            (self._export_button, 0, wx.EXPAND)])

        self.SetSizer(main_sizer)

    def update_position_btn_label(self):
        self._position_change_btn.Label = str(self.position) if self.position is not None else _('Unknown')

    def enable_buttons(self, enable: bool = True):
        self._compute_button.Enable(enable)
        self._export_button.Enable(enable)

    def disable_buttons(self):
        self.enable_buttons(False)

    def on_position_checkbox(self, event):
        self.activate_position = event.IsChecked()
        self._position_change_btn.Enable(self.activate_position)

        if self.activate_position and self.position is None:
            self.on_position_button()

    def on_position_button(self, _=None):
        pos_win = PositionWindow(self, self.position)
        pos_win.ShowModal()
        self.position = pos_win.position
        if self.position is not None:
            self.update_position_btn_label()
        else:
            self._position_checkbox.SetValue(False)
            self._position_change_btn.Disable()

    def date_changed(self, _):
        self.compute_date = date.fromisoformat(self._date_picker.GetValue().FormatISODate())

    def timezone_changed(self, _):
        self.timezone = self._timezone_spin.GetValue()

    def compute_button_clicked(self, _):
        wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(EVT_COMPUTE_BUTTON.typeId, self.GetId()))

    def export_button_clicked(self, _):
        wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(EVT_EXPORT_BUTTON.typeId, self.GetId()))


class MoonPhasePanel(wx.Panel):
    def __init__(self, parent):
        super(MoonPhasePanel, self).__init__(parent)

        self.moon_bitmap = wx.StaticBitmap(self, size=wx.Size(100, 100))

        self.moon_txt_l1 = wx.StaticText(self)
        self.moon_txt_l2 = wx.StaticText(self)

        self.moon_txt_l1.SetFont(wx.Font(wx.DEFAULT, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        label_sizer = wx.GridSizer(3, 1, 0, 0)
        label_sizer.AddMany([(wx.StaticText(self), 0, wx.ALIGN_LEFT),
                             (self.moon_txt_l1, 0, wx.ALIGN_LEFT | wx.EXPAND),
                             (self.moon_txt_l2, 0, wx.ALIGN_LEFT | wx.EXPAND)])

        main_sizer = wx.FlexGridSizer(4, 0, 10)
        main_sizer.AddGrowableCol(0)
        main_sizer.AddGrowableCol(2)
        main_sizer.AddMany([(wx.StaticText(self), 0, wx.ALIGN_LEFT),
                            (self.moon_bitmap, 0, wx.ALIGN_RIGHT),
                            (label_sizer, 0, wx.ALIGN_LEFT)])

        self.SetSizer(main_sizer)

    def set_moon_phase(self, moon_phase: MoonPhase):
        moon_img = wx.Image(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                         '..', 'assets', 'moonphases', 'png',
                                         '.'.join([moon_phase.identifier.lower().replace('_', '-'),
                                                   'png'])))
        moon_img = moon_img.Scale(100, 100)
        bitmap = moon_img.ConvertToBitmap()
        self.moon_bitmap.SetBitmap(bitmap)

        self.moon_txt_l1.SetLabel(moon_phase.get_phase())
        self.moon_txt_l2.SetLabel(_('{next_moon_phase} on {next_moon_phase_date} at {next_moon_phase_time}').format(
            next_moon_phase=moon_phase.get_next_phase_name(),
            next_moon_phase_date=moon_phase.next_phase_date.strftime(FULL_DATE_FORMAT),
            next_moon_phase_time=moon_phase.next_phase_date.strftime(TIME_FORMAT)
        ))

        self.Layout()
        self.Fit()


class ResultPanel(wx.Panel):
    ephemerides: [AsterEphemerides]
    events: [Event]
    moon_phase: Union[None, MoonPhase]

    def __init__(self, parent):
        super(ResultPanel, self).__init__(parent)
        self.moon_phase = None
        self.ephemerides = None
        self.events = None

        self._moon_phase_panel = MoonPhasePanel(self)

        self._grid_ephemerides = wx.grid.Grid(self)
        self._grid_ephemerides.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self._grid_ephemerides.CreateGrid(numRows=0, numCols=3)
        self._grid_ephemerides.EnableEditing(False)
        self._grid_ephemerides.SetColLabelValue(0, _('Rise time'))
        self._grid_ephemerides.SetColLabelValue(1, _('Culmination time'))
        self._grid_ephemerides.SetColLabelValue(2, _('Set time'))
        self._grid_ephemerides.EnableEditing(False)

        self._list_events = wx.richtext.RichTextCtrl(self, size=wx.Size(0, 300),
                                                     style=wx.richtext.RE_READONLY | wx.richtext.RE_MULTILINE)

        main_sizer = wx.FlexGridSizer(2, 1, 5, 5)
        main_sizer.AddGrowableCol(0)
        main_sizer.AddGrowableRow(1, 2)

        sizer = wx.FlexGridSizer(2, 5, 5)
        sizer.AddGrowableCol(0, 0)
        sizer.AddGrowableCol(1, 1)
        sizer.AddMany([(self._grid_ephemerides, 0, wx.EXPAND | wx.ALL),
                       (self._list_events, 0, wx.EXPAND | wx.ALL)])

        main_sizer.AddMany([(self._moon_phase_panel, 0, wx.EXPAND | wx.ALL, 5),
                            (sizer, 0, wx.EXPAND | wx.ALL)])
        self.SetSizer(main_sizer)

    def render(self):
        if self.moon_phase is not None:
            self._moon_phase_panel.set_moon_phase(self.moon_phase)

        if self._grid_ephemerides.NumberRows > 0:
            self._grid_ephemerides.DeleteRows(numRows=self._grid_ephemerides.NumberRows)

        if self.ephemerides is not None and len(self.ephemerides) > 0:
            for ephemeris in self.ephemerides:
                rise_time = ephemeris.rise_time.strftime(TIME_FORMAT) if ephemeris.rise_time is not None else ''
                culmination_time = ephemeris.culmination_time.strftime(TIME_FORMAT) if ephemeris.culmination_time is not None else ''
                set_time = ephemeris.set_time.strftime(TIME_FORMAT) if ephemeris.set_time is not None else ''

                self._grid_ephemerides.AppendRows()
                row = self._grid_ephemerides.NumberRows - 1
                self._grid_ephemerides.SetRowLabelValue(row, ephemeris.object.name)
                self._grid_ephemerides.SetCellValue(row, 0, rise_time)
                self._grid_ephemerides.SetCellValue(row, 1, culmination_time)
                self._grid_ephemerides.SetCellValue(row, 2, set_time)

        self._grid_ephemerides.Show(len(self.ephemerides) > 0)
        self._grid_ephemerides.AutoSize()

        if self.events is not None and len(self.events) > 0:
            content = ''
            for event in self.events:
                content += '\n' if content != '' else ''
                content += _('- {event_time}: {event_description}').format(
                    event_time=event.start_time.strftime(TIME_FORMAT),
                    event_description=event.get_description()
                )

            self._list_events.SetValue(content)
        else:
            self._list_events.SetValue(_('No events for this day.'))

        self.Layout()
