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


def run_hindiSong(_):
    interpreter=RasaNLUInterpreter(nlu_model_path)
    test_text_list = ['is there a way you get me a song raaj dilon ke khul jaate',
                      'could you please play some prank call of Maheshwari',
                      'play raj ki baat kah du to jaane mahfil me fir kya ho',
                      'play a movie review of Razz the terror',
                      'play me some songs from dil ki baat movie',
                      'play har dil jo pyar karega',
                      'need to hear song jaane kaha gaye wo din',
                      'kindly play standup comedy by tamna',
                      'please play next song',
                      'give me next song',
                      'repeat this one',
                      'I wanna hear the same song again'
                      
    ]
    
    print(str(datetime.datetime.now()))
    for test_text in test_text_list : 
        print("Entities in '%s'" % test_text)
        out_val=interpreter.parse(test_text)
        
        print(str(out_val))

    print(str(datetime.datetime.now()))

#    print("end of interpretor")
    #    agent = Agent.load("examples/hindiSong/models/policy/current",
#                       interpreter=RasaNLUInterpreter(nlu_model_path))

#    if serve_forever:
#        agent.handle_channel(ConsoleInputChannel())
#    return agent


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.register("type", "bool", lambda v: v.lower() == "true")
  parser.add_argument(
      "--input_line",
      type=str,
      default="",
      help="Input line for parsing"
  )
  parser.add_argument(
      "--hd_file",
      type=str,
      default="../inputs/stores_holidays_map.csv",
      help="overall holiday file"
  )
  FLAGS, unparsed = parser.parse_known_args()
  #  main
  logging.basicConfig(level="DEBUG")
  run_hindiSong(FLAGS)
