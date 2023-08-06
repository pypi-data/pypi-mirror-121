'''
Operations to speed up S3 access.
'''
import pandas as pd


def get_lastest_file(dongle_id: str):
    """
    Get the lastest file in the bucket.
    TODO: eventually paratemrize the -1 to get any file
    """
    import boto3

    s3_resource = boto3.resource('s3')
    bucket_name = 'creationlabs-raw-data'
    bucket = s3_resource.Bucket(bucket_name)

    last_segment, last_complete_drive = get_selected_drives(None, s3_resource, bucket_name, dongle_id, 10)
    # 064b1a99381ec054 2021-09-09--16-31-00 
    drive = '--'.join(last_segment.drive.split('--')[:-1])
    ret = f"http://cl-cabana.eba-eez4uaij.eu-west-1.elasticbeanstalk.com/cabana/?route={last_segment.dongle_id}%7C{drive}"
    return ret

def get_drives_df(s3_resource, bucket_name, dongle_id: str):
    '''
    TODO: this probably requires a significant refactoring.
    '''
    from dt.ext.aws_s3_list import s3list

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
    
    return df

def get_selected_drives(s3, s3_resource, bucket_name, dongle_id, show_n):
    df = get_drives_df(s3_resource, bucket_name, dongle_id)
    latest_drive = df.iloc[0]
    last_complete_drives = df[df.seg_num!=0]

    if len(last_complete_drives) > 0:
        last_complete_drive = last_complete_drives.iloc[0]
    else:
        last_complete_drive = latest_drive

    return latest_drive, last_complete_drive

def get_dongle_drives(s3, s3_resource, bucket_name, dongle_id: str, show_n: int):
    from tqdm import tqdm 

    raw_data_buckets = s3.list_objects_v2(Bucket='creationlabs-raw-data',Delimiter='/')
    dongle_ids = [x['Prefix'].split('/')[0] for x in raw_data_buckets['CommonPrefixes']]

    latest_files = []

    for did in tqdm(sorted(dongle_ids[:show_n])):
        latest_drive, last_complete_drive = get_selected_drives(s3, s3_resource, bucket_name, did, show_n)
        latest_files.append(latest_drive)
        latest_files.append(last_complete_drive)

    df = pd.DataFrame(latest_files).reset_index()
    return df
    

def get_drives(target, bucket_name: str = 'creationlabs-raw-data', 
                        show_n: int = 25, num_segments: int = 1):
    # TODO: profile
    # get all dongle ids
    import boto3 
    import humanize

    pd.set_option('display.max_colwidth',70)
    
    s3 = boto3.session.Session(region_name='eu-west-1').client('s3')
    s3_resource = boto3.resource('s3')

    if target=='-1':
        df = get_dongle_drives(s3, s3_resource, bucket_name, target, show_n)
    else:
        df = get_drives_df(s3_resource, bucket_name, dongle_id=target)

    df['upload_time'] = df.drive.str.split('--').str[:-1].str.join('--')

    # TODO: fix this
    df = df[df.upload_time.str.len() > 16 ]
    df['upload_time'] = pd.to_datetime(df.upload_time, format='%Y-%m-%d--%H-%M-%S')

    # get naturaltime from now to the time of the latest file
    df['time'] = df['upload_time'].apply(lambda x: humanize.naturaldelta(x))
    df = df.sort_values(by='upload_time', ascending=False)

    df = df[['dongle_id','drive','time','upload_time','seg_num']]

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