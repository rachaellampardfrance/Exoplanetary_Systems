import os

from helpers import get_user_confirm

message = "Request updated data? "
if get_user_confirm(message):
    os.system("py helpers/stellar_hosts_data.py")
    os.system("py helpers/stellar_data.py")
    os.system("py helpers/planetary_data.py")

message = "Create new figures? "
if get_user_confirm(message):
    os.system("py helpers/plots.py")

print("Exiting...")