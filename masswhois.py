#!/usr/bin/python
import pythonwhois;
import argparse;
import sys;

def pick_name(whois_info):
  try:
    return whois_info['contacts']['admin']['name'];
  except:
    try:
      return whois_info['contacts']['registrant']['name'];
    except:
      return "unknown";

def pick_registrar(whois_info):
  try:
    return whois_info['registrar'][0];
  except:
    return "unknown";

def lookup_domain_list(domain_list):
  whois_results=[];

  for dns_name in domain_list:
    try:
      dns_name = dns_name.strip();
      if len(dns_name)>0:
        print("Looking up:\"" + dns_name + "\"");
        whois_info = pythonwhois.get_whois(dns_name);
        assoc_name=pick_name(whois_info).replace(',','.');
        registrar=pick_registrar(whois_info).replace(',','.');

        whois_results.append([dns_name, registrar, assoc_name,whois_info['updated_date'][0].isoformat(' ')]);
    except:
      print("Error looking up:" +dns_name);

  for dns_list in whois_results:
    sys.stdout.write("%s\n" %(",".join(map(str,dns_list))))
	

def main(argv):


  parser = argparse.ArgumentParser();
  parser.add_argument('-i', '--infile', default='');
  args = parser.parse_args();


  domain_list='';
  if vars(args)['infile'] == '':
    domain_list=sys.stdin;
  else:
    f=open(vars(args)['infile']);
    domain_list=f.readlines();

  lookup_domain_list(domain_list);


if __name__ == "__main__":
  main(sys.argv[1:]);
