# -*- coding: utf-8 -*-

import os
from simple_logging import logger
import consulate

session = consulate.Consul(host='consul.ynu.edu.cn', port=80, datacenter='ynu0', token='ae59ac81-8d99-adb6-08a3-14f07900576e', scheme='http')


# see more details on http://tools.ietf.org/html/rfc1035
class DNSRecord(object):
    DNS_CLASS_A = "A"
    DNS_CLASS_AAAA = "AAAA"
    DNS_CLASS_CNAME = "CNAME"
    DNS_CLASS_SUPPORT = [DNS_CLASS_A, DNS_CLASS_AAAA, DNS_CLASS_CNAME]

    def __init__(self, name, type, dns_class, value):
        self.name = name
        self.type = type
        self.dns_class = dns_class
        self.value = value

    def __str__(self):
        str = None
        if not self.dns_class in DNSRecord.DNS_CLASS_SUPPORT:
            str = "unsupport dns record parse class {dns_class}".format(dns_class=self.dns_class)
        else:
            str = "{name} ---{dns_class}---> {value}".format(name=self.name, dns_class=self.dns_class, value=self.value)
        return str


class ZoneFileParse(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.records = {}

    def parse(self):
        with open(self.file_path) as f:
            for line in f.readlines():
                line = line.strip()
                # blank line
                if line == "" or line.startswith(";"):
                    continue
                # start normal parse
                segements = line.split()
                if len(segements) != 4:
                    logger.error("parse error: %s", line)
                    continue
                # construct dns record
                record = DNSRecord(segements[0], segements[1], segements[2], segements[3])
                logger.debug("parsed record: %s", record)
                if not self.records.has_key(record.name):
                    self.records[record.name] = {}
                self.records[record.name][record.dns_class] = record.value

    def update_to_consul(self):
        for key, value in self.records.iteritems():
            # iteration for A records
            if DNSRecord.DNS_CLASS_A in value:
                logger.debug("update a record for %s->%s", key, value[DNSRecord.DNS_CLASS_A])
                session.kv['dns/A/{name}/comment'.format(name=key)] = 'itc build-initial-kv liudonghua initialization'
                session.kv['dns/A/{name}/name'.format(name=key)] = key
                session.kv['dns/A/{name}/ipv4'.format(name=key)] = value[DNSRecord.DNS_CLASS_A]
            # iteration for CNAME records
            elif DNSRecord.DNS_CLASS_CNAME in value:
                logger.debug("update cname record for %s->%s", key, value[DNSRecord.DNS_CLASS_CNAME])
                session.kv['dns/CNAME/{name}/comment'.format(name=key)] = 'itc build-initial-kv liudonghua initialization'
                session.kv['dns/CNAME/{name}/name'.format(name=key)] = key
                session.kv['dns/CNAME/{name}/canonical-name'.format(name=key)] = value[DNSRecord.DNS_CLASS_CNAME]



    def get_simple_ipv4_resolve(self):
        simple_ipv4_resolve = {}
        # First iteration for A records
        for key, value in self.records.iteritems():
            if DNSRecord.DNS_CLASS_A in value:
                logger.debug("find a record for %s->%s", key, value[DNSRecord.DNS_CLASS_A])
                simple_ipv4_resolve[key] = value[DNSRecord.DNS_CLASS_A]
        # Secord iteration for CNAME records
        for key, value in self.records.iteritems():
            if DNSRecord.DNS_CLASS_CNAME in value:
                # Find the final a relevant record
                intermedia_cname = []
                cname_record = self.records[key]
                found = True
                while DNSRecord.DNS_CLASS_CNAME in cname_record:
                    intermedia_cname.append(cname_record[DNSRecord.DNS_CLASS_CNAME])
                    try:
                        cname_record = self.records[cname_record[DNSRecord.DNS_CLASS_CNAME]]
                        if DNSRecord.DNS_CLASS_A in cname_record:
                            break
                    except:
                        found = False
                        logger.error(
                            "could not resolve cname record for %s->%s, for there is no such relevant a record",
                            key, value[DNSRecord.DNS_CLASS_CNAME])
                        break
                    else:
                        logger.debug("find intermedia cname record %s", cname_record)
                if found:
                    logger.debug("find cname record for %s->%s->%s", key, '->'.join(intermedia_cname),
                                 cname_record[DNSRecord.DNS_CLASS_A])
                    simple_ipv4_resolve[key] = cname_record[DNSRecord.DNS_CLASS_A]
        return simple_ipv4_resolve

    def save_simple_ipv4_records(self, save_file_path, simple_ipv4_records):
        with open(save_file_path, "w") as f:
            for key, value in simple_ipv4_records.iteritems():
                f.writelines("{key}\t{value}\n".format(key=key, value=value))


if __name__ == "__main__":
    file_path = "db.ynu.edu.cn.txt"
    zoneFileParse = ZoneFileParse(file_path)
    zoneFileParse.parse()
    zoneFileParse.update_to_consul()
    # simple_ipv4_records = zoneFileParse.get_simple_ipv4_resolve()
    # for key, value in simple_ipv4_records.iteritems():
    #     logger.info("%s->%s", key, value)
    # # save the result on a file for persist
    # zoneFileParse.save_simple_ipv4_records("parsed_file.txt", simple_ipv4_records)


