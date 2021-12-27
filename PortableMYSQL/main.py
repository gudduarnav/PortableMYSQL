# Portable MySQL
# Developed by Arnav Mukhopadhyay
# EMAIL: gudduarnav@gmail.com
# ******* Run MySQL on Windows from USB without installing ****************
# MySQL Server included and ready to go

import PySimpleGUI as sg
import shutil
from configparser import ConfigParser
import os
import subprocess
from time import sleep

def save_settings(c : ConfigParser, fname: str):
    with open(fname, "w") as f:
        c.write(f)


def init_daemon(settings : dict, bSecure : bool):
    host = settings["host"]
    port = settings["port"]
    admin_host = settings["admin_host"]
    admin_port = settings["admin_port"]
    user = settings["user"]
    password = settings["password"]

    base_dir = settings["base_dir"]
    bin_dir = base_dir + "/" + settings["bin_dir"]
    data_dir = base_dir + "/" + settings["data_dir"]
    daemon = bin_dir + "/" + settings["daemon"]
    sqladmin = bin_dir + "/" + settings["sqladmin"]

    base_dir = os.path.abspath(base_dir)
    bin_dir = os.path.abspath(bin_dir)
    data_dir = os.path.abspath(data_dir)
    daemon = os.path.abspath(daemon)
    sqladmin = os.path.abspath(sqladmin)

    print("host=", host, "port=", port)
    print("admin host=", host, "port=", port)
    print("user=", user)
    print("base_dir=", base_dir)
    print("bin_dir=", bin_dir)
    print("data_dir=", data_dir)
    print("daemon=", daemon)
    print("sqladmin=", sqladmin)

    if not os.path.isdir(base_dir):
        sg.PopupError(base_dir+" base directory not found", title="Error")
        return

    if not os.path.isdir(bin_dir):
        sg.PopupError(bin_dir+" bin directory not found", title="Error")
        return

    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)
        if not os.path.isdir(data_dir):
            sg.PopupError(data_dir+" data directory not found", title="Error")
            return

    if not os.path.isfile(daemon):
        sg.PopupError(daemon+" daemon not found", title="Error")
        return

    if not os.path.isfile(sqladmin):
        sg.PopupError(sqladmin+" sqladmin not found", title="Error")
        return

    print("Clean up data directory", data_dir)
    shutil.rmtree(data_dir)
    print("Cleared", data_dir)

    print("Create data_dir", data_dir)
    os.mkdir(data_dir)
    if not os.path.isdir(data_dir):
        sg.PopupError(data_dir+" data directory not found", title="Error")
        return
    print("Data dir", data_dir, "created")

    exe_param = [
        daemon,
        "--basedir={}".format(base_dir),
        "--datadir={}".format(data_dir),
        "--admin-address={}".format(admin_host),
        "--admin-port={}".format(admin_port),
        "--bind-address={}".format(host),
        "--port={}".format(port),
        "--console"
    ]
    if bSecure:
        exe_param.append("--initialize")
    else:
        exe_param.append("--initialize-insecure")
    print(exe_param)

    subprocess.Popen(exe_param).wait()
    print("MYSQL Intialization complete")

    sg.PopupOK("MYSQL Server and Database initialized", title="MYSQL Server Initialized")








