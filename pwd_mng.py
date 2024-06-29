import json, os
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode

key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode())

def decrypt_data(encrypted_data):
    return cipher_suite.decrypt(encrypted_data).decode()

def add_account(website, username, password):
    with open('passwords.json', 'r') as file:
        data = json.load(file)
    
    data[website] = {
        'username': username,
        'password': b64encode(encrypt_data(password)).decode('utf-8')
    }
    
    with open('passwords.json', 'w') as file:
        json.dump(data, file, indent=4)
        print("Account added successfully!")

def delete_account(website):
    with open('passwords.json', 'r') as file:
        data = json.load(file)
    
    if website in data:
        del data[website]
    
    with open('passwords.json', 'w') as file:
        json.dump(data, file, indent=4)
        print("Account deleted successfully!")

def edit_account(website, new_username, new_password):
    with open('passwords.json', 'r') as file:
        data = json.load(file)
    
    if website not in data:
        print("Account doesn't exist!")
        return 
    
    if website in data:
        data[website]['username'] = new_username
        data[website]['password'] = b64encode(encrypt_data(new_password)).decode('utf-8')
    
    with open('passwords.json', 'w') as file:
        json.dump(data, file, indent=4)
        print("Account edited successfully!")

def retrieve_accounts():
    with open('passwords.json', 'r') as file:
        data = json.load(file)
    
    for website, account_info in data.items():
        username = account_info['username']
        password = decrypt_data(b64decode(account_info['password']))
        print(f"Website: {website}, Username: {username}, Password: {password}")

if __name__ == '__main__':
    with open('passwords.json', 'w') as file:
        json.dump({}, file, indent=4)

    while True:
        print("\nPassword Manager Menu:")
        print("1. Add Account")
        print("2. Edit Account")
        print("3. Delete Account")
        print("4. List Accounts")
        print("5. Exit")
        choice = input("\nEnter your choice (1-5): ")

        os.system("cls")
        
        if choice == '1':
            website = input("Enter website/application name: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            add_account(website, username, password)
        elif choice == '2':
            website = input("Enter website/application name to edit: ")
            username = input("Enter new username: ")
            password = input("Enter new password: ")
            edit_account(website, username, password)
        elif choice == '3':
            website = input("Enter website/application name to delete: ")
            delete_account(website)
        elif choice == '4':
            print("\nList of Accounts:")
            retrieve_accounts()
        elif choice == '5':
            print("Exiting Password Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
