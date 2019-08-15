import User

if __name__ == '__main__':
    username = raw_input('Username: ')
    first_name = raw_input('First Name: ')
    middle_name = raw_input('Middle Name: ')
    last_name = raw_input('Last Name: ')
    email_address = raw_input('Email Address: ')
    password = raw_input('Password: ')
    verify_pass = raw_input('Verify Password: ')

    new_user = User.User()
    new_user.username = username
    new_user.first_name = first_name
    new_user.middle_name = middle_name
    new_user.last_name = last_name
    new_user.email_address = email_address
    new_user.role_id = 0
    if password == verify_pass:
        new_user.password = password
        new_user.Add()
        print('User added: {}'.format(User.User.GetByUsername(username).__dict__))
    else:
        print('passwords don\'t match')
