"""

Installation:
pip install boto3
pip install pprint

Usage:

  python go.py

Options:

  -p | --profile  AWS Profile '(.aws 'default' credential is default!)'

"""

VERSION = (0, 0, 1, '')

__author__    = 'Justen Doherty'
__license__   = 'BSD 2-Clause'
__version__   = u'.'.join(map(str, VERSION[0:3])) + u''.join(VERSION[3:])

from optparse import OptionParser
import boto3
import pprint
pp = pprint.PrettyPrinter(indent=1)

def dd(stuff):
    print "-------------"
    pp.pprint(stuff)

def getConfig():
    parser = OptionParser()
    parser.add_option('-p', '--profile', dest='profile', default='default',   help='AWS Profile')
    options, args = parser.parse_args()
    return options

def get_s3_bucket_policies(s3):

    buckets = []
    bucket_policies = []

    print "processing s3 bucket policies..."

    bucket_list = s3.list_buckets()

    for bucket in bucket_list['Buckets']:
        bucket_name = bucket['Name']

        if bucket_name not in buckets:
            buckets.append(bucket_name)

        try:
            policies = s3.get_bucket_policy(Bucket=bucket_name)
        except:
            pass
        else:
            if bucket_name not in bucket_policies:
                bucket_policies.append((bucket_name, policies))

    return buckets, bucket_policies

def get_s3_bucket_acls(s3):

    bucket_acls = {}
    bucketList = s3.list_buckets()

    print "processing s3 bucket acls..."

    for bucket in bucketList['Buckets']:

        bucketName = bucket['Name']
        bucket_acls[bucketName] = {}

        grants = s3.get_bucket_acl(Bucket=bucketName)

        for grant in grants['Grants']:

            grantee_name = 'None'
            grantee_id   = 'None'
            grantee = grant['Grantee']

            if 'DisplayName' in grantee:
                grantee_name = grantee['DisplayName']
                grantee_id   = grantee['ID']
            elif 'URI' in grantee:
                grantee_name = grantee['URI'].split('/')[-1]
                grantee_id   = grantee['URI']

            if grantee_name not in bucket_acls[bucketName]:
                bucket_acls[bucketName][grantee_name] = []

            bucket_acls[bucketName][grantee_name].append((grantee_id,grant['Permission']))

    return bucket_acls

'''
get_iam_attached_user_policies(iam)
-----------------------------------
list all iam users and fetch attached policy
return list of users and user_policies
'''
def get_iam_attached_user_policies(iam):

    print "processing iam attached user policies..."

    users = []
    user_policies = []

    for user in iam.list_users()['Users']:

        user_name = user['UserName']

        if user_name not in users:
            users.append(user_name)

        try:
            policies = iam.list_attached_user_policies(UserName=user_name)
        except:
            pass
        else:
            if user_name not in user_policies:
                user_policies.append((user_name, policies))

    return users, user_policies

'''
get_iam_policies(iam)
--------------------------
returns a list of all iam policies
'''
def get_iam_policies(iam):

    print "processing iam policies..."
    iam_policies = []

    for policy in iam.list_policies(Scope='All')['Policies']:
        arn = policy['Arn']
        if arn not in iam_policies:
            iam_policies.append((arn, policy))

    return iam_policies

'''
get_iam_groups_attached_policies(iam)
-------------------------------------
list all groups and fetch attached policy
return list of groups and group_policies
'''
def get_iam_groups_attached_policies(iam):

    groups = []
    group_policies = []

    print "processing iam groups attached policies..."

    for group in iam.list_groups()['Groups']:

        group_name = group['GroupName']

        if group_name not in groups:
            groups.append(group_name)

        for attached_group_policy in iam.list_attached_group_policies(GroupName=group_name)['AttachedPolicies']:
            arn = attached_group_policy['PolicyArn']
            if arn not in group_policies:
                group_policies.append((arn, attached_group_policy))

    return groups, group_policies

'''
print_iam_policy(iam, policy-arn)
---------------------------
print out iam policy information
'''
def print_iam_policy(iam, policyArn):
    dd(iam.get_policy(PolicyArn=policyArn)['Policy'])

'''
run(profile)
-----------
fetch all the info and display it!
'''
def run(profile):

    # get the AWS API clients
    bs = boto3.session.Session(profile_name=profile)
    s3 = bs.client('s3', config=boto3.session.Config(signature_version='s3v4'))
    iam = boto3.client('iam', config=boto3.session.Config(signature_version='s3v4'))

    # fetch the info
    buckets, bucket_policies = get_s3_bucket_policies(s3)
    bucket_acls = get_s3_bucket_acls(s3)
    users, user_policies = get_iam_attached_user_policies(iam)
    iam_policies = get_iam_policies(iam)
    attached_group_policies = get_iam_groups_attached_policies(iam)

    # display..
    output(iam, buckets, bucket_policies, bucket_acls, users, user_policies, iam_policies, attached_group_policies)

'''
output(iam, buckets, bucket_policies, bucket_acls, users, user_policies, iam_policies, attached_group_policies)
---------------
display the info
'''
def output(iam, buckets, bucket_policies, bucket_acls, users, user_policies, iam_policies, attached_group_policies):

    print "------------ "
    print "UNCOMMENT IN SECTIONS IN output() TO VIEW iam, buckets, bucket_policies, bucket_acls, users, user_policies, iam_policies, attached_group_policies CONFIGURATION!!"
    print "------------ "

#    print "buckets"
#    dd(buckets)

#    print "------------ "
#    print "bucket_policies"
#    dd(bucket_policies)

#    print "------------ "
#    print "bucket_acls"
#    dd(bucket_acls)

#    for bucketName, bucket_acl in bucket_acls:
#        print "===================="
#        print "Bucket Name: '%s' | Acl '%s'" % (bucketName, bucket_acl)

#    print "------------ "
#    print "users"
#    dd(users)

#    print "------------ "
#    print "user_policies"
#    for username, policies in user_policies:
#        print "===================="
#        print "policies attached to username '%s'" % username
#        for policy in policies['AttachedPolicies']:
#            print "Policy Name: '%s' | Policy Arn '%s'" % (policy['PolicyName'], policy['PolicyArn'])
#            print_iam_policy(iam, policy['PolicyArn'])

#    print "------------ "
#    print "iam_policies"
#    for arn, policy in iam_policies:
#        print "===================="
#        print "Arn: '%s' | Policy '%s'" % (arn, policy)
#        print_iam_policy(iam, arn)

#    print "------------ "
#    print "attached_group_policies"
#    dd(attached_group_policies)

if __name__ == '__main__':

    profile = getConfig().profile
    run(profile)
