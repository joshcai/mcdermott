import os
import sys

list_file = sys.argv[1]
file_dir = sys.argv[2]

applicants = open(list_file, 'r')
file_names = os.listdir(file_dir)
print file_names

for applicant, file_name in zip(applicants, sorted(file_names)):
  extension = file_name.split('.')[-1]
  new_file_name = '%s.%s' % (applicant.rstrip(), extension)
  os.rename('%s/%s' % (file_dir, file_name), '%s/%s' % (file_dir, new_file_name))

print os.listdir(file_dir)
