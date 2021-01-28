import re
from db_config import connection, cursor


def existed_root_user_checker():
    existed_user_query = "SELECT username FROM passwords WHERE service='root_service';"
    try:
        cursor.execute(existed_user_query)
        existed_user = cursor.fetchall()
        return len(existed_user)
    except IndexError as e:
        return '*** you need to create root password ***'


def root_password_checker(password):
    root_password_query = "SELECT password FROM passwords WHERE service='root_service'"
    cursor.execute(root_password_query)
    root_password = cursor.fetchone()
    if str(password) == str(root_password[0]):
        return '*** success ***'
    else:
        return '*** failed ***'


def set_up_root_password(password):
    root_password_set_up_query = 'INSERT INTO passwords(id, service, username, password, hash_password)' \
                                 ' VALUES(1, \'root_service\', \'root_user\', \'%s\', \'***\' );' % password
    cursor.execute(root_password_set_up_query)
    connection.commit()
    return '*** root password was created ***'


def root_password_requirements_checker(password):
    pattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$"
    if len(password) >= 8:
        result = re.findall(pattern, password)
        if result:
            set_up_root_password(password)
            return "*** password requirements are met ***"
        else:
            return "*** password requirements not met ***"


def commands_info():
    output_info = '*** available commands ***\n' \
                  '\t -a - to add new password\n' \
                  '\t -v - to view your passwords\n' \
                  '\t -d - to delete your password\n'
    return output_info


def command_checker(command_input):
    command_list = ['-a', '-v', '-d']
    if command_input not in command_list:
        return f'*** {command_input} is not a command ***'
    elif command_input == '-a':
        pass
    elif command_input == '-v':
        pass
    elif command_input == '-d':
        pass


if __name__ == '__main__':
    if existed_root_user_checker() == 0:
        root_password_set_up = input('create your root password: ')
        print(set_up_root_password(root_password_set_up))
    else:
        root_password_for_check = input('your root password: ')
        print(root_password_checker(root_password_for_check))
        print(commands_info())
