from rolepermissions.roles import AbstractUserRole

class Staff(AbstractUserRole):
  available_permissions = {
    'see_all_info': True,
    'edit_all_info': True,
    'create_users': True
  }

class Scholar(AbstractUserRole):
  avaliable_permissions = {}

class CurrentScholar(AbstractUserRole):
  avaliable_permissions = {}

class Alumni(AbstractUserRole):
  available_permissions = {}

class Admin(AbstractUserRole):
  available_permissions = {
    'create_users': True
  }
