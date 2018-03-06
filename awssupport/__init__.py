"""
    AWS Support Client
    Reference: http://boto3.readthedocs.io/en/latest/reference/services/support.html#id16
"""

import boto3
from botocore.exceptions import ClientError
import sys


class Client(object):

    def __init__(self, profile):
        """Authentication"""
        self.profile = profile
        session = boto3.Session(profile_name=self.profile, region_name='us-east-1')
        self.client = session.client('support')

    """
        Trusted Advisor
    """
    def describe_checks(self):
        try:
            response = self.client.describe_trusted_advisor_checks(language='en')
            return response
        except ClientError as e:
            print(e.response['Error']['Code'])
            sys.exit()

    def checks_summary(self, check_ids):
        try:
            response = self.client.describe_trusted_advisor_check_summaries(checkIds=check_ids)
            return response
        except ClientError as e:
            print(e.response['Error']['Code'])
            sys.exit()
