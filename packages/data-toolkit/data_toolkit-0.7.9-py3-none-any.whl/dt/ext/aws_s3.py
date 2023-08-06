'''
Operations to speed up S3 access.
'''

def get_lastest_file(dongle_id: str):
    """
    Get the lastest file in the bucket.
    """
    import boto3
    import pandas as pd

    bucket = 'creationlabs-raw-data'

    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, dongle_id)
    files = obj.meta.client.list_objects(Bucket=bucket, Prefix=dongle_id, Delimiter='/')
    df = pd.DataFrame(files['Contents'])
    last_file = df.sort_values('LastModified',ascending=False).iloc[0]
    last_segment = '/'.join(last_file['Key'].split('/')[:-1])
    ret = f"s3://creationablas-raw-data/{last_segment}"
    return ret

def get_latest_drives(s3_resource, bucket_name, dongle_id: str):
    from dt.ext.aws_s3_list import s3list
    import pandas as pd

    bucket = s3_resource.Bucket(bucket_name)
    bucket_list = list(s3list(bucket, dongle_id, recursive=False, list_dirs=True))
    df = pd.DataFrame(bucket_list) 
    # filter out files with boot crash or swaglog
    df = df[~df.key.str[-5:-1].isin(['glog','boot','rash'])]

    df = df.key.str.split('/', expand=True)
    df.columns = ['dongle_id', 'drive','ext']

    df['date'] = df.drive.str[:10]
    df['time'] = df.drive.str[12:20]
    df['seg_num'] = df.drive.str.split('--').str[-1]

    df = df.sort_values(by=['date','time'], ascending=False)
    df.seg_num = pd.to_numeric(df.seg_num, errors='coerce')
    
    latest_drive = df.iloc[0]
    if len(df) > 1:
        last_complete_drive = df[df.seg_num!=0].iloc[0]
    else:
        last_complete_drive = latest_drive

    return latest_drive, last_complete_drive

    

def get_latest_bucket(target, bucket_name: str = 'creationlabs-raw-data', show_n: int = 25):
    # TODO: profile
    # get all dongle ids
    import boto3 
    import pandas as pd
    import humanize

    pd.set_option('display.max_colwidth',70)
    
    s3 = boto3.resource('s3')
    s3_resource = boto3.session.Session(region_name='eu-west-1').client('s3')


    raw_data_buckets = s3_resource.list_objects_v2(Bucket='creationlabs-raw-data',Delimiter='/')
    dongle_ids = [x['Prefix'].split('/')[0] for x in raw_data_buckets['CommonPrefixes']]

    latest_files = []

    for did in dongle_ids:
        latest_drive, last_complete_drive = get_latest_drives(s3, bucket_name, did)
        latest_files.append(latest_drive)
        latest_files.append(last_complete_drive)

    df = pd.DataFrame(latest_files).reset_index()

    # df['upload_time'] =  df.file.str.split('/').str[-1].str.split('--').str[0:2].str.join('--')
    df['upload_time'] = df.drive.str.split('--').str[:-1].str.join('--')

    # TODO: fix this
    df = df[df.upload_time.str.len() > 16 ] # TODO: fix
    df['upload_time'] = pd.to_datetime(df.upload_time, format='%Y-%m-%d--%H-%M-%S')

    # get naturaltime from now to the time of the latest file
    df['time'] = df['upload_time'].apply(lambda x: humanize.naturaldelta(x))
    df = df.sort_values(by='upload_time', ascending=False)
    print(df.head(show_n))

def download_latest(dongle_id):
    """
    Download the latest file in the bucket.
    """
    import boto3
    import os

    bucket = 'creationlabs-raw-data'
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, dongle_id)
    files = obj.meta.client.list_objects(Bucket=bucket, Prefix=dongle_id)
    last_segment = '/'.join(files['Contents'][-1]['Key'].split('/')[:-1])
    last_drive = '--'.join(last_segment.split('--')[:-1])
    cmd = f'aws s3 sync s3://{bucket}/{dongle_id} .  --exclude="*" --include="{last_drive}*"'
    # s3.meta.client.download_file(bucket, last_drive, dongle_id)
    print(f"Running {cmd}")
    os.system(cmd)