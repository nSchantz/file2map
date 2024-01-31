import clip2yt as c2yt
import os
import sys
import filetypes as ft
import json
import hashlib
import shutil
import exiftool as et

WEBSITE_PATH = '../website' #prob want absolute path
HASH_BYTES = 1024

UPLOAD_LIMIT = 5
vid_upload_cnt = 0

def main():
    if len(sys.argv) != 4:
        print('Usage: python3 file2map <File Directory> <File Type> <Tag>')
        print('File Types: Image=0, Video=1, Text=2')
        exit()

    dir = sys.argv[1]
    type = int(sys.argv[2])
    tag = sys.argv[3]

    # Check Dir Exist
    if not os.path.exists(dir):
        print(f'Path \'{dir}\' does not exist. Exiting...')
        exit()

    json_data = get_json(WEBSITE_PATH, type)

    # open directory with files
    for cnt, file in enumerate(os.listdir(dir)):
        print(f'({cnt + 1}) Processing file \'{file}\'...')
        gen_file(file, json_data, dir, type, tag)
        print(f'\n-----------------------------')

        if vid_upload_cnt >= UPLOAD_LIMIT:
            print('Reached daily upload limit for youtube API. Stopping video processing...')
            break

    print('All files uploaded. Writing json file.')
    write_json(json_data, WEBSITE_PATH, type)


def get_json(web_dir, type):
    map_path = f'{web_dir}/resources'
    
    # This will break if json is empty
    if type is ft.IMAGE_TYPE:
        f = open(f'{map_path}/map-img.json', 'r')
    elif type is ft.VIDEO_TYPE:
        f = open(f'{map_path}/map-vid.json', 'r')
    elif type is ft.TEXT_TYPE:
        f = open(f'{map_path}/map-txt.json', 'r')
    else:
        print('File Type is invalid. Exiting...')
        exit()

    json_data = json.load(f)
    f.close()
    return json_data


def gen_file(file, json_data, file_dir, type, tag):
    file_data = ft.FileData()

    file_data.tag = tag
    
    # file is sha256'd for storage and ID assigning
    assign_id(file, file_dir, file_data)
    
    # check that the file id is not already in its associated json data
    if not new_file_check(file_data, json_data):
        print(f'File \'{file}\' already exists, skipping... (id={file_data.id})')
        return

    # parsing metadata about the file
    if type is ft.IMAGE_TYPE:
        success = parse_img_metadata(file, file_dir, file_data)
    elif type is ft.VIDEO_TYPE:
        result = parse_vid_name(file, file_data)
        success = result[0]
        vid_title = result[1]
    elif type is ft.TEXT_TYPE:
        print("Todo")
    if not success:
        print(f'File \'{file}\' metadata failed to parse, skipping...')
        return    
    
    # uploading file
    if type is ft.IMAGE_TYPE:
        # move image to website resource dir. store the path to image 
        file_data.url = move_img(file, file_dir, file_data, WEBSITE_PATH)
    elif type is ft.VIDEO_TYPE:
        # use moviepy to render/compress raw mp4
        render = render_vid(file)
        if render is None:
            print(f'Video \'{file}\' failed to render, skipping...')
            return

        # get video description
        if tag == '2023-Cross-Country-Trip':
            vid_desc = 'This is some footage during my solo cross country trip riding a V-Strom 650xt. I rode 9000 miles in seven weeks from Georgia to Washington and back. Thanks for watching!'
        else:
            print(f'Tag \'{tag}\' does not have an associated video description, exiting...')
            exit()

        # upload clip and get youtube url
        url = c2yt.upload(render, vid_title, vid_desc)
        if url is None:
            print(f'Video \'{file}\' failed to upload, skipping...')
            return

        # store the youtube link for the video
        vid_data.url = url
    elif type is ft.TEXT_TYPE:
        print("Todo")

    # update json
    update_json(file_data, json_data)

    print(f'File \'{file}\' uploaded.')
    print(f'File Metadata: {file_data}.')

    if type is VIDEO_TYPE:
        vid_upload_cnt = vid_upload_cnt + 1

def new_file_check(file_data, json_data):
    for marker in json_data['markers']:
        if marker['id'] == file_data.id:
            return False

    return True

def assign_id(file, file_dir, file_data):
    with open(f'{file_dir}/{file}', 'rb') as f:
        file_bytes = f.read()
        if len(file_bytes) >= HASH_BYTES:
            hash = hashlib.sha256(file_bytes[:HASH_BYTES]).hexdigest()
        else:
            hash = hashlib.sha256(file_bytes).hexdigest()
            
    file_data.id = hash

def parse_img_metadata(img, file_dir, img_data):
    metadata = et.ExifToolHelper().get_tags(f'{file_dir}/{img}', tags=['EXIF:GPSLatitude', 'EXIF:GPSLongitude'])    
    for d in metadata:
        for k, v in d.items():
            if k == 'EXIF:GPSLatitude':
                img_data.lat = float(v)
            if k == 'EXIF:GPSLongitude':
                img_data.long = float(v)

    if img_data.lat is None or img_data.long is None:
        return False
                
    return True

def move_img(img, file_dir, file_data, web_dir):
    img_type = img.split('.')[1] # This is gonna break at somepoint
    
    src_path = f'{file_dir}/{img}'
    rsrc_path = f'/resources/images/{file_data.id}.{img_type}'
    dst_path = f'{web_dir}{rsrc_path}'
    shutil.copyfile(src_path, dst_path)

    return rsrc_path

# clips should follow the naming scheme:  poslong_poslat_Video Title_.mp4  (this is silly)
def parse_vid_name(vid_name, vid_data):
    v = vid_name.split('_')

    try:
        vid_data.long = float(v[0])
        vid_data.lat = float(v[1])
        title = v[2]
    except IndexError as e:
        print(f'Video name \'{vid_name}\' does not contain all components:\n\'poslat_poslot\'.')
        return (False, None)
    except ValueError as e:
        print(f'Longitude or Latitude in video name \'{vid_name}\' are not valid numbers.')
        return (False, None)

    return (True, vid_title)


def render_vid(video):
    print("Stub")


def update_json(file_data, json_data):
    file_data_dict = ft.asdict(file_data)
    json_data['markers'].append(file_data_dict)

def write_json(json_data, web_dir, type):
    map_path = f'{web_dir}/resources'

    if type is ft.IMAGE_TYPE:
        f = open(f'{map_path}/map-img.json', 'w')
    elif type is ft.VIDEO_TYPE:
        f = open(f'{map_path}/map-vid.json', 'w')
    elif type is ft.TEXT_TYPE:
        f = open(f'{map_path}/map-txt.json', 'w')

    json.dump(json_data, f, indent=2)
    f.close()
    

if __name__ == '__main__':
    main()
