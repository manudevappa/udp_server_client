#!/usr/bin/env python3
# coding: UTF-8

# code extracted from nigiri
# Got running on current version and Python3

import os
import datetime
import sys
import traceback
import re
import logging
import locale
import ipaddress
import urwid
from urwid import MetaSignals
from datetime import datetime
import threading
import socket
import time
import json
IP_Found = False

#debug 
DEBUG_ENABLE = True
# Server information
server_ip = ''  # Replace with the server IP address
server_port = 12345  # Replace with the server port number
join_request_send = False
ClientUserName = None

class ExtendedListBox(urwid.ListBox):
    """
        Listbow widget with embeded autoscroll
    """

    __metaclass__ = urwid.MetaSignals
    signals = ["set_auto_scroll"]


    def set_auto_scroll(self, switch):
        if type(switch) != bool:
            return
        self._auto_scroll = switch
        urwid.emit_signal(self, "set_auto_scroll", switch)


    auto_scroll = property(lambda s: s._auto_scroll, set_auto_scroll)


    def __init__(self, body):
        urwid.ListBox.__init__(self, body)
        self.auto_scroll = True


    def switch_body(self, body):
        if self.body:
            urwid.disconnect_signal(body, "modified", self._invalidate)

        self.body = body
        self._invalidate()

        urwid.connect_signal(body, "modified", self._invalidate)


    def keypress(self, size, key):
        urwid.ListBox.keypress(self, size, key)

        if key in ("page up", "page down"):
            logging.debug("focus = %d, len = %d" % (self.get_focus()[1], len(self.body)))
            if self.get_focus()[1] == len(self.body)-1:
                self.auto_scroll = True
            else:
                self.auto_scroll = False
            logging.debug("auto_scroll = %s" % (self.auto_scroll))


    def scroll_to_bottom(self):
        logging.debug("current_focus = %s, len(self.body) = %d" % (self.get_focus()[1], len(self.body)))

        if self.auto_scroll:
            # at bottom -> scroll down
            self.set_focus(len(self.body)-1)



"""
 -------context-------
| --inner context---- |
|| HEADER            ||
||                   ||
|| BODY              ||
||                   ||
|| DIVIDER           ||
| ------------------- |
| FOOTER              |
 ---------------------

inner context = context.body
context.body.body = BODY
context.body.header = HEADER
context.body.footer = DIVIDER
context.footer = FOOTER

HEADER = Notice line (urwid.Text)
BODY = Extended ListBox
DIVIDER = Divider with information (urwid.Text)
FOOTER = Input line (Ext. Edit)
"""



