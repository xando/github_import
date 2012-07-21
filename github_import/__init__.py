import sys
import imp
import os
import new
import subprocess


class ImportHook(object):

    def find_module(self, fullname, path=None):
        if fullname.startswith('github'):
            return self

    def load_module(self, fullname):

        if len(fullname.split(".")) < 4:
            module = new.module(fullname)
            module.__file__ = "fake:" + fullname
            module.__path__ = []
            return sys.modules.setdefault(fullname, module)

        module_name = fullname.split(".")[-1]
        repo_root = "/tmp/github"
        repo_dir = "%s/%s" % (repo_root, module_name)

        if len(fullname.split(".")) == 4:

            user = fullname.split(".")[-2]

            if not os.path.exists(repo_root):
                os.mkdir(repo_root)

            if os.path.exists(repo_dir):
                subprocess.call(
                    "cd %s && git pull -q" % repo_dir, shell=True
                )
            else:
                subprocess.call(
                    "git clone git://github.com/%s/%s.git %s -q"
                    % (user, module_name, repo_dir),
                    shell=True
                )
            sys.path.insert(0, repo_root)

            try:
                return __import__(module_name)
            except ImportError:
                sys.path.pop(0)

                module = imp.new_module(fullname)
                module.__file__ = "fake:" + fullname
                module.__path__ = [fullname]
                module.__loader__ = self
                sys.modules.setdefault(fullname, module)
                return module

        if len(fullname.split(".")) > 4:
            try:
                return __import__(".".join(fullname.split(".")[3:]))
            except ImportError:
                sys.modules.pop(module_name, None)

                sys.path.insert(
                    0,os.path.join(repo_dir, "/".join(fullname.split(".")[5:])))

                return __import__(".".join(fullname.split(".")[4:]))



sys.meta_path.insert(0, ImportHook())

