#
# Copyright (c) 2021 Dilili Labs, Inc.  All rights reserved. Contains Dilili Labs Proprietary Information. RESTRICTED COMPUTER SOFTWARE.  LIMITED RIGHTS DATA.
#

import fnmatch
import os
import glob
import subprocess
import sys
from argparse import ArgumentParser

import requests
import wget
from bs4 import BeautifulSoup
from PyInquirer import Separator, prompt, style_from_dict

VISIONCAPSULES_EXT = ".cap"

TBODY_PRODUCTION = "✨"
TBODY_REQUIRED_INPUT_TYPE = "Type:"
TBODY_REQUIRED_INPUT_DETECTIONS = "Detections:"
TBODY_REQUIRED_INPUT_TRACKED = "Tracked:"
TBODY_OUTPUT_TYPE = "Type:"
TBODY_OUTPUT_CLASSIFIES = "Classifies:"
TBODY_OUTPUT_DETECTIONS = "Detections:"
TBODY_OUTPUT_ENCODED = "Encoded:"
TBODY_OUTPUT_TRACKED = "Tracked:"
TBODY_OUTPUT_EXPAND = "Expand"

TBODY_DOWNLOAD_URL = "a"
TBODY_FILE_NAME = "FileName"

class Thead:
    thead_name:           str
    thead_description:    str
    thead_hardware:       str
    thead_required_input: str
    thead_output:         str

