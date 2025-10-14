from core.models import LegacyStudent
def get_all_students():
    return LegacyStudent.objects.all()

def search_students(query='', school_name=None, limit=20):
    students = LegacyStudent.objects.all()
    if query:
        students = students.filter(name__icontains=query)
    if school_name:
        students = students.filter(school_name__icontains=school_name)
    return students[:limit]