from rolepermissions.roles import AbstractUserRole

class Staff(AbstractUserRole):
  available_permissions = {
    'see_all_info': True,
    'edit_all_info': True,
    'create_users': True,
    'edit_applicants': True,
  }

class Scholar(AbstractUserRole):
  avaliable_permissions = {
    'edit_applicants': False
  }

class CurrentScholar(AbstractUserRole):
  avaliable_permissions = {}

class Alumni(AbstractUserRole):
  available_permissions = {}

class Dev(AbstractUserRole):
  available_permissions = {
    'create_users': True,
    'edit_all_info': True
  }

class ApplicantEditor(AbstractUserRole):
  avaliable_permissions = {
    'edit_applicants': True
  }

class Selection(AbstractUserRole):
    avaliable_permissions = {
    'edit_applicants': True
  }