def find_localfiles(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
        break
    return result


def connect_marketplace(marketplace_url, marketplace_path):

    # Retrieve table from remote website
    print("Connect to VisionCapsules Marketplace at " + marketplace_url)

    response = requests.get(marketplace_url + marketplace_path)
    html = response.content.decode("utf-8")  # text
    soup = BeautifulSoup(html, features="lxml")
    table = soup.find("table")

    return table

def parse_thead(table):
    thead = Thead()

    # Parse table head
    rows = table.find("thead").find_all("tr")

    for row in rows:
        cols = row.find_all("th")
        thead.thead_name = cols[0].string.strip()
        thead.thead_description = cols[1].string.strip()
        thead.thead_hardware = cols[2].string.strip()
        thead.thead_required_input = cols[3].string.strip()
        thead.thead_output = cols[4].string.strip()

    return thead

def parse_table(marketplace_url, table, thead):

    HREF_STARTSWITH = "/release"

    # Parse table body

    tbody = table.find("tbody")
    rows = tbody.find_all("tr")

    vcap_table = []

    VisionCapsules_FullList = []
    for row in rows:
        tbody_production = ""
        tbody_required_input_type = ""
        tbody_required_input_detections = ""
        tbody_required_input_tracked = False
        tbody_output_type = ""
        tbody_output_classifies = ""
        tbody_output_detections = ""
        tbody_output_encoded = False
        tbody_output_tracked = False
        tbody_output_expand = False
        tbody_download_url = ""
        tbody_file_name = ""

        # Parse vcap download URL
        link = row.find("a")
        if link.has_attr("href"):
            linktext = link["href"]
            startswith = linktext.startswith(HREF_STARTSWITH)
            endswith = linktext.endswith(VISIONCAPSULES_EXT)
            if startswith and endswith:
                download_url = marketplace_url + linktext
                VisionCapsules_FullList.append(download_url)

                tbody_download_url = download_url
                tbody_file_name = download_url.split("/")[-1]

        cols = row.find_all("td")

        # Parse the text in the first 3 columns: Name, Description, Hardware
        tbody_name = cols[0].string
        tbody_description = cols[1].string
        if tbody_description.startswith(TBODY_PRODUCTION):
            tbody_description = tbody_description.replace(TBODY_PRODUCTION, "").strip()
            tbody_production = "Ready"

        tbody_hardware = cols[2].get_text(separator=" ").strip()

        # Parse the text in the Required Input column
        vcap_required_input = cols[3].find_all("strong")
        items = cols[3].find_all("strong")
        for item in vcap_required_input:
            item_name = item.contents[0]

            next_item = item.nextSibling
            item_value = next_item.string

            if item_name == TBODY_REQUIRED_INPUT_TYPE:
                tbody_required_input_type = item_value
            if item_name == TBODY_REQUIRED_INPUT_DETECTIONS:
                tbody_required_input_detections = str(item_value)
            if item_name == TBODY_REQUIRED_INPUT_TRACKED:
                tbody_required_input_tracked = item_value

        # Parse the text in the Output column
        vcap_output = cols[4].find("summary")
        if vcap_output:
            tbody_output_expand = True

        vcap_output = cols[4].find_all("strong")
        for item in vcap_output:

            item_name = item.contents[0]

            next_item = item.nextSibling
            item_value = next_item.string

            next_item = next_item.nextSibling
            item_detail = next_item

            if item_name == TBODY_OUTPUT_TYPE:
                tbody_output_type = item_value
            if item_name == TBODY_OUTPUT_DETECTIONS:
                tbody_output_detections = item_value
            if item_name == TBODY_OUTPUT_ENCODED:
                tbody_output_encoded = item_value
            if item_name == TBODY_OUTPUT_TRACKED:
                tbody_output_tracked = item_value
            if item_name == TBODY_OUTPUT_CLASSIFIES:
                if item_detail:
                    tbody_output_classifies = str(item_detail)
                    while next_item:
                        next_item = next_item.nextSibling  # skip a <br>
                        if next_item:
                            next_item = next_item.nextSibling
                            item_detail2 = next_item
                            tbody_output_classifies = (
                                tbody_output_classifies + ". " + str(item_detail2)
                            )

        vcap_item = {
            thead.thead_name: tbody_name,
            thead.thead_description: tbody_description,
            TBODY_PRODUCTION: tbody_production,
            thead.thead_hardware: tbody_hardware,
            # thead_required_input: vcap_required_input,
            TBODY_REQUIRED_INPUT_TYPE: tbody_required_input_type,
            TBODY_REQUIRED_INPUT_DETECTIONS: tbody_required_input_detections,
            TBODY_REQUIRED_INPUT_TRACKED: tbody_required_input_tracked,
            # thead_output:         vcap_output,
            TBODY_OUTPUT_TYPE: tbody_output_type,
            TBODY_OUTPUT_CLASSIFIES: tbody_output_classifies,
            TBODY_OUTPUT_DETECTIONS: tbody_output_detections,
            TBODY_OUTPUT_ENCODED: tbody_output_encoded,
            TBODY_OUTPUT_TRACKED: tbody_output_tracked,
            TBODY_OUTPUT_EXPAND: tbody_output_expand,
            TBODY_DOWNLOAD_URL: tbody_download_url,
            TBODY_FILE_NAME: tbody_file_name,
        }

        vcap_table.append(vcap_item)

    return vcap_table


def retrieve_vcap_url(vcap_table, vcap_file_name):

    for vcap_rol in vcap_table:
        vcap_remote_file_name = vcap_rol.get(TBODY_FILE_NAME)

        if vcap_file_name.strip() == vcap_remote_file_name.strip():
            vcap_url = vcap_rol.get(TBODY_DOWNLOAD_URL)
            return vcap_url
        else:
            pass

    print(f"Error: {vcap_file_name} not found")


def build_vcap_list(vcap_local_list, vcap_table, thead):

    # Initialize the Choices list, mark the downloaded VisionCapsules as True in the list
    vcap_choices = []
    last_selection_name = ""
    for vcap_rol in vcap_table:

        vcap_url = vcap_rol.get(TBODY_DOWNLOAD_URL)

        # Use the first word of the vcap file name as the section name
        vcap_remote_file_name = vcap_rol.get(TBODY_FILE_NAME)
        selection_name = vcap_remote_file_name.split("_")[0]

        exists = False
        for vcap_local_file_path in vcap_local_list:

            vcap_local_file_name = vcap_local_file_path.split("/")[-1]
            if vcap_remote_file_name == vcap_local_file_name:
                exists = True
                break
            else:
                exists = False

        if selection_name != last_selection_name:
            SeparatorText = "======== " + selection_name + " ========"
            vcap_choices.append(Separator(SeparatorText))
            last_selection_name = selection_name

        # Add VisionCapsules download url line
        vcap_choices.append({"name": vcap_url, "checked": exists})

        # Add VisionCapsules Name, Description
        vcap_text = vcap_rol.get(thead.thead_name) + ": "
        if vcap_rol.get(TBODY_PRODUCTION):
            vcap_text = (
                vcap_text + "(Production " + vcap_rol.get(TBODY_PRODUCTION) + ") "
            )

        vcap_text = vcap_text + vcap_rol.get(thead.thead_description)

        vcap_choices.append(Separator("  " + vcap_text))

        # Add VisionCapsules Hardware, Required Input, Output
        vcap_text = thead.thead_hardware + ": " + vcap_rol.get(thead.thead_hardware)
        vcap_choices.append(Separator("  " + vcap_text))

        vcap_text = (
            thead.thead_required_input + ": " + vcap_rol.get(TBODY_REQUIRED_INPUT_TYPE)
        )
        if vcap_rol.get(TBODY_REQUIRED_INPUT_TRACKED):
            vcap_text = vcap_text + ". " + TBODY_REQUIRED_INPUT_TRACKED + "True "
        if vcap_rol.get(vcap_rol.get(TBODY_REQUIRED_INPUT_DETECTIONS)):
            vcap_text = vcap_text + ". " + vcap_rol.get(TBODY_REQUIRED_INPUT_DETECTIONS)
        vcap_choices.append(Separator("  " + vcap_text))

        vcap_text = thead.thead_output + ": " + vcap_rol.get(TBODY_OUTPUT_TYPE)
        if vcap_rol.get(TBODY_OUTPUT_ENCODED):
            vcap_text = vcap_text + ". " + TBODY_OUTPUT_ENCODED + "True "
        if vcap_rol.get(TBODY_OUTPUT_TRACKED):
            vcap_text = vcap_text + ". " + TBODY_OUTPUT_TRACKED + "True "
        if vcap_rol.get(TBODY_OUTPUT_CLASSIFIES):
            vcap_text = (
                vcap_text
                + ". "
                + TBODY_OUTPUT_CLASSIFIES
                + " "
                + vcap_rol.get(TBODY_OUTPUT_CLASSIFIES)
            )
        if vcap_rol.get(TBODY_OUTPUT_DETECTIONS):
            vcap_text = (
                vcap_text
                + ". "
                + TBODY_OUTPUT_DETECTIONS
                + " "
                + vcap_rol.get(TBODY_OUTPUT_DETECTIONS)
            )
        vcap_choices.append(Separator("  " + vcap_text))
    return vcap_choices

def prompt_questions(vcap_choices):

    questions = [
        {
            "type": "checkbox",
            "qmark": "[?]",
            "message": "Select VisionCapsules",
            "name": "vcap choices",
            "choices": vcap_choices,
            "validate": lambda answer: "Thanks for using VisionCapsules."
            if len(answer) == 0
            else True,
        }
    ]

#    custom_style_2 = style_from_dict(
#        {
#            "separator": '#6C6C6C',
#            "questionmark": '#FF9D00 bold',
#            "selected": '#5F819D',
#            "pointer": '#FF9D00 bold',
#            "instruction": '',
#            "answer": '#5F819D bold',
#            "question": '',
#        }
#    )

#    answers = prompt(questions, style=custom_style_2)
    answers = prompt(questions)

    vcap_selected_list = answers.get("vcap choices")
    return vcap_selected_list

def download_capsules(vcap_url, capsules_path):

    vcap_local_file_name_to_be_downloaded = (
        capsules_path + "/" + vcap_url.split("/")[-1]
    )

    if not os.path.exists(vcap_local_file_name_to_be_downloaded):

        print("\nDownloading " + vcap_url)
        wget.download(vcap_url, out=capsules_path)

def update_capsules(vcap_local_list, vcap_selected_list, capsules_path):

    # Download newly selected VisionCapsules
    for vcap_url in vcap_selected_list:

        download_capsules(vcap_url, capsules_path)

    # Delete unselected VisionCapsules
    for vcap_local_file in vcap_local_list:

        vcap_local_file_name = vcap_local_file.split("/")[-1]
        delete_me = True
        for vcap_url in vcap_selected_list:
            if vcap_local_file_name in vcap_url:
                delete_me = False
                break
        if delete_me:
            remove_capsules(vcap_local_file)

def remove_capsules(vcap_local_file):

    try:
        os.remove(vcap_local_file)
        print(f"{vcap_local_file} has been removed.");

    except OSError as e:
        print("Error: %s : %s" % (vcap_local_file, e.strerror))


def remove_all_capsules(vcap_local_file):

    files = glob.glob(vcap_local_file+'/*')
    for f in files:
        try:
            os.remove(f)
            print(f"{f} has been removed.");

        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))


