import re
import base64
from db_config import connection, cursor


def existed_root_user_checker():
    existed_user_query = "SELECT username FROM passwords WHERE service='root_service';"
    try:
        cursor.execute(existed_user_query)
        existed_user = cursor.fetchall()
        return len(existed_user)
    except IndexError as e:
        return '*** you need to create root password ***\n'


def root_password_checker(password):
    root_password_query = "SELECT password FROM passwords WHERE service='root_service'"
    cursor.execute(root_password_query)
    root_password = cursor.fetchone()
    if str(password) == str(root_password[0]):
        return '*** success ***\n'
    else:
        return '*** failed ***\n'


def set_up_root_password(password):
    root_password_set_up_query = 'INSERT INTO passwords(service, username, password, hash_password)' \
                                 ' VALUES(\'root_service\', \'root_user\', \'%s\', \'***\' );' % password
    cursor.execute(root_password_set_up_query)
    connection.commit()
    return '*** root password was created ***\n'


def root_password_requirements_checker(password):
    pattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$"
    if len(password) >= 8:
        result = re.findall(pattern, password)
        if result:
            set_up_root_password(password)
            return "*** password requirements are met ***\n"
        else:
            return "*** password requirements not met ***\n"


def commands_info():
    output_info = '*** available commands ***\n' \
                  '\t -a - to add new password\n' \
                  '\t -v - to view your passwords\n' \
                  '\t -d - to delete your password\n' \
                  '\t -q - to close program\n'
    return output_info


def command_checker(command_input):
    command_list = ['-a', '-v', '-d', '-q']
    if command_input not in command_list:
        return f'*** {command_input} is not a command ***'
    elif command_input == '-a':
        print(add_password())
    elif command_input == '-v':
        print(view_passwords())
    elif command_input == '-d':
        print(delete_password())


def add_password():
    print('*** add password ***')
    service = input('service name: ')
    username = input('username: ')
    password = input('password: ')
    row_hash_password = str(base64.b64encode(b'{password}'))
    hash_password = row_hash_password[2:-1]
    insert_new_password_query = "INSERT INTO passwords(service, username, password, hash_password)" \
                                " VALUES ('%s', '%s', '%s', '%s');" % (service, username, password, hash_password)
    cursor.execute(insert_new_password_query)
    connection.commit()
    return f'*** {username} \'s password for {service} was added ***\n'


def view_passwords():
    print('*** view passwords ***')
    view_passwords_query = "SELECT * FROM passwords OFFSET 1;"
    cursor.execute(view_passwords_query)
    output = ''
    for row in cursor:
        output += f'service - {row[1]}, username - {row[2]}, password - {row[3]}\n'
    return output


def delete_password():
    print("*** delete password ***")
    service = input('input service name: ').lower()
    delete_password_query = "DELETE FROM passwords WHERE service='%s';" % service
    cursor.execute(delete_password_query)
    connection.commit()
    return f'*** password for {service} was deleted ***\n'


if __name__ == '__main__':
    if existed_root_user_checker() == 0:
        root_password_set_up = input('create your root password: ')
        print(set_up_root_password(root_password_set_up))
    else:
        root_password_for_check = input('your root password: ')
        print(root_password_checker(root_password_for_check))
        print(commands_info())
        while True:
            command = input('command: ')
            command_checker(command)
            if command == '-q':
                print('*** closed ***')
                break
