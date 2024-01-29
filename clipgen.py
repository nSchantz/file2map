import clip2yt
import os

@dataclass
class VidData:
    id: int
    tag: str,
    state: str,
    long: int,
    lat: int,
    url: str,

def main():
    # open directory with clips


    # open map.json for reading/writing
    with open('./map-vid.json', 'rw') as json:
        # for each clip in directory...
        for video in videos:
            # clips should follow the naming scheme:  tag_state_poslong_poslat.mp4
            vid_data = parse_name(video)
            if vid_data is None:
                print(f'Video \'{video}\' failed to parse, skipping...')
                continue
    
            # clip is sha256'd for storage and ID assigning
            ret = assign_id(vid_data)
            if ret is None:
                print(f'Video \'{video}\' failed to obtain an id, skipping...')

            # use moviepy to render/compress raw mp4
            render = render_vid(video)
            if render is None:
                print(f'Video \'{video}\' failed to render, skipping...')
                continue

            # upload clip and get youtube url
            url = upload(render)
            if url is None:
                print(f'Video \'{video}\' failed to upload, skipping...')
                continue

            # have: ID, type(video), tag, state, position, url
            vid_data.url = url

            # map.json is updated
            update_json(vid_data, json)

def parse_name(vid_name):
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

def assign_id(vid_data):
    print("Stub")

def render_vid(video):
    print("Stub")

def update_json(vid_data, json):
    print("Stub")
    json.flush()
    os.fsync()
    
if __name__ == '__main__':
    main()
