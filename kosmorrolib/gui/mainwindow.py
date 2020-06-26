import wx

import platform
from typing import Union
import webbrowser
from threading import Thread
from datetime import date

from . import panel

from ..data import Position, AsterEphemerides, Event, MoonPhase
from ..exceptions import UnavailableFeatureError
from ..ephemerides import get_ephemerides, get_moon_phase
from ..events import search_events
from ..version import VERSION
from ..dumper import PdfDumper
from ..i18n import _

MIN_SIZE = wx.Size(700, 0)

# Events definitions

myEVT_EPHEMERIDES_COMPUTED = wx.NewEventType()
EVT_EPHEMERIDES_COMPUTED = wx.PyEventBinder(myEVT_EPHEMERIDES_COMPUTED, 1)


class EphemeridesComputedEvent(wx.PyCommandEvent):
    def __init__(self, etype, eid, value=None):
        super(EphemeridesComputedEvent, self).__init__(etype, eid)
        self.value = value


myEVT_MOON_PHASE_COMPUTED = wx.NewEventType()
EVT_MOON_PHASE_COMPUTED = wx.PyEventBinder(myEVT_MOON_PHASE_COMPUTED, 1)


class MoonPhaseComputedEvent(wx.PyCommandEvent):
    def __init__(self, etype, eid, value=None):
        super(MoonPhaseComputedEvent, self).__init__(etype, eid)
        self.value = value


myEVT_EVENTS_COMPUTED = wx.NewEventType()
EVT_EVENTS_COMPUTED = wx.PyEventBinder(myEVT_EVENTS_COMPUTED, 1)


class EventsComputedEvent(wx.PyCommandEvent):
    def __init__(self, etype, eid, value=None):
        super(EventsComputedEvent, self).__init__(etype, eid)
        self.value = value


# Computing threads

class MoonPhaseComputer(Thread):
    def __init__(self, parent, compute_date: date):
        super(MoonPhaseComputer, self).__init__()
        self._parent = parent
        self.compute_date = compute_date
        self.moon_phase = None

    def run(self):
        self.moon_phase = get_moon_phase(self.compute_date)
        wx.PostEvent(self._parent, EphemeridesComputedEvent(myEVT_MOON_PHASE_COMPUTED, -1, self.moon_phase))


class EphemeridesComputer(Thread):
    def __init__(self, parent, compute_date: date, position: Position, timezone: int):
        super(EphemeridesComputer, self).__init__()
        self._parent = parent
        self.compute_date = compute_date
        self.position = position
        self.timezone = timezone
        self.ephemerides = []

    def run(self):
        self.ephemerides = get_ephemerides(self.compute_date, self.position, self.timezone)
        wx.PostEvent(self._parent, EphemeridesComputedEvent(myEVT_EPHEMERIDES_COMPUTED, -1, self.ephemerides))


class EventsComputer(Thread):
    def __init__(self, parent, compute_date: date, timezone: int):
        super(EventsComputer, self).__init__()
        self._parent = parent
        self.compute_date = compute_date
        self.timezone = timezone
        self.events = []

    def run(self):
        self.events = search_events(self.compute_date, self.timezone)
        wx.PostEvent(self._parent, EventsComputedEvent(myEVT_EVENTS_COMPUTED, -1, self.events))


# Main window

