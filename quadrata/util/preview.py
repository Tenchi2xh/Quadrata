import base64
import webbrowser
from subprocess import Popen, PIPE


def open_in_same_tab(url):
    script = '''tell application "Google Chrome"
                    tell front window
                        set URL of active tab to "%s"
                    end tell
                end tell ''' % url.replace('"', '%22')

    p = Popen(["osascript", "-"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(bytes(script, encoding="utf-8"))


def preview(data, mimetype="image/svg+xml"):
    b64 = base64.b64encode(bytes(data, "utf-8"))
    browser = webbrowser.get("chrome")
    open_in_same_tab("data:%s;base64,%s" % (mimetype, b64.decode("utf-8")))
