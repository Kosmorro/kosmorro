import wx

from ..data import Position
from ..i18n import _


class PositionWindow(wx.Dialog):
    position: Position

    def __init__(self, parent, position: Position = None):
        super(PositionWindow, self).__init__(parent, title=_('Set position'), style=wx.DEFAULT_DIALOG_STYLE ^ wx.CLOSE_BOX)
        self.position = position

        latitude_lbl = wx.StaticText(self, label=_('Latitude:'))
        self._latitude_input = wx.SpinCtrlDouble(self, initial=position.latitude if position is not None else 0,
                                                 min=-90, max=90)
        self._latitude_input.SetDigits(4)

        longitude_lbl = wx.StaticText(self, label=_('Longitude:'))
        self._longitude_input = wx.SpinCtrlDouble(self, initial=position.longitude if position is not None else 0,
                                                  min=-180, max=180)
        self._longitude_input.SetDigits(4)

        ok_button = wx.Button(self, label=_('OK'))
        cancel_button = wx.Button(self, label=_('Cancel'))

        self.Bind(wx.EVT_BUTTON, self.on_ok, ok_button)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, cancel_button)

        btn_sizer = wx.GridSizer(1, 2, 5, 5)
        btn_sizer.AddMany([(ok_button, 0, wx.EXPAND),
                           (cancel_button, 0, wx.EXPAND)])

        sizer = wx.FlexGridSizer(2, 5, 5)
        sizer.AddGrowableCol(0, 2)
        sizer.AddMany([(latitude_lbl, 0, wx.EXPAND | wx.ALL, 5),
                       (self._latitude_input, 0, wx.EXPAND | wx.ALL, 5),
                       (longitude_lbl, 0, wx.EXPAND | wx.ALL, 5),
                       (self._longitude_input, 0, wx.EXPAND | wx.ALL, 5),
                       (wx.StaticText(self), 0, wx.EXPAND | wx.ALL, 5),
                       (btn_sizer, 0, wx.EXPAND | wx.ALL, 5)])

        self.SetSizer(sizer)
        self.Fit()
        self.Center()

        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)

    def on_cancel(self, _=None):
        self.Close()

    def on_ok(self, _=None):
        self.position = Position(self._latitude_input.GetValue(), self._longitude_input.GetValue())
        self.Close()

    def on_key_down(self, event):
        key = event.GetKeyCode()

        if key == wx.WXK_ESCAPE:
            self.on_cancel()
        elif key in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
            self.on_ok()
        else:
            event.Skip()
