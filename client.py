from os import error
import socket
import threading
from py_cui.keys import KEY_ENTER

from py_cui.widgets import ScrollMenu, ScrollTextBlock, TextBox
import common
import sys
import datetime
from rich import print
import py_cui

TERMIMAL_ROWS = 10
TERMINAL_COLS = 10
nickname: str = ""
isConnected: bool = False
root = py_cui.PyCUI(TERMIMAL_ROWS, TERMINAL_COLS)
connected_list: ScrollMenu = None
chat_log: ScrollTextBlock = None
message_bar: TextBox = None
client = None
user_list: list = []


def create_gui():
    global connected_list
    global chat_log
    global message_bar

    root.title_bar = None

    logo = root.add_block_label(common.get_ascii_logo(), row=0, column=2,
                                row_span=3, column_span=TERMINAL_COLS - 2, center=True)

    logo.set_selectable = False

    connected_list = root.add_scroll_menu(
        title='Connected Clients', row=0, column=0, row_span=TERMIMAL_ROWS, column_span=TERMINAL_COLS - 8)

    connected_list.set_focus_text(
        "Use Arrow keys, Page Up / Page Dn / Home / End to navigate the Connected List. Press 'esc' to stop focusing.")

    chat_log = root.add_text_block(
        title='Chat Log', row=1, column=2, row_span=TERMIMAL_ROWS - 2, column_span=TERMINAL_COLS - 2)

    chat_log.set_focus_text(
        "Use Arrow keys, Page Up / Page Dn / Home / End to navigate the Chat Log. Press 'esc' to stop focusing.")

    message_bar = root.add_text_box(
        title='Message', row=9, column=2, column_span=TERMINAL_COLS - 2)

    message_bar.set_focus_text(
        "Type a message and press 'enter' to send it. Tip: you can format your message using markup, for example [b magenta]will make your text bold and magenta[/b magenta]. Press 'esc' to stop focusing.")

    message_bar.add_key_command(KEY_ENTER, write)

    root.run_on_exit(leave)

    root.show_text_box_popup("Enter a nickname", command=login)

    root.set_refresh_timeout(1)

    root.start()


def connect():
    try:
        global client
        # socket initialization
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connecting client to server
        client.connect((sys.argv[1], int(sys.argv[2])))

        global isConnected
        isConnected = True

        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

    except ConnectionError:
        report_error(
            "Unable to connect to chat room, please check address and port and try again")


def receive():
    global client
    while isConnected:  # making valid connection
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
                connected_list.add_item(message)
            else:
                chat_log.set_text(chat_log.get() + "\n" + message)
        except error:  # case on wrong ip/port details
            client.close()
            break


def write():
    global client
    if isConnected:  # message layout
        message = message_bar.get()
        message_bar.clear()
        timestamp = datetime.datetime.now()
        formatted_message = '{} {}: {}'.format(timestamp, nickname, message)
        client.send(formatted_message.encode('ascii'))


def report_error(error: str):
    timestamp = datetime.datetime.now()
    print("[bold red]{} {}[/bold red]".format(timestamp, error))
    quit()


def leave():
    global client
    global isConnected
    if isConnected is True:
        timestamp = datetime.datetime.now()
        message = '{} {}: has left the chat room'.format(timestamp, nickname)
        client.send(message.encode('ascii'))
        isConnected = False
        quit()
    else:
        quit()


def login(new_nickname: str):
    global nickname
    nickname = new_nickname
    connect()


if len(sys.argv) < 2:
    print("Failed to start client\nUsage: client.py server_ip port")
    quit()

common.try_import("py-cui")
common.try_import("rich")

create_gui()
