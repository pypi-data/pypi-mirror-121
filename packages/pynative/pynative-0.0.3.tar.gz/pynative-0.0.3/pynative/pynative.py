#!/usr/bin/python
# -*- coding: utf-8 -*-

__copyright__ = """

MIT License

Copyright (c) 2021 Samapriya Roy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


"""
__license__ = "MIT License"

import requests
import json
import sys
import pkg_resources
import argparse
import os
from os.path import expanduser
from bs4 import BeautifulSoup
from operator import itemgetter


class Solution:
    def compareVersion(self, version1, version2):
        versions1 = [int(v) for v in version1.split(".")]
        versions2 = [int(v) for v in version2.split(".")]
        for i in range(max(len(versions1), len(versions2))):
            v1 = versions1[i] if i < len(versions1) else 0
            v2 = versions2[i] if i < len(versions2) else 0
            if v1 > v2:
                return 1
            elif v1 < v2:
                return -1
        return 0


ob1 = Solution()

# Get package version
def pynative_version():
    url = "https://pypi.org/project/pynative/"
    source = requests.get(url)
    html_content = source.text
    soup = BeautifulSoup(html_content, "html.parser")
    company = soup.find("h1")
    vcheck = ob1.compareVersion(
        company.string.strip().split(" ")[-1],
        pkg_resources.get_distribution("pynative").version,
    )
    if vcheck == 1:
        print(
            "\n"
            + "========================================================================="
        )
        print(
            "Current version of pynative is {} upgrade to lastest version: {}".format(
                pkg_resources.get_distribution("pynative").version,
                company.string.strip().split(" ")[-1],
            )
        )
        print(
            "========================================================================="
        )
    elif vcheck == -1:
        print(
            "\n"
            + "========================================================================="
        )
        print(
            "Possibly running staging code {} compared to pypi release {}".format(
                pkg_resources.get_distribution("pynative").version,
                company.string.strip().split(" ")[-1],
            )
        )
        print(
            "========================================================================="
        )


pynative_version()


### download source
def source(mtype, path):
    if mtype == "territories":
        url = "https://native-land.ca/wp-content/themes/Native-Land-Theme/files/indigenousTerritories.json"
    elif mtype == "languages":
        url = "https://native-land.ca/wp-content/themes/Native-Land-Theme/files/indigenousLanguages.json"
    elif mtype == "treaties":
        url = "https://native-land.ca/wp-content/themes/Native-Land-Theme/files/indigenousTreaties.json"
    else:
        sys.exit("No matching map type found")
    response = requests.get(url, allow_redirects=True)
    if response.status_code == 200:
        print(f"Downloading to {path}")
        open(path, "wb").write(response.content)
    else:
        print(
            f"Download failed with error code {response.status_code}: Attempting to use API endpoint"
        )
        response = requests.get(
            f"https://native-land.ca/wp-json/nativeland/v1/api/index.php?maps={mtype}"
        )
        if response.status_code == 200:
            data = {"type": "FeatureCollection", "features": response.json()}
            with open(path, "w") as outfile:
                json.dump(data, outfile, indent=4)
        else:
            print(
                f"All attempts failed with error code: {response.status_code} try again later"
            )


def fetch_from_parser(args):
    source(mtype=args.mtype, path=args.path)


def position(ll, mtype, path):
    ll = ll[0]
    type_list = ["territories", "languages", "treaties"]
    if not mtype in type_list:
        sys.exit("No matching map type found")
    response = requests.get(
        f"https://native-land.ca/api/index.php?maps={mtype}&position={str(ll)}"
    )
    if response.status_code == 200 and len(response.json()) > 0:
        print(f"Downloading to {path} for {ll}")
        data = {"type": "FeatureCollection", "features": response.json()}
        with open(path, "w") as outfile:
            json.dump(data, outfile, indent=4)
    elif response.status_code == 200 and len(response.json()) == 0:
        print(f"No results returned for location {ll}")
    else:
        print(f"Request failed with error code: {response.status_code}")


def location_from_parser(args):
    position(ll=args.ll, mtype=args.mtype, path=args.path)


def place(addr, mtype, path):
    location_list = []
    if (",") in addr:
        addr = addr.split(",")
        real = ",".join(addr)
    else:
        real = addr
    response = requests.get(
        "https://nominatim.openstreetmap.org/search?q=" + real + "&format=jsonv2"
    )
    if response.status_code == 200:
        response = response.json()
        for things in response:
            try:
                if len(response) > 1 and things["importance"] >= 0.7:
                    location_list.append(
                        {
                            "ll": f"{things['lat']},{things['lon']}",
                            "importance": things["importance"],
                        }
                    )
            except Exception as e:
                print(e)
    if len(location_list) == 0:
        sys.exit(f"Location {addr} could not be parsed")
    newlist = sorted(location_list, key=itemgetter("importance"), reverse=True)
    ll = newlist[-1].get("ll")
    type_list = ["territories", "languages", "treaties"]
    if not mtype in type_list:
        sys.exit("No matching map type found")
    response = requests.get(
        f"https://native-land.ca/api/index.php?maps={mtype}&position={str(ll)}"
    )
    if response.status_code == 200 and len(response.json()) > 0:
        print(f"Downloading to {path} for {ll}")
        data = {"type": "FeatureCollection", "features": response.json()}
        with open(path, "w") as outfile:
            json.dump(data, outfile, indent=4)
    elif response.status_code == 200 and len(response.json()) == 0:
        print(f"No results returned for location {addr[0]} with lat:long {ll}")
    else:
        print(f"Request failed with error code: {response.status_code}")


def place_from_parser(args):
    place(addr=args.addr, mtype=args.mtype, path=args.path)


def main(args=None):
    parser = argparse.ArgumentParser(description="Simple CLI for Native Land API")
    subparsers = parser.add_subparsers()

    parser_fetch = subparsers.add_parser(
        "fetch", help="Download most updated map and type as GeoJSON file"
    )
    required_named = parser_fetch.add_argument_group("Required named arguments.")
    required_named.add_argument(
        "--mtype", help="Map type territories|languages|treaties", required=True
    )
    required_named.add_argument(
        "--path", help="Full path to map.geojson", required=True
    )
    parser_fetch.set_defaults(func=fetch_from_parser)

    parser_location = subparsers.add_parser(
        "location",
        help="Search using lat long pair location for data and download as GeoJSON file",
    )
    required_named = parser_location.add_argument_group("Required named arguments.")
    required_named.add_argument(
        "--ll",
        help="Comma seperated latitude,longitude",
        required=True,
        nargs=argparse.REMAINDER,
    )
    required_named.add_argument(
        "--mtype", help="Map type territories|languages|treaties", required=True
    )
    required_named.add_argument(
        "--path", help="Full path to map.geojson", required=True
    )
    parser_location.set_defaults(func=location_from_parser)

    parser_place = subparsers.add_parser(
        "place",
        help="Search using a place name or address and download as GeoJSON file",
    )
    required_named = parser_place.add_argument_group("Required named arguments.")
    required_named.add_argument(
        "--addr", help="Comma seperate place name or address", required=True
    )
    required_named.add_argument(
        "--mtype", help="Map type territories|languages|treaties", required=True
    )
    required_named.add_argument(
        "--path", help="Full path to map.geojson", required=True
    )
    parser_place.set_defaults(func=place_from_parser)

    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)


if __name__ == "__main__":
    main()
