"""
Parse exported 2d trackers.
 
trackers = [
    {'name': 'TrackerName',
     'keys': [
        {'frame': 0,
         'x': 10,
         'y': 20}},
     ]
    }},
]

"""

import re

def _lookup_keyframe(string):
    pattern = r'(^\d+)\s(\d+\.\d{15})\s(\d+\.\d{15}$)'

    matchObj = re.search(pattern, string)
    if matchObj:
        return {'frame': int(matchObj.group(1)),
                'x': float(matchObj.group(2)),
                'y': float(matchObj.group(3))}
    return

def TreeDETracks(filepath):

    # Open file
    try:
        file_ = open(filepath, 'r')
    except OSError as error:
        print('Error reading file: {0}'.format(error))
        file_.close()

    trackers = []
    tracker = {'name': '', 'keys': []}

    STATES = {'total': 0,
              'name': 1,
              'color': 2,
              'len': 3,
              'key': 4}
    PrevState = STATES['total']
    # Lines loop
    for idx, line in enumerate(file_):
        key =  _lookup_keyframe(line)
        if idx == 0:
            # First line
            PrevState = STATES['total']
            continue
        elif _lookup_keyframe(line):
            # Key
            PrevState = STATES['key']
            tracker['keys'].append(key)
        else:
            if PrevState == STATES['key']:
                # name
                PrevState = STATES['name']
                if tracker['name'] and tracker['keys']:
                    trackers.append(tracker)
                tracker = {'name': line, 'keys': []}
            else:
                # color + count
                PrevState += 1
                continue


    # End of file
    if tracker['name'] and tracker['keys']:
        trackers.append(tracker)
    file_.close()

    return trackers


def createTracks(tracks):
    node = hou.pwd()
    geo = node.geometry()
    for t in tracks:
        for k in t['keys']:
            if k['frame'] == hou.frame():
                geo.createPoints([(k['x'], k['y'], 0)])




if __name__ == '__main__':
    print('blop')
    fp = r'Z:\TMP\houdini\camera_vectorField\2d_tracks_v001.txt'
    t = TreeDETracks(fp)
    print(t[0]['name'])
    for b in t[0]['keys']:
        print(b)
    #print(t[0])