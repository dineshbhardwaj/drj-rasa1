from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import datetime

import six
import argparse

from rasa_core.interpreter import RasaNLUInterpreter


nlu_model_path = './models/nlu_s/default/current_py3'
interpreter=RasaNLUInterpreter(nlu_model_path)


def run_hindiSong(input_str):
    val_name_list=[]
    entity_val_list=[]
    entity_name_list=[]
    print(str(datetime.datetime.now()))
    for test_text in test_text_list : 
        print("Entities in '%s'" % test_text)
        out_val=interpreter.parse(test_text)
        for entity_prop in out_val.get("entities"):
            entity_val_list.append(entity_prop.get("value")) 
            entity_name_list.append(entity_prop.get("entity"))

        print("entities_val: " + str(entity_val_list))
        print("entities_name: " + str(entity_name_list))
    val_name_list.append(entity_val)
    val_name_list.append(entity_name)
    return val_name_list

