import clip2yt
import os
import sys
import types
import json
import hashlib

WEBSITE_PATH = '../website/'

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
        json_data = get_json(type)
            # for each file in directory...
            for file in files:
                gen_file(file, json_data, type)
                write_json(json_data)


def get_json(type):
    if type is IMAGE_TYPE:
        f = open('./map-img.json')
    elif type is VIDEO_TYPE:
        f = open('./map-vid.json')
    elif type is TEXT_TYPE:
        f = open('./map-txt.json')
    else:
        print('File Type is invalid. Exiting...')
        exit()

    json_data = json.load(f)
    f.close()
    return json_data


def gen_file(file, json_data, type):
    # check that the file id is not already in its associated json data
    if not new_file_check(file, json_data):
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

    # file is sha256'd for storage and ID assigning
    ret = assign_id(file_data)
    if ret is None:
        print(f'File \'{file}\' failed to obtain an id, skipping...')
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

def new_file_check(file_data, json):
    print("Stub")

def assign_id(file_data):
    print("Stub")

def parse_img_metadata(img, web_dir):
    print("Stub")

    return path

def move_img(img, )


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


def update_json(file_data, json):
    print("Stub")
    json.flush()
    os.fsync()

def write_json(json):
    print("Stub")
    
if __name__ == '__main__':
    main()
