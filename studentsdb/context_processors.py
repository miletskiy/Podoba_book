from .settings import PORTAL_URL

def students_proc(request):
	return {'PORTAL_URL':PORTAL_URL}

# from .util import get_groups
# from students.util import get_groups

# def groups_processor(request):
#     return {'GROUPS':get_groups(request)}