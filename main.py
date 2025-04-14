import os
import json
import llm_interface
from utils import list_directories
from colorama import init, Fore, Style


def get_main_directory():
    while True:
        main_dir = input("Enter the main directory path: ")
        if os.path.exists(main_dir):
            break
        print("Invalid directory path. Please try again.")

    # Initialize JSON if it doesn't exist
    if not os.path.exists("dirs.json"):
        return main_dir, {}  # Return empty dict initially

    with open("dirs.json", "r") as f:
        dirs = json.load(f)

    main_dir_json = dirs.get(main_dir, {"keep": [], "recon": [], "delete": []})
    return main_dir, main_dir_json


def organize_directories(main_dir):
    directories = list_directories(main_dir)
    print("Directories:")
    for directory in directories:
        print(directory.name)

def user_loop(main_dir, main_dir_json):
    help_text = "Commands: [help, exit, keep 'dir', recon 'dir', delete 'dir', info 'dir', moreinfo 'dir']"
    print(help_text)

    llm = llm_interface.LLMInterface(main_dir)

    while True:
        try:
            user_input = input("> ")

            if user_input == "help":
                print(help_text)
                continue

            if user_input == "exit":
                break

            if user_input == "list":
                directories = list_directories(main_dir)
                set_directories = []
                
                for dir in main_dir_json["keep"]:
                    set_directories.append(dir)
                
                for dir in main_dir_json["recon"]:
                    set_directories.append(dir)
                
                for dir in main_dir_json["delete"]:
                    set_directories.append(dir)
                
                print(Fore.RED + Style.BRIGHT + "Directories:" + Style.RESET_ALL)
                for directory in directories:
                    if directory.name not in set_directories:
                        print(directory.name)
                continue

            try:
                parts = user_input.split(" ")
                command = parts[0]
                target_dir = " ".join(parts[1:])  # Handle multi-word dir names

                if command == "keep":
                    main_dir_json = add_status(main_dir, main_dir_json, "keep", target_dir)
                elif command == "recon":
                    main_dir_json = add_status(main_dir, main_dir_json, "recon", target_dir)
                elif command == "delete":
                    main_dir_json = add_status(main_dir, main_dir_json, "delete", target_dir)
            except ValueError as e:
                print(e)
                continue

            # LLM Commands (Illustrative - needs full implementation)
            if user_input.startswith("info "):
                want_dir = user_input[5:].strip('"')  # Extract directory name
                context = llm.get_context(want_dir)
                print(Fore.GREEN + context + Style.RESET_ALL) # Green text

            elif user_input.startswith("moreinfo "):
                want_dir = user_input[9:].strip('"')
                query = input("Enter the query: ")
                info = llm.get_info_based_on_query(want_dir, query)
                print(Fore.BLUE + info + Style.RESET_ALL) # Blue text
            elif user_input.startswith("inst "):
                want_dir = user_input[5:].strip('"')
                install = llm.get_is_installation(want_dir)
                print(Fore.YELLOW + install + Style.RESET_ALL) # Yellow text
                
        except ValueError as e:
            print(Fore.RED + Style.BRIGHT + f"An error occurred: {e}" + Style.RESET_ALL)

    return main_dir_json

def add_status(main_dir, main_dir_json, status_type, directory_name):
    joined = os.path.join(main_dir, directory_name)
    
    if os.path.exists(joined):
        main_dir_json[status_type].append(directory_name)
    else:
        raise ValueError(f"Directory {directory_name} does not exist.")
    
    return main_dir_json

def save_main_dir_json(main_dir_json):
    with open("dirs.json", "r") as f:
        dirs = json.load(f)

    dirs[main_dir] = main_dir_json
    
    with open("dirs.json", "w") as f:
        json.dump(dirs, f, indent=4)


if __name__ == "__main__":
    init()
    
    main_dir, main_dir_json = get_main_directory()
    #organize_directories(main_dir)
    main_dir_json = user_loop(main_dir, main_dir_json)
    save_main_dir_json(main_dir_json)
