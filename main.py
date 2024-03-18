import re
import os
import yaml
from pyarr import SonarrAPI
from thefuzz import fuzz

current_directory = os.getcwd()

config_path = f"{current_directory}/config.yml"

with open(config_path, "r") as config_file:
    config = yaml.safe_load(config_file)

# sonarr api settings
host_url = config["sonarr"]["url"]
api_key = config["sonarr"]["api_key"]
# init sonarr api
sonarr = SonarrAPI(host_url, api_key)

show_id = config["sonarr"]["show_id"]

# get show
show = sonarr.get_episodes_by_series_id(show_id)

# pprint.pp(show)

inital_dir = config["directories"]["saved_dir"]
output_dir = config["directories"]["output_dir"]


def sanitize_filename(filename):
    # Remove invalid characters
    filename = re.sub('[\\\\/:*?"<>|]', "", filename)
    return filename


for episode in show:
    # if episode["seasonNumber"] < 25:
    #     continue
    for file in os.listdir(inital_dir):
        sanitized_file = sanitize_filename(file)
        file_title, extension = os.path.splitext(sanitized_file)
        similarity = fuzz.ratio(file_title, episode["title"])
        if similarity > 80:
            season_num = episode["seasonNumber"]
            episode_num = episode["episodeNumber"]
            print(
                f"Renaming File: {file_title} to S{season_num}E{episode_num} - {file_title}{extension}"
            )
            try:
                os.rename(
                    f"{inital_dir}/{file}",
                    f"{output_dir}/S{season_num}E{episode_num} - {file_title}{extension}",
                )
            except:
                print(
                    f"Error Renaming File: {file_title} to S{season_num}E{episode_num} - {file_title}{extension}"
                )
                continue

for file in os.listdir(inital_dir):
    print(f"Could not find match for {file}")
