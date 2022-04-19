import os
import subprocess
import json
import pandas as pd
import argparse
#Simple script parse all hosts in the inventory file and export to csv
parser = argparse.ArgumentParser(description='Ansible inventory generator')
parser.add_argument("--ansible_hosts_dir", help="Location of anible inventory files")
parser.add_argument("--export_csv_dir", help="Location of export csv /path/to/file.csv", default="/tmp/inventory.csv")
args = parser.parse_args()

ansible_hosts_dir = args.ansible_hosts_dir
directory = os.fsencode(ansible_hosts_dir)
csv_out=args.export_csv_dir  
export_cols = ['ansible_host','external_ip','internal_ip','other_column_to_export']
if os.path.exists(csv_out):
    print('Removing old file')
    os.remove(csv_out)
else:
    print("Skip as file is not exist")

for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if not (filename.endswith(".yml") or filename.endswith(".yaml")): 
         out = subprocess.check_output(['ansible-inventory', '-i', ansible_hosts_dir + filename, '--list'],text=True)
         j = json.loads(out)
         df = pd.DataFrame(j['_meta']['hostvars']).T
         df = df.reindex(df.columns.union(export_cols, sort=False), axis=1, fill_value='n/a')
         print('Processing ',filename)
         if os.path.exists(csv_out):
            df.to_csv(csv_out,mode='a',columns=export_cols,header=False)
         else:
            df.to_csv(csv_out,columns=export_cols)
         
         continue
     else:
         continue