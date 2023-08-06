import os
import urllib.request
from zipfile import ZipFile

from tqdm import tqdm

# File are copied from https://poe.ninja/data-dumps
ZIP_FILES = [
    "Ritual.2021-01-15.2021-04-12.zip",
    "Heist.2020-09-18.2021-01-11.zip",
    "Harvest.2020-06-19.2020-09-14.zip",
    "Delirium.2020-03-13.2020-06-15.zip",
    "Metamorph.2019-12-13.2020-03-09.zip",
    "Blight.2019-09-06.2019-12-09.zip",
    "Legion.2019-06-07.2019-09-02.zip",
    "Synthesis.2019-03-08.2019-06-04.zip",
    "Betrayal.2018-12-07.2019-03-05.zip",
    "Delve.2018-08-31.2018-12-03.zip",
    "Incursion.2018-06-01.2018-08-28.zip",
    "Bestiary.2018-03-02.2018-05-28.zip",
    "Abyss.2017-12-08.2018-03-01.zip",
    "Harbinger.2017-08-04.2017-12-04.zip",
    "Legacy.2017-03-03.2017-07-31.zip",
    "Breach.2016-12-02.2017-02-28.zip",
]


def download_files(files, directory):
    os.makedirs(directory, exist_ok=False)
    opener = urllib.request.build_opener()
    opener.addheaders = [("User-agent", "Mozilla/5.0")]
    urllib.request.install_opener(opener)
    for file in tqdm(files):
        league_name = file.split(".")[0]
        url = f"https://poe.ninja/data-dumps/{league_name}/{file}"
        urllib.request.urlretrieve(url, f"{directory}/{file}")


def unzip_files(files, directory):
    for file in tqdm(files):
        with ZipFile(f"{directory}/{file}", "r") as zip_file:
            league_name = file.split(".")[0]
            zip_file.extractall(f"{directory}/{league_name}/")
