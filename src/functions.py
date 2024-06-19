from os import getenv
import logging
from typing import NoReturn, Union
import sys
import rtoml
import os

from configs.config import (XML_FILE_PATH, TXT_OUTPUT_PATH)


class GeneralFunctions(object):
    def __init__(self) -> None:
        pass
    
    def local_logger(self, file_path: str='logs/debug.log'):
        """ Set up a local logger

        Args:
            file_path (str, optional): _description_. Defaults to 'logs/debug.log'.
        """
        local_logging = getenv(key="LOCAL_LOGGING", default=False)
        if local_logging:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s [%(levelname)s] %(message)s",
                handlers=[
                    logging.FileHandler(file_path),
                    logging.StreamHandler()
                ]
            )
        return
        
    def load_toml(self, toml_file_path: str) -> Union[dict, NoReturn]:
        """ Load a toml file and return it as a dictionary

        Args:
            toml_file_path (str): _description_

        Returns:
            Union[dict, NoReturn]: _description_
        """
        try:
            f = open(toml_file_path, 'r')
            toml_loaded_dict = rtoml.load(f.read())
            return toml_loaded_dict
        except Exception as e:
            logging.error(e)
            return sys.exit(1)
        
    def txt_to_csv(self, txt_file_path: str, csv_file_path: str) -> NoReturn:
        """ Convert a txt file to a csv file

        Args:
            txt_file_path (str): _description_
            csv_file_path (str): _description_
        """
        try:
            txt_file = open(txt_file_path, 'r')
            csv_file = open(csv_file_path, 'w')
            for line in txt_file:
                csv_file.write(line.replace('\t', ','))
            txt_file.close()
            csv_file.close()
            return
        except Exception as e:
            logging.error(e)
            return sys.exit(1)

    def xml_parser_publications(self) -> None:
        """
            Parse the xml file and write the publications to a txt file
        """
        with open(XML_FILE_PATH, 'r') as f:
            text = f.read()
            words = ["3d", "2d", "animation", "synthesize", "image", "gpu", "geometry", "rendering", "visualization", "art"
                    , "games", "effects", "imaging", "render", "photorealistic", "visual", "textures", "geometry"
                    , "polygonal", "fluid", "illumination", "shading", "surface", "relighting"]
            text = text.split("\n")
            count = dict()
            total = 0
            for itemIndex in range(len(text)):
                if text[itemIndex][1:6] == "title":
                    for word in words:
                        if word in text[itemIndex]:
                            logging.info(total, " : ", text[itemIndex][7:-8])
                            if "year" in text[itemIndex + 1]:
                                logging.info(text[itemIndex + 1][6:10])
                                if text[itemIndex + 1][6:10] not in count:
                                    count[text[itemIndex + 1][6:10]] = 1
                                else:
                                    count[text[itemIndex + 1][6:10]] += 1
                                    total += 1
                            break
        f = open(TXT_OUTPUT_PATH, "w")
        f.write("Year" + "\t" + "Publications\n")
        for i in sorted(count):
            f.write((str(i) + "\t" + str(count[i]) + "\n"))
        f.close()
        d = count.items()
        sorted_items = sorted(d)
        logging.info(sorted_items)
        logging.info("Total publications: ", total)
        return