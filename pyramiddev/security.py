import bcrypt

GROUPS = {'gabon': ['Administration']}

def groupfinder(user, request):
	return GROUPS.get(user, [])
