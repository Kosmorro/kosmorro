#!/usr/bin/env python3

#    Kosmorro - Compute The Next Ephemerides
#    Copyright (C) 2019  Jérôme Deuchnord <jerome@deuchnord.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from abc import ABC, abstractmethod
import datetime
import json
import os
import tempfile
import subprocess
import shutil
from pathlib import Path

from kosmorrolib.exceptions import UnavailableFeatureError
from tabulate import tabulate
from termcolor import colored

from kosmorrolib import AsterEphemerides, Event
from kosmorrolib.model import ASTERS, MoonPhase

from .i18n.utils import _, FULL_DATE_FORMAT, SHORT_DATETIME_FORMAT, TIME_FORMAT
from .i18n import strings
from .__version__ import __version__ as version
from .exceptions import (
    CompileError,
    UnavailableFeatureError as KosmorroUnavailableFeatureError,
)
from .debug import debug_print


class Dumper(ABC):
    ephemerides: [AsterEphemerides]
    moon_phase: MoonPhase
    events: [Event]
    date: datetime.date
    timezone: int
    with_colors: bool
    show_graph: bool

    def __init__(
        self,
        ephemerides: [AsterEphemerides],
        moon_phase: MoonPhase,
        events: [Event],
        date: datetime.date,
        timezone: int,
        with_colors: bool,
        show_graph: bool,
    ):
        self.ephemerides = ephemerides
        self.moon_phase = moon_phase
        self.events = events
        self.date = date
        self.timezone = timezone
        self.with_colors = with_colors
        self.show_graph = show_graph

    def get_date_as_string(self, capitalized: bool = False) -> str:
        date = self.date.strftime(FULL_DATE_FORMAT)

        if capitalized:
            return "".join([date[0].upper(), date[1:]])

        return date

    def __str__(self):
        return self.to_string()

    @abstractmethod
    def to_string(self):
        pass

    @staticmethod
    def is_file_output_needed() -> bool:
        return False


class JsonDumper(Dumper):
    def to_string(self):
        return json.dumps(
            {
                "ephemerides": [
                    ephemeris.serialize() for ephemeris in self.ephemerides
                ],
                "moon_phase": self.moon_phase.serialize(),
                "events": [event.serialize() for event in self.events],
            },
            indent=4,
        )


