import bcrypt

from .models import UserModel

def groupfinder(user_id, request):
	user = UserModel()
	acl_list = user.getAcl(user_id)
	return acl_list
