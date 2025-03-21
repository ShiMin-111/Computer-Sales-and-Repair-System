#Yu Shi Min
#TP076601

UserData = [
    ['SuperUser', 'S001','janiceong', 'Justtest@09', 'Janice Ong Yixuan','N/A', '791124-01-9512', 'janiceong@klccc.com', '1012345678', 'Selangor', 'N/A', 'N/A']
]

try:
    # Attempt to open the file in exclusive creation mode
    with open('users.txt', 'x') as file:
        # File does not exist, so it will be created
        for row in UserData:
            file.write('\t'.join(row) + '\n')
except FileExistsError:
    # File already exists, do nothing
    pass

# Ensure inventory.txt exists
try:
    with open('inventory.txt', 'x') as file:
        pass  # Just create the file if it does not exist
except FileExistsError:
    # File already exists, do nothing
    pass

from datetime import datetime

def get_input(prompt):
    while True:
        value = input(prompt)
        if value.strip():
            return value
        print("This field cannot be empty. Please try again.")

def log_login_attempt(username, user, success, logout_time):
    log_filename = 'login_data.txt'
    login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_filename, 'a') as log_file:
        log_file.write(f"{login_time}\t{user}\t{username}\t{'Success' if success else 'Failure'}\t{logout_time}\n")

def login(username, password):
    with open('users.txt', 'r') as file:
        for line_number, line in enumerate(file):
            line = line.strip()
            user_data = line.split('\t')
            if user_data[2] == username and user_data[3] == password:
                return user_data
        return None

def logout(user_data):
    print("Logging out...See you next time!")
    logout_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('login_data.txt', 'r') as file:
        lines = file.readlines()

    with open('login_data.txt', 'w') as file:
        for line in lines:
            line_data = line.strip().split('\t')
            if line_data[2] == user_data[2]:  # Check if this is the user's line
                line_data[4] = logout_time  # Update the logout_time
                line = '\t'.join(line_data) + '\n'
            file.write(line)

def display_audit_logs():
    log_filename = 'login_data.txt'

    try:
        with open(log_filename, 'r') as log_file:
            print("\n----------Audit Log----------\n")
            print(f"{'Timestamp':<20} {'User Type':<15} {'Username':<15} {'Status':<10} {'Logout Time':<20}")
            print("-" * 75)
            for line in log_file:
                # Split the line into its components
                log_entry = line.strip().split('\t')
                if len(log_entry) == 5:  # Ensure there are enough fields
                    timestamp, user_type, username, status, logout_time = log_entry
                    print(f"{timestamp:<20} {user_type:<15} {username:<15} {status:<10} {logout_time:<20}")
                else:
                    print("Malformed log entry, skipping...")
    except FileNotFoundError:
        print("Log file not found. Please check if 'login_data.txt' exists.")
    except Exception as e:
        print(f"An error occurred while reading the log file: {e}")

def check_username_exists(username):
    with open('users.txt', 'r') as file:
        for line_number, line in enumerate(file):
            line = line.strip()
            user_data = line.split('\t')
            if user_data[2] == username:
                return True
    return False


def is_valid_username(username):
    """ Validate that username contains only letters and is at least 5 characters long. """
    return username.isalpha() and len(username) >= 5


def is_valid_password(password):
    """ Validate that password meets the required criteria. """
    return (
            len(password) >= 8 and
            any(char.islower() for char in password) and
            any(char.isupper() for char in password) and
            any(char.isdigit() for char in password) and
            any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/~' for char in password)
    )


def is_valid_full_name(full_name):
    """ Validate that full name contains at least a first name and a last name. """
    return len(full_name.split()) >= 2

def is_valid_email(email):
    """ Validate that the email format is correct. """
    return "@" in email and "." in email and email.index("@") < email.rindex(".")


def is_valid_phone(phone):
    """ Validate that phone number is numeric and between 10 to 11 digits long. """
    return phone.isdigit() and 9 <= len(phone) <= 10