class TextDumper(Dumper):
    def to_string(self):
        text = [self.style(self.get_date_as_string(capitalized=True), "h1")]

        if len(self.ephemerides) > 0:
            text.append(self.stringify_ephemerides())

        text.append(self.get_moon(self.moon_phase))

        if len(self.events) > 0:
            text.append(
                "\n".join(
                    [
                        self.style(_("Expected events:"), "h2"),
                        self.get_events(self.events),
                    ]
                )
            )

        if self.timezone == 0:
            text.append(self.style(_("Note: All the hours are given in UTC."), "em"))
        else:
            tz_offset = str(self.timezone)
            if self.timezone > 0:
                tz_offset = "".join(["+", tz_offset])
            text.append(
                self.style(
                    _(
                        "Note: All the hours are given in the UTC{offset} timezone."
                    ).format(offset=tz_offset),
                    "em",
                )
            )

        return "\n\n".join(text)

    def style(self, text: str, tag: str) -> str:
        if not self.with_colors:
            return text

        styles = {
            "h1": lambda t: colored(t, "yellow", attrs=["bold"]),
            "h2": lambda t: colored(t, "magenta", attrs=["bold"]),
            "th": lambda t: colored(t, "white", attrs=["bold"]),
            "strong": lambda t: colored(t, attrs=["bold"]),
            "em": lambda t: colored(t, attrs=["dark"]),
        }

        return styles[tag](text)

    def stringify_ephemerides(self) -> str:
        data = []

        for ephemeris in self.ephemerides:
            object_name = strings.from_object(ephemeris.object.identifier)
            if object_name is None:
                continue

            name = self.style(object_name, "th")

            if ephemeris.rise_time is not None:
                time_fmt = (
                    TIME_FORMAT
                    if ephemeris.rise_time.day == self.date.day
                    else SHORT_DATETIME_FORMAT
                )
                planet_rise = ephemeris.rise_time.strftime(time_fmt)
            else:
                planet_rise = "-"

            if ephemeris.culmination_time is not None:
                time_fmt = (
                    TIME_FORMAT
                    if ephemeris.culmination_time.day == self.date.day
                    else SHORT_DATETIME_FORMAT
                )
                planet_culmination = ephemeris.culmination_time.strftime(time_fmt)
            else:
                planet_culmination = "-"

            if ephemeris.set_time is not None:
                time_fmt = (
                    TIME_FORMAT
                    if ephemeris.set_time.day == self.date.day
                    else SHORT_DATETIME_FORMAT
                )
                planet_set = ephemeris.set_time.strftime(time_fmt)
            else:
                planet_set = "-"

            data.append([name, planet_rise, planet_culmination, planet_set])

        return tabulate(
            data,
            headers=[
                self.style(_("Object"), "th"),
                self.style(_("Rise time"), "th"),
                self.style(_("Culmination time"), "th"),
                self.style(_("Set time"), "th"),
            ],
            tablefmt="simple",
            stralign="center",
            colalign=("left",),
        )

    def get_events(self, events: [Event]) -> str:
        data = []

        for event in events:
            description = strings.from_event(event)
            time_fmt = (
                TIME_FORMAT
                if event.start_time.day == self.date.day
                else SHORT_DATETIME_FORMAT
            )
            data.append(
                [
                    self.style(event.start_time.strftime(time_fmt), "th"),
                    description,
                ]
            )

        return tabulate(data, tablefmt="plain", stralign="left")

    def get_moon(self, moon_phase: MoonPhase) -> str:
        if moon_phase is None:
            return _("Moon phase is unavailable for this date.")

        current_moon_phase = " ".join(
            [
                self.style(_("Moon phase:"), "strong"),
                strings.from_moon_phase(moon_phase.phase_type),
            ]
        )
        new_moon_phase = _(
            "{next_moon_phase} on {next_moon_phase_date} at {next_moon_phase_time}"
        ).format(
            next_moon_phase=_(strings.from_moon_phase(moon_phase.get_next_phase())),
            next_moon_phase_date=moon_phase.next_phase_date.strftime(FULL_DATE_FORMAT),
            next_moon_phase_time=moon_phase.next_phase_date.strftime(TIME_FORMAT),
        )

        return "\n".join([current_moon_phase, new_moon_phase])


