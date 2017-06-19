#!/usr/bin/env python3
import click
import boto3
import re
import time


def exit_if_no_match(match):
  if not match:
    print("s3key was not in format bucket_name/key")
    exit(-1)

def split_to_bucket_and_key(s3key):
  match = re.match("^s3://(?P<bucket>.+)/(?P<key>.*)", s3key)
  exit_if_no_match(match)

  bucket = match.group('bucket')
  key = match.group('key')
  return bucket, key

@click.command()
@click.argument('s3key')
def rollback(s3key):
  """Rollbacks the S3 object to previous version. s3Key must be like s3://mybucket/myfile.txt"""
  bucket, key = split_to_bucket_and_key(s3key)
  s3 = boto3.resource('s3')

  # Delete the latest version
  obj = s3.Object(bucket, key)
  obj.delete(VersionId=obj.version_id)
  latest_version = obj.version_id

  # Mimic touch operation by copying the latest to same bucket and key so that we have same object twice
  # versioned to s3. Delete the second last version, because it is duplicate. The copy operation updates the timestamp.
  s3.meta.client.copy({'Bucket':bucket, 'Key':key, 'VersionId':latest_version},
    bucket, key, ExtraArgs={'Metadata': {'updated_at':str(time.time())}})
  second_latest_version = latest_version # Latest version became second latest when we copied it

  # Delete the second latest version because it is the same as the latest because of copy
  obj.delete(VersionId=second_latest_version)





if __name__ == '__main__':
  rollback()
