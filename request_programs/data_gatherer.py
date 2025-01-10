import os

from helpers import get_user_confirm, render_figlet

def main():
    render_figlet("Data Gatherer")

    message = "Request updated data? "
    if get_user_confirm(message):
        os.system("py request_programs/stellar_hosts_data.py")
        os.system("py request_programs/stellar_data.py")
        os.system("py request_programs/planetary_data.py")

    message = "Create new figures Y/N?  "
    if get_user_confirm(message):
        os.system("py request_programs/plots.py")

    print("Exiting...")

if __name__ == "__main__":
    main()