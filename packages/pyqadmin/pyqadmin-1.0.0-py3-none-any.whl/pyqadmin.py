####################
##
##  BY : QUEREYZ <queryzram@gmail.com> (ALEXANDER PROKOPENKO)
##  VERSION : 1.0.0
##  NAME : PYADMIN
##
####################


import ctypes, sys


def admin(function):
    def get(*args, **kwargs):
        def is_admin():
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False

        if is_admin():
            function(*args, **kwargs)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    return get