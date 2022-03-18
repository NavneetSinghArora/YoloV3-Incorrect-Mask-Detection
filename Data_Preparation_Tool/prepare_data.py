import os
from jproperties import Properties


class Data_Preparation:

    def __init__(self):
        self.image_files = []
        self.train_file_directory = None
        self.val_file_directory = None
        self.train_writable_data = []
        self.val_writable_data = []
        self.config_file_directory = None
        self.number_of_classes = None
        self.class_names = None
        self.server_directory_path = "/export/scratch/navneet/yolo_v3_model/data/pwmfd/images"

    def fetch_properties(self):
        configurations = Properties()
        with open('configuration.properties', 'rb') as read_properties:
            configurations.load(read_properties)

        self.train_file_directory = configurations.get("train_file_directory").data
        self.val_file_directory = configurations.get("val_file_directory").data
        self.config_file_directory = configurations.get("config_file_directory").data
        self.number_of_classes = configurations.get("number_of_classes").data
        self.class_names = configurations.get("class_names").data

    def create_filepath(self):
        for file in os.listdir(self.train_file_directory):
            file_path = "{}/{}".format(self.server_directory_path, file)
            self.train_writable_data.append(file_path)

        for file in os.listdir(self.val_file_directory):
            file_path = "{}/{}".format(self.server_directory_path, file)
            self.val_writable_data.append(file_path)

    def create_and_write_files(self):
        file_path = "{}/{}".format(self.train_file_directory, "train.txt")
        file = open(file_path, 'w+')
        for data in self.train_writable_data:
            file.write(data)
            file.write("\n")
        file.close()

        file_path = "{}/{}".format(self.val_file_directory, "val.txt")
        file = open(file_path, 'w+')
        for data in self.train_writable_data:
            file.write(data)
            file.write("\n")
        file.close()

    def create_class_name_file(self):
        names = self.class_names.split(',')
        file_path = "{}/{}".format(self.config_file_directory, "pwmfd.name")
        file = open(file_path, 'w+')
        for name in names:
            file.write(name)
            file.write("\n")
        file.close()

    def create_config_file(self):
        file_path = "{}/{}".format(self.config_file_directory, "pwmfd.data")
        file = open(file_path, 'w+')
        file.write("classes=" + self.number_of_classes + "\n")
        file.write("train=" + ("{}/{}".format(self.train_file_directory, "train.txt")) + "\n")
        file.write("valid=" + ("{}/{}".format(self.val_file_directory, "val.txt")) + "\n")
        file.write("names=" + ("{}/{}".format(self.config_file_directory, "pwmfd.names")) + "\n")
        file.close()


data_preparation = Data_Preparation()
data_preparation.fetch_properties()
data_preparation.create_filepath()
data_preparation.create_and_write_files()
data_preparation.create_class_name_file()
data_preparation.create_config_file()