def is_valid_ic(ic):
    # Check IC length and numeric
    if len(ic) != 12 or not ic.isdigit():
        return False

    # Extract year, month, and day from IC
    year = int(ic[:2])
    month = int(ic[2:4])
    day = int(ic[4:6])

    # Get current year and its last two digits
    current_year_full = datetime.now().year
    current_year = current_year_full % 100

    # Determine full year
    if year > current_year:
        full_year = 1900 + year
    else:
        full_year = 2000 + year

    # Validate the month part
    if month < 1 or month > 12:
        return False

    # Determine if the year is a leap year
    is_leap_year = (full_year % 4 == 0 and full_year % 100 != 0) or full_year % 400 == 0

    # Define the days in each month
    days_in_month = [31, 29 if is_leap_year else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Validate the day part
    if day < 1 or day > days_in_month[month - 1]:
        return False

    # Validate the state code
    state_code = ic[6:8]
    if not (
            state_code in {'01', '21', '22', '23', '24'} or  # Johor
            state_code in {'02', '25', '26', '27'} or  # Kedah
            state_code in {'03', '28', '29'} or  # Kelantan
            state_code in {'04', '30'} or  # Malacca
            state_code in {'05', '31', '59'} or  # Negeri Sembilan
            state_code in {'06', '32', '33'} or  # Pahang
            state_code in {'07', '34', '35'} or  # Penang
            state_code in {'08', '36', '37', '38', '39'} or  # Perak
            state_code in {'09', '40'} or  # Perlis
            state_code in {'10', '41', '42', '43', '44'} or  # Selangor
            state_code in {'11', '45', '46'} or  # Terengganu
            state_code in {'12', '47', '48', '49'} or  # Sabah
            state_code in {'13', '50', '51', '52', '53'} or  # Sarawak
            state_code in {'14', '54', '55', '56', '57'} or  # Federal Territory of Kuala Lumpur
            state_code in {'15', '58'} or  # Federal Territory of Labuan
            state_code == '16'  # Federal Territory of Putrajaya
    ):
        return False

    return True


def format_ic(ic):
    """ Format IC number with hyphens. """
    return f"{ic[:6]}-{ic[6:8]}-{ic[8:]}"


def get_city_of_domicile(ic):
    # Mapping of state codes to cities
    state_code_to_city = {
        '01': 'Johor', '21': 'Johor', '22': 'Johor', '23': 'Johor', '24': 'Johor',
        '02': 'Kedah', '25': 'Kedah', '26': 'Kedah', '27': 'Kedah',
        '03': 'Kelantan', '28': 'Kelantan', '29': 'Kelantan',
        '04': 'Malacca', '30': 'Malacca',
        '05': 'Negeri Sembilan', '31': 'Negeri Sembilan', '59': 'Negeri Sembilan',
        '06': 'Pahang', '32': 'Pahang', '33': 'Pahang',
        '07': 'Penang', '34': 'Penang', '35': 'Penang',
        '08': 'Perak', '36': 'Perak', '37': 'Perak', '38': 'Perak', '39': 'Perak',
        '09': 'Perlis', '40': 'Perlis',
        '10': 'Selangor', '41': 'Selangor', '42': 'Selangor', '43': 'Selangor', '44': 'Selangor',
        '11': 'Terengganu', '45': 'Terengganu', '46': 'Terengganu',
        '12': 'Sabah', '47': 'Sabah', '48': 'Sabah', '49': 'Sabah',
        '13': 'Sarawak', '50': 'Sarawak', '51': 'Sarawak', '52': 'Sarawak', '53': 'Sarawak',
        '14': 'Federal Territory of Kuala Lumpur', '54': 'Federal Territory of Kuala Lumpur',
        '55': 'Federal Territory of Kuala Lumpur', '56': 'Federal Territory of Kuala Lumpur',
        '57': 'Federal Territory of Kuala Lumpur',
        '15': 'Federal Territory of Labuan', '58': 'Federal Territory of Labuan',
        '16': 'Federal Territory of Putrajaya'
    }

    state_code = ic[6:8]
    return state_code_to_city.get(state_code, "Unknown state code")

def review_and_edit(username, password, full_name, ic, email, phone, address):
    while True:
        print("\n--- Review Your Information ---")
        print(f"1. Username: {username}")
        print(f"2. Password: {password}")
        print(f"3. Full Name: {full_name}")
        print(f"4. IC Number: {format_ic(ic)}")
        print(f"5. Email: {email}")
        print(f"6. Phone: {phone}")
        print("7. Confirm and Submit")

        edit_choice = input("Enter the number of the field you want to edit (or 7 to confirm): ").strip()

        if edit_choice == '1':
            username = input("Enter new username (only letters allowed, at least 5 characters long): ")
            while not is_valid_username(username) or check_username_exists(username):
                if not is_valid_username(username):
                    print("Invalid username. It should only contain letters and be at least 5 characters long.")
                else:
                    print("Username already exists. Please choose a different username.")
                username = input("Enter new username (only letters allowed, at least 5 characters long): ")

        elif edit_choice == '2':
            password = input("Enter new password (min 8 characters, at least 1 uppercase, 1 lowercase, 1 number, and 1 symbol): ")
            while not is_valid_password(password):
                print("Invalid password. Ensure it meets all requirements.")
                password = input("Enter new password (min 8 characters, at least 1 uppercase, 1 lowercase, 1 number, and 1 symbol): ")

        elif edit_choice == '3':
            full_name = input("Enter new full name (first and last name): ")
            while not is_valid_full_name(full_name):
                print("Invalid name. Ensure you provide at least a first and last name.")
                full_name = input("Enter new full name (first and last name): ")

        elif edit_choice == '4':
            ic = input("Enter new IC number (12 digits only): ")
            while not is_valid_ic(ic):
                print("Invalid IC number. Ensure it is exactly 12 digits long and valid.")
                ic = input("Enter new IC number (12 digits only): ")
            address = get_city_of_domicile(ic)

        elif edit_choice == '5':
            email = input("Enter your email: ")
            while not is_valid_email(email):
                print("Invalid email format. Please enter a valid email.")
                email = input("Enter your email: ")

        elif edit_choice == '6':
            phone = input("Enter new phone number (9 to 10 digits, numeric only): +60")
            while not is_valid_phone(phone):
                print("Invalid phone number. Ensure it is numeric and between 9 to 10 digits long.")
                phone = input("Enter new phone number (9 to 10 digits, numeric only): +60")

        elif edit_choice == '7':
            return username, password, full_name, ic, email, phone, address

        else:
            print("Invalid choice. Please enter a number from 1 to 8.")

def get_next_id(user_type):
    """ Generate the next ID for either Customer or Staff based on the user_type """
    prefix = 'C' if user_type == 'Customer' else 'S'
    max_id = 0

    with open('users.txt', 'r') as file:
        for line in file:
            user_data = line.strip().split('\t')
            if user_type == 'Customer':
                # Check if the current line is for a customer
                if user_data[1].startswith('C'):
                    current_id = int(user_data[1][1:])  # Extract ID number after 'C'
                    if current_id > max_id:
                        max_id = current_id
            else:
                # Check if the current line is for any type of staff
                if user_data[1].startswith('S'):
                    current_id = int(user_data[1][1:])  # Extract ID number after 'S'
                    if current_id > max_id:
                        max_id = current_id

    # Return the next ID in the sequence
    next_id = max_id + 1
    return f"{prefix}{next_id:03d}" #next id is formatted to three digits


def staff_sign_up():
    """ Handle the staff sign-up process. """
    while True:
        # Gather user information
        username = input("Enter username (only letters allowed, at least 5 characters long): ")
        while not is_valid_username(username) or check_username_exists(username):
            if not is_valid_username(username):
                print("Invalid username. It should only contain letters and be at least 5 characters long.")
            else:
                print("Username already exists. Please choose a different username.")
            username = input("Enter username (only letters allowed, at least 5 characters long): ")

        password = input(
            "Enter password (min 8 characters, at least 1 uppercase, 1 lowercase, 1 number, and 1 symbol): ")
        while not is_valid_password(password):
            print("Invalid password. Ensure it meets all requirements.")
            password = input(
                "Enter password (min 8 characters, at least 1 uppercase, 1 lowercase, 1 number, and 1 symbol): ")

        full_name = input("Enter your full name (first and last name): ")
        while not is_valid_full_name(full_name):
            print("Invalid name. Ensure you provide at least a first and last name.")
            full_name = input("Enter your full name (first and last name): ")

        ic = input("Enter your IC number (12 digits only): ")
        while not is_valid_ic(ic):
            print("Invalid IC number. Ensure it is exactly 12 digits long.")
            ic = input("Enter your IC number (12 digits only): ")
        address = get_city_of_domicile(ic)

        email = input("Enter your email: ")
        while not is_valid_email(email):
            print("Invalid email format. Please enter a valid email.")
            email = input("Enter your email: ")

        phone = input("Enter your phone number (9 to 10 digits, numeric only): +60")
        while not is_valid_phone(phone):
            print("Invalid phone number. Ensure it is numeric and between 9 to 10 digits long.")
            phone = input("Enter your phone number (9 to 10 digits, numeric only): +60")

        # Review and edit user information
        username, password, full_name, ic, email, phone, address = review_and_edit(
            username, password, full_name, ic, email, phone, address
        )

        # Generate new ID
        new_id = get_next_id('Staff')

        # Format IC number
        formatted_ic = format_ic(ic)
        registration_date = datetime.now().strftime('%Y-%m-%d')
        approval_date = 'N/A'  # Default value as approval status is still pending

        # Write new user data to file
        with open('users.txt', 'a') as file:
            user_data = ['Staff', new_id, username, password, full_name, 'pending', formatted_ic, email, phone, address,
                         registration_date, approval_date]
            file.write('\t'.join(user_data) + '\n')

        print("Sign up successful! Please wait for account approval.")
        return


def cus_sign_up():
    """Handle the customer sign-up process."""
    print("Customer Sign-Up")
    while True:
        # Gather user information
        username = input("Enter username (only letters allowed, at least 5 characters long): ")
        while not is_valid_username(username) or check_username_exists(username):
            if not is_valid_username(username):
                print("Invalid username. It should only contain letters and be at least 5 characters long.")
            else:
                print("Username already exists. Please choose a different username.")
            username = input("Enter username (only letters allowed, at least 5 characters long): ")

        password = input("Enter password (min 8 characters, at least 1 uppercase, 1 lowercase, 1 number, and 1 symbol): ")
        while not is_valid_password(password):
            print("Invalid password. Ensure it meets all requirements.")
            password = input("Enter password (min 8 characters, at least 1 uppercase, 1 lowercase, 1 number, and 1 symbol): ")

        full_name = input("Enter your full name (first and last name): ")
        while not is_valid_full_name(full_name):
            print("Invalid name. Ensure you provide at least a first and last name.")
            full_name = input("Enter your full name (first and last name): ")

        ic = input("Enter your IC number (12 digits only): ")
        while not is_valid_ic(ic):
            print("Invalid IC number. Ensure it is exactly 12 digits long and valid.")
            ic = input("Enter your IC number (12 digits only): ")
        address = get_city_of_domicile(ic)

        email = input("Enter your email: ")
        while not is_valid_email(email):
            print("Invalid email format. Please enter a valid email.")
            email = input("Enter your email: ")

        phone = input("Enter your phone number (9 to 10 digits, numeric only): +60")
        while not is_valid_phone(phone):
            print("Invalid phone number. Ensure it is numeric and between 9 to 10 digits long.")
            phone = input("Enter your phone number (9 to 10 digits, numeric only): +60")

        # Review and edit user information
        username, password, full_name, ic, email, phone, address = review_and_edit(
            username, password, full_name, ic, email, phone, address
        )

        # Generate new ID
        new_id = get_next_id('Customer')

        # Format IC number
        formatted_ic = format_ic(ic)
        registration_date = datetime.now().strftime('%Y-%m-%d')
        approval_date = 'N/A'  # Default value as approval status is still pending

        # Write new user data to file
        with open('users.txt', 'a') as file:
            user_data = ['Customer', new_id, username, password, full_name, 'pending', formatted_ic, email, phone, address,
                         registration_date, approval_date]
            file.write('\t'.join(user_data) + '\n')

        print("Sign up successful! Please wait for account approval.")
        return



def homepage():
    print('------Welcome to KL Central Computer Company------')
    while True:
        userIntend = input('1 - Login\n2 - Sign Up\nChoose an option: ')
        if userIntend == '1':
            print("\n","-" * 15,"Login Page","-" * 14)
            while True:
                username = input("Enter username (or press 'B' to go back): ")
                if username.upper() == 'B':
                    break  # Go back to the main menu
                if check_username_exists(username):
                    while True:
                        password = input("Enter password: ")
                        if password.upper() == 'B':
                            break # Go back to the username entry
                        user_data = login(username, password)
                        if user_data:
                            if user_data[5].lower() == 'pending':
                                print("Your account is still pending approval.")
                                log_login_attempt(username, user_data[0], success=False , logout_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                                return
                            elif user_data[5].lower() == 'declined':
                                print("Your account has been declined.")
                                log_login_attempt(username, user_data[0], success=False , logout_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                                return
                            else:
                                print(f"Login successful! Menu for {user_data[0]}")
                                log_login_attempt(username, user_data[0], success=True, logout_time='N/A')
                                if user_data[0] == 'Customer':
                                    customer_menu(username,user_data)
                                elif user_data[0] == 'SuperUser':
                                    super_user_menu(user_data)
                                elif user_data[0] == 'Admin':
                                    admin_menu(user_data)
                                elif user_data[0] == 'InventoryStaff':
                                    inventory_staff_menu(user_data)
                                return
                        else:
                            print("Incorrect password. Please try again.")
                            log_login_attempt(username, 'N/A', success=False,logout_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        break
                else:
                    print("Username does not exist. Please enter a valid username.")
        elif userIntend == '2':
            print("\n", "-" * 15, "Sign Up Page", "-" * 14)
            while True:
                userType = input('Sign Up As\n1 - Customer\n2 - Staff\nB - Back\nChoose an option: ')
                if userType.upper() == 'B':
                    break
                elif userType == '1':
                    cus_sign_up()
                    return
                elif userType == '2':
                    staff_sign_up()
                    return
                else:
                    print("Invalid user type. Please choose a valid option.")

        else:
            print("Invalid option. Please choose 1 for Login or 2 for Sign Up.")


def inventory_staff_menu(user_data):
    while True:
        try:
            print('1 - Manage Inventory\n2 - Manage Stock Order\n3 - Log Out')
            choice = get_input('Choose an option: ')

            if choice == '1':
                inventory_menu()
            elif choice == '2':
                manage_stock_orders()
            elif choice == '3':
                logout(user_data)
                break
            else:
                print('Invalid option. Please try again.')
        except Exception as e:
            print(f"An error occurred: {e}")

def admin_menu(user_data):
    while True:
        try:
            print('1 - Approval\n2 - User Details\n3 - Customer Orders\n4 - Customer Repairs\n5 - Log Out')
            choice = get_input('Choose an option: ')

            if choice == '1':
                admin_approval_menu()
            elif choice == '2':
                admin_user_details_menu()
            elif choice == '3':
                cus_orders()
            elif choice == '4':
                manage_repair_requests()
            elif choice == '5':
                logout(user_data)
                break
            else:
                print('Invalid option. Please try again.')
        except Exception as e:
            print(f"An error occurred: {e}")

def admin_approval_menu():
    print("------Approval Menu------")

    # Read user data from the file
    user_data = []  # Initialize the user_data list
    try:
        with open('users.txt', 'r') as file:
            user_data = [line.strip().split('\t') for line in file]  # Read all users

        pending_users = [user for user in user_data if user[5].lower() == 'pending' and user[0] == 'Customer']  # Filter pending users

        if not pending_users:
            print("No users pending approval.")
            return
        else:
            print(
                f"{'No.':<5} {'User Type':<15} {'Username':<15} {'Full Name':<30} {'IC Number':<15} {'Email':<25} {'Phone(+60)':<15}")
            print("-" * 140)
            for index, user in enumerate(pending_users):
                user_type = user[0]
                username = user[2]
                full_name = user[4]
                ic = user[6]
                email = user[7]
                phone = user[8]
                print(f"{index + 1:<5} {user_type:<15} {username:<15} {full_name:<30} {ic:<15} {email:<25} {phone:<15}")

            # Optional: option to approve or decline users
            print("\nOptions:")
            print("1 - Approve User")
            print("2 - Decline User")
            print("B - Back")
            choice = get_input("Choose an option: ")
            if choice == '1':
                admin_approve_user(user_data, pending_users)  # Call approve_user with pending_users
            elif choice == '2':
                decline_user(user_data, pending_users)  # Call decline_user with pending_users
            elif choice.upper() == 'B':
                return  # Go back to the admin menu

    except FileNotFoundError:
        print("User data file not found. Please check if the 'users.txt' file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")


def admin_approve_user(user_data, pending_users):
    while True:
        user_choice = get_input("Enter the number of the user to approve (or 'B' to go back): ")
        if user_choice.upper() == 'B':
            return  # Return to approval menu
        try:
            user_number = int(user_choice) - 1
            if 0 <= user_number < len(pending_users):
                user = pending_users[user_number]
                user[5] = 'approved'  # Update status to approved
                user[11] = datetime.now().strftime('%Y-%m-%d')
                username = user[2]
                print(f"User '{username}' has been approved.")
                update_user_file(user_data)  # Pass updated user_data
                return
            else:
                print("Invalid user number. Please try again.")
        except ValueError:
            print("Please enter a valid number or 'B' to go back.")

def admin_user_details_menu():
    print("------User Details Menu------")

    try:
        while True:
            with open('users.txt', 'r') as file:
                user_data = [line.strip().split('\t') for line in file if line.strip()]  # Read all users and ignore empty lines

            if not user_data:
                print("No users found.")
                return

            # Define column widths
            col_widths = [5, 15, 15, 20, 25, 15, 25, 15, 30, 10]
            headers = ['No.', 'User Type', 'Username', 'Password', 'Full Name', 'IC Number', 'Email', 'Phone', 'City of Domicile', 'Status']

            # Print header
            header_row = ' '.join(f"{header:<{col_widths[i]}}" for i, header in enumerate(headers))
            print(header_row)
            print("-" * (sum(col_widths) + len(col_widths) - 1))

            # Print user data
            for index, user in enumerate(user_data):
                if len(user) < 10:  # Ensure there are enough fields
                    continue

                user_type = user[0]
                username = user[2]
                password = user[3]
                full_name = user[4]
                ic = user[6]
                email = user[7]
                phone = user[8]
                address = user[9]
                status = user[5]

                # Format user data row
                user_row = f"{index + 1:<{col_widths[0]}} {user_type:<{col_widths[1]}} {username:<{col_widths[2]}} {password:<{col_widths[3]}} {full_name:<{col_widths[4]}} {ic:<{col_widths[5]}} {email:<{col_widths[6]}} {phone:<{col_widths[7]}} {address:<{col_widths[8]}} {status:<{col_widths[9]}}"
                print(user_row)

            while True:
                print("\nOptions:")
                print("B - Back")
                choice = get_input("Choose an option: ")

                if choice.upper() == 'B':
                    return  # Go back to the previous menu
                else:
                    print("Invalid option. Please try again.")

    except FileNotFoundError:
        print("User data file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def update_user_file(user_data):
    """Update the users.txt file with current user data."""
    with open('users.txt', 'w') as file:
        for user in user_data:  # Use the updated user data list
            file.write('\t'.join(user) + '\n')

def assign_roles(user_data, username):
    print("\nAssign a role to the user:\n1 - Inventory Staff\n2 - Admin")
    while True:
        choice = get_input("Choose a role number: ")
        for user in user_data:
            if user[2] == username:
                if choice == '1':
                    user[0] = 'InventoryStaff'
                    print(f"User '{username}' has been assigned the role of Inventory Staff.")
                elif choice == '2':
                    user[0] = 'Admin'
                    print(f"User '{username}' has been assigned the role of Admin.")
                else:
                    print("Invalid role choice. Please try again.")
                    continue
                update_user_file(user_data)
                return

def approve_user(user_data, pending_users):
    while True:
        user_choice = get_input("Enter the number of the user to approve (or 'B' to go back): ")
        if user_choice.upper() == 'B':
            return  # Return to approval menu
        try:
            user_number = int(user_choice) - 1
            if 0 <= user_number < len(pending_users):
                user = pending_users[user_number]
                user[5] = 'approved'  # Update status to approved
                user[11] = datetime.now().strftime('%Y-%m-%d')
                username = user[2]
                print(f"User '{username}' has been approved.")
                update_user_file(user_data)  # Pass updated user_data
                if user[0] == 'Staff':  # Only assign roles if the user is a staff member
                    assign_roles(user_data, username)  # Assign roles after approval
                return
            else:
                print("Invalid user number. Please try again.")
        except ValueError:
            print("Please enter a valid number or 'B' to go back.")

def decline_user(user_data, pending_users):
    while True:
        user_choice = get_input("Enter the number of the user to decline (or 'B' to go back): ")
        if user_choice.upper() == 'B':
            return  # Return to approval menu
        try:
            user_number = int(user_choice) - 1
            if 0 <= user_number < len(pending_users):
                user = pending_users[user_number]
                user[5] = 'declined'  # Update status to declined
                username = user[2]
                print(f"User '{username}' has been declined.")
                update_user_file(user_data)  # Pass updated user_data
                return
            else:
                print("Invalid user number. Please try again.")
        except ValueError:
            print("Please enter a valid number or 'B' to go back.")

def approval_menu():
    print("------Approval Menu------")

    # Read user data from the file
    user_data = []  # Initialize the user_data list
    try:
        with open('users.txt', 'r') as file:
            user_data = [line.strip().split('\t') for line in file]  # Read all users

        pending_users = [user for user in user_data if user[5].lower() == 'pending']  # Filter pending users

        if not pending_users:
            print("No users pending approval.")
            return
        else:
            print(f"{'No.':<5} {'User Type':<15} {'Username':<15} {'Full Name':<30} {'IC Number':<15} {'Email':<25} {'Phone':<15}")
            print("-" * 140)
            for index, user in enumerate(pending_users):
                user_type = user[0]
                username = user[2]
                full_name = user[4]
                ic = user[6]
                email = user[7]
                phone = user[8]
                print(f"{index + 1:<5} {user_type:<15} {username:<15} {full_name:<30} {ic:<15} {email:<25} {phone:<15}")

            # Optional: Add an option to approve or decline users
            print("\nOptions:")
            print("1 - Approve User")
            print("2 - Decline User")
            print("B - Back")
            choice = get_input("Choose an option: ")
            if choice == '1':
                approve_user(user_data, pending_users)  # Call approve_user with pending_users
            elif choice == '2':
                decline_user(user_data, pending_users)  # Call decline_user with pending_users
            elif choice.upper() == 'B':
                return  # Go back to the super user menu

    except FileNotFoundError:
        print("User data file not found. Please check if the 'users.txt' file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")


def modify_user(user_data, user_index):
    user = user_data[user_index]
    fields = ['Username', 'Password', 'Full Name', 'IC Number', 'Email', 'Phone']
    print("\nModify User Information:")

    if user[5] == 'declined':
        print("You cannot modify user information since he/she declined.")
        return

    while True:
        print("\nOptions:")
        for i, field in enumerate(fields):
            print(f"{i + 1} - {field}")
        print("B - Back")

        choice = get_input("Choose a field to edit: ")
        if choice.upper() == 'B':
            break

        try:
            choice = int(choice)
            if 1 <= choice <= len(fields):
                field_name = fields[choice - 1]
                if field_name == 'Username':
                    new_username = get_input(f"{field_name} [{user[2]}]: ") or user[2]
                    while not is_valid_username(new_username) or check_username_exists(new_username):
                        if not is_valid_username(new_username):
                            print("Invalid username. It should only contain letters and be at least 5 characters long.")
                        else:
                            print("Username already exists. Please choose a different username.")
                        new_username = get_input(
                            "Enter new username (only letters allowed, at least 5 characters long): ")
                    user[2] = new_username
                elif field_name == 'Password':
                    new_password = get_input(f"{field_name} [{user[3]}]: ") or user[3]
                    while not is_valid_password(new_password):
                        if not is_valid_password(new_password):
                            print("Invalid password. Ensure it meets all requirements.")
                        new_password = get_input("Enter new password (min 8 characters, at least 1 uppercase, 1 lowercase, 1 number, and 1 symbol): ")
                    user[3] = new_password
                elif field_name == 'Full Name':
                    new_fullname = get_input(f"{field_name} [{user[4]}]: ") or user[4]
                    while not is_valid_full_name(new_fullname):
                        if not is_valid_full_name(new_fullname):
                            print("Invalid name. Ensure you provide at least a first and last name.")
                        new_fullname = get_input("Enter new full name (first and last name): ")
                    user[4] = new_fullname
                elif field_name == 'IC Number':
                    new_ic = get_input(f"{field_name} [{user[6]}]: ") or user[6]
                    while not is_valid_ic(new_ic):
                        if not is_valid_ic(new_ic):
                            print("Invalid IC number. Ensure it is exactly 12 digits long and valid.")
                        new_ic = get_input("Enter new IC number (12 digits only): ")
                    new_address = get_city_of_domicile(new_ic)  # Change ic to new_ic
                    user[9] = new_address
                    user[6] = new_ic
                elif field_name == 'Email':
                    new_email = get_input(f"{field_name} [{user[7]}]: ") or user[7]
                    while not is_valid_email(new_email):
                        if not is_valid_email(new_email):
                            print("Invalid email format. Please enter a valid email.")
                        new_email = get_input("Enter your email: ")
                    user[7] = new_email
                elif field_name == 'Phone':
                    new_phone = get_input(f"{field_name} [{user[8]}]: ") or user[8]
                    while not is_valid_phone(new_phone):
                        if not is_valid_phone(new_phone):
                            print("Invalid phone number. Ensure it is numeric and between 9 to 10 digits long.")
                        new_phone = get_input("Enter new phone number (9 to 10 digits, numeric only): +60")
                    user[8] = new_phone
                print(f"{field_name} has been updated.")
                update_user_file(user_data)
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Please enter a valid number or 'B' to go back.")


def delete_user(user_data, user_index):
    user = user_data.pop(user_index)
    print(f"User '{user[2]}' has been deleted.")
    update_user_file(user_data)


def user_details_menu():
    print("------User Details Menu------")

    try:
        while True:
            with open('users.txt', 'r') as file:
                user_data = [line.strip().split('\t') for line in file if line.strip()]  # Read all users and ignore empty lines

            if not user_data:
                print("No users found.")
                return

            # Define column widths
            col_widths = [5, 15, 15, 20, 25, 15, 25, 15, 30, 10]
            headers = ['No.', 'User Type', 'Username', 'Password', 'Full Name', 'IC Number', 'Email', 'Phone', 'City of Domicile', 'Status']

            # Print header
            header_row = ' '.join(f"{header:<{col_widths[i]}}" for i, header in enumerate(headers))
            print(header_row)
            print("-" * (sum(col_widths) + len(col_widths) - 1))

            # Print user data
            for index, user in enumerate(user_data):
                if len(user) < 10:  # Ensure there are enough fields
                    continue

                user_type = user[0]
                username = user[2]
                password = user[3]
                full_name = user[4]
                ic = user[6]
                email = user[7]
                phone = user[8]
                address = user[9]
                status = user[5]

                # Format user data row
                user_row = f"{index + 1:<{col_widths[0]}} {user_type:<{col_widths[1]}} {username:<{col_widths[2]}} {password:<{col_widths[3]}} {full_name:<{col_widths[4]}} {ic:<{col_widths[5]}} {email:<{col_widths[6]}} {phone:<{col_widths[7]}} {address:<{col_widths[8]}} {status:<{col_widths[9]}}"
                print(user_row)

            print("\nOptions:")
            print("1 - Modify User Info")
            print("2 - Delete User")
            print("B - Back")
            choice = get_input("Choose an option: ")

            if choice.upper() == 'B':
                return  # Go back to the previous menu

            user_number = get_input("Enter the number of the user (or 'B' to go back): ")
            if user_number.upper() == 'B':
                return  # Go back to the user details menu

            try:
                user_index = int(user_number) - 1
                if 0 <= user_index < len(user_data):
                    user_type = user_data[user_index][0]
                    if user_type == "SuperUser":
                        print("SuperUser cannot be modified or deleted.")
                        continue

                    if choice == '1':
                        modify_user(user_data, user_index)
                    elif choice == '2':
                        delete_user(user_data, user_index)
                    else:
                        print("Invalid option. Please try again.")
                else:
                    print("Invalid user number. Please try again.")
            except ValueError:
                print("Please enter a valid number or 'B' to go back.")
    except FileNotFoundError:
        print("User data file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def super_user_menu(user_data):
    while True:
        try:
            print('1 - Approval\n2 - User Details\n3 - Customer Orders\n4 - Customer Repairs\n5 - Manage Inventory\n6 - Manage Stock Order\n7 - Audit Log\n8 - Log Out')
            choice = get_input('Choose an option: ')

            if choice == '1':
                approval_menu()
            elif choice == '2':
                user_details_menu()
            elif choice == '3':
                cus_orders()
            elif choice == '4':
                manage_repair_requests()
            elif choice == '5':
                inventory_menu()
            elif choice == '6':
                manage_stock_orders()
            elif choice == '7':
                display_audit_logs()
                while True:
                    sub_choice = get_input("\nB - Back to menu: ")
                    if sub_choice.upper() == 'B':
                        break
                    else:
                        print("Invalid option. Please try again.")
            elif choice == '8':
                logout(user_data)
                break
            else:
                print('Invalid option. Please try again.')
        except Exception as e:
            print(f"An error occurred: {e}")


def load_inventory():
    try:
        with open('inventory.txt', 'r') as file:
            inventory_data = [line.strip().split('\t') for line in file if line.strip()]  # Ignore empty lines
        # Ensure that each item has the expected number of fields (5)
        inventory_data = [item for item in inventory_data if len(item) == 5]
        return inventory_data
    except FileNotFoundError:
        print("Inventory file not found. Creating a new inventory file.")
        with open('inventory.txt', 'w') as file:
            pass  # Create a new file if it doesn't exist
        return []
    except Exception as e:
        print(f"An error occurred while loading inventory: {e}")
        return []

def save_inventory(inventory_data):
    try:
        with open('inventory.txt', 'w') as file:
            for item in inventory_data:
                file.write('\t'.join(item) + '\n')
        print("Inventory data has been updated.")
    except Exception as e:
        print(f"An error occurred while saving inventory data: {e}")

def display_inventory(inventory_data):
    if not inventory_data:
        print("No items in inventory.")
        return
    print(f"{'No.':<5} {'Item ID':<10} {'Item Name':<30} {'Quantity':<10} {'Price':<10} {'Type':<10}")
    print("-" * 80)
    for index, item in enumerate(inventory_data):
        try:
            item_id = item[0]
            item_name = item[1]
            quantity = item[2]
            price = item[3]
            item_type = item[4]
            print(f"{index + 1:<5} {item_id:<10} {item_name:<30} {quantity:<10} {price:<10} {item_type:<10}")
        except IndexError:
            print(f"Error: Item data is incomplete for item index {index}.")
            continue

def validate_item_id(item_id):
    # Item ID must contain at least one letter, one number, and be 6 characters at most
    if len(item_id) > 6:
        return False
    has_letter = any(char.isalpha() for char in item_id)
    has_number = any(char.isdigit() for char in item_id)
    return has_letter and has_number

def validate_quantity_price(value):
    try:
        # Convert value to a float
        number = float(value)
        # Check if the number is positive
        return number > 0
    except ValueError:
        # If conversion fails, value is not a valid number
        return False

def item_id_exists(item_id, inventory_data):
    return any(item[0] == item_id for item in inventory_data)

def add_item(inventory_data):
    while True:
        item_id = get_input("Enter Item ID: ")
        if item_id_exists(item_id, inventory_data):
            print("Item ID already exists. Please modify the existing item instead.")
            return  # Exit the function
        if not validate_item_id(item_id):
            print("Invalid Item ID. It must contain at least one letter, one number, and be at most 6 characters long.")
            continue
        break

    item_name = get_input("Enter Item Name: ")

    while True:
        quantity = get_input("Enter Quantity: ")
        if not validate_quantity_price(quantity):
            print("Invalid Quantity. It must be a positive number.")
            continue
        break

    while True:
        price = get_input("Enter Price (per unit): ")
        if not validate_quantity_price(price):
            print("Invalid Price. It must be a positive number and numeric value only.")
            continue
        break

    item_type = get_input("Enter Item Type (1 for Wares, 2 for Repairs): ")
    item_type = "Wares" if item_type == "1" else "Repairs" if item_type == "2" else "Unknown"

    inventory_data.append([item_id, item_name, quantity, price, item_type])  # Add new item with type
    save_inventory(inventory_data)
    print("Item added successfully.")


def modify_item(inventory_data, item_index):
    item = inventory_data[item_index]
    fields = ['Item ID', 'Item Name', 'Quantity', 'Price', 'Item Type']
    print("\nModify Item Information:")

    while True:
        print("\nOptions:")
        for i, field in enumerate(fields):
            print(f"{i + 1} - {field}")
        print("B - Back")

        choice = get_input("Choose a field to edit: ")
        if choice.upper() == 'B':
            break

        try:
            choice = int(choice)
            if 1 <= choice <= len(fields):
                field_name = fields[choice - 1]
                if field_name == 'Item ID':
                    while True:
                        new_value = get_input(f"{field_name} [{item[choice - 1]}]: ")
                        if validate_item_id(new_value):
                            item[choice - 1] = new_value
                            print(f"{field_name} has been updated.")
                            break
                        else:
                            print("Invalid Item ID. It must contain at least one letter, one number, and be at most 6 characters long.")
                elif field_name in ['Quantity', 'Price']:
                    while True:
                        new_value = get_input(f"{field_name} [{item[choice - 1]}]: ")
                        if validate_quantity_price(new_value):
                            item[choice - 1] = new_value
                            print(f"{field_name} has been updated.")
                            break
                        else:
                            print(f"Invalid {field_name}. It must be a positive number.")
                elif field_name == 'Item Type':
                    while True:
                        new_value = get_input(f"{field_name} [{item[choice - 1]}] (1 for Wares, 2 for Repairs): ")
                        if new_value in ['1', '2']:
                            item[choice - 1] = "Wares" if new_value == "1" else "Repairs"
                            print(f"{field_name} has been updated.")
                            break
                        else:
                            print("Invalid option. Please enter 1 for Wares or 2 for Repairs.")
                else:
                    item[choice - 1] = get_input(f"{field_name} [{item[choice - 1]}]: ") or item[choice - 1]
                    print(f"{field_name} has been updated.")
                save_inventory(inventory_data)
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Please enter a valid number or 'B' to go back.")
        except IndexError:
            print("Error: The item does not have the expected number of fields.")

def delete_item(inventory_data, item_index):
    try:
        del inventory_data[item_index]
        save_inventory(inventory_data)
        print("Item deleted successfully.")
    except IndexError:
        print("Error: Invalid item index for deletion.")

def inventory_menu():
    print("------ Inventory Menu ------")

    inventory_data = load_inventory()

    while True:
        display_inventory(inventory_data)

        print("\nOptions:")
        print("1 - Add Item")
        print("2 - Modify Item")
        print("3 - Delete Item")
        print("B - Back")
        choice = get_input("Choose an option: ")

        if choice.upper() == 'B':
            return  # Go back to the main menu

        if choice == '1':
            add_item(inventory_data)
        elif choice == '2':
            while True:
                item_number = get_input("Enter the number of the item to modify (or 'B' to go back): ")
                if item_number.upper() == 'B':
                    break
                try:
                    item_index = int(item_number) - 1
                    if 0 <= item_index < len(inventory_data):
                        modify_item(inventory_data, item_index)
                        break
                    else:
                        print("Invalid item number. Please try again.")
                except ValueError:
                    print("Please enter a valid number or 'B' to go back.")
        elif choice == '3':
            while True:
                item_number = get_input("Enter the number of the item to delete (or 'B' to go back): ")
                if item_number.upper() == 'B':
                    break
                try:
                    item_index = int(item_number) - 1
                    if 0 <= item_index < len(inventory_data):
                        while True:
                            subchoice = get_input("Are you sure you want to delete this item? Y/N: ")
                            if subchoice.upper() == 'Y':
                                delete_item(inventory_data, item_index)
                                break
                            elif subchoice.upper() == 'N':
                                break
                            else:
                                print("Invalid option. Please only enter Y/N.")
                        break
                    else:
                        print("Invalid item number. Please try again.")
                except ValueError:
                    print("Please enter a valid number or 'B' to go back.")
        else:
            print("Invalid option. Please try again.")



def add_to_cart(cart, inventory_data):
    while True:
        user_input = get_input("Enter the index number of the item to add to cart (or 'B' to go back): ").strip()

        if user_input.upper() == 'B':
            return False  # Indicate that the user chose to go back

        try:
            index = int(user_input) - 1

            if 0 <= index < len(inventory_data):
                item_id, item_name, available_quantity, price, item_type = inventory_data[index]
                available_quantity = int(available_quantity)

                # Initialize current_quantity_in_cart
                current_quantity_in_cart = 0

                # Check if the item is already in the cart and its quantity
                item_in_cart = next((cart_item for cart_item in cart if cart_item[0] == item_id), None)

                if item_in_cart:
                    current_quantity_in_cart = int(item_in_cart[2])
                    if current_quantity_in_cart >= available_quantity:
                        print(f"You already have the maximum available quantity of {item_name} in your cart.")
                        continue  # Prompt the user to select a different item

                while True:
                    quantity_input = get_input(f"Enter the quantity of {item_name} to add to cart (Available: {available_quantity}): ").strip()

                    try:
                        quantity = int(quantity_input)

                        if 0 < quantity <= available_quantity:
                            if item_in_cart:
                                new_quantity = current_quantity_in_cart + quantity
                                if new_quantity > available_quantity:
                                    print(f"You cannot add more than {available_quantity} of {item_name} to your cart.")
                                    continue  # Go back to item selection

                                item_in_cart[2] = str(new_quantity)
                                print(f"Added {quantity} more {item_name}(s) to the cart. Total quantity now: {item_in_cart[2]}")
                            else:
                                cart.append([item_id, item_name, str(quantity), price])
                                print(f"Added {quantity} {item_name}(s) to the cart.")
                            return True  # Indicate that an item was added
                        else:
                            print(f"Please enter a valid quantity (1 to {available_quantity}).")
                    except ValueError:
                        print("Invalid input. Please enter a valid number for quantity.")
            else:
                print("Invalid index number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def view_catalog(cart):
    print("------ Product Catalog ------")
    inventory_data = load_inventory()
    available_items = [item for item in inventory_data if int(item[2]) > 0 and item[4] == "Wares"]

    if available_items:
        display_inventory(available_items)
        while True:
            if not add_to_cart(cart, available_items):
                break  # Exit if the user chose to go back
            another = get_input("Do you want to add another item? (Y to add and anything else to back to menu): ").strip().upper()
            if another != 'Y':
                break
    else:
        print("No items available in the catalog at the moment.")

def display_inventory(inventory_data):
    if not inventory_data:
        print("No items in inventory.")
        return
    print(f"{'No.':<5} {'Item ID':<10} {'Item Name':<30} {'Quantity':<10} {'Price':<10} {'Type':<10}")
    print("-" * 80)
    for index, item in enumerate(inventory_data):
        try:
            item_id = item[0]
            item_name = item[1]
            quantity = item[2]
            price = item[3]
            item_type = item[4]
            print(f"{index + 1:<5} {item_id:<10} {item_name:<30} {quantity:<10} {price:<10} {item_type:<10}")
        except IndexError:
            print(f"Error: Item data is incomplete for item index {index}.")
            continue

def display_cart(cart):
    if not cart:
        print("Your cart is empty.")
        return

    headers = ["No.", "Item ID", "Item Name", "Quantity", "Price (per unit)", "Total Price(RM)"]
    col_widths = [5, 10, 30, 10, 20, 15]


    header_line = "".join(f"{headers[i]:<{col_widths[i]}}" for i in range(len(headers)))
    separator_line = "-" * sum(col_widths)

    print(header_line)
    print(separator_line)

    for index, item in enumerate(cart):
        item_id, item_name, quantity, price = item
        quantity = int(quantity)  # Convert quantity to integer
        price = float(price)  # Convert price to float
        total_price = price * quantity
        print(
            f"{index + 1:<{col_widths[0]}}{item_id:<{col_widths[1]}}{item_name:<{col_widths[2]}}{quantity:<{col_widths[3]}}{price:<{col_widths[4]}.2f}{total_price:<{col_widths[5]}.2f}"
        )

def manage_cart(cart, username):
    while True:
        print("------ Shopping Cart ------")
        display_cart(cart)
        print("\nOptions:")
        print("1 - Remove Item")
        print("2 - Checkout")
        print("B - Back")
        choice = get_input("Choose an option: ")

        if choice.upper() == 'B':
            break
        elif choice == '1':
            remove_from_cart(cart)
        elif choice == '2':
            checkout(cart, username)
            break
        else:
            print("Invalid option. Please try again.")


def remove_from_cart(cart):
    if not cart:
        print("Your cart is empty.")
        return

    while True:
        item_number = get_input("Enter the number of the item to remove from the cart (or 'B' to go back): ")
        if item_number.upper() == 'B':
            break
        try:
            item_index = int(item_number) - 1
            if 0 <= item_index < len(cart):
                removed_item = cart.pop(item_index)
                print(f"Removed {removed_item[1]} from cart.")
                break
            else:
                print("Invalid item number. Please try again.")
        except ValueError:
            print("Please enter a valid number or 'B' to go back.")


def checkout(cart, username):
    if not cart:
        print("Your cart is empty.")
        return

    inventory_data = load_inventory()
    inventory_dict = {item[0]: item for item in inventory_data}

    for item in cart:
        item_id, item_name, quantity_in_cart, _ = item
        if item_id in inventory_dict:
            available_quantity = int(inventory_dict[item_id][2])
            while int(quantity_in_cart) > available_quantity:
                print(f"Error: Not enough quantity available for {item_name}. Available: {available_quantity}, In Cart: {quantity_in_cart}")
                quantity_in_cart = get_input(f"Enter a new quantity for {item_name} (max {available_quantity}): ").strip()
                if not quantity_in_cart.isdigit() or int(quantity_in_cart) > available_quantity:
                    print("Invalid input. Please enter a valid number.")
                    continue
                item[2] = quantity_in_cart
        else:
            print(f"Error: {item_name} is no longer available in the inventory.")
            return

    # Removed the total_cost calculation here
    while True:
        payment_choice = get_input("Choose payment method - 1 for Pay Now, 2 for Pay Later: ").strip()
        if payment_choice == "1":
            paid_status = "Paid"
            break
        elif payment_choice == "2":
            paid_status = "Not Paid"
            break
        else:
            print("Invalid choice. Please choose '1' for Pay Now or '2' for Pay Later.")

    billing_info = payment_page() if paid_status == "Paid" else {"address": "N/A", "contact_number": "N/A"}

    if paid_status == "Paid":
        payment_successful = billing_info is not None
    else:
        payment_successful = True

    if payment_successful:
        save_order_to_history(username, cart, paid_status, billing_info)  # Pass only relevant data

        if paid_status == "Paid":
            for item in cart:
                item_id, item_name, quantity_in_cart, _ = item
                if item_id in inventory_dict:
                    inventory_dict[item_id][2] = str(int(inventory_dict[item_id][2]) - int(quantity_in_cart))
            save_inventory([inventory_dict[key] for key in inventory_dict])
            print("Checkout complete. Your cart is now empty.")
        else:
            print("Order placed. You can pay later at ORDER HISTORY. Your cart has been cleared.")

        cart.clear()
    else:
        print("Payment failed. Please try again.")



def is_valid_credit_card(card_number):
    # Check if the card number is numeric and has 16 digits
    return card_number.isdigit() and len(card_number) == 16


def is_valid_expiration_date(expiration_date):
    # Check if the expiration date is in the format MM/YY
    if len(expiration_date) == 5 and expiration_date[2] == '/':
        month = expiration_date[:2]
        year = expiration_date[3:]

        # Check if month and year are numeric and within valid ranges
        if month.isdigit() and year.isdigit() and 1 <= int(month) <= 12:
            # Get the current month and year
            current_date = datetime.now()
            current_month = current_date.month
            current_year = current_date.year % 100  # Get last two digits of the year

            # Check if the card is expired
            if int(year) > current_year or (int(year) == current_year and int(month) >= current_month):
                return True  # Card is valid and not expired
    return False

def is_valid_cvv(cvv):
    # Check if the CVV is numeric and has 3 digits
    return cvv.isdigit() and len(cvv) == 3

def payment_page():
    print("------ Payment Page ------")

    billing_info = {}

    billing_address = get_input("Enter your billing address: ")
    billing_info['address'] = billing_address

    while True:
        phone = get_input("Enter your contact number (9-10 digits): +60")
        if is_valid_phone(phone):
            billing_info['contact_number'] = phone
            break
        else:
            print("Invalid contact number. Please enter a numeric number with 9 to 10 digits.")

    while True:
        credit_card = get_input("Enter your credit card number (16 digits): ")
        if is_valid_credit_card(credit_card):
            break
        else:
            print("Invalid credit card number. Please enter a 16-digit number.")

    while True:
        expiration_date = get_input("Enter the expiration date (MM/YY): ")
        if is_valid_expiration_date(expiration_date):
            break
        else:
            print("Invalid expiration date. Please enter in MM/YY format.")

    while True:
        cvv = get_input("Enter the CVV (3 digits): ")
        if is_valid_cvv(cvv):
            break
        else:
            print("Invalid CVV. Please enter a 3-digit number.")

    print("Payment successful! Thank you for your purchase.")
    return billing_info  # Return the billing info for further use

def save_order_to_history(username, cart, paid_status, billing_info):
    order_filename = 'order_history.txt'
    delivery_status = "Packaging" if paid_status == "Paid" else ""
    order_lines = []

    for item in cart:
        item_id = item[0]
        item_name = item[1]
        quantity = int(item[2])  # Ensure quantity is an integer
        price_per_item = float(item[3])  # Ensure price per item is a float
        total_price = quantity * price_per_item  # Calculate total price for the item

        order_lines.append(
            f"{username}\t{item_id}:{item_name}:{quantity}:{price_per_item}\t{total_price}\t{paid_status}\t{delivery_status}\t{billing_info['address']}\t{billing_info['contact_number']}"
        )

    try:
        with open(order_filename, 'a') as order_file:
            for line in order_lines:
                order_file.write(line + '\n')
    except Exception as e:
        print(f"An error occurred while saving the order: {e}")



def view_order_history(username):
    print("------ Order History ------")
    try:
        with open('order_history.txt', 'r') as order_file:
            orders = order_file.readlines()
            user_orders = [line.strip() for line in orders if line.startswith(username)]

            if not user_orders:
                print("No orders found for this user.")
                return

            print(f"{'No.':<5} {'Item Name':<30} {'Quantity':<10} {'Total Price':<15} {'Payment Status':<15} {'Delivery Status':<15} {'Billing Address':<30} {'Contact Number':<15}")
            print("-" * 150)

            for order_number, order in enumerate(user_orders, 1):
                order_data = order.split('\t')
                items = order_data[1:-5]  # Get all items except username, total price, payment status, delivery status, and billing info
                total_price = order_data[-5]  # This needs to be the total price for all items in the order
                payment_status = order_data[-4]
                delivery_status = order_data[-3]
                billing_address = order_data[-2]
                contact_number = order_data[-1]

                for item in items:
                    item_info = item.split(':')
                    if len(item_info) < 4:
                        continue
                    item_name = item_info[1]
                    quantity = item_info[2]
                    price_per_item = item_info[3]
                    # Use the total_price from order_data instead of price_per_item
                    print(f"{order_number:<5} {item_name:<30} {quantity:<10} {total_price:<15} {payment_status:<15} {delivery_status:<15} {billing_address:<30} {contact_number:<15}")

            while True:
                action = input("Enter the order number to Cancel or Pay (or 'B' to go back): ").strip().upper()
                if action == 'B':
                    break
                try:
                    order_index = int(action) - 1
                    if 0 <= order_index < len(user_orders):
                        order_data = user_orders[order_index].split('\t')
                        payment_status = order_data[-4]

                        if payment_status == "Not Paid":
                            action_choice = input("Enter 'C' to Cancel or 'P' to Pay: ").strip().upper()
                            if action_choice == 'C':
                                cancel_order(username, order_index, user_orders)
                                break
                            elif action_choice == 'P':
                                pay_order(username, order_index, user_orders)
                                break
                            else:
                                print("Invalid choice. Please enter 'C' to Cancel or 'P' to Pay.")
                        else:
                            print("This order is already paid or canceled and cannot be modified.")
                    else:
                        print("Invalid order number. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a valid order number.")
    except FileNotFoundError:
        print("No order history found.")
    except Exception as e:
        print(f"An error occurred while reading order history: {e}")


def cancel_order(username, order_index, user_orders):
    try:
        with open('order_history.txt', 'w') as order_file:
            for i, line in enumerate(user_orders):
                if i == order_index and line.startswith(username):
                    order_data = line.strip().split('\t')
                    order_data[-4] = "Cancelled"  # Update payment status to "Cancelled"
                    updated_order = '\t'.join(order_data) + '\n'
                    order_file.write(updated_order)  # Write the updated order
                else:
                    order_file.write(line + '\n')
        print("Order has been canceled.")
    except Exception as e:
        print(f"An error occurred while canceling the order: {e}")

def pay_order(username, order_index, user_orders):
    try:
        order_data = user_orders[order_index].strip().split('\t')
        billing_info = payment_page()  # This should return the updated billing info

        if billing_info:  # If payment was successful
            # Update the order status in order history
            with open('order_history.txt', 'w') as order_file:
                for i, line in enumerate(user_orders):
                    if i == order_index and line.startswith(username):
                        order_data[-4] = "Paid"  # Update payment status to "Paid"
                        order_data[-3] = "Packaging"  # Update delivery status to "Packaging"
                        # Update billing address and contact number
                        order_data[-2] = billing_info['address']
                        order_data[-1] = billing_info['contact_number']
                        updated_order = '\t'.join(order_data) + '\n'
                        order_file.write(updated_order)
                    else:
                        order_file.write(line + '\n')
            print("Payment successful! The order status has been updated to 'Paid', delivery status to 'Packaging', and billing info updated.")

            # Update inventory
            inventory_data = load_inventory()
            inventory_dict = {item[0]: item for item in inventory_data}

            items = order_data[1:-5]  # Get all items for this order
            for item in items:
                item_info = item.split(':')
                item_id = item_info[0]
                quantity = int(item_info[2])  # Get the quantity ordered

                if item_id in inventory_dict:
                    available_quantity = int(inventory_dict[item_id][2])
                    new_quantity = available_quantity - quantity
                    if new_quantity < 0:
                        print(f"Error: Not enough stock for item {item_id}.")
                    else:
                        inventory_dict[item_id][2] = str(new_quantity)  # Update the available quantity
                else:
                    print(f"Warning: Item {item_id} not found in inventory.")

            save_inventory([inventory_dict[key] for key in inventory_dict])  # Save updated inventory

        else:
            print("Payment was not successful. Please try again.")
    except Exception as e:
        print(f"An error occurred while processing the payment: {e}")



def customer_menu(username,user_data):
    cart = []
    while True:
        try:
            print("\n--- Customer Menu ---")
            print("1 - View Catalog")
            print("2 - Shopping Cart")
            print("3 - Order History")
            print("4 - Profile")
            print("5 - Repair Service")
            print("6 - Logout (Item in shopping cart will be removed)")

            choice = get_input("Choose an option: ")

            if choice == '1':
                view_catalog(cart)
            elif choice == '2':
                manage_cart(cart, username)
            elif choice == '3':
                view_order_history(username)
            elif choice == '4':
                modify_profile(user_data)
            elif choice == '5':
                customer_repair_menu(username)
            elif choice == '6':
                logout(user_data)
                break
            else:
                print('Invalid option. Please try again.')
        except Exception as e:
            print(f"An error occurred: {e}")


def manage_stock_orders():
    while True:
        print("\n--- Stock Order Management ---")
        print("1 - Place a Stock Order")
        print("2 - View Stock Order History")
        print("3 - Update Stock Status")
        print("B - Back")

        choice = get_input("Choose an option: ")

        if choice == '1':
            place_stock_order()
        elif choice == '2':
            view_stock_order_history()
        elif choice == '3':
            update_stock_status()
        elif choice.upper()== 'B':
            break
        else:
            print('Invalid option. Please try again.')


def place_stock_order():
    try:
        item_id = get_input("Enter the item ID to purchase (or 'B' to go back): ").strip()
        if item_id.upper() == 'B':
            return
        item_name = get_input("Enter the item name: ").strip()

        # Choose stock type
        stock_type_choice = get_input("Choose stock type (1 - Wares, 2 - Repairs): ")
        if stock_type_choice == '1':
            stock_type = 'Wares'
        elif stock_type_choice == '2':
            stock_type = 'Repairs'
        else:
            print("Invalid choice. Defaulting to 'Wares'.")
            stock_type = 'Wares'

        quantity = int(get_input("Enter the quantity to purchase: ").strip())
        price = float(get_input("Enter the price per unit: ").strip())
        status = "Pending"
        total_price = quantity * price  # Calculate total price

        with open('stock_orders.txt', 'a') as stock_file:
            stock_file.write(f"{item_id}\t{item_name}\t{quantity}\t{price}\t{total_price}\t{status}\t{stock_type}\n")

        print(f"Stock order placed for {quantity} units of {item_name}, total price RM{total_price}. Status: {status}, Type: {stock_type}")

    except ValueError:
        print("Invalid input. Please enter valid numbers for quantity and price.")
    except Exception as e:
        print(f"An error occurred while placing the stock order: {e}")


def view_stock_order_history():
    try:
        with open('stock_orders.txt', 'r') as stock_file:
            orders = stock_file.readlines()

        print("------ Stock Order History ------")
        print(
            f"{'No.':<5} {'Item ID':<10} {'Item Name':<30} {'Quantity':<10} {'Price':<10} {'Total Price(RM)':<18} {'Status':<10} {'Type':<10}")
        print("-" * 115)

        for index, line in enumerate(orders):
            order_data = line.strip().split('\t')
            if len(order_data) == 7:  # Ensure there are enough fields
                print(
                    f"{index + 1:<5} {order_data[0]:<10} {order_data[1]:<30} {order_data[2]:<10} {order_data[3]:<10} {order_data[4]:<18} {order_data[5]:<10} {order_data[6]:<10}")

    except FileNotFoundError:
        print("No stock order history found.")
    except Exception as e:
        print(f"An error occurred while reading stock order history: {e}")



def update_stock_status():
    try:
        with open('stock_orders.txt', 'r') as stock_file:
            orders = stock_file.readlines()

        print("------ Pending Stock Orders ------")
        pending_orders = []
        for index, line in enumerate(orders):
            order_data = line.strip().split('\t')
            if order_data[-2] == "Pending":  # Check status
                pending_orders.append((index, order_data))
                print(
                    f"{len(pending_orders)}. {order_data[1]} - {order_data[2]} units at {order_data[3]} each. Status: {order_data[-2]}, Type: {order_data[-1]}")

        if not pending_orders:
            print("No pending orders found.")
            return

        while True:
            try:
                order_choice = int(get_input("Enter the number of the order to update to 'Received': ").strip()) - 1

                if 0 <= order_choice < len(pending_orders):
                    order_index, order_data = pending_orders[order_choice]
                    orders[order_index] = "\t".join(
                        order_data[:-2] + ["Received", order_data[-1]]) + "\n"  # Keep the stock type

                    with open('stock_orders.txt', 'w') as stock_file:
                        stock_file.writelines(orders)

                    # Update inventory
                    item_id = order_data[0]
                    item_name = order_data[1]
                    quantity = int(order_data[2])
                    stock_type = order_data[-1]  # Get stock type

                    inventory = load_inventory()
                    inventory_dict = {item[0]: item for item in inventory}

                    if item_id in inventory_dict:
                        inventory_dict[item_id][2] = str(int(inventory_dict[item_id][2]) + quantity)
                    else:
                        inventory_dict[item_id] = [item_id, item_name, str(quantity), order_data[3],
                                                   stock_type]  # Save stock type

                    save_inventory([inventory_dict[key] for key in inventory_dict])
                    print(f"Order for {order_data[1]} has been updated to 'Received' and inventory has been updated.")
                    return  # Exit function after successful update

                else:
                    print("Invalid order number. Please try again.")

            except ValueError:
                print("Invalid input. Please enter a valid number.")
            except Exception as e:
                print(f"An error occurred while updating the stock status: {e}")

    except FileNotFoundError:
        print("No stock order history found.")
    except Exception as e:
        print(f"An error occurred while reading stock orders: {e}")


def update_user_info_in_file(username,field_index, new_value):
    # Open the file and read all lines
    with open('users.txt', 'r') as file:
        lines = file.readlines()

    # Open the file in write mode to update user info
    with open('users.txt', 'w') as file:
        for line in lines:
            data = line.strip().split('\t')  # Assuming tab-separated values
            if data[2] == username: # Check if this is the user's line
                data[field_index] = new_value  # Update the specific field
                line = '\t'.join(data) + '\n'  # Reconstruct the line with updated information
            file.write(line)

def modify_profile(user_data):
    while True:
        print(f"\n--- {user_data[4]}'s profile ---")
        print(f"1. Username: {user_data[2]}")
        print(f"2. Password: {user_data[3]}")
        print(f"3. Full Name: {user_data[4]}")
        print(f"4. IC Number: {user_data[6]}")
        print(f"5. Email: {user_data[7]}")
        print(f"6. Phone: +60{user_data[8]}")
        print("7. Back to customer menu")
        option = input('Which information that you want to modify?: ').strip()


        if option == '1':
            while True:
                username = input(
                    "Enter new username (only letters allowed, at least 5 characters long) or 'B' to go back: ")
                if username.upper() == 'B':
                    break
                elif not is_valid_username(username):
                    print("Invalid username. It should only contain letters and be at least 5 characters long.")
                elif username == user_data[2]:
                    print("New username cannot be the same as the previous one.")
                elif check_username_exists(username):
                    print("Username already exists. Please choose a different username.")
                else:
                    update_user_info_in_file(user_data[2],2,username) # Update username
                    user_data[2] = username  # Update the username in user_data
                    print("Username modify successfully!")
                    break

        elif option == '2':
            while True:
                password = input("Enter new password (at least 8 characters, including 1 uppercase, 1 lowercase, and 1 symbol) or 'B' to go back: ").strip()
                if password.upper() == 'B':
                    break
                elif not is_valid_password(password):
                    print("Invalid password. It should be at least 8 characters long and include at least one uppercase letter, one lowercase letter, and one symbol.")
                elif password == user_data[3]:
                    print("Entered password is same as previous.")
                else:
                    update_user_info_in_file(user_data[2],3, password)  # Update password
                    user_data[3] = password  # Update the password in user_data
                    print("Password modified successfully!")
                    break

        elif option == '3':
            while True:
                full_name = input("Enter new full name (or 'B' to go back): ").strip()
                if full_name.upper() == 'B':
                    break
                elif full_name == user_data[4]:
                    print("Entered full_name is same as previous.")
                elif not is_valid_full_name(full_name):
                    print("Invalid full name. It should contain at least a first name and a last name.")
                else:
                    update_user_info_in_file(user_data[2],4, full_name)  # Update full name
                    user_data[4] = full_name  # Update the full name in user_data
                    print("Full name modified successfully!")
                    break

        elif option == '4':
            while True:
                ic_number = input("Enter new IC Number (or 'B' to go back): ").strip()
                if ic_number.upper() == 'B':
                    break
                formatted_ic = format_ic(ic_number)  # Format the IC number
                if formatted_ic == user_data[6]:
                    print("Entered IC Number is the same as the previous one.")
                elif not is_valid_ic(ic_number):
                    print("Invalid IC Number. Ensure it is 12 digits long and contains only digits.")
                else:
                    update_user_info_in_file(user_data[2], 6, formatted_ic)  # Update IC Number
                    city = get_city_of_domicile(ic_number)
                    update_user_info_in_file(user_data[2], 9, city)  # Update City
                    user_data[6] = formatted_ic
                    print("IC Number modified successfully!")
                    break

        elif option == '5':
            while True:
                email = input("Enter new email (or 'B' to go back): ").strip()
                if email.upper() == 'B':
                    break
                elif email == user_data[7]:
                    print("Entered email is same as previous.")
                elif not is_valid_email(email):
                    print("Invalid email format. Ensure it is in xxx@xxx.xxx format.")
                else:
                    update_user_info_in_file(user_data[2], 7, email)  # Update email
                    user_data[7] = email  # Update the email in user_data
                    print("Email modified successfully!")
                    break


        elif option == '6':
            while True:
                phone = input("Enter your phone number (9 to 10 digits, numeric only) or 'B' to go back: +60").strip()
                if phone.upper() == 'B':
                    break
                elif phone == user_data[8]:
                    print("Entered phone number is same as previous.")
                elif not is_valid_phone(phone):
                    print("Invalid phone number. It must be numeric and between 9 to 10 digits long.")
                else:
                    update_user_info_in_file(user_data[2], 8, phone)  # Update phone
                    user_data[8] = phone  # Update the phone in user_data
                    print("Phone number modified successfully!")
                    break

        elif option == '7':
            print("Returning to customer menu...")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


def cus_orders():
    while True:
        print("------ All Customer Orders ------")
        orders = load_order_history()

        if not orders:
            print("No orders found.")
            return

        print(f"{'No.':<5} {'Username':<15} {'Item Name':<30} {'Quantity':<10} {'Total Price':<15} {'Payment Status':<15} {'Delivery Status':<15} {'Billing Address':<30} {'Contact Number(+60)':<15}")
        print("-" * 165)

        order_number = 1
        for order in orders:
            username = order[0]
            items = order[1:-5]  # Get all items except username, total price, payment status, delivery status, and billing info
            total_price = order[-5]
            payment_status = order[-4]
            delivery_status = order[-3]
            billing_address = order[-2]
            contact_number = order[-1]

            for item in items:
                item_info = item.split(':')
                if len(item_info) < 4:
                    continue

                item_name = item_info[1]
                quantity = item_info[2]

                print(f"{order_number:<5} {username:<15} {item_name:<30} {quantity:<10} {total_price:<15} {payment_status:<15} {delivery_status:<15} {billing_address:<30} {contact_number:<15}")
                order_number += 1

        action = get_input("Enter the order number to view details or 'B' to go back: ").strip().upper()
        if action == 'B':
            break
        try:
            order_index = int(action) - 1
            if 0 <= order_index < len(orders):
                order_data = orders[order_index]
                payment_status = order_data[-4]
                delivery_status = order_data[-3]

                # Admin action menu
                while True:
                    action_choice = get_input("Enter 'C' to Cancel, or 'D' to Change Delivery Status (or 'B' to go back): ").strip().upper()
                    if action_choice == 'B':
                        break
                    elif action_choice == 'C':
                        staff_cancel_order(order_index, orders)
                        break
                    elif action_choice == 'D':
                        if delivery_status == "Packaging" and payment_status not in ["Canceled", "Not Paid"]:
                            change_delivery_status(order_index, orders)  # Change delivery status
                            break
                        else:
                            print("Delivery status cannot be changed as the order is already being processed or payment status is not valid.")
                    else:
                        print("Invalid choice. Please enter 'M', 'C', 'D', or 'B'.")
            else:
                print("Invalid order number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid order number.")
        except Exception as e:
            print(f"An error occurred: {e}")


def change_delivery_status(order_index, orders):
    try:
        order_data = orders[order_index]
        order_data[-3] = "Delivered"  # Update delivery status to "Delivered"

        # Update the order history file
        with open('order_history.txt', 'w') as order_file:
            for i, line in enumerate(orders):
                if i == order_index:
                    # Convert all elements to strings before joining
                    updated_order = '\t'.join(str(item) for item in order_data) + '\n'
                    order_file.write(updated_order)
                else:
                    # Ensure each line is written correctly as it was read
                    order_file.write('\t'.join(str(item) for item in line) + '\n')

        print("Delivery status updated to 'Delivered'.")
    except Exception as e:
        print(f"An error occurred while updating the delivery status: {e}")


def load_order_history(username=None):
    try:
        with open('order_history.txt', 'r') as file:
            orders = file.readlines()
            if username:
                return [order.strip().split('\t') for order in orders if order.startswith(username)]
            return [order.strip().split('\t') for order in orders]
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"An error occurred while loading order history: {e}")
        return []

def staff_cancel_order(order_index, orders):
    try:
        # Check if the delivery status allows for cancellation
        delivery_status = orders[order_index][-3]
        if delivery_status == "Delivered":
            print("Order cannot be canceled as it has already been delivered.")
            return

        # Update the order status to "Canceled"
        orders[order_index][-4] = "Canceled"

        # Write the updated orders back to the file
        with open('order_history.txt', 'w') as file:
            for order in orders:
                file.write('\t'.join(order) + '\n')

        print("Order has been canceled.")
    except Exception as e:
        print(f"An error occurred while canceling the order: {e}")


def load_delivered_items(username):
    delivered_items = []
    try:
        with open('order_history.txt', 'r') as file:
            for line in file:
                data = line.strip().split('\t')
                if data[0] == username and data[4] == 'Delivered':  # Check username and delivery status
                    item_details = data[1].split(':')
                    delivered_items.append(item_details[1])  # Extract the item name (2nd part)
    except FileNotFoundError:
        print("Order history file not found.")
    return delivered_items


def customer_repair_menu(username):
    while True:
        print("\n------ Customer Repair Menu ------")
        print("1 - View Repair Order History")
        print("2 - Request a Repair")
        print("3 - Go Back")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            view_repair_order_history(username)
        elif choice == '2':
            request_repair(username)
        elif choice == '3':
            break
        else:
            print("Invalid option. Please try again.")


def request_repair(username):
    print("------ Request Repair ------")

    # Load delivered items
    delivered_items = load_delivered_items(username)

    if not delivered_items:
        print("You have no delivered items to request a repair for.")
        return

    print("You can request repairs for the following items:")
    for idx, item in enumerate(delivered_items, 1):
        print(f"{idx}. {item}")

    # Choose delivered item
    while True:
        choice = input("Choose an item to repair (or 'B' to go back): ").strip().upper()
        if choice == 'B':
            return
        try:
            item_index = int(choice) - 1
            if 0 <= item_index < len(delivered_items):
                selected_item = delivered_items[item_index]
                break
            else:
                print("Invalid choice. Please select a valid item number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Choose issue type
    while True:
        issue_type = input("Choose issue type (1 - Hardware, 2 - Software): ").strip()
        if issue_type in ['1', '2']:
            issue_type = 'Hardware' if issue_type == '1' else 'Software'
            break
        else:
            print("Invalid choice. Please enter 1 for Hardware or 2 for Software.")

    # Describe issue
    issue_description = input("Describe your issue: ").strip()

    # Write repair request to file
    with open('repair_requests.txt', 'a') as file:
        file.write(f"{username}\t{selected_item}\t{issue_type}\t{issue_description}\tPending\n")

    print("Repair request submitted successfully.")


def manage_repair_requests():
    print("------ Manage Repair Requests ------")
    repair_requests = load_repair_requests()

    if not repair_requests:
        print("No repair requests found.")
        return

    # Admins see all requests, including Pending, Canceled, and Approved
    print(f"{'No.':<5} {'Username':<15} {'Item Name':<15} {'Issue Type':<15} {'Issue Description':<40} {'Status':<15}")
    print("-" * 120)

    for idx, request in enumerate(repair_requests, 1):
        if len(request) >= 5:  # Check for at least 5 columns
            username, item_name, issue_type, issue_description, status = request[:5]
            print(f"{idx:<5} {username:<15} {item_name:<15} {issue_type:<15} {issue_description:<40} {status:<15}")

    while True:
        action = input("Enter the request number to manage (or 'B' to go back): ").strip().upper()
        if action == 'B':
            break

        try:
            request_index = int(action) - 1
            if 0 <= request_index < len(repair_requests):
                request_data = repair_requests[request_index]
                if len(request_data) >= 5:  # Ensure at least 5 columns are processed
                    username, item_name, issue_type, issue_description, status = request_data[:5]

                    if status == 'Pending':
                        action_choice = input("Enter 'A' to Approve, 'C' to Cancel (or 'B' to go back): ").strip().upper()
                        if action_choice == 'B':
                            continue
                        elif action_choice == 'C':
                            request_data[4] = 'Canceled'
                            print("Repair request canceled.")
                        elif action_choice == 'A':
                            if issue_type == 'Hardware':
                                repair_item = assign_repair_item()
                                request_data.append(repair_item)
                            request_data[4] = 'Approved'
                            print("Repair request approved.")
                        else:
                            print("Invalid choice. Please enter 'A', 'C', or 'B'.")
                    else:
                        print("This request has already been processed.")

                    # Update repair requests file
                    update_repair_requests_file(repair_requests)
            else:
                print("Invalid request number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid request number.")
        except Exception as e:
            print(f"An error occurred: {e}")


def assign_repair_item():
    inventory_file = 'inventory.txt'
    repair_items = []
    inventory_data = []

    # Load inventory from inventory.txt
    try:
        with open(inventory_file, 'r') as file:
            for line in file:
                data = line.strip().split('\t')
                item_id = data[0]
                item_name = data[1]
                item_quantity = int(data[2])
                item_price = float(data[3])
                item_type = data[4]

                inventory_data.append([item_id, item_name, item_quantity, item_price, item_type])

                if item_type == "Repairs":
                    repair_items.append([item_id, item_name, item_quantity, item_price])
    except FileNotFoundError:
        print("Inventory file not found.")
        return 'N/A'

    if not repair_items:
        print("No repair items available.")
        return 'N/A'

    print("Available Repair Items:")
    for idx, (item_id, item_name, item_quantity, item_price) in enumerate(repair_items, 1):
        print(f"{idx}. {item_name} (Quantity: {item_quantity}, Price: {item_price})")

    while True:
        choice = input("Choose a repair item to assign (or 'B' to go back): ").strip().upper()
        if choice == 'B':
            return 'N/A'
        try:
            item_index = int(choice) - 1
            if 0 <= item_index < len(repair_items):
                selected_item = repair_items[item_index]
                selected_item_id = selected_item[0]
                selected_item_name = selected_item[1]
                selected_item_quantity = selected_item[2] - 1  # Decrement the quantity

                if selected_item_quantity < 0:
                    print("No more of this item is available.")
                    return 'N/A'

                # Update the inventory data with the new quantity
                for item in inventory_data:
                    if item[0] == selected_item_id:
                        item[2] = selected_item_quantity  # Update the quantity

                # Write the updated inventory back to the file
                try:
                    with open(inventory_file, 'w') as file:
                        for item in inventory_data:
                            file.write('\t'.join([str(i) for i in item]) + '\n')
                except IOError:
                    print("Error writing to inventory file.")
                    return 'N/A'

                print(f"Assigned {selected_item_name}. Remaining quantity: {selected_item_quantity}")
                return selected_item_name  # Return the name of the selected item
            else:
                print("Invalid choice. Please select a valid item number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def view_repair_order_history(username):
    print("------ Repair Order History ------")
    repair_orders = load_repair_requests(username)

    if not repair_orders:
        print("No repair orders found.")
        return

    print(f"{'Order ID':<10} {'Item Name':<30} {'Issue':<40} {'Status':<15}")
    print("-" * 100)

    for idx, order in enumerate(repair_orders, 1):
        order_id = idx
        item_name = order[1]
        issue = order[2]
        status = order[4]
        print(f"{order_id:<10} {item_name:<30} {issue:<40} {status:<15}")



def load_repair_requests(username=None):
    repair_requests = []
    try:
        with open('repair_requests.txt', 'r') as file:
            for line in file:
                data = line.strip().split('\t')
                if not username or data[0] == username:
                    repair_requests.append(data)
    except FileNotFoundError:
        pass
    return repair_requests


def update_repair_requests_file(repair_requests):
    with open('repair_requests.txt', 'w') as file:
        for req in repair_requests:
            file.write('\t'.join(req) + '\n')

homepage()