def __parse_args__():

    brainframe_info_data_path = subprocess.getoutput("brainframe info data_path")
    default_local_vcap_dir = brainframe_info_data_path + "/capsules"

    parser = ArgumentParser(
        description="A helper utility for downloading BrainFrame capsules."
    )

    parser.add_argument(
        "-d",
        "--directory",
        default= default_local_vcap_dir,
        help=f'The path to the BrainFrame capsule directory. default is {default_local_vcap_dir}',
    )

    parser.add_argument(
        "-f",
        "--file-names",
        nargs='+',
        help="The capsule files to be downloaded. A selection list will be prompt if the argument is not provided",
    )

    parser.add_argument(
        '-r',
        '--remove',
        action = "store_true",
        help="The capsule file to be removed. default is all local capsules will be removed",
    )

    args = parser.parse_args()
    return args


def main():

    WEBSITE_URL = "https://aotu.ai"
    WEBSITE_PATH = "/docs/downloads/"

    args = __parse_args__()

    if args.remove:
        if args.file_names:
            for file_name in args.file_names:
                remove_capsules(args.directory + '/' + file_name)
        else:
            remove_all_capsules(args.directory)

    else:
        # Download table from VisionCapsules marketplace
        table = connect_marketplace(WEBSITE_URL, WEBSITE_PATH)

        # Parse the table
        thead = parse_thead(table)
        vcap_table = parse_table(WEBSITE_URL, table, thead)

        # Build VisionCapsules lists from local path
        vcap_local_list = find_localfiles("*" + VISIONCAPSULES_EXT, args.directory)

        # Build VisionCapsules question list
        vcap_choices = build_vcap_list(vcap_local_list, vcap_table, thead)

        if not args.file_names:
            # Prompt questions
            vcap_selected_list = prompt_questions(vcap_choices)

            # Update the local VisionCapsules
            update_capsules(vcap_local_list, vcap_selected_list, args.directory)
        else:
            for file_name in args.file_names:
                vcap_url = retrieve_vcap_url(vcap_table, file_name)
                if vcap_url:
                    download_capsules(vcap_url, args.directory)


    print("\nCurrent local VisionCapsules:\n")

    if os.listdir(args.directory):
        print("\n    + " + "\n    + ".join(os.listdir(args.directory)) + "\n")
    else:
        print("    empty\n")


if __name__ == "__main__":
    main()