def start_daemon(settings : dict):
    host = settings["host"]
    port = settings["port"]
    admin_host = settings["admin_host"]
    admin_port = settings["admin_port"]
    user = settings["user"]
    password = settings["password"]

    base_dir = settings["base_dir"]
    bin_dir = base_dir + "/" + settings["bin_dir"]
    data_dir = base_dir + "/" + settings["data_dir"]
    daemon = bin_dir + "/" + settings["daemon"]
    sqladmin = bin_dir + "/" + settings["sqladmin"]

    base_dir = os.path.abspath(base_dir)
    bin_dir = os.path.abspath(bin_dir)
    data_dir = os.path.abspath(data_dir)
    daemon = os.path.abspath(daemon)
    sqladmin = os.path.abspath(sqladmin)

    print("host=", host, "port=", port)
    print("admin host=", host, "port=", port)
    print("user=", user)
    print("base_dir=", base_dir)
    print("bin_dir=", bin_dir)
    print("data_dir=", data_dir)
    print("daemon=", daemon)
    print("sqladmin=", sqladmin)

    if not os.path.isdir(base_dir):
        sg.PopupError(base_dir+" base directory not found", title="Error")
        return

    if not os.path.isdir(bin_dir):
        sg.PopupError(bin_dir+" bin directory not found", title="Error")
        return

    if not os.path.isdir(data_dir):
        sg.PopupError(data_dir+" data directory not found", title="Error")
        return

    if not os.path.isfile(daemon):
        sg.PopupError(daemon+" daemon not found", title="Error")
        return

    if not os.path.isfile(sqladmin):
        sg.PopupError(sqladmin+" sqladmin not found", title="Error")
        return

    exe_param = [
        daemon,
        "--basedir={}".format(base_dir),
        "--datadir={}".format(data_dir),
        "--admin-address={}".format(admin_host),
        "--admin-port={}".format(admin_port),
        "--bind-address={}".format(host),
        "--port={}".format(port),
        "--console"
    ]
    print(exe_param)

    h = subprocess.Popen(exe_param, creationflags=subprocess.CREATE_NEW_CONSOLE)
    for _ in range(3):
        try:
            h.wait(timeout=5)
        except:
            if h.returncode is not None:
                sg.PopupError("MYSQL Server Crashed", title="ERROR")
                return
            else:
                print("MySQL server running now...")
    print("MYSQL Server started")

    subprocess.Popen([
        sqladmin,
        "--host={}".format(admin_host),
        "--port={}".format(admin_port),
        "--user={}".format(user),
        "--password={}".format(password),
        "status"
    ]).wait()

    for _ in range(3):
        try:
            h.wait(timeout=5)
        except:
            if h.returncode is not None:
                sg.PopupError("MYSQL Server Crashed", title="ERROR")
                return
            else:
                print("MySQL server running now...")
    print("MYSQL Server is properly running")
    sg.PopupOK("MYSQL Server running", title="MYSQL Server Started")


def stop_daemon(settings : dict):
    host = settings["host"]
    port = settings["port"]
    admin_host = settings["admin_host"]
    admin_port = settings["admin_port"]
    user = settings["user"]
    password = settings["password"]

    base_dir = settings["base_dir"]
    bin_dir = base_dir + "/" + settings["bin_dir"]
    data_dir = base_dir + "/" + settings["data_dir"]
    daemon = bin_dir + "/" + settings["daemon"]
    sqladmin = bin_dir + "/" + settings["sqladmin"]

    base_dir = os.path.abspath(base_dir)
    bin_dir = os.path.abspath(bin_dir)
    data_dir = os.path.abspath(data_dir)
    daemon = os.path.abspath(daemon)
    sqladmin = os.path.abspath(sqladmin)

    print("host=", host, "port=", port)
    print("admin host=", host, "port=", port)
    print("user=", user)
    print("base_dir=", base_dir)
    print("bin_dir=", bin_dir)
    print("data_dir=", data_dir)
    print("daemon=", daemon)
    print("sqladmin=", sqladmin)

    if not os.path.isdir(base_dir):
        return

    if not os.path.isdir(bin_dir):
        return

    if not os.path.isdir(data_dir):
        return

    if not os.path.isfile(daemon):
        return

    if not os.path.isfile(sqladmin):
        return

    subprocess.Popen([
        sqladmin,
        "--host={}".format(admin_host),
        "--port={}".format(admin_port),
        "--user={}".format(user),
        "--password={}".format(password),
        "shutdown"
    ]).wait()
    sleep(15)


    print("MYSQL Server stopped")