class _LatexDumper(Dumper):
    def to_string(self):
        template_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "assets", "pdf", "template.tex"
        )

        with open(template_path, mode="r") as file:
            template = file.read()

        return self._make_document(template)

    def _make_document(self, template: str) -> str:
        kosmorro_logo_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "assets",
            "png",
            "kosmorro-logo.png",
        )

        moon_phase_graphics = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "assets",
            "moonphases",
            "png",
            ".".join(
                [self.moon_phase.phase_type.name.lower().replace("_", "-"), "png"]
            ),
        )

        document = template

        if self.ephemerides is None:
            document = self._remove_section(document, "ephemerides")

        if len(self.events) == 0:
            document = self._remove_section(document, "events")

        document = self.add_strings(document, kosmorro_logo_path, moon_phase_graphics)

        if self.show_graph:
            # The graphephemerides environment beginning tag must end with a percent symbol to ensure
            # that no extra space will interfere with the graph.
            document = document.replace(
                r"\begin{ephemerides}", r"\begin{graphephemerides}%"
            ).replace(r"\end{ephemerides}", r"\end{graphephemerides}")

        return document

    def add_strings(
        self, document: str, kosmorro_logo_path: str, moon_phase_graphics: str
    ) -> str:
        document = document.replace("+++KOSMORRO-VERSION+++", version)
        document = document.replace("+++KOSMORRO-LOGO+++", kosmorro_logo_path)
        document = document.replace("+++DOCUMENT-TITLE+++", _("Overview of your sky"))
        document = document.replace(
            "+++DOCUMENT-DATE+++", self.get_date_as_string(capitalized=True)
        )
        document = document.replace(
            "+++INTRODUCTION+++",
            "\n\n".join(
                [
                    _(
                        "This document summarizes the ephemerides and the events of {date}. "
                        "It aims to help you to prepare your observation session. "
                        "All the hours are given in {timezone}."
                    ).format(
                        date=self.get_date_as_string(),
                        timezone="UTC+%d" % self.timezone
                        if self.timezone != 0
                        else "UTC",
                    ),
                    _(
                        "Don't forget to check the weather forecast before you go out with your equipment."
                    ),
                ]
            ),
        )
        document = document.replace(
            "+++SECTION-EPHEMERIDES+++", _("Ephemerides of the day")
        )
        document = document.replace("+++EPHEMERIDES-OBJECT+++", _("Object"))
        document = document.replace("+++EPHEMERIDES-RISE-TIME+++", _("Rise time"))
        document = document.replace(
            "+++EPHEMERIDES-CULMINATION-TIME+++", _("Culmination time")
        )
        document = document.replace("+++EPHEMERIDES-SET-TIME+++", _("Set time"))
        document = document.replace("+++EPHEMERIDES+++", self._make_ephemerides())
        document = document.replace("+++GRAPH_LABEL_HOURS+++", _("hours"))
        document = document.replace("+++MOON-PHASE-GRAPHICS+++", moon_phase_graphics)
        document = document.replace("+++CURRENT-MOON-PHASE-TITLE+++", _("Moon phase:"))
        document = document.replace(
            "+++CURRENT-MOON-PHASE+++",
            strings.from_moon_phase(self.moon_phase.phase_type),
        )
        document = document.replace("+++SECTION-EVENTS+++", _("Expected events"))
        document = document.replace("+++EVENTS+++", self._make_events())

        for aster in ASTERS:
            object_name = strings.from_object(aster.identifier)
            if object_name is None:
                continue

            document = document.replace(
                "+++ASTER_%s+++" % aster.skyfield_name.upper().split(" ")[0],
                object_name,
            )

        return document

    def _make_ephemerides(self) -> str:
        latex = []
        graph_y_component = 18

        if self.ephemerides is not None:
            for ephemeris in self.ephemerides:
                if ephemeris.rise_time is not None:
                    time_fmt = (
                        TIME_FORMAT
                        if ephemeris.rise_time.day == self.date.day
                        else SHORT_DATETIME_FORMAT
                    )
                    aster_rise = ephemeris.rise_time.strftime(time_fmt)
                else:
                    aster_rise = "-"

                if ephemeris.culmination_time is not None:
                    time_fmt = (
                        TIME_FORMAT
                        if ephemeris.culmination_time.day == self.date.day
                        else SHORT_DATETIME_FORMAT
                    )
                    aster_culmination = ephemeris.culmination_time.strftime(time_fmt)
                else:
                    aster_culmination = "-"

                if ephemeris.set_time is not None:
                    time_fmt = (
                        TIME_FORMAT
                        if ephemeris.set_time.day == self.date.day
                        else SHORT_DATETIME_FORMAT
                    )
                    aster_set = ephemeris.set_time.strftime(time_fmt)
                else:
                    aster_set = "-"

                if not self.show_graph:
                    object_name = strings.from_object(ephemeris.object.identifier)
                    if object_name is not None:
                        latex.append(
                            r"\object{%s}{%s}{%s}{%s}"
                            % (
                                object_name,
                                aster_rise,
                                aster_culmination,
                                aster_set,
                            )
                        )
                else:
                    if ephemeris.rise_time is not None:
                        raise_hour = ephemeris.rise_time.hour
                        raise_minute = ephemeris.rise_time.minute
                    else:
                        raise_hour = raise_minute = 0
                        aster_rise = ""

                    if ephemeris.set_time is not None:
                        set_hour = ephemeris.set_time.hour
                        set_minute = ephemeris.set_time.minute
                    else:
                        set_hour = 24
                        set_minute = 0
                        aster_set = ""
                    sets_after_end = set_hour > raise_hour

                    if not sets_after_end:
                        latex.append(
                            r"\graphobject{%d}{gray}{0}{0}{%d}{%d}{}{%s}"
                            % (graph_y_component, set_hour, set_minute, aster_set)
                        )
                        set_hour = 24
                        set_minute = 0

                    latex.append(
                        r"\graphobject{%d}{gray}{%d}{%d}{%d}{%d}{%s}{%s}"
                        % (
                            graph_y_component,
                            raise_hour,
                            raise_minute,
                            set_hour,
                            set_minute,
                            aster_rise,
                            aster_set if sets_after_end else "",
                        )
                    )
                    graph_y_component -= 2

        return "".join(latex)

    def _make_events(self) -> str:
        latex = []

        for event in self.events:
            event_name = strings.from_event(event)
            if event_name is None:
                continue

            latex.append(
                r"\event{%s}{%s}" % (event.start_time.strftime(TIME_FORMAT), event_name)
            )

        return "".join(latex)

    @staticmethod
    def _remove_section(document: str, section: str):
        begin_section_tag = "%%%%%% BEGIN-%s-SECTION" % section.upper()
        end_section_tag = "%%%%%% END-%s-SECTION" % section.upper()

        document = document.split("\n")
        new_document = []

        ignore_line = False
        for line in document:
            if begin_section_tag in line or end_section_tag in line:
                ignore_line = not ignore_line
                continue
            if ignore_line:
                continue
            new_document.append(line)

        return "\n".join(new_document)


