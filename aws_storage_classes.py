# This is used to create 2 different location to store files in /media/ and /static/
from storages.backends.s3boto import S3BotoStorage

# For Static files
class StaticStorage(S3BotoStorage):
	location = 'static'

# For Media Files
class MediaStorage(S3BotoStorage):
	location = 'media'
