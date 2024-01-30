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

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 file2map <File Directory> <File Type> <Tag>")
        print("File Types: Image=0, Video=1, Text=2")
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
    for file in os.listdir(dir):
        print(f'Processing file \'{file}\'...')
        gen_file(file, json_data, dir, type, tag)
        print(f'\n-----------------------------')

    print('All files uploaded. Writing json file.')
    # write_json(json_data, WEBSITE_PATH, type)


def get_json(web_dir, type):
    map_path = f'{web_dir}/resources'
    
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
        success = parse_img_metadata(file, file_data)
    elif type is ft.VIDEO_TYPE:
        success = parse_vid_name(file, file_data)
    elif type is ft.TEXT_TYPE:
        print("Todo")
    if not success:
        print(f'File \'{file}\' metadata failed to parse, skipping...')
        return    
    
    # uploading file
    if type is ft.IMAGE_TYPE:
        # move image to website resource dir. store the path to image 
        file_data.url = move_img(file, file_dir, WEBSITE_PATH)
    elif type is ft.VIDEO_TYPE:
        # use moviepy to render/compress raw mp4
        render = render_vid(file)
        if render is None:
            print(f'Video \'{file}\' failed to render, skipping...')
            return

        # upload clip and get youtube url
        url = c2yt.upload(render)
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
    print(f'Debug json: {json_data}')

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

def parse_img_metadata(img, img_data):
    metadata = et.ExifToolHelper().get_tags(f'./test_dir/{img}', tags=['EXIF:GPSLatitude', 'EXIF:GPSLongitude'])    
    for d in metadata:
        for k, v in d.items():
            if k == 'EXIF:GPSLatitude':
                img_data.lat = float(v)
            if k == 'EXIF:GPSLongitude':
                img_data.long = float(v)

    if img_data.lat is None or img_data.long is None:
        return False
                
    return True

def move_img(img, file_dir, web_dir):
    src_path = f'{file_dir}/{img}'
    rsrc_path = f'/resources/images/{img}'
    dst_path = f'{web_dir}{rsrc_path}'
    shutil.copyfile(src_path, dst_path)

    return rsrc_path

# clips should follow the naming scheme:  poslong_poslat_.mp4
def parse_vid_name(vid_name, vid_data):
    v = vid_name.split('_')

    try:
        vid_data.long = float(v[0])
        vid_data.lat = float(v[1])
    except IndexError as e:
        print(f'Video name \'{vid_name}\' does not contain all components:\n\'poslat_poslot\'.')
        return False
    except ValueError as e:
        print(f'Longitude or Latitude in video name \'{vid_name}\' are not valid numbers.')
        return False

    return True


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