def mainWindow():
    if "nt" not in os.name.lower().strip():
        sg.PopupError("Windows OS not detected.", title="Windows Required")
        exit(1)

    config = ConfigParser()
    config_filename=os.path.abspath("./config.ini")
    print("Configuration File:", config_filename)
    config.read(config_filename)

    if "mysqld" not in config.sections():
        config["mysqld"] = {
            "host": "127.0.0.1",
            "port": 36000,
            "user": "root",
            "password": "",
            "admin_host": "127.0.0.1",
            "admin_port": 36001,
            "base_dir": ".",
            "bin_dir": "/bin",
            "data_dir": "/data",
            "daemon": "mysqld.exe",
            "sqladmin": "mysqladmin.exe"
        }

        save_settings(config, config_filename)

    config_sqld = config["mysqld"]


    layout = [
        [sg.Text("CLIENT Host"), sg.InputText(default_text=config_sqld["host"], key="host", size=(20,1)),
         sg.Text("Port"), sg.InputText(default_text=config_sqld["port"], key="port", size=(7,1)),],
        [sg.Text("ADMIN  Host"), sg.InputText(default_text=config_sqld["admin_host"], key="admin_host", size=(20,1)), sg.Text("Port"),
         sg.InputText(default_text=config_sqld["admin_port"], key="admin_port", size=(7,1)), ],

        [sg.Text("Username"), sg.InputText(default_text=config_sqld["user"], key="user", size=(20, 1)),
         sg.Text("Password"),
         sg.InputText(default_text=config_sqld["password"], key="password", size=(20, 1)), ],

        [sg.Text("MYSQL Base Directory"), sg.InputText(default_text=config_sqld["base_dir"], key="base_dir")],
        [sg.Text("MYSQL Bin  Directory"), sg.InputText(default_text=config_sqld["bin_dir"], key="bin_dir")],
        [sg.Text("MYSQL Data Directory"), sg.InputText(default_text=config_sqld["data_dir"], key="data_dir")],
        [sg.Text("MYSQL Daemon"), sg.InputText(default_text=config_sqld["daemon"], key="daemon")],
        [sg.Text("MYSQL Admin "), sg.InputText(default_text=config_sqld["sqladmin"], key="sqladmin")],

        [
            sg.Button("Start", key="btnStart"),
            sg.Button("Stop", key="btnStop"),
            sg.Button("Reset Secure", key="btnResetSecure"),
            sg.Button("Reset Insecure", key="btnResetInsecure"),
            sg.Button("Save", key="btnSave"),
            sg.Button("Exit", key="btnExit")
        ]
    ]

    w = sg.Window(title="Portable MySQL", layout=layout, size=(512,320))

    while True:
        event, values = w.read()

        if event is None or event is sg.WINDOW_CLOSED or event == "btnExit":
            w.hide()
            stop_daemon(values)
            break
        elif event == "btnSave":
            w.hide()
            config["mysqld"] = {
                "host": values["host"],
                "port": values["port"],
                "user": values["user"],
                "password": values["password"],
                "admin_host": values["admin_host"],
                "admin_port": values["admin_port"],
                "base_dir": values["base_dir"],
                "bin_dir": values["bin_dir"],
                "data_dir": values["data_dir"],
                "daemon": values["daemon"],
                "sqladmin": values["sqladmin"]
            }
            save_settings(config, config_filename)
            sg.PopupOK("Settings saved to "+ config_filename, title="Saved")
            w.un_hide()
        elif event == "btnStart":
            w.hide()
            start_daemon(settings=values)
            w.un_hide()
        elif event == "btnStop":
            w.hide()
            stop_daemon(values)
            sg.PopupOK("MYSQL Server stopped", title="MYSQL Server Stopped")
            w.un_hide()
        elif event == "btnResetSecure":
            w.hide()
            stop_daemon(values)
            init_daemon(values, True)
            w.un_hide()
        elif event == "btnResetInsecure":
            w.hide()
            stop_daemon(values)
            init_daemon(values, False)
            w.un_hide()

    w.close()

if __name__=="__main__":
    mainWindow()