import bcrypt

GROUPS = {'gabon': ['group:administration']}

def groupfinder(user, request):
	return GROUPS.get(user, [])
