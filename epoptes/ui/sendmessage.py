#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################
# Message sending.
#
# Copyright (C) 2010 Fotis Tsamis <ftsamis@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FINESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# On Debian GNU/Linux systems, the complete text of the GNU General
# Public License can be found in `/usr/share/common-licenses/GPL".
###########################################################################

import gtk
import os
import pygtk
from glib import markup_escape_text

from epoptes.common import constants

pygtk.require('2.0')

wTree = gtk.Builder()
get = lambda obj: wTree.get_object(obj)

def quote_message(text):
    """
    Puts single quotes around text, double quotes around any single
    quotes within it, and escapes any pango special characters so that
    text can be passed as a shell parameter to zenity
    """

    return "'%s'" % markup_escape_text(text.replace("'", "'\"'\"'"))

def changed_cb(combobox):
    """
    Callback function that serves for changing
    the icon according to the message type selected
    from the combobox
    """

    icon = get('msgIcon')
    msg_type_id = combobox.get_active()

    # According to message type set the appropriate
    # icon
    if msg_type_id == 0: icon.set_from_stock(gtk.STOCK_DIALOG_INFO,
                                                gtk.ICON_SIZE_DIALOG)
    elif msg_type_id == 1: icon.set_from_stock(gtk.STOCK_DIALOG_WARNING,
                                                gtk.ICON_SIZE_DIALOG)
    elif msg_type_id == 2: icon.set_from_stock(gtk.STOCK_DIALOG_ERROR,
                                                gtk.ICON_SIZE_DIALOG)

def startSendMessageDlg():
    """
    Retrieve dialog window from glade format and
    according to type of message requested to send
    Returns: a 2-tuple containing the message text
    and the message type.
    """

    wTree.add_from_file('sendMessage.ui')
    dlg = get('sendMessageDialog')

    msgTypeCombo = get('typeOfMessage')
    msgTypeCombo.connect('changed', changed_cb)

    textView = get('Message')

    reply = dlg.run()
    msg = ()
    msg_types = {0 : 0, 1 : 1, 2 : 3}

    if reply == 1:
        buf = textView.get_buffer()
        s = buf.get_start_iter()
        e = buf.get_end_iter()
        text = quote_message(textView.get_buffer().get_text(s,e))
        
        # Get active type of message requested
        msg_type = msg_types[msgTypeCombo.get_active()]
        msg = (text, msg_type)

    # Hide dialog after any kind of function
    dlg.hide()

    # Return the command to be executed on clients
    return msg
