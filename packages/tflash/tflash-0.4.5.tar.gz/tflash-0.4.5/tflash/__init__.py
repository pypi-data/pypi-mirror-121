# -*- coding: utf-8 -*-
"""
Created on Mon Sept 2 18:33:21 2019
@author: Nugroho Fredivianus
"""

from __future__ import print_function, division
from time import time, strftime, localtime
import numpy as np
import imageio
import requests
import os
import pkg_resources
import PIL.ImageFont as ImageFont

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from tqdm import tqdm

import tflash.label_map_util as lmu
import tflash.visualization_utils as vis

default_model_file = "faster_rcnn_inception_v2_coco.pb"
images = ['jpg', 'jpeg']
videos = ['mp4', 'avi', 'mov']
allowed = images + videos


def download(url, fname):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
            desc=fname,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


class Detector:
    def __init__(self, model_file=None):
        self.detection_graph = None
        self.category_index = None
        self.font_file = 'roboto.ttf'
        self.font_size = 20
        self.font = ImageFont.truetype(pkg_resources.resource_filename(__name__, self.font_file), self.font_size)
        if model_file is not None and os.path.isfile(model_file):
            self.model_file = model_file
        else:
            self.model_file = default_model_file

    def reset(self):
        self.__init__()

    def set_font(self, file, size=None):
        self.font_file = file

        if size is None:
            size = self.font_size
        else:
            self.font_size = size

        try:
            self.font = ImageFont.truetype(self.font_file, size)
        except:
            print("Font cannot be loaded. Using Arial as default.")
            self.font = ImageFont.truetype(pkg_resources.resource_filename(__name__, 'arial.ttf'), size)

    def set_font_size(self, size):
        self.font_size = size
        self.set_font(self.font_file, self.font_size)

    def load_model(self, model_file=None):
        """
        :param model_file: PB model file
        :return: Detection graph and category index
        """
        if model_file is not None:
            if model_file in ["", "default", "reset"]:
                if model_file != self.model_file:
                    self.model_file = default_model_file
                    print("Using default model file.")
            else:
                self.model_file = model_file
                if os.path.isfile(self.model_file):
                    print("Model file updated.")

        # check if model exists
        if not os.path.isfile(self.model_file):
            if input("Model file not found. Download default model (54.5Mb) [y/N]? ").lower()[:1] == 'y':
                self.model_file = default_model_file
                print("Downloading...")
                download("https://drive.google.com/uc?export=download&id=1PW8WMk2kcYGL2HDbZZXNtTEtz5d_bBzU",
                         self.model_file)
            else:
                print("EXIT: Model file required.")
                exit()

        # check default model integrity
        else:
            if self.model_file == default_model_file and os.path.getsize(self.model_file) < 57153785:
                if input("Model file corrupt. Delete and re-download (54.5Mb) [y/N]?").lower()[:1] == 'y':
                    os.remove(self.model_file)
                    print("Downloading...")
                    download("https://drive.google.com/uc?export=download&id=1PW8WMk2kcYGL2HDbZZXNtTEtz5d_bBzU",
                             self.model_file)

        # load model
        try:
            self.detection_graph = tf.Graph()
            with self.detection_graph.as_default():
                graph_def = tf.compat.v1.GraphDef()
                with tf.io.gfile.GFile(self.model_file, 'rb') as mfile:
                    serialized_graph = mfile.read()
                    graph_def.ParseFromString(serialized_graph)
                    tf.import_graph_def(graph_def, name='')
        except:
            print("ERROR: Model file cannot be read.")
            self.model_file = default_model_file
            exit()

        # load classes
        path = pkg_resources.resource_filename(__name__, 'mscoco_label_map.pbtxt')
        label_map, num_classes = lmu.load(path)
        categories = lmu.convert_to_categories(label_map, max_num_classes=num_classes, use_display_name=True)
        self.category_index = lmu.create_category_index(categories)

    def detect(self, fname, min_score=.5, print_output=True):
        """
        :param fname: (string) File name to be detected
        :param min_score: (float) Minimal detection score
        :param print_output: (Boolean) print output to file
        :return: (Dictionary) coordinates of boxes and filenames
        """
        if not os.path.isfile(fname):
            print("File not found: " + fname)
            return {"output": "none"}

        split = fname.split('.')
        ext = split[-1]

        if ext not in allowed:
            print("Only {} allowed.".format(allowed))
            return {}

        file_output = '.'.join(split[:-1]) + strftime("_%d%m%Y_%H%M%S.", localtime()) + ext

        if ext in videos:
            print_output = True
        elif isinstance(print_output, str):
            file_output = print_output
            print_output = True
        elif not print_output:
            file_output = "None"
        elif not isinstance(print_output, bool):
            print_output = False

        if self.detection_graph is None or self.category_index is None:
            try:
                self.load_model()
                print("Model loaded.")
            except:
                print("ERROR: Model cannot be loaded. Please use another model file.")
                exit()

        mode = 'video' if ext in videos else 'image'
        print("Processing: {}".format(fname))

        with self.detection_graph.as_default():
            with tf.compat.v1.Session(graph=self.detection_graph) as sess:
                image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
                detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
                detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
                detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

                video_reader = imageio.get_reader(fname)
                fps = None
                back = None
                total_frames = 1
                if mode == 'video':
                    metadata = video_reader.get_meta_data()
                    fps = metadata['fps'] if 'fps' in metadata else 30
                    total_frames = round(fps * metadata['duration'])
                    size = metadata["size"]
                    if size[0] % 16 > 0 or size[1] % 16 > 0:
                        import math
                        topdown = 16 * math.ceil(size[0] / 16)
                        leftright = 16 * math.ceil(size[1] / 16)
                        back = np.zeros((leftright, topdown, 3), dtype=np.uint8)

                    t0 = int(time())

                if print_output:
                    video_writer = imageio.get_writer(file_output, fps=fps)

                for i, image in zip(tqdm(range(total_frames), desc="Progress"), video_reader):
                    if back is not None:
                        img = back.copy()
                        img[:size[1], :size[0]] = image
                        image = img
                    image_exp = np.expand_dims(image, axis=0)

                    # Detection part
                    boxes, scores, classes, num = sess.run(
                        [detection_boxes, detection_scores, detection_classes, num_detections],
                        feed_dict={image_tensor: image_exp})

                    if print_output:
                        # Visualization part
                        vis.visualize(image, np.squeeze(boxes), np.squeeze(classes).astype(np.int32),
                                      np.squeeze(scores),
                                      self.category_index, self.font, min_score_thresh=min_score, line_thickness=2)

                        video_writer.append_data(image)

                if total_frames > 1:
                    fps = total_frames / (int(time()) - t0)
                    print("Frames processed: %s, Speed: %s fps" % (total_frames, fps))

                if print_output:
                    video_writer.close()

        result = []
        if mode == "image":
            for i in range(int(num)):
                b = [float(box) for box in boxes[0][i]]
                row = {'class': self.category_index[classes[0][i]]['name'], 'score': scores[0][i], 'box': b}
                result.append(row)

        response = {"input": fname, "output": file_output, "detections": result}
        return response

    def detect_multiple(self, fnames, min_score=.5, model_file=None, print_output=None):
        """
        :param fnames: (list) file names
        :param min_score: (float) minimal detection score
        :param model_file: (string) PB model file
        :param print_output: Anticipatory parameter, not used at all for multiple detections.
        :return: (list of dict) detection results
        """
        if model_file is not None and model_file != self.model_file:
            self.category_index = None
            self.model_file = model_file

        if self.detection_graph is None or self.category_index is None:
            self.load_model(model_file=self.model_file)

        if print_output is not None:
            print("For multiple detections, outputs always with default filenames.")

        return [self.detect(f, min_score=min_score) for f in fnames]


def help():
    print("TFlash: Quick Detection Practice using TensorFlow")
    print("======")
    print("import tflash")
    print("flash = tflash.Detector()")
    print("detection = flash.detect(\"mypic.jpg\")  # jpg, png, mp4 etc")
    print("======")
    print("Alternative trained models at TF Model Zoo:")
    print("https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf1_detection_zoo.md")


if __name__ == '__main__':
    help()
