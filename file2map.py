import clip2yt
import os
import sys
import types
import json
import hashlib

WEBSITE_PATH = '../website'

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 file2map <File Directory> <File Type>")
        print("File Types: Image=0, Video=1, Text=2")
        exit()

    dir = sys.argv[1]
    type = sys.argv[2]

    # Check Dir Exist
    
    # open directory with files
    with open(dir, 'rw') as dir:   
        json_data = get_json(WEBSITE_PATH, type)
            # for each file in directory...
            for file in files:
                gen_file(file, json_data, type)
                write_json(json_data, WEBSITE_PATH, type)


def get_json(web_dir, type):
    map_path = f'web_dir/{resources}'
    
    if type is IMAGE_TYPE:
        f = open(f'{map_path}/map-img.json', 'r')
    elif type is VIDEO_TYPE:
        f = open(f'{map_path}/map-vid.json', 'r')
    elif type is TEXT_TYPE:
        f = open(f'{map_path}/map-txt.json', 'r')
    else:
        print('File Type is invalid. Exiting...')
        exit()

    json_data = json.load(f)
    f.close()
    return json_data


def gen_file(file, json_data, type):
    file_data = FileData()
    
    # file is sha256'd for storage and ID assigning
    assign_id(file, file_data)
    
    # check that the file id is not already in its associated json data
    if not new_file_check(file_data, json_data):
        print(f'File \'{file}\' already exists, skipping...')
        return

    # parsing metadata about the file
    if type is IMAGE_TYPE:
        file_data = parse_img_metadata(file)
    elif type is VIDEO_TYPE:
        file_data = parse_vid_name(file)
    elif type is TEXT_TYPE:
        print("Do text")
    if file_data is None:
        print(f'File \'{file}\' metadata failed to parse, skipping...')
        return    
    
    # uploading file
    if type is IMAGE_TYPE:
        # move image to website resource dir. store the path to image 
        file_data.url = move_img(file, WEBSITE_PATH)
    elif type is VIDEO_TYPE:
        # use moviepy to render/compress raw mp4
        render = render_vid(file)
        if render is None:
            print(f'Video \'{file}\' failed to render, skipping...')
            return

        # upload clip and get youtube url
        url = upload(render)
        if url is None:
            print(f'Video \'{file}\' failed to upload, skipping...')
            return

        # store the youtube link for the video
        vid_data.url = url
    elif type is TEXT_TYPE:
        print("Do Text")

    # update json
    update_json(file_data, json_data)

def new_file_check(file_data, json_data):
    for marker in json_data['markers']:
        if marker['id'] == file_data.id:
            return False

    return True

def assign_id(file, file_data):
    file_data.id = hashlib.sha256(file).hexdigest()

def parse_img_metadata(img):
    print("Stub")

    return path

def move_img(img, web_dir):
    print("Stub")


# clips should follow the naming scheme:  tag_state_poslong_poslat.mp4
def parse_vid_name(vid_name):
    v = vid_name.split('_')

    vid_data = VidData

    try:
        vid_data = VidData(None, v[0], v[1], int(v[2]), int(v[3]), None)
    except IndexError as e:
        print(f'Video name \'{vid_name}\' does not contain all components:\n\'tag_state_poslat_poslot\'.')
        return None
    except ValueError as e:
        print(f'Longitude or Latitude in video name \'{vid_name}\' are not valid numbers.')
        return None

    return vid_data


def render_vid(video):
    print("Stub")


def update_json(file_data, json_data):
    print("Stub")


def write_json(json_data, web_dir, type):
    map_path = f'web_dir/{resources}'

    if type is IMAGE_TYPE:
        f = open(f'{map_path}/map-img.json', 'w')
    elif type is VIDEO_TYPE:
        f = open(f'{map_path}/map-vid.json', 'w')
    elif type is TEXT_TYPE:
        f = open(f'{map_path}/map-txt.json', 'w')

    f.write(json_data)
    f.close()
    

if __name__ == '__main__':
    main()
