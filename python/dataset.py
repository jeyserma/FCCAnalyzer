
import os

class Dataset:

    def __init__(self, name, path, xsec):

        self.name = name
        self.path = path
        self.xsec = xsec
        self.rootfiles = self.findROOTFiles(self.path)

    def findROOTFiles(self, basedir, regex = ""):
        if ".root" in basedir: return [basedir]
        if regex != "":
            if basedir[-1] == "/": basedir = basedir[:-1]
            regex = basedir + "/" + regex

        files = []
        for root, directories, filenames in os.walk(basedir):
            for f in filenames:
                filePath = os.path.join(os.path.abspath(root), f)
                if not ".root" in filePath:
                    continue
                if regex == "" or fnmatch.fnmatch(filePath, regex): files.append(filePath)
        return files
