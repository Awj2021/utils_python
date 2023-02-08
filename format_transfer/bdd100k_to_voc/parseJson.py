#!/usr/bin/env python
# -*- coding: utf8 -*-
#parse json，input json filename,output info needed by voc

import json

def parse_json(json_file):
    # parames: json_file, one json file includes info of all the frames in a folder.
    # return: the list of key info that required for XML file.
    f = open(json_file)
    info = json.load(f)                                        # info = [{}, {}, ... {}]

    one_video_info = {}                                        # one video(folder) info.
    for one_frame_info in info:
        one_frame_objs = []
        frame_name = one_frame_info['name']
        video_name = one_frame_info['videoName']
        labels = one_frame_info['labels']                      # all the bboxes and corresponding coordinates. list.
        for label in labels:
            obj = []
            obj.append(int(label['box2d']['x1']))
            obj.append(int(label['box2d']['y1']))
            obj.append(int(label['box2d']['x2']))
            obj.append(int(label['box2d']['y2']))
            obj.append(label['category'])
            one_frame_objs.append(obj)
        one_video_info[frame_name] = one_frame_objs
    return one_video_info

# result = parse_json("/home/users/tianjiao_li/scratch/awj/track/data/BDDK100/bdd100k/labels/box_track_20/train/01ed3f01-c4dd8d1d.json")
# # ipdb.set_trace()
# print(result)