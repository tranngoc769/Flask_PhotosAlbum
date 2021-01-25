import os
import os.path 
import datetime
def get_extension(filename):
      extension = os.path.splitext(filename)[1][1:]
      return extension
def create_dir(dir_path):
      try:
            os.mkdir(dir_path)
      except:
            pass
def get_current_time():
      now = datetime.datetime.now()
      return now.strftime("%Y-%m-%d %H:%M:%S")