# DON'T REMOVE BELOW AUTHOR LINE
# AUTHOR => AjRaj
# Github => github/iamajraj
import requests
import json
from os import system, name
# COLOR OPTION


class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
# CLEAR FUNCTION


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
# LOGO


def logo():
    print(bcolors.GREEN + bcolors.BOLD + r"""
           ____                      ,
          /---.'.__  WORDPRESS  ____//
               '--.\\ USERNAME  /.---'
          _______  \\ FINDER  //
        /.------.\  \|      .'/  ______
       //  ___  \ \ ||/|\  //  _/_----.\__
      |/  /.-.\  \ \:|< >|// _/.'..\   '--'
         //   \'. | \'.|.'/ /_/ /  \\
        //     \ \_\/" ' ~\-'.-'    \\
       //       '-._| :A: |'-.__     \\
      //           (/'==='\)'-._\     ||
      ||                        \\    \|
      ||                         \\    '
      |/ AUTHOR: github/iamajraj  \\
                                   ||
                                   ||
                                   \\
                                    '""" + bcolors.ENDC)
# URL VALIDATION FUNCTION
def validate_url(url: str) -> str:
    """Basic URL validation and formatting"""
    if not url:
        raise ValueError("URL cannot be empty")
    
    # Remove whitespace and ensure proper protocol
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    return url


def find_username():
    """Function to find WordPress username (first user only)"""
    print(bcolors.BLUE + "Enter the URL (example.com or www.example.com): ")
    user_input = input(": ").strip()
    
    try:
        # Validate and format URL
        url = validate_url(user_input)
        api_url = url + "/wp-json/wp/v2/users"
        
        print(bcolors.BLUE + "Fetching data..." + bcolors.ENDC)
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        data = response.json()
        
        if not data or len(data) == 0:
            print(bcolors.FAIL + "No users found or WordPress API not accessible!" + bcolors.ENDC)
            return
            
        result = data[0]["slug"]
        print(bcolors.GREEN + "Success! Username found: " + bcolors.BOLD + result + bcolors.ENDC)
        
    except requests.exceptions.Timeout:
        print(bcolors.FAIL + "Error: Request timed out. Please check the URL and try again." + bcolors.ENDC)
    except requests.exceptions.ConnectionError:
        print(bcolors.FAIL + "Error: Could not connect to the website. Please check the URL." + bcolors.ENDC)
    except requests.exceptions.HTTPError as e:
        print(bcolors.FAIL + f"Error: HTTP {e.response.status_code} - {e.response.reason}" + bcolors.ENDC)
    except json.JSONDecodeError:
        print(bcolors.FAIL + "Error: Invalid response format. This might not be a WordPress site." + bcolors.ENDC)
    except KeyError:
        print(bcolors.FAIL + "Error: Username field not found in response." + bcolors.ENDC)
    except ValueError as e:
        print(bcolors.FAIL + f"Error: {str(e)}" + bcolors.ENDC)
    except Exception as e:
        print(bcolors.FAIL + f"Unexpected error occurred: {str(e)}" + bcolors.ENDC)


def find_multiple_usernames():
    """Function to find multiple WordPress usernames by scanning user IDs"""
    print(bcolors.BLUE + "Enter the URL (example.com or www.example.com): ")
    user_input = input(": ").strip()
    
    print(bcolors.BLUE + "Enter the maximum user ID to scan (default: 10): ")
    max_id_input = input(": ").strip()
    
    try:
        max_id = int(max_id_input) if max_id_input else 10
        if max_id <= 0:
            print(bcolors.FAIL + "Error: Maximum ID must be a positive number!" + bcolors.ENDC)
            return
    except ValueError:
        print(bcolors.FAIL + "Error: Please enter a valid number!" + bcolors.ENDC)
        return
    
    try:
        # Validate and format URL
        url = validate_url(user_input)
        
        print(bcolors.BLUE + f"Scanning user IDs from 1 to {max_id}..." + bcolors.ENDC)
        found_users = []
        
        for user_id in range(1, max_id + 1):
            try:
                api_url = f"{url}/wp-json/wp/v2/users/{user_id}"
                response = requests.get(api_url, timeout=5)
                
                if response.status_code == 200:
                    user_data = response.json()
                    username = user_data.get("slug", "N/A")
                    name = user_data.get("name", "N/A")
                    found_users.append({
                        "id": user_id,
                        "username": username,
                        "name": name
                    })
                    print(bcolors.GREEN + f"✓ ID {user_id}: {username} ({name})" + bcolors.ENDC)
                elif response.status_code == 404:
                    print(bcolors.FAIL + f"✗ ID {user_id}: User not found" + bcolors.ENDC)
                else:
                    print(bcolors.FAIL + f"✗ ID {user_id}: HTTP {response.status_code}" + bcolors.ENDC)
                    
            except requests.exceptions.Timeout:
                print(bcolors.FAIL + f"✗ ID {user_id}: Timeout" + bcolors.ENDC)
            except Exception as e:
                print(bcolors.FAIL + f"✗ ID {user_id}: Error - {str(e)}" + bcolors.ENDC)
        
        # Summary
        print("\n" + bcolors.HEADER + "=" * 50 + bcolors.ENDC)
        print(bcolors.HEADER + "SCAN SUMMARY" + bcolors.ENDC)
        print(bcolors.HEADER + "=" * 50 + bcolors.ENDC)
        
        if found_users:
            print(bcolors.GREEN + f"Found {len(found_users)} user(s):" + bcolors.ENDC)
            for user in found_users:
                print(bcolors.BOLD + f"ID: {user['id']} | Username: {user['username']} | Name: {user['name']}" + bcolors.ENDC)
        else:
            print(bcolors.FAIL + "No users found!" + bcolors.ENDC)
            
    except requests.exceptions.Timeout:
        print(bcolors.FAIL + "Error: Request timed out. Please check the URL and try again." + bcolors.ENDC)
    except requests.exceptions.ConnectionError:
        print(bcolors.FAIL + "Error: Could not connect to the website. Please check the URL." + bcolors.ENDC)
    except ValueError as e:
        print(bcolors.FAIL + f"Error: {str(e)}" + bcolors.ENDC)
    except Exception as e:
        print(bcolors.FAIL + f"Unexpected error occurred: {str(e)}" + bcolors.ENDC)


# MAIN START
def main():
    while True:
        clear()
        logo()
        print(bcolors.HEADER + "*******" + bcolors.UNDERLINE + "Welcome to WP Username Finder!" +
              bcolors.ENDC + bcolors.HEADER + "******" + bcolors.ENDC)
        print(bcolors.BLUE + "Select Options:")
        print("1. Find Username (First User)")
        print("2. Scan Multiple User IDs")
        print("3. Exit")
        
        inp = input("Choose: ").strip()
        
        if inp == "1":
            clear()
            logo()
            find_username()
            input(bcolors.BLUE + "\nPress Enter to continue..." + bcolors.ENDC)
        elif inp == "2":
            clear()
            logo()
            find_multiple_usernames()
            input(bcolors.BLUE + "\nPress Enter to continue..." + bcolors.ENDC)
        elif inp == "3":
            print(bcolors.GREEN + "Have a nice day!" + bcolors.ENDC)
            break
        else:
            print(bcolors.FAIL + "Invalid option selected. Please try again." + bcolors.ENDC)
            input(bcolors.BLUE + "Press Enter to continue..." + bcolors.ENDC)


if __name__ == "__main__":
    main()
