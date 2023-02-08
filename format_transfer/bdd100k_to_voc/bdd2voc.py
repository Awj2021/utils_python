# -*- coding: utf8 -*-
import os
import pascal_voc_io
import parseJson
import ipdb
from tqdm import tqdm

def main(split, srcDir, dstDir):
    """
    params:
        split: ['train', 'test', 'val']
        srcDir: the original dir of dataset.
        dstDir: direct dir of saving dataset.
    """
    frames_list = []
    fp_txt = open(dstDir + '/ImageSets/Main/' + '{}.txt'.format(split), 'w')
    i = 1
    xml_dir = os.path.join(dstDir, 'Annotations/')
    for dir_path, _, video_jsons in os.walk(os.path.join(srcDir, split)):
        for one_video_json in video_jsons:
            dir_one_video_json = os.path.join(dir_path, one_video_json)
            print("processing: {}, {}".format(i, dir_one_video_json))
            i = i + 1
            # parse this video json file.
            one_video_info = parseJson.parse_json(str(dir_one_video_json))   # type: dict.
            # Loop for every frame, and then save every frame xml into the corresponding folder.
            if len(one_video_info):
                for frame_name, objs in tqdm(one_video_info.items()):
                    xml_file_name = frame_name[:-4]                          # remove .json
                    frames_list.append(xml_file_name)
                    tmp = pascal_voc_io.PascalVocWriter(xml_dir, xml_file_name, (720,1280,3), None)
                    for obj in objs:
                        tmp.addBndBox(obj[0], obj[1], obj[2], obj[3], obj[4])
                        tmp.save()
            else:
                print('Please Check this file: {}'.format(dir_one_video_json))
        # fp_txt.writelines(frames_list + '\n')
        for line in frames_list:
            fp_txt.write(str(line) + '\n')
    fp_txt.close()

if __name__ == '__main__':
    srcDir = '/home/users/tianjiao_li/scratch/awj/track/data/BDDK100/bdd100k/labels/box_track_20'
    dstDir = '/home/users/tianjiao_li/scratch/awj/code/TRACK/first_stage/data/bdd100'
    splits = ['train', 'val']
    for split in splits:
        main(split, srcDir, dstDir)
