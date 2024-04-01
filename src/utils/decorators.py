# https://stackoverflow.com/questions/76249636/class-properties-in-python-3-11
class classproperty:
    def __init__(self, func):
        self.fget = func
    def __get__(self, instance, owner):
        return self.fget(owner)