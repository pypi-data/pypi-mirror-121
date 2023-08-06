#!/usr/bin/python3
"""
    DNS Zone Transfer Testing Tool

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
import re
import sys

from ptlibs import ptmisclib, ptjsonlib
from ptthreads import ptthreads

import dns.resolver
import dns.zone


class ptaxfr:
    def __init__(self, args):
        self.use_json = args.json
        self.ptjsonlib = ptjsonlib.ptjsonlib(self.use_json)
        self.ptthreads = ptthreads.ptthreads()
        try:
            self.domains = ptmisclib.read_file(args.file) if args.file else args.domain
        except FileNotFoundError:
            ptmisclib.end_error("File not found", self.ptjsonlib.add_json(SCRIPTNAME), self.ptjsonlib, self.use_json)
        self.vulnerable_only = args.vulnerable_only
        self.silent = args.silent
        self.print_dns = args.print_dns
        self.print_subdomains = args.print_subdomains

    def run(self, args):
        if not self.print_dns and not self.print_subdomains:
            self.print_dns = True
        if self.print_dns and self.print_subdomains:
            ptmisclib.end_error("Cannot use -pd and -ps parameters together", self.ptjsonlib.add_json("ns_check"), self.ptjsonlib, self.use_json)
        if self.vulnerable_only:
            ptmisclib.ptprint(ptmisclib.out_ifnot("Vulnerable domains:", "TITLE", self.use_json))
        self.ptthreads.threads(self.domains, self.ns_check, args.threads)
        ptmisclib.ptprint(ptmisclib.out_if(self.ptjsonlib.get_all_json(), None, self.use_json))

    def ns_check(self, domain):
        """Finds and tests all nameservers of <domain> for zone transfer"""
        printlock = ptthreads.printlock()
        json_no = self.ptjsonlib.add_json("ns_check")
        is_vulnerable = None
        vulnerable_ns_zones = []
        self.ptjsonlib.add_data(json_no, {"domain": domain, "NS": []})
        printlock.add_string_to_output(ptmisclib.out_ifnot(ptmisclib.get_colored_text(f"Testing domain: {domain}", "TITLE"), "TITLE", self.use_json or self.vulnerable_only), silent=self.silent)
        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = 15
            ns_query = resolver.resolve(domain, "NS", tcp=True)
            domain_nameservers = []
            for rdata in ns_query:
                nameserver_name = str(rdata)[:-1]
                nameserver_ip = [str(ip) for ip in resolver.resolve(str(rdata)[:-1], "A")][0]
                domain_nameservers.append({"ns_name": str(rdata)[:-1], "ns_ip": nameserver_ip, "vulnerable": "null", "data": []})
                try:
                    printlock.add_string_to_output(ptmisclib.out_ifnot(f"Nameserver: {nameserver_name}", "INFO", self.use_json or self.vulnerable_only), silent=self.silent)
                    printlock.add_string_to_output(ptmisclib.out_ifnot(f"IP: {nameserver_ip}", "INFO", self.use_json or self.vulnerable_only), silent=self.silent)
                    zone = dns.zone.from_xfr(dns.query.xfr(nameserver_ip, domain, lifetime=5.01))
                    printlock.add_string_to_output(ptmisclib.out_ifnot(f"Vulnerable: True", "VULN", self.use_json or self.vulnerable_only), silent=self.silent, end="\n")
                    domain_nameservers[-1].update({"vulnerable": "True"})
                    vulnerable_ns_zones.append({nameserver_name: zone})
                    is_vulnerable = True
                except dns.exception.Timeout:
                    # TODO Zkontrolovat spolehlivost.
                    printlock.add_string_to_output(ptmisclib.out_ifnot(f"Timeout error", "ERROR", self.use_json or self.vulnerable_only), silent=self.silent)
                    domain_nameservers[-1].update({"vulnerable": "TimeOutErrorDebug"})
                except dns.exception.DNSException:
                    printlock.add_string_to_output(ptmisclib.out_ifnot(f"Vulnerable: False", "NOTVULN", self.use_json or self.vulnerable_only), silent=self.silent, end="\n")
                    domain_nameservers[-1].update({"vulnerable": "False"})

            if is_vulnerable:
                printlock.add_string_to_output(domain, self.vulnerable_only)
            self.ptjsonlib.set_status(json_no, "ok")
            self.ptjsonlib.add_data(json_no, {"NS": domain_nameservers})
            self.ptjsonlib.set_vulnerable(json_no, is_vulnerable)

            if is_vulnerable and not self.vulnerable_only:
                printlock.add_string_to_output(ptmisclib.out_title_ifnot(f"Enumerating vulnerable nameservers of {domain} ...", "INFO", self.use_json), silent=self.silent)
                for i in vulnerable_ns_zones:
                    for nameserver, zone in i.items():
                        printlock.add_string_to_output(ptmisclib.out_ifnot(f"{nameserver}:", "INFO", self.use_json), silent=self.silent)
                        if self.print_dns:
                            data = self.extract_dns_records(zone, printlock)
                        else:
                            data = self.extract_subdomains(zone, printlock)
                        for j in domain_nameservers:
                            if j["ns_name"] == nameserver:
                                j["data"] = data
        except Exception as e: 
            self.ptjsonlib.set_status(json_no, "error", "domain not reachable")
            printlock.add_string_to_output(ptmisclib.out_ifnot(f"Domain not reachable - {e}", "ERROR", self.use_json or self.vulnerable_only), silent=self.silent)
        printlock.lock_print_output(end="")

    def extract_dns_records(self, zone, printlock):
        data = []
        for name, node in zone.nodes.items():
            names = re.findall(r"DNS IN ([\(\)\w]*) rdataset", str(node.rdatasets))
            for i, rdataset in enumerate(node.rdatasets):
                if not self.vulnerable_only:
                    rdataset_records_str = str(rdataset).replace("\n", ", ")
                    rdataset_records_list = list(rdataset_records_str.split(","))
                    for rdataset_record in rdataset_records_list:
                        multiline_record = None
                        rdataset_data = re.findall(rf"{names[i].replace('(', ' ').replace(')', ' ')}(.*)", rdataset_record)[0]
                        rdataset_type = names[i]
                        split_list = rdataset_records_str.split()
                        if len(rdataset_records_str.split(", ")) > 1:
                            multiline_record = [record.split() for record in rdataset_records_str.split(", ")]
                        if not multiline_record:
                            printlock.add_string_to_output(ptmisclib.out_ifnot(f"{str(name)}{' '*(30-len(str(name)))}{split_list[0]}{' '*(10-len(str(split_list[0])))}{split_list[1]}{' '*(10-len(str(split_list[1])))}{split_list[2]}{' '*(10-len(str(split_list[2])))}{' '.join(split_list[3:])}", None, self.use_json), trim=True)
                        else:
                            printlock.add_string_to_output(ptmisclib.out_ifnot(f"{str(name)}", None, self.use_json), trim=False, end="")
                            for r_no in range(len(multiline_record)):
                                if r_no == 0:
                                    printlock.add_string_to_output(ptmisclib.out_ifnot(f"{' '*(30-len(str(name)))}", None, self.use_json), trim=False, end="")
                                else:
                                    printlock.add_string_to_output(ptmisclib.out_ifnot(f"{' '*30}", None, self.use_json), trim=False, end="")
                                #printlock.add_string_to_output(ptmisclib.out_ifnot(f"ASD\n", None, self.use_json), trim=False, end="")
                                printlock.add_string_to_output(ptmisclib.out_ifnot(f"{multiline_record[r_no][0]}{' '*(10-len(multiline_record[r_no][0]))}{multiline_record[r_no][1]}{' '*(10-len(multiline_record[r_no][1]))}{multiline_record[r_no][2]}{' '*(10-len(multiline_record[r_no][2]))}{' '.join(multiline_record[r_no])}", None, self.use_json), trim=False)
                                
                            #printlock.add_string_to_output(ptmisclib.out_ifnot(f"\n"))
                        data.append({"subdomain": str(name), "type": rdataset_type, "content": rdataset_data.lstrip()})
        return data

    def extract_subdomains(self, zone, printlock):
        data = []
        result_final = set()
        for name in zone.nodes.keys():
            result_final.add(str(name))
        result_final = list(result_final)
        result_final.sort()
        for name in result_final:
            if name == "@":
                continue
            data.append({"subdomain": str(name)})
            if not self.vulnerable_only:
                printlock.add_string_to_output(ptmisclib.out_ifnot(f"{str(name)}", None, self.use_json), trim=True)
        return data


def get_help():
    return [
        {"description": ["DNS Zone Transfer Testing Tool"]},
        {"usage": ["ptaxfr <options>"]},
        {"usage_example": ["ptaxfr -d example.com", "ptaxfr -d example1.com example2.com example3.com", "ptaxfr -f domain_list.txt"]},
        {"options": [
            ["-d",  "--domain",           "<domain>",   "Test domain"],
            ["-f",  "--file",             "<file>",     "Test domains from file"],
            ["-pd", "--print_dns",        "",           "Print DNS records (default option)"],
            ["-ps", "--print_subdomains", "",           "Print subdomains only"],
            ["-V",  "--vulnerable_only",  "",           "Print only vulnerable domains"],
            ["-s",  "--silent",           "",           "Silent mode (show result only)"],
            ["-t",  "--threads",          "<threads>",  "Number of threads (default 20)"],
            ["-j",  "--json",             "",           "Enable JSON output"],
            ["-v",  "--version",          "",           "Show script version and exit"],
            ["-h",  "--help",             "",           "Show this help message and exit"],
        ]}
    ]

def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    required = parser.add_argument_group("One of the following arguments is required")
    required = required.add_mutually_exclusive_group(required=True)
    required.add_argument("-d", "--domain", type=str, nargs="+")
    required.add_argument("-f", "--file", type=str)
    parser.add_argument("-pd", "--print_dns", action="store_true")
    parser.add_argument("-ps", "--print_subdomains", action="store_true")
    parser.add_argument("-V", "--vulnerable_only", action="store_true")
    parser.add_argument("-s", "--silent", action="store_true")
    parser.add_argument("-t", "--threads", type=int, default=20)
    parser.add_argument("-j", "--json", action="store_true")
    parser.add_argument("-v", "--version", action="version", version=f"{SCRIPTNAME} {__version__}")
    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        ptmisclib.help_print(get_help(), SCRIPTNAME, __version__)
        sys.exit(0)
    args = parser.parse_args()
    return args


def main():
    global SCRIPTNAME
    SCRIPTNAME = "ptaxfr"
    args = parse_args()
    script = ptaxfr(args)
    script.run(args)


if __name__ == "__main__":
    main()
