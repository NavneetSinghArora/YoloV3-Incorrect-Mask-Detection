import os
from jproperties import Properties
from bs4 import BeautifulSoup


class Annotation_Converter:

    def __init__(self):
        self.xml_files = []
        self.xml_file_directory = None
        self.txt_file_directory = None
        self.classes = None
        self.writable_data = []

    def fetch_properties(self):
        configurations = Properties()
        with open('configuration.properties', 'rb') as read_properties:
            configurations.load(read_properties)

        self.xml_file_directory = configurations.get("input_directory").data
        self.txt_file_directory = configurations.get("output_directory").data
        self.classes = configurations.get("classes").data

    def create_annotation_filepath(self):
        for file in os.listdir(self.xml_file_directory):
            if file.endswith(".xml"):
                file_path = "{}/{}".format(self.xml_file_directory, file)
                self.xml_files.append(file_path)

    def get_class_id(self, classname):
        classnames = self.classes.split(',')
        for name in classnames:
            if classname in name:
                return name.split('|')[1]

    def convert_format(self, data_tuple):
        normalized_width = 1.0 / data_tuple[2]
        normalized_height = 1.0 / data_tuple[3]
        x = ((data_tuple[4] + data_tuple[5]) / 2.0) * normalized_width
        y = ((data_tuple[6] + data_tuple[7]) / 2.0) * normalized_height
        w = (data_tuple[5] - data_tuple[4]) * normalized_width
        h = (data_tuple[7] - data_tuple[6]) * normalized_height
        class_id = self.get_class_id(data_tuple[1])
        print(data_tuple[0], class_id, x, y, w, h)

        return data_tuple[0], class_id, x, y, w, h

    def extract_context(self, data):
        filename = data.find('filename').text
        image_width = float(data.find('width').text)
        image_height = float(data.find('height').text)
        classnames = data.findAll('name')
        x_mins = data.findAll("xmin")
        x_maxs = data.findAll("xmax")
        y_mins = data.findAll("ymin")
        y_maxs = data.findAll("ymax")

        for i in range(len(classnames)):
            classname = classnames[i].text
            x_min = float(x_mins[i].text)
            x_max = float(x_maxs[i].text)
            y_min = float(y_mins[i].text)
            y_max = float(y_maxs[i].text)
            data_tuple = (filename, classname, image_width, image_height, x_min, x_max, y_min, y_max)
            data_tuple = self.convert_format(data_tuple)
            self.writable_data.append(data_tuple)

    def read_annotation_files(self):
        for file in enumerate(self.xml_files):
            with open(file[1], 'r') as xml_file:
                xml_data = xml_file.readlines()
            xml_data = "".join(xml_data)
            data = BeautifulSoup(xml_data, "lxml")
            self.extract_context(data)

    def create_and_write_files(self):
        for data in self.writable_data:
            filename = data[0].split('.')[0] + ".txt"
            file_path = "{}/{}".format(self.txt_file_directory, filename)
            content = str(data[1]) + " " + str(data[2]) + " " + str(data[3]) + " " + str(data[4]) + " " + str(data[5])
            if os.path.exists(file_path):
                file = open(file_path, 'a')
            else:
                file = open(file_path, 'w')
            file.write(content)
            file.write("\n")
            file.close()


annotation_converter = Annotation_Converter()
annotation_converter.fetch_properties()
annotation_converter.create_annotation_filepath()
annotation_converter.read_annotation_files()
annotation_converter.create_and_write_files()
