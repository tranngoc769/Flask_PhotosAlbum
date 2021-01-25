import os
def get_extension(filename):
      extension = os.path.splitext(filename)[1][1:]
      return extension