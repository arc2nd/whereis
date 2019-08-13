#!/usr/bin/env python

from datetime import datetime
import bcrypt
import config
import db


class User(object):
    role_id = 0
    username = 'John'
    password = 'test'
    email_address = 'fake@email.com'
    first_name = 'John'
    middle_name = 'Q'
    last_name = 'Doe'

    def __init__(self):
        self.role_id = 0

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def _get_db_conn():
        return db.build_conn('users')

    @staticmethod
    def GetAll():
        all_users = []
        for doc in User._get_db_conn().find():
            all_users.append(doc)
        return all_users

    # Properties
    @property
    def full_name(self):
        name = None
        name = self.first_name

        if self.middle_name != None:
            name += ' ' + self.middle_name

        if self.last_name != None:
            name += ' ' + self.last_name

        return name

    # Create operations
    def Add(self):
        """ Add a user """
        # allUsers = User.GetAll()
        # for user in allUsers:
        #     if user.email_address == self.email_address:
        #         raise ErrorHandler.ErrorHandler(message="user with that email address already exists", status_code=400)

        # if(not self.first_name or not self.password or not self.username):
        #     raise ErrorHandler.ErrorHandler(message="one or more required fields are missing", status_code=400)

        # encrypt the password
        self.password = User.EncryptPassword(self.password)


        user_dict = {'username': self.username, 
                     'pwd_hash': self.password, 
                     'email_address': self.email_address, 
                     'role_id': self.role_id, 
                     'first_name': self.first_name, 
                     'middle_name': self.middle_name, 
                     'last_name': self.last_name}

        coll_store = self._get_db_conn()
        if not coll_store.find(user_dict).count():
            rec_id = coll_store.insert_one(user_dict)
            return rec_id.inserted_id
        else:
            print('already found: {0} in DB\nDon\'t want to make a duplicate'.format(user_dict))

        return True

    def Load(self):
        """ Load user data form db """
        coll_store = self._get_db_conn()
        if self.VerifyPassword(self.password):
            myself = self._get_db_conn().find_one({'username': self.username})
            self.role_id = myself['role_id']
            self.first_name = myself['first_name']
            self.middle_name = myself['middle_name']
            self.last_name = myself['last_name']
            self.email_address = myself['email_address']
            
            

    # Read operations
    @staticmethod
    def GetByUsername(username):
        """ Return a user by username """
        user = User()
        if os.path.exists('users.json'):
            with open('users.json', 'r') as fp:
                all_users = json.load(fp)
            if username in all_users:
                temp = all_users[username]
            user.username = temp.username
            user.password = temp.password
            user.email_address = temp.email_address
            user.first_name = temp.first_name
            user.middle_name = temp.middle_name
            user.last_name = temp.last_name
        return user

    # Update operations
    
    def ResetPassword(self, new_password=None, new_password_verify=None):
        """ Updates a user's password without old password verification """

        if(not new_password or not new_password_verify):
            raise ErrorHandler.ErrorHandler(message="password or password verification was empty", status_code=400)

        if new_password == new_password_verify:
            new_password = User.EncryptPassword(new_password)
            self.password = new_password
            db.session.commit()
            return True
        else:
            raise ErrorHandler.ErrorHandler(message="passwords do not match", status_code=400)
        

    def UpdatePassword(self, new_password=None, new_password_verify=None, old_password=None):
        """ Updates a user's password """
        if new_password == new_password_verify:
            if self.VerifyPassword(old_password):
                new_password = User.EncryptPassword(new_password)
                self.password = new_password
                db.session.commit()
                return True
            else:
                raise ErrorHandler.ErrorHandler(message="old password does not match stored password", status_code=400)
        else:
            raise ErrorHandler.ErrorHandler(message="passwords do not match", status_code=400)

    # Delete operations

    # Utility operations
    @staticmethod
    def EncryptPassword(password_to_encrypt):
        """ Encode, encrypt, and return the hashed password"""
        if(not password_to_encrypt):
            raise ErrorHandler.ErrorHandler(message="password cannot be empty", status_code=400)
            
        password_to_encrypt = password_to_encrypt.encode('utf-8')
        password_to_encrypt = bcrypt.hashpw(password_to_encrypt, bcrypt.gensalt(12)).decode('utf-8')
        
        return password_to_encrypt

    def VerifyPassword(self, password_to_test=None):
        """ Verifies that an entered password is correct """
        #encrypt password and check against database
        if(bcrypt.checkpw(password_to_test.encode('utf-8'), self.GetHashedPassword().encode('utf-8'))):
            return True
        else:
            return False

    def GetHashedPassword(self):
        """ Get a hashed password from the db """
        # return User.query.filter_by(id=self.id).first().password
        my_hash = None
        my_hash = self._get_db_conn().find_one({'username': self.username})['pwd_hash']
        return my_hash

