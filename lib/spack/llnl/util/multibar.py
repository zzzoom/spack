# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Utilities for making multiple progress bars in the console."""
from __future__ import division
from __future__ import print_function

import contextlib
import six
import sys
from datetime import datetime

import ansiescapes as ansi

#: draw period per bar in seconds
_draw_period = .03


def total_seconds(td):
    """Get total seconds from a timedelta (needed for 2.6 compatibility)."""
    return (td.days * 86400 +
            td.seconds +
            td.microseconds / 1000000.0)


def hms(td):
    """Print out a time delta in '5h 4m 3s' format."""
    sec = total_seconds(td)
    hours = td.seconds // 3600

    sec -= hours * 3600
    minutes = sec // 60

    sec -= minutes * 60

    result = ''
    if hours:
        result += '%dh' % hours
    if hours or minutes:
        result += '%dm' % minutes
    result += '%.1fs' % sec

    return result


class ProgressBar(object):
    """A progress bar that can be added to BarGroups."""

    def __init__(self, width=50, out=sys.stdout,
                 prefix='', suffix='', finish='',
                 group=None, line=None, data=None):
        """Create a new ProgressBar.

        Args:
            width (int): width in characters of the bar
            out (file object): file object to write output
            prefix (str): printed before the bar
            suffix (str): printed after the bar
            finish (str): printed after progress reaches 100%
            group (BarGroup): BarGroup this bar is a part of
            line (int): line from top of BarGroup (starting at 0) where
                this bar should appear
            data (object): arbitrary data stored on this bar, retrievable
                later via bar.data; use to store information on the bar
        """
        # bar starts with dummy values for progress and total
        self.progress = 0
        self.total = 100
        self.done = False

        # appearance parameters (caller can set)
        self.width = width
        self.prefix = prefix
        self.finish = finish
        self.suffix = suffix

        # output
        self.out = out

        # output
        self._start_time = None   # time of first update with progress
        self._last_update = None  # last update with progress
        self._last_draw = None    # last time drawn

        # set up as a member of a group (if needed)
        self.group = group
        self.line = line

        # record a name if one was provided
        self.data = data

        # initial dummy update
        self.draw()

    def update(self, progress, total):
        """Update the bar with progress so far and a total.

        Arguments:
            progress (number or str): progress so far
            total (total): total progress required to finish

        If progress is evrer >= total, the bar is marked done and further
        updates will raise an error.

        If progress is a string instead of some numeric type, we display
        its value in the bar instead of showing progress.  You can use
        this for things that don't support progress, to display messages
        like "Downloading".  You will need to call ``update()`` with
        progress >= total to force the bar to complete.
        """
        if self.done:
            raise RuntimeError("Can't call update once finished!")

        now = datetime.now()
        self.total = total

        if self._start_time is None:
            self._start_time = now
            self._last_drawn = now

        self._last_update = now

        self.progress = progress
        if not isinstance(progress, six.string_types):
            if self.progress > self.total:
                self.progress = self.total

            # mark whether we're done or not.
            if self.progress >= self.total:
                self.done = True

        # draw every _draw_period seconds, or on the very last call
        delta = now - self._last_drawn
        if total_seconds(delta) > _draw_period or self.done:
            self._last_drawn = now
            self.draw()

    def _draw(self):
        """Draw the bar on the current line on the screen."""
        self.out.write('\r')

        if isinstance(self.progress, six.string_types):
            # if it's a string, just put the string in the status bar
            percent = 0.0
            content = self.progress[:self.width]
            padding = ' ' * (self.width - len(content))
            bar = content + padding
        else:
            # if it's a number, draw an arrow according to % total
            percent = "%.1f" % (100 * self.progress / float(self.total))
            width_done = int(self.width * self.progress // self.total)
            padding = ' ' * (self.width - width_done)
            bar = ((width_done - 1) * '=') + '>' + padding

        # not started yet
        if self._last_update is None:
            self.out.write('%s Waiting.' % self.prefix)
            self.out.write(ansi.eraseEndLine)

        else:
            # in progress
            self.out.write(
                '%s [%s] %s%% %s' % (self.prefix, bar, percent, self.suffix))
            if self._last_update is not None:
                self.out.write(' (%s)' % hms(self._last_update - self._start_time))
            self.out.write('\r')

            if self.done and self.finish:
                # erase as this text may be shorter than what was there.
                self.out.write(ansi.eraseEndLine)
                self.out.write('%s Done.\r' % self.prefix)

    def draw(self):
        if self.group:
            assert self.line is not None
            with self.group.move_to_line(self.line):
                self._draw()
        else:
            self._draw()
        self.out.flush()



class BarGroup(object):
    """A group of progress bars that can update concurrently.

    Bars can be added dynamically to the group with ``add_bar()``, and
    the bars are displayed on the first N lines, followed by M lines of
    margin (for status messages), and the cursor stays at the bottom of
    the BarGroup while bars are not done.

    Example::

        $ python command
        prefix [========>----------------------------------------] suffix
        prefix [==============>----------------------------------] suffix
        prefix [===================>-----------------------------] suffix
        prefix [==============>----------------------------------] suffix
        prefix [==============>----------------------------------] suffix
        text in the margin goes here
        X <---- cursor

    """
    def __init__(self, width=50, out=sys.stdout, bottom_margin=0, title=None):
        """Create a new group of progress bars, all with the same width.

        Args:
            width (int): width of progress bars in this group
            out (file object): stream to write data out to
            bottom_margin (int): lines at bottom of bar group left blank
                for status messages, etc.
            title (str, optional): a title for this BarGroup, to be
                displayed above all the bars
        """
        self.width = width
        self.out = out
        self.bars = []
        self.length = 0

        self.title = title
        if self.title is not None:
            self.out.write(ansi.cursorDown())

        self.bottom_margin = bottom_margin
        if bottom_margin:
            self.out.write(ansi.cursorDown(bottom_margin))

    def __len__(self):
        return self.length

    @property
    def height(self):
        return (self.title is not None) + len(self) + self.bottom_margin

    @contextlib.contextmanager
    def move_to_line(self, line):
        """Move to the specified line in the group, do something, move back."""
        lines_from_bottom = self.height - line
        self.out.write(ansi.cursorUp(lines_from_bottom))
        yield
        self.out.write(ansi.cursorDown(lines_from_bottom) + '\r')

    def draw_title(self):
        """Print out the title of the bar group on the first (0th) line."""
        if self.title is None:
            return

        with self.move_to_line(0):
            self.out.write(self.title)
            self.out.write(ansi.eraseEndLine)

    def redraw(self):
        """Redraw the entire bar group."""
        self.draw_title()
        for bar in self.bars:
            bar.draw()

    def add_bar(self, *args, **kwargs):
        """Add a bar to the progress bar group."""

        # disallow some arguments to be set independently for a group
        for arg in ('group', 'width', 'out'):
            if arg in kwargs:
                raise ValueError("Cannot pass %s to add_bar()" % arg)

        # move down one row
        self.out.write(ansi.cursorDown())
        self.length += 1

        # update kwargs with group-related arguments
        kwargs.update({
            'group': self,
            'width': self.width,
            'line': (self.title is not None) + len(self.bars),
            'out': self.out
        })

        # this makes the new bar appear
        bar = ProgressBar(*args, **kwargs)

        # redraw all the others (even completed ones), as adding a new
        # bar may cause all bars to move up one line in the console.
        self.redraw()

        # add the new bar after redraw, so that it's not drawn twice
        self.bars.append(bar)

        return bar