class PdfDumper(Dumper):
    def to_string(self):
        try:
            latex_dumper = _LatexDumper(
                self.ephemerides,
                self.moon_phase,
                self.events,
                date=self.date,
                timezone=self.timezone,
                with_colors=self.with_colors,
                show_graph=self.show_graph,
            )

            return self._compile(latex_dumper.to_string())
        except RuntimeError as error:
            raise KosmorroUnavailableFeatureError(
                _(
                    "Building PDF was not possible, because some dependencies are not"
                    " installed.\nPlease look at the documentation at https://kosmorro.space/cli/generate-pdf/ "
                    "for more information."
                )
            ) from error

    @staticmethod
    def is_file_output_needed() -> bool:
        return True

    @staticmethod
    def _compile(latex_input) -> bytes:
        package = str(Path(__file__).parent.absolute()) + "/assets/pdf/kosmorro.sty"
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        current_dir = (
            os.getcwd()
        )  # Keep the current directory to return to it after the PDFLaTeX execution

        try:
            temp_dir = tempfile.mkdtemp()

            shutil.copy(package, temp_dir)

            temp_tex = "%s/%s.tex" % (temp_dir, timestamp)

            with open(temp_tex, "w") as tex_file:
                tex_file.write(latex_input)

            os.chdir(temp_dir)
            debug_print("LaTeX content:\n%s" % latex_input)

            subprocess.run(
                ["pdflatex", "-interaction", "nonstopmode", "%s.tex" % timestamp],
                capture_output=True,
                check=True,
            )

            os.chdir(current_dir)

            with open("%s/%s.pdf" % (temp_dir, timestamp), "rb") as pdffile:
                return bytes(pdffile.read())

        except FileNotFoundError as error:
            raise KosmorroUnavailableFeatureError(
                "TeXLive is not installed."
            ) from error

        except subprocess.CalledProcessError as error:
            with open("/tmp/kosmorro-%s.log" % timestamp, "wb") as file:
                file.write(error.stdout)

            raise CompileError(
                _(
                    "An error occurred during the compilation of the PDF.\n"
                    "Please open an issue at https://github.com/Kosmorro/kosmorro/issues and share "
                    "the content of the log file at /tmp/kosmorro-%s.log" % timestamp
                )
            ) from error
