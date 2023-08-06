#!/usr/bin/python3
"""
    HTTP Methods Testing Tool

    Copyright (c) 2020 HACKER Consulting s.r.o.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__version__ = "0.0.1"

import argparse
import sys
import urllib

import requests

from ptlibs import ptjsonlib, ptmisclib


class ptmethods:
    def __init__(self, args):
        self.use_json = args.json
        self.ptjsonlib = ptjsonlib.ptjsonlib(self.use_json)
        self.json_no = self.ptjsonlib.add_json("ptmethods")        
        self.ptjsonlib.add_data(self.json_no, {"urls": []})

        self.show_headers = args.show_headers
        self.show_response = args.show_response

        if args.cookie:
            args.cookie = '; '.join(args.cookie)

        self.headers = ptmisclib.get_request_headers(args)
        self.proxy = {"http": args.proxy, "https": args.proxy}
        self.redirects = args.redirects

        if not (args.file or args.url):
            ptmisclib.end_error("Missing -u/-f parameter!", self.json_no, self.ptjsonlib, self.use_json)
        elif args.url and args.file:
            ptmisclib.end_error("Cannot use both -u and -f parameters together!", self.json_no, self.ptjsonlib, self.use_json)
        try:
            self.url_list = ptmisclib.read_file(args.file) if args.file else args.url
        except FileNotFoundError:
            ptmisclib.end_error("File not found!", self.json_no, self.ptjsonlib, self.use_json)
        ptmisclib.check_connectivity()

    def parse_url(self, url):
        o = urllib.parse.urlparse(url)
        if o.scheme not in ["http", "https"]:
            raise Exception("Missing or unsupported scheme")
        return urllib.parse.urlunparse(o)

    def run(self):
        """Main function"""
        for url in self.url_list:
            ptmisclib.ptprint(ptmisclib.out_title_ifnot(f"Testing: {url}", self.use_json), end="\n")
            self.data = {"url": url, "status": "null", "vulnerable:": "null", "options": {}, "methods": {}}
            try:
                url = self.parse_url(url)
                methods = self.check_methods(url)
                options = self.get_options(url)
                #connect_test = self.check_connect_method(url_scheme + "://" + url_domain)
                #proxy_test = self.check_proxy_method(url)
                self.print_result(options, methods)
                self.data.update({"status": "ok", "options": options, "methods": methods})
                if self.use_json:
                    self.ptjsonlib.json_list[self.json_no]["data"]["urls"].append(self.data)
            except Exception as e:
                if len(self.url_list) > 1:
                    self.data.update({"status": "error", "message": str(e)})
                    if self.use_json:
                        self.ptjsonlib.json_list[self.json_no]["data"]["urls"].append(self.data)
                    ptmisclib.ptprint(ptmisclib.out_ifnot(f"Error: {e}, skipping. \n", "ERROR", self.use_json))
                    continue
                else:
                    ptmisclib.end_error(str(e), self.json_no, self.ptjsonlib, self.use_json)
        ptmisclib.ptprint(ptmisclib.out_if(self.ptjsonlib.get_all_json(), "", self.use_json))

    def get_response(self, url, method, proxy=None):
        if proxy is None:
            proxy = self.proxy
        r = requests.request(method, url, allow_redirects=self.redirects, headers=self.headers, proxies=proxy, verify=False)
        return r

    def check_connect_method(self, url):
        pass
        #r = self.get_response("https://www.example.com:443", "CONNECT", {"https": url})

    def check_proxy_method(self, url):
        pass
        #r = self.get_response("http://example.com", "GET", {"http": url})

    def get_options(self, url):
        response = self.get_response(url, "OPTIONS")
        if "allow" in response.headers:
            allowed_methods = response.raw.headers.getlist('allow')
            allowed_methods = "".join(allowed_methods).split(",")
            return allowed_methods
        else:
            return ["None"]

    def check_methods(self, url):
        METHOD_LIST = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD", "TRACE", "DEBUG", "FOO"]
        methods_result = {"available_methods": [], "not_available_methods": []}
        for method in METHOD_LIST:
            response = self.get_response(url, method)
            json_data = {"method": method, "status": response.status_code, "headers": [], "response": []}
            if self.show_headers:
                json_data["headers"].append(dict(response.headers))
            if self.show_response:
                json_data["response"].append(response.text)
            if response.status_code == 200:
                methods_result["available_methods"].append(json_data)
            else:
                methods_result["not_available_methods"].append(json_data)
        return methods_result

    def print_result(self, options, methods):
        ptmisclib.ptprint(ptmisclib.out_ifnot(f"Response for OPTIONS: {', '.join(options)}", "INFO", self.use_json))
        for key, value in methods.items():
                ptmisclib.ptprint(ptmisclib.out_ifnot(f"{key.capitalize().replace('_',' ')}:", "INFO", self.use_json))
                if not value: 
                    ptmisclib.ptprint(ptmisclib.out_ifnot(f"    None", "", self.use_json))
                for idx, dictionary in enumerate(value):
                    ptmisclib.ptprint(ptmisclib.out_ifnot(f"{dictionary['method']}{' '*(9-len(dictionary['method']))}[{dictionary['status']}]", "", self.use_json))
                    """
                    if not self.show_headers:
                        ptmisclib.ptprint(ptmisclib.out_ifnot(f" ", "", self.use_json))
                    """
                    if self.show_headers:
                        for header, value in dictionary["headers"][0].items():
                            ptmisclib.ptprint(ptmisclib.out_ifnot(ptmisclib.get_colored_text(f'{header} : {value}', 'ADDITIONS'), "", self.use_json))
                    if self.show_headers and self.show_response:
                        ptmisclib.ptprint(ptmisclib.out_ifnot(f" ", "", self.use_json))
                    if self.show_response:
                        ptmisclib.ptprint(ptmisclib.out_ifnot(ptmisclib.get_colored_text(f'{"".join(dictionary["response"])}', 'ADDITIONS'), "", self.use_json))

def get_help():
    return [
        {"description": ["Allowed HTTP Methods Testing Tool"]},
        {"usage": ["ptmethods <options>"]},
        {"Tip": ["Optimally use this script against homepage, any image and sources protected by HTTP authentication"]},
        {"usage_example": [
            "ptmethods -u https://www.example.com/image.jpg",
            "ptmethods -u https://www.example.com/index.php",
            "ptmethods -u https://www.example.com/index.php -c PHPSESSID=abcdef",
            "ptmethods -f URL_list.txt",
        ]},
        {"options": [
            ["-u",  "--url",                    "<url>",            "Test specified URL"],
            ["-f",  "--file",                   "<file>",           "Load list of URLs from file"],
            ["-sh", "--show-headers",           "",                 "Show response headers"],
            ["-sr", "--show-response",          "",                 "Show response text"],
            ["-p",  "--proxy",                  "<proxy>",          "Set proxy (e.g. http://127.0.0.1:8080)"],
            ["-ua",  "--user-agent",            "<ua>",             "Set User-Agent header"],
            ["-H",  "--headers",                "<header:value>",   "Set custom header(s)"],
            ["-c",  "--cookie",                 "<cookie>",         "Set cookie(s)"],
            ["-r",  "--redirects",              "",                 "Follow redirects (default False)"],
            ["-j",  "--json",                   "",                 "Output in JSON format"],
            ["-v",  "--version",                "",                 "Show script version and exit"],
            ["-h",  "--help",                   "",                 "Show this help message and exit"]
        ]
        }]


def parse_args():
    parser = argparse.ArgumentParser(add_help=False, usage="ptmethods <options>")
    parser.add_argument("-u", "--url", type=str, nargs="+")
    parser.add_argument("-f", "--file", type=str)
    parser.add_argument("-p", "--proxy", type=str)
    parser.add_argument("-ua", "--user-agent", type=str, default="Penterep Tools")
    parser.add_argument("-c", "--cookie", type=str, nargs="+")
    parser.add_argument("-H", "--headers", type=ptmisclib.pairs, nargs="+")
    parser.add_argument("-j", "--json", action="store_true")
    parser.add_argument("-r", "--redirects", action="store_true")
    parser.add_argument("-sr", "--show-response", action="store_true")
    parser.add_argument("-sh", "--show-headers", action="store_true")
    parser.add_argument("-v", "--version", action="version", version=f"{SCRIPTNAME} {__version__}")

    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        ptmisclib.help_print(get_help(), SCRIPTNAME, __version__)
        sys.exit(0)
    args = parser.parse_args()
    ptmisclib.print_banner(SCRIPTNAME, __version__, args.json)
    return args


def main():
    global SCRIPTNAME
    SCRIPTNAME = "ptmethods"
    requests.packages.urllib3.disable_warnings()
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    args = parse_args()
    script = ptmethods(args)
    script.run()


if __name__ == "__main__":
    main()
