"""
Referring this link:
https://zhuanlan.zhihu.com/p/160930039
https://github.com/PanXF-HUST/mot2voc
Firstly, transfer the danceTrack into VOC format.
"""
import os
import argparse
import shutil
import codecs
import ipdb
from tqdm import tqdm

# Using os.
def parse_args():
    parser = argparse.ArgumentParser(description='Convert DanceTrack into Voc format')
    parser.add_argument('--data_dir', type=str, default='/home/users/tianjiao_li/scratch/awj/track/data/DanceTrack/',
                        help='The dir of DanceTrack, subfolder is train/test')
    args = parser.parse_args()
    return args

def parse_ini(one_dir): # TODO: what's the purpose of this function?
    # dir: /home/users/tianjiao_li/scratch/awj/track/data/DanceTrack/train/dancetrack0016
    ini_fp = open(os.path.join(one_dir, 'seqinfo.ini'), 'r')
    seq_info = ini_fp.readlines()
    seqLenth = int(seq_info[4][10:].strip('\n'))
    imWidth = int(seq_info[5][8:].strip('\n'))
    imHeight = int(seq_info[6][9:].strip('\n'))
    return seqLenth, imWidth, imHeight


def gennerate_gt(gt, Annotation, frame, filename, width, height):
    fp_gt = open(gt)
    gt_lines = fp_gt.readlines()

    gt_fram = []
    for line in gt_lines:
        fram_id = int(line.split(',')[0])
        if fram_id == frame:
            visible = float(line.split(',')[8])
            label_class = line.split(',')[7]
            if (label_class == '1' or label_class == '2' or label_class == '7') and visible > 0.3:
                gt_fram.append(line)

    with codecs.open(Annotation + filename + '.xml', 'w') as xml:
        xml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        xml.write('<annotation>\n')
        xml.write('\t<folder>' + 'voc' + '</folder>\n')
        xml.write('\t<filename>' + filename + '.jpg' + '</filename>\n')
        xml.write('\t<source>\n')
        xml.write('\t\t<database> The MOT-Det </database>\n')
        xml.write('\t</source>\n')
        xml.write('\t<size>\n')
        xml.write('\t\t<width>' + str(width) + '</width>\n')
        xml.write('\t\t<height>' + str(height) + '</height>\n')
        xml.write('\t\t<depth>' + '3' + '</depth>\n')
        xml.write('\t</size>\n')
        xml.write('\t\t<segmented>0</segmented>\n')
        for bbox in gt_fram:
            x1 = int(bbox.split(',')[2])
            y1 = int(bbox.split(',')[3])
            x2 = int(bbox.split(',')[4])
            y2 = int(bbox.split(',')[5])

            xml.write('\t<object>\n')
            xml.write('\t\t<name>person</name>\n')
            xml.write('\t\t<pose>Unspecified</pose>\n')
            xml.write('\t\t<truncated>0</truncated>\n')
            xml.write('\t\t<difficult>0</difficult>\n')
            xml.write('\t\t<bndbox>\n')
            xml.write('\t\t\t<xmin>' + str(x1) + '</xmin>\n')
            xml.write('\t\t\t<ymin>' + str(y1) + '</ymin>\n')
            xml.write('\t\t\t<xmax>' + str(x1 + x2) + '</xmax>\n')
            xml.write('\t\t\t<ymax>' + str(y1 + y2) + '</ymax>\n')
            xml.write('\t\t</bndbox>\n')
            xml.write('\t</object>\n')
        xml.write('</annotation>')


# 用于校验图片数量和标注数量是否一致
def check_num(data_dir, JPEGImage_dir, Annotations_dir=None, ori_num=0):
    num = 0
    lens_folder = []
    for folder in data_dir:
        folder_len, _, _ = parse_ini(folder)
        num += folder_len
        lens_folder.append(folder_len)
        print(folder_len)
    # ipdb.set_trace()
    img_list = os.listdir(JPEGImage_dir)
    if ori_num == 0:
        img_num = len(img_list)
    else:
        img_num = len(img_list) - ori_num
    # print('img_num:',img_num)
    # ipdb.set_trace()
    if Annotations_dir:
        ann_list = os.listdir(Annotations_dir)
        ann_num = len(ann_list)
        assert ann_num == num
    assert img_num == num, 'if it is the second time run this demo, please delete the JPEGImages folder and retry'
    # print('num:', num)
    print('folders {} have been succeed checked'.format(data_dir))
    return num

def main():
    args = parse_args()

    # directly save under the folder of 'first_stage'
    Annotations = './data/Annotations/'
    ImageSets = './data/ImageSets/'
    JPEGImages = './data/JPEGImages/'
    Main = ImageSets + 'Main/'

    if not os.path.exists(Annotations):
        os.makedirs(Annotations)
    if not os.path.exists(ImageSets):
        os.makedirs(ImageSets)
    if not os.path.exists(JPEGImages):
        os.makedirs(JPEGImages)
    if not os.path.exists(Main):
        os.makedirs(Main)

    splits = ['val']  # 2.6. train has finished.
    for split in splits:
        fp_txt = open(Main + '{}.txt'.format(split), 'w')
        data_dirs = [os.path.join(args.data_dir, split, folder) for folder in os.listdir(os.path.join(args.data_dir, split))]
        print(data_dirs)
        for one_dir in data_dirs:                                      # data_dirs: dancetrack0001.
            seqLenth, imWidth, imHeight = parse_ini(one_dir)           # read info from seqinfo.ini file.
            img1 = os.path.join(one_dir, 'img1')
            gt = os.path.join(one_dir, 'gt/gt.txt')

            folder_id = one_dir[-4:]                                  # folder id: e.g., 0001
            img_list = os.listdir(img1)                                 # image files.

            assert len(img_list) == seqLenth
            print('========== Processing file: {}'.format(one_dir))
            for img in tqdm(img_list):
                format_name = folder_id + img
                fp_txt.writelines(format_name[:-4] + '\n')               # 将生成的新的文件名写入train.txt，用于后续数据集拆分
                shutil.copy(img1 + '/' + img, JPEGImages + '/' + format_name)  # 将文件移动到指定文件夹并重新命名
                frame = int(img[:-4])                                    # e.g., 110
                gennerate_gt(gt, Annotation=Annotations, frame=frame, filename=format_name[:-4], width=imWidth,
                             height=imHeight)                            # 生成标注文件
        fp_txt.close()

        check_num(data_dirs, JPEGImages, Annotations)

if __name__ == '__main__':
    main()