class MainWindow(object):

    __metaclass__ = MetaSignals
    signals = ["quit","keypress"]

    _palette = [
            ('divider','black','dark cyan', 'standout'),
            ('text','light gray', 'default'),
            ('bold_text', 'light gray', 'default', 'bold'),
            ("body", "text"),
            ("footer", "text"),
            ("header", "text"),
        ]

    for type, bg in (
            ("div_fg_", "dark cyan"),
            ("", "default")):
        for name, color in (
                ("red","dark red"),
                ("blue", "dark blue"),
                ("green", "dark green"),
                ("yellow", "yellow"),
                ("magenta", "dark magenta"),
                ("gray", "light gray"),
                ("white", "white"),
                ("black", "black")):
            _palette.append( (type + name, color, bg) )


    def __init__(self, sender="1234567890"):
        self.shall_quit = False
        self.sender = sender
        self.IP_Found = False
        self.ClientUserName = "PC User"
        #self.generic_output_walker = []  # Define the generic_output_walker attribute as an empty list
        #self.body = None  # Initialize the body attribute as None

    def main(self):
        """ 
            Entry point to start UI 
        """

        self.ui = urwid.raw_display.Screen()
        self.ui.register_palette(self._palette)
        self.build_interface()
        self.ui.run_wrapper(self.run)


    def run(self):
        """ 
            Setup input handler, invalidate handler to
            automatically redraw the interface if needed.

            Start mainloop.
        """

        # I don't know what the callbacks are for yet,
        # it's a code taken from the nigiri project
        def input_cb(key):
            if self.shall_quit:
                raise urwid.ExitMainLoop
            self.keypress(self.size, key)

        self.size = self.ui.get_cols_rows()

        self.main_loop = urwid.MainLoop(
                self.context,
                screen=self.ui,
                handle_mouse=False,
                unhandled_input=input_cb,
            )

        def call_redraw(*x):
            self.draw_interface()
            invalidate.locked = False
            return True

        inv = urwid.canvas.CanvasCache.invalidate

        def invalidate (cls, *a, **k):
            inv(*a, **k)

            if not invalidate.locked:
                invalidate.locked = True
                self.main_loop.set_alarm_in(0, call_redraw)

        invalidate.locked = False
        urwid.canvas.CanvasCache.invalidate = classmethod(invalidate)
        
        try:
            socketThread.start()
            self.main_loop.run()
        except KeyboardInterrupt:
            self.quit()


    def quit(self, exit=True):
        """ 
            Stops the ui, exits the application (if exit=True)
        """
        urwid.emit_signal(self, "quit")

        self.shall_quit = True

        if exit:
            sys.exit(0)


    def build_interface(self):
        """ 
            Call the widget methods to build the UI 
        """

        self.header = urwid.Text("Chat")
        self.footer = urwid.Edit("> ")
        self.divider = urwid.Text("Initializing.")

        self.generic_output_walker = urwid.SimpleListWalker([])
        self.body = ExtendedListBox(
            self.generic_output_walker)


        self.header = urwid.AttrWrap(self.header, "divider")
        self.footer = urwid.AttrWrap(self.footer, "footer")
        self.divider = urwid.AttrWrap(self.divider, "divider")
        self.body = urwid.AttrWrap(self.body, "body")

        self.footer.set_wrap_mode("space")

        main_frame = urwid.Frame(self.body, 
                                header=self.header,
                                footer=self.divider)
        
        self.context = urwid.Frame(main_frame, footer=self.footer)

        self.divider.set_text(("divider",
                               ("Send message:")))

        self.context.set_focus("footer")


    def draw_interface(self):
        self.main_loop.draw_screen()


    def keypress(self, size, key):
        """ 
            Handle user inputs
        """

        urwid.emit_signal(self, "keypress", size, key)

        # scroll the top panel
        if key in ("page up","page down"):
            self.body.keypress (size, key)

        # resize the main windows
        elif key == "window resize":
            self.size = self.ui.get_cols_rows()

        elif key in ("ctrl d", 'ctrl c'):
            self.quit()

        elif key == "enter":
            # Parse data or (if parse failed)
            # send it to the current world
            text = self.footer.get_edit_text()

            self.footer.set_edit_text(" "*len(text))
            self.footer.set_edit_text("")

            if text in ('/quit', '/q'):
                data_to_send  = self.json_encode(None, "quit", self.ClientUserName, None)
                self.send_socket(data_to_send)
                time.sleep(5)
                self.quit()

            if "/ip" in text:   
                input = text.split(' ')
                size = len(input)
                if size == 1:
                    if DEBUG_ENABLE:
                        self.print_sent_message("IP Missing!", "right")
                else:
                    try:
                        server_ip = ipaddress.ip_address(input[1])
                        temp_text = "Server IP Updated " + input[1]
                        self.print_text(temp_text)
                        # Create a UDP socket
                        self.IP_Found = True

                    except ValueError:
                        # If the input is not a valid IP address, catch the exception and print an error message    
                        self.print_text("Invalid IP address")
                        size = len(text)

            elif "/join" in text:
                join_request_send = True
                self.ClientUserName = text[6:]
                data_to_send  = self.json_encode(None, "join", self.ClientUserName, None)
                self.send_socket(data_to_send)
            elif text.strip():
                if self.IP_Found == True:
                    self.print_sent_message(text, "right")
                    encoded_data  = self.json_encode(None, "group", self.ClientUserName, text)
                    self.send_socket(encoded_data)
                else:
                    self.print_text("Enter UDP Server IP : \"/ip <server_ip_address>\"")

                
        else:
            self.context.keypress (size, key)

    def print_sent_message(self, text, print_where):
        """
            Print a sent message
        """
        # Send the message to the server
        current_time = datetime.now().strftime(" : %I:%M:%S %p")
        
        time_text =  text + current_time;
        time_text = urwid.Text(time_text)
        time_text.set_align_mode(print_where)
        self.print_text(time_text)
        
    def print_received_message(self, text, where):
        """
            Print a Received message
        """
            
        current_time = datetime.now().strftime("%I:%M:%S %p : ")
        time_text =  current_time + text;
        time_text = urwid.Text(time_text)
        time_text.set_align_mode(where)
        self.print_text(time_text)
        self.main_loop.draw_screen()

    def print_text(self, text):
        """
            Print the given text in the _current_ window
            and scroll to the bottom. 
            You can pass a Text object or a string
        """

        walker = self.generic_output_walker

        if not isinstance(text, urwid.Text):
            text = urwid.Text(text)

        walker.append(text)

        self.body.scroll_to_bottom()


    def get_time(self):
        """
            Return formated current datetime
        """
        return datetime.datetime.now().strftime('%H:%M:%S')

    def json_encode(self, towhome, message_type, uname, message):
        # Create a dictionary
        data = {
            'to_whom'   : towhome,
            'type'      : message_type,
            'u_name'    : uname,
            'message'   : message
        }
        # Convert the dictionary to a JSON string   
        json_data = json.dumps(data)
        # Return the JSON object
        return json_data

    def send_socket(self, socket_data):
        server_ip = '192.168.0.136'
        client_socket.sendto(socket_data.encode(), (server_ip, server_port))

