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


if __name__ == '__main__':
    if existed_root_user_checker() == 0:
        root_password_set_up = input('create your root password: ')
        print(set_up_root_password(root_password_set_up))
    else:
        print('*** command list ***')
