'''
    Argument parser for both 
        vm_deallocate
        sub_death_ray.py

    Arguments needed:
        org         - Organization Name
                        This will be used to title any output files 
        sub_prefix  - A pattern to find specific subs using a prefix
                      to the sub name, for example 'ag-ce' and is 
                      case insensitive.
                      OPTIONAL : If subs is empty and this is set, a prefix
                      is used. 
        subs        - Subscription list to process. This will be a JSON
                      file consisting ONLY of a list of sub id's or names
                      in which to process. 
                      OPTIONAL - If provided this overrides sub_prefix
        processed   - Subscription list that has already been processed. 
                      This MUST be a JSON file as a list only of sub-ids
                      that have already been processed.
                      OPTIONAL - Only used with sub_death_ray.py
        whatif      - Flag True or False to indicate that we just want to see
                      what happens or not. Optional and default is False                      
        
'''
import os
import sys
import json
import argparse

class ProgramArguments:
    def __init__(self, command_line):
        self.command_line = command_line
        self.parser = None
        self.account_prefix = None
        self.organization = None
        self.sub_file = None
        self.subs_to_process = []
        self.sub_processed_file = None
        self.subs_already_processed = []
        self.whatif = False

        self._parse_program_arguments()

    def _parse_program_arguments(self):
        self.parser = argparse.ArgumentParser(description='General Clean Up Arguments')
        self.parser.add_argument("-org", required=True, type=str, help="Organization Name")
        self.parser.add_argument("-sub_prefix", required=False, default=None, type=str, help="Optional Sub Prefix")
        self.parser.add_argument("-subs", required=False, default=None, type=str, help="Optional JSON file with subscriptions to process")
        self.parser.add_argument("-processed", required=False, default=None, type=str, help="Optional JSON file with subscriptions that have already been processed")
        self.parser.add_argument("-whatif", required=False, default=False, type=bool, help="When true, just dumps out what would happen.")

        arguments_parser = self.parser.parse_args(self.command_line)
        self.organization = arguments_parser.org
        self.account_prefix = arguments_parser.sub_prefix
        self.sub_file = arguments_parser.subs
        self.sub_processed_file = arguments_parser.processed
        self.whatif = arguments_parser.whatif

        if self.sub_file:
            self.subs_to_process = self._load_json_list(self.sub_file)
        if self.sub_processed_file:
            self.subs_already_processed = self._load_json_list(self.sub_processed_file)

    def _load_json_list(self,file_name):
        if not os.path.exists(file_name):
            raise Exception("Input file {} does not exist".format(file_name))
        
        return_list = []
        file_data = None
        with open(file_name,"r") as input_file:
            file_data = input_file.readlines()
        
        file_data = '\n'.join(file_data)
        return_list = json.loads(file_data)

        if not isinstance(return_list, list):
            raise Exception("Data in input file {} must be a list".format(file_name))
        
        return return_list

