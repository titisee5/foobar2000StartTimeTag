import glob
import music_tag
import re
from collections import OrderedDict


music_folder = 'F:\\Music\\TestMusic'
file_types = ('*.acc', '*.aiff', '*.dsl', '*.flac', '*.m4a', '*.mp3', '*.ogg', '*.opus', '*.wav', '*.wv')
album_keys = ('album_artist', 'album')
tag_name = 'start_time'


def get_all_files():
    files = []
    for type in file_types:
        files.extend(glob.glob(music_folder + '/**/' + type, recursive=True))
    return files


def get_all_albums(files):
    albums = {}
    for file in files:
        f = music_tag.load_file(file)

        key = ''
        for key_elem in album_keys:
            key = key + str(f[key_elem])

        if key not in albums:
            albums[key] = [file]
        else:
            albums[key].append(file)

    return albums


def add_start_time_all_albums(albums):
    for key, album in albums.items():
        ret = check_track_numbers_and_sort(key, album)

        if ret[0]:
            add_start_time_single(key, ret[1])


def check_track_numbers_and_sort(key, album):
    track_numbers = {}

    for file in album:
        f = music_tag.load_file(file)
        track_num = int(f['track_number'].value)
        if track_num in track_numbers:
            print('Invalid Album - repeated Tracknumber - Albumkey: ' + key)
            return False, None
        else:
            track_numbers[track_num] = file

    track_numbers = OrderedDict(sorted(track_numbers.items(), key=lambda t: t[0]))

    if list(track_numbers.keys())[0] != 1 or list(track_numbers.keys())[-1] != len(track_numbers):
        print('Invalid Album - Tracknumbers missing - Albumkey: ' + key)
        return False, None

    return True, track_numbers.values()


def add_start_time_single(key, album):
    cur_time = 0
    for file in album:
        f = music_tag.load_file(file)

        rounded_time = round(cur_time)

        h = rounded_time // 3600
        m = rounded_time % 3600 // 60
        s = rounded_time % 3600 % 60

        if h == 0:
            tag_value = '{:d}:{:02d}'.format(m, s)
        else:
            tag_value = '{:d}:{:02d}:{:02d}'.format(h, m, s)

        f.set_raw(tag_name, tag_name, tag_value, appendable=False)
        f.save()
        print('Added start time tag {} to {} in Album {}'.format(tag_value, f['tracktitle'], key))

        try:
            length = int(re.search("'length': \['(\d+)'\]", str(f.mfile)).group(1))
        except:
            try:
                # try using TinyTag
                from tinytag import TinyTag
                tag = TinyTag.get(file)

                length = tag.duration
            except:
                # skip remaining album
                return

        cur_time = cur_time + length


if __name__ == '__main__':
    files = get_all_files()
    albums = get_all_albums(files)
    add_start_time_all_albums(albums)