def except_hook(extype, exobj, extb, manual=False):
    if not manual:
        try:
            main_window.quit(exit=False)
        except NameError:
            pass

    message = _("An error occured:\n%(divider)s\n%(traceback)s\n"\
        "%(exception)s\n%(divider)s" % {
            "divider": 20*"-",
            "traceback": "".join(traceback.format_tb(extb)),
            "exception": extype.__name__+": "+str(exobj)
        })

    logging.error(message)

    print >> sys.stderr, message


def setup_logging():
    """ set the path of the logfile to tekka.logfile config
        value and create it (including path) if needed.
        After that, add a logging handler for exceptions
        which reports exceptions catched by the logger
        to the tekka_excepthook. (DBus uses this)
    """
    try:
        class ExceptionHandler(logging.Handler):
            """ handler for exceptions caught with logging.error.
                dump those exceptions to the exception handler.
            """
            def emit(self, record):
                if record.exc_info:
                    except_hook(*record.exc_info)

        logfile = '/tmp/log.log'
        logdir = os.path.dirname(logfile)

        if not os.path.exists(logdir):
            os.makedirs(logdir)

        logging.basicConfig(filename=logfile, level=logging.DEBUG,
            filemode="w")

        logging.getLogger("").addHandler(ExceptionHandler())

    except BaseException(e):
        print >> sys.stderr, "Logging init error: %s" % (e)


def receiveSocket():
    while True:
        response, server_address = client_socket.recvfrom(1024)
        raw_json = response.decode()
        formatted_json = json.loads(raw_json)
        match formatted_json['to_whom']:
            case "self":
                if formatted_json['type'] == "join_ack":
                    main_window.print_received_message("You Joined Channel", "center")
                elif formatted_json['type'] == "quit_ack":
                    main_window.print_received_message("You Left Channel", "center")
                else:
                    main_window.print_received_message("Error <I_unknow_type>", "center")
            case "group":
                if formatted_json['type'] == "new_joinee":
                    temp_text = formatted_json['u_name'] + " Joined Channel"
                    main_window.print_received_message(temp_text, "center")

                elif formatted_json['type'] == "someone_left":
                    temp_text = formatted_json['u_name'] + " Left Channel"
                    main_window.print_received_message(temp_text, "center")                    

                elif formatted_json['type'] == "group":
                    temp_text = formatted_json['u_name'] + " : " + formatted_json['message']
                    main_window.print_received_message(temp_text, "left")
                else:
                    main_window.print_received_message("Error <G_unknow_type>", "center")

if __name__ == "__main__":
    
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    setup_logging()
    main_window = MainWindow()  

    socketThread     = threading.Thread(target=receiveSocket)

    main_window.main()
    
    #p2.join()
    """

    sys.excepthook = except_hook
    p1 = Process(target=main_window.main())
    p1.start()
    #p1.join()
    """
    #main_window.main()