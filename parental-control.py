# NOTE: This file should be copied to /etc/parental-control directory
import sys
import datetime
import subprocess
import os


COL_USER = 0
COL_FUNC = 1
COL_WKDY = 2
COL_SU = COL_WKDY
COL_MO = COL_SU + 1
COL_TU = COL_SU + 2
COL_WE = COL_SU + 3
COL_TH = COL_SU + 4
COL_FR = COL_SU + 5
COL_SA = COL_SU + 6

# F U N C T I O N S
def get_cfg_file_path(cfg_file):
    return os.path.dirname(cfg_file)


def stop_internet_connection():
    subprocess.run(["iptables", "-F"])


def restore_internet_connection(res_file):
    print("res_file = ", res_file)
    stop_internet_connection()
    subprocess.run(["iptables-restore", "-c", "<", res_file], timeout=1, shell=True)


def get_current_user():
    return subprocess.run(["who"], stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()[-1].split()[0]


def logout_user(user):
    subprocess.run(["skill", "-KILL", "-u", user])


def get_timespent_by_user(user, ac_output):
    tspent = 0
    for line in reversed(ac_output):
        if "Today" in line:
            continue
        if user in line:
            tspent = float(line.split()[1]) * 60
            break
    return tspent


def get_timeallowed_user(user, function, cfg_table):
    tallowed = 7 * 24 * 60.0
    for row in cfg_table:
        if row[COL_USER] == user and row[COL_FUNC] == function:
            wkday = datetime.datetime.today().weekday() + COL_WKDY
            tallowed = float(row[wkday])
            break
    return tallowed


# Commandline Argument: this, config-file, log-file
CMDL_ARGS = 2
if len(sys.argv) >= CMDL_ARGS:
    cfg_file    = sys.argv[1]
    cfg_path    = get_cfg_file_path(cfg_file)
    username = get_current_user()
else:
    print("Not enough arguments passed (", len(sys.argv), " >= ", CMDL_ARGS, ")")
    print(sys.argv)
    exit(-1)


# Read configurations from configuration file
with open(cfg_file) as f:
    contents = f.readlines()

cfg_table = []
for line in contents:
    sline = line.replace(" ", "").replace("\t", "").replace("\n", "")
    if len(sline) == 0:
        continue
    if sline[0] == '#':
        continue
    cfg_table.append(line.split())


# Find out how many minutes the user had already spent
ac_output = subprocess.run(["ac", "-dp"], stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
time_spent = get_timespent_by_user(username, ac_output)
print("time_spent by", username, "=", time_spent, "minutes")

# Find out how many minutes the user is allowed today
login_allowed = get_timeallowed_user(username, "login", cfg_table)
brows_allowed = get_timeallowed_user(username, "http", cfg_table)
print("time_allowed: login =", login_allowed, "browsing =", brows_allowed, "minutes")

# Check and take actions
if login_allowed < 24 * 60.0:
    print("Restore connections (if stopped in previous login)")
    restore_internet_connection(cfg_path + "/parental-control.ip.rules.v4")
    if time_spent > brows_allowed:
        print("stopping internet!")
        stop_internet_connection()
    if time_spent > login_allowed:
        print("logging out user")
        logout_user(username)


now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")
time = now.strftime("%H:%M")


print("username = ", username)
print(date, " ", time)
