__author__ = 'TTc9082'
import boto
import config

class AWSS3:
    def __init__(self):
        self.conn = boto.connect_s3(aws_access_key_id=config.my_access_key,
                                                  aws_secret_access_key =config.my_secret_key)
        self.c = boto.connect_cloudfront(config.my_access_key, config.my_secret_key)
        print 'establish connection for s3'

    def create_bucket(self, name):
        name = name
        bucket = self.conn.create_bucket(name)
        print 'created an s3 bucket.'
        return bucket

    def create_cloudfront(self, bucket):
        s3origin = boto.cloudfront.origin.S3Origin(dns_name=bucket +'.s3.amazonaws.com')
        stream = self.c.create_streaming_distribution(s3origin, True)
        down = self.c.create_distribution(s3origin, True)
        return down, stream

    def listBuckets(self):
        myBucket = self.conn.get_all_buckets() # Substitute in your bucket name
        return myBucket

    def save_string(self, bucket, name, value):
        myBucket = self.conn.get_bucket(bucket_name=bucket)
        k = myBucket.new_key(name)
        k.set_contents_from_string(value)
        return k.name

    def get_string(self, bucket, name):
        myBucket = self.conn.get_bucket(bucket_name=bucket)
        k = myBucket.lookup(name)
        return k.get_contents_as_string()

    def saveFile(self, bucket, name, filename):
        myBucket = self.conn.get_bucket(bucket)
        k = myBucket.new_key(name)
        k.set_contents_from_filename(filename, policy='public-read')
        return k.name

    def delFile(self, name, bucket):
        myBucket = self.conn.get_bucket(bucket)
        if myBucket:
            k = myBucket.get_key(name)
            if k:
                k.delete()
        return 1

    def makeUrl(self, bucket, keyName):
        myBucket = self.conn.get_bucket(bucket)
        k = myBucket.lookup(keyName)
        if k:
            url = k.generate_url(60, force_http=True)
            return url
        else:
            return False

    def get_all_buckets(self):
        buckets = self.conn.get_all_buckets()
        return buckets