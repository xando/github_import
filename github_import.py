import importlib
import sys
import ipdb
import imp
import os


class ImportHook(object):

    def find_module(self, fullname, path=None):
        if fullname.startswith('github') and len(fullname.split(".")) < 5:
            return self

    def load_module(self, fullname):
        if len(fullname.split(".")) == 4:
            user = fullname.split(".")[-2]
            repo = fullname.split(".")[-1]

            repo_root = "/tmp/github"

            if not os.path.exists(repo_root):
                os.mkdir(repo_root)

            repo_dir = "%s/%s" % (repo_root, repo)

            if os.path.exists(repo_dir):
                os.system("cd %s && git pull" % repo_dir)
            else:
                os.system("git clone git://github.com/%s/%s.git %s"
                          % (user, repo, repo_dir))

            sys.path.insert(0, repo_root)
            return importlib.import_module(repo)

        else:
            module = imp.new_module(fullname)
            module.__file__ = "fake:" + fullname
            module.__path__ = []
            module.__loader__ = self
            sys.modules.setdefault(fullname, module)
            return module

sys.meta_path.insert(0, ImportHook())

