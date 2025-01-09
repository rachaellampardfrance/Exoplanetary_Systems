import os

from helpers import get_user_confirm, render_figlet

def main():
    render_figlet("Data Gatherer")

    message = "Request updated data? "
    if get_user_confirm(message):
        os.system("py helpers/stellar_hosts_data.py")
        os.system("py helpers/stellar_data.py")
        os.system("py helpers/planetary_data.py")

    message = "Create new figures Y/N?  "
    if get_user_confirm(message):
        os.system("py helpers/plots.py")

    print("Exiting...")

if __name__ == "__main__":
    main()