class MainWindow(wx.Frame):
    ephemerides: [AsterEphemerides]
    events: [Event]
    moon_phase: Union[None, MoonPhase]

    def __init__(self):
        super(MainWindow, self).__init__(None, title='Kosmorro',
                                         style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        self.export_path = None
        self.config_panel = panel.ConfigPanel(self)
        self.Bind(panel.EVT_COMPUTE_BUTTON, self.compute)
        self.Bind(panel.EVT_EXPORT_BUTTON, self.export)

        self.result_presenter = panel.ResultPanel(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.AddMany([(self.config_panel, 0, wx.EXPAND | wx.ALL, 5),
                            (self.result_presenter, 0, wx.EXPAND | wx.ALL, 5)])

        self.SetSizer(self.sizer)
        self.make_menu_bar()

        status_bar = self.CreateStatusBar()
        status_bar.SetFieldsCount(2)
        status_bar.SetStatusWidths([-2, -1])
        self.progress_bar = wx.Gauge(status_bar, -1, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        rect = status_bar.GetFieldRect(1)
        self.progress_bar.SetPosition((rect.x + 2, rect.y + 2))
        self.progress_bar.SetSize((rect.width - 4, rect.height - 4))
        self.result_presenter.Hide()

        self.SetMinSize(MIN_SIZE)

        self.Fit()
        self.Center()
        self.progress_bar.Hide()

    def resize(self, width: int, height: int, center: bool = False):
        self.resize(wx.Size(width, height), center)

    def resize(self, size: wx.Size, center: bool = False):
        self.Size = size
        if center:
            self.Center()

    def resize(self, center: bool = False):
        self.Fit()
        if center:
            self.Center()

    def make_menu_bar(self):
        menu_bar = wx.MenuBar()

        if platform.system() != 'Darwin':
            # "Application" menu
            app_menu = wx.Menu()
            exit_item = app_menu.Append(wx.ID_EXIT)

            # "Help" menu
            help_menu = wx.Menu()
            about_item = help_menu.Append(wx.ID_ABOUT)

            menu_bar.Append(app_menu, _('&Application'))
            menu_bar.Append(help_menu, _('&Help'))
            self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        else:
            # On macOS, put the menu items to the place they belong to: the application name menu
            apple_menu = menu_bar.OSXGetAppleMenu()
            about_item = apple_menu.Insert(0, wx.ID_ABOUT)

        self.Bind(wx.EVT_MENU, self.on_about, about_item)
        self.SetMenuBar(menu_bar)

    def on_exit(self, event):
        self.Close(True)

    def on_about(self, event):
        message = wx.MessageDialog(caption='Kosmorro version %s' % VERSION,
                                   message='© Jérôme Deuchnord - 2020\n\n' +
                                           _('This is a free software licensed under the '
                                             'GNU Affero General Public License.'),
                                   style=wx.OK | wx.HELP | wx.ICON_INFORMATION,
                                   parent=self)
        message.SetOKLabel(_('Close'))
        message.SetHelpLabel(_('Website'))
        btn = message.ShowModal()

        if btn == wx.ID_HELP:
            webbrowser.open('http://kosmorro.space')

    def compute(self, __=None):
        # Reset data
        self.moon_phase = None
        self.ephemerides = None
        self.events = None

        self.config_panel.disable_buttons()
        self.SetCursor(wx.Cursor(wx.CURSOR_WAIT))

        self.SetStatusText(_('Computing…'))
        self.progress_bar.SetValue(0)
        self.progress_bar.Show()

        thread_moon_phase = MoonPhaseComputer(self, self.config_panel.compute_date)
        thread_ephemerides = EphemeridesComputer(self, self.config_panel.compute_date, self.config_panel.position,
                                                 self.config_panel.timezone)
        thread_events = EventsComputer(self, self.config_panel.compute_date, self.config_panel.timezone)

        self.Bind(EVT_MOON_PHASE_COMPUTED, self.on_moon_phase_computed)
        self.Bind(EVT_EPHEMERIDES_COMPUTED, self.on_ephemerides_computed)
        self.Bind(EVT_EVENTS_COMPUTED, self.on_events_computed)

        thread_moon_phase.start()

        if self.config_panel.activate_position and self.config_panel.position is not None:
            thread_ephemerides.start()
        else:
            self.ephemerides = []
            self.progress_bar.SetValue(50)

        thread_events.start()

    def export(self, __):
        self.export_path = self.get_export_file_path()
        if self.export_path is None:
            self.SetStatusText('Aborted.')
            return

        self.compute()

    def on_moon_phase_computed(self, event):
        self.moon_phase = event.value
        self.progress_bar.SetValue(self.progress_bar.GetValue() + 10)

        if self.is_all_computed():
            self.show_results()

    def on_ephemerides_computed(self, event):
        self.ephemerides = event.value
        self.progress_bar.SetValue(self.progress_bar.GetValue() + 50)

        if self.is_all_computed():
            self.show_results()

    def on_events_computed(self, event):
        self.events = event.value
        self.progress_bar.SetValue(self.progress_bar.GetValue() + 40)

        if self.is_all_computed():
            self.config_panel.enable_buttons()
            self.SetStatusText('')
            self.progress_bar.Hide()
            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

            if self.export_path is not None:
                ephemerides = self.ephemerides if len(self.ephemerides) > 0 else None
                dumper = PdfDumper(date=self.config_panel.compute_date, ephemerides=ephemerides,
                                   events=self.events, moon_phase=self.moon_phase, timezone=self.config_panel.timezone,
                                   show_graph=True)

                try:
                    with open(self.export_path, 'wb') as file:
                        file.write(dumper.to_string())
                    self.SetStatusText(_('PDF export saved in "{path}"!').format(path=self.export_path))
                except UnavailableFeatureError as error:
                    wx.MessageDialog(self, error.msg, caption=_('Error while exporting your document'),
                                     style=wx.OK | wx.ICON_ERROR).ShowModal()
                finally:
                    self.export_path = None

                return

            self.show_results()
            self.result_presenter.Show()
            self.resize(center=True)

    def is_all_computed(self) -> bool:
        return self.moon_phase is not None and self.ephemerides is not None and self.events is not None

    def show_results(self):
        self.result_presenter.moon_phase = self.moon_phase
        self.result_presenter.ephemerides = self.ephemerides
        self.result_presenter.events = self.events
        self.result_presenter.render()

    def get_export_file_path(self) -> Union[None, str]:
        dialog = wx.FileDialog(parent=self, message=_('Please select an export file location'),
                               wildcard='*.pdf', style=wx.FD_SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            return dialog.GetPath()
        else:
            return None


def start() -> bool:
    app = wx.App()
    window = MainWindow()

    window.Show()

    return app.MainLoop() == 0
