#!/usr/bin/python3
import sys
import os
import requests
import shutil

def send_file_to_aws(statement_dir: str, filename: str, aws_api_url: str, s3_bucket: str):
    post_url = "{}/{}/{}".format(aws_api_url, s3_bucket, filename)
    file_path = "{}/{}".format(statement_dir, filename)
    
    with open(file_path, "r") as f:        
        response = requests.put(post_url, files={"file":f})

    return response

def move_file_to_archive(archive_dir: str, statement_dir: str, filename: str) -> bool:
    shutil.move("{}/{}".format(statement_dir, filename), "{}/{}".format(archive_dir, filename))

def list_files(directory: str) -> list:
    return os.listdir(directory)

def main() -> None:

    for i in range(1, len(sys.argv)):
        args = sys.argv[i].split("=")
        if (args[0] == "input"):
            statement_dir: str = args[1]
        elif (args[0] == "archive"):
            archive_dir: str = args[1]
        elif (args[0] == "api"):
            aws_api_url: str = args[1]
        elif (args[0] == "s3"):
            s3_bucket = args[1]
    
    files = list_files(statement_dir)

    for f in files:
        r = send_file_to_aws(statement_dir, f, aws_api_url, s3_bucket)
        if r.text != "":
            print("Error occurred: {}".format(r.text))
        else:
            move_file_to_archive(archive_dir, statement_dir, f)


if __name__ == "__main__":
    main()