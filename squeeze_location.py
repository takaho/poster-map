import os, sys, re, argparse
import json
import pandas as pd
import shutil
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_path', default='public/data', type=str, required=True)
    parser.add_argument('-o', '--output_path', default='public/shinagawa', required=True)
    parser.add_argument('--region', type=str, default='品川区')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path
    verbose = args.verbose
    region = args.region
    
    if os.path.abspath(input_path) == os.path.abspath(output_path):
        raise Exception('input and output is identical')

    blockdir = os.path.join(input_path, 'block')
    dstdir = os.path.join(output_path, 'block')
    os.makedirs(dstdir, exist_ok=1)
    for fn in os.listdir(blockdir):
        if fn.endswith('.json') is False: continue
        with open(os.path.join(blockdir, fn)) as fi, open(os.path.join(dstdir, fn), 'w') as fo:
            blockdata = json.load(fi)
            sout = []
            for bd in blockdata:
                if bd['area_id'] == 8:
                    bd['status'] = 0
                    sout.append(bd)
                pass
            json.dump(sout, fo, indent=2)


    data = pd.read_csv(os.path.join(input_path, 'all.csv'))
    data['status'] = 0
    sub = data[data['area']==region]
    sub.to_csv(os.path.join(output_path, 'all.csv'))
    with open(os.path.join(output_path, 'all.json'), 'w') as fo:
        shinagawa = []
        sub = sub[['name', 'lat', 'long', 'status', 'note']]
        for row in sub.values:
            shinagawa.append({'area_id':8, 'name':row[0], 'lat':row[1], 'long':row[2], 'status':row[3], 'note':row[4]})
        json.dump(shinagawa, fo, indent=4)

    sub = {}    
    with open(os.path.join(input_path, 'arealist.json')) as fi:
        obj = json.load(fi)
        for key, val in obj.items():
            if val['area_name'] == region:
                sub[key] = val
        with open(os.path.join(output_path, 'arealist.json'), 'w') as fo:
            json.dump(sub, fo, indent=4)

    with open(os.path.join(input_path, 'vote_venue.json')) as fi:
        obj = json.load(fi)
        sub = []
        for elem in obj:
            if elem['address'].find(region) >= 0:
                sub.append(elem)
                print(elem)
        with open(os.path.join(output_path, 'vote_venue.json'), 'w') as fo:
            json.dump(sub, fo, indent=4)
    for name in ('summary.json', 'summary_absolute.json'):
        shutil.copy(os.path.join(input_path, 'vote_venue.json'),
                    os.path.join(output_path, 'vote_venue.json'))
    

if __name__ == '__main__':
    main()