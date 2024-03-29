from __future__ import print_function
from virus_total_apis import PublicApi as VirusTotalPublicApi
import argparse
import sys
import json
import time
import os
import re
import zipfile
DATEANDTIME = time.strftime("%d%m%Y%H%M%S")
Konum = os.path.dirname(os.path.abspath(__file__))

def str_to_file(text, filename):
    output = open(filename, "w")
    output.write(text)
    output.close()

beginning = ''' This tool generates HTML reports by comparing hashes from the VirusTotal database. \n Example Usage: checker.py Source_ioc_List.txt'''
show = argparse.ArgumentParser(description=beginning)
#show.add_argument("-hash", "--hash", type=str, help='Hash turu (md5, MD5, sha1, SHA1, sha256,SHA256)')
show.add_argument("file", type=str, help='IoC Listesi (txt dosyasi)')



ibrhm = show.parse_args()

#VirusTotal API Degerini Buraya Giriniz.
virustotal = VirusTotalPublicApi('622e109677c759071b58a9f0fcc4583026812ed3f4500e9b671cbfc30fd190f3')

dashboard_mesaj = '''
  __  __       _                           _____ _               _             
 |  \/  |     | |                         / ____| |             | |            
 | \  / | __ _| |_      ____ _ _ __ ___  | |    | |__   ___  ___| | _____ _ __ 
 | |\/| |/ _` | \ \ /\ / / _` | '__/ _ \ | |    | '_ \ / _ \/ __| |/ / _ \ '__|
 | |  | | (_| | |\ V  V / (_| | | |  __/ | |____| | | |  __/ (__|   <  __/ |   
 |_|  |_|\__,_|_| \_/\_/ \__,_|_|  \___|  \_____|_| |_|\___|\___|_|\_\___|_|   
                    
                   Malware Checker (VirusTotal) V1.0
         
                    DevOps Engineer: Uros Orolicki                                                                   
                                                                               
'''
print(dashboard_mesaj)
blglu = open(sys.argv[1])
lines = blglu.readlines()
print("Scan Started...Creating HTML Report...\n\n")

print("|-------------------------------------------------|")
print("|            ## Quick View Result ##              |")
print("|-------------------------------------------------|\n")

zip_file_name = 'src/file.ibaloglu'
zip_core = zipfile.ZipFile(zip_file_name)
zip_core.extractall(r'.')



rapor_adi=Konum+"/Report_"+DATEANDTIME+".html"
myFile= open(rapor_adi, 'w+')
html_baslangic = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Malware Checker Report</title>
    <link rel="stylesheet" href="theme_scripts/bootstrap.css">
    <link rel="stylesheet" href="theme_scripts/dataTables.bootstrap4.min.css">
    <link rel="stylesheet" href="theme_scripts/buttons.bootstrap4.min.css">
    <link rel="stylesheet" href="theme_scripts/responsive.bootstrap4.min.css">
</head>
<body>
<br><b><center style="font-size: 33px;">Malware Checker Report</center></b><br>
<style>

.footer {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  background-color: #42A5F5;
  color: white;
  text-align: center;
}
</style>
    <table id="example" class="table table-striped table-bordered dt-responsive nowrap" style="width:100%">

 <thead>
            <tr>
                <th>Type</th>
                <th>IoC</th>
                <th>Kaspersky</th>
                <th>Symantec</th>
                <th>Score</th>
                <th>Scanned Date</th>
                <th>Detail Url</th>
            </tr>
        </thead>
<tbody>
            <tr><td>


"""

def validip(ip):
    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    if(re.search(regex, ip)):
        return True
sayac=0

myFile.write(html_baslangic)
for line in lines:

    ip_true=0
    hash_true=0
    Domain_true=0
    


    if validip(line):
        #print(line + " -> IP Adresi")
        ip_check= virustotal.get_ip_report(str(line).replace("\n",""))
        json_data = json.loads(json.dumps(ip_check))
        data=str(line).replace("\n","")
        type_url=data
        ip_true=1
        time.sleep(15)

    valid_Domain= re.finditer(r'(((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*)', line)
    valid_Domain_check = [match.group(1) for match in valid_Domain]

    if valid_Domain_check:
        Domain_check= virustotal.get_url_report(str(line).replace("\n",""))
        json_data = json.loads(json.dumps(Domain_check))
        data=str(line).replace("\n","")
        type_url=data
        Domain_true=1
        time.sleep(15)

    validHash_MD5 = re.finditer(r'(?=(\b[A-Fa-f0-9]{32}\b))', line)
    MD5_check = [match.group(1) for match in validHash_MD5]
    if MD5_check:
        hash_type_report="MD5"

    validHash_SHA1 = re.finditer(r'(?=(\b[0-9a-f]{40}\b))', line)
    SHA1_check = [match.group(1) for match in validHash_SHA1]
    if SHA1_check:
        hash_type_report="SHA1"

    validHash_SHA256 = re.finditer(r'(?=(\b[A-Fa-f0-9]{64}\b))', line)
    SHA256_check = [match.group(1) for match in validHash_SHA256]
    if SHA256_check:
        hash_type_report="SHA256"

    if MD5_check or SHA1_check or SHA256_check:
        hash_check = virustotal.get_file_report(line)
        json_data = json.loads(json.dumps(hash_check))
        data=str(line).replace("\n","")
        type_url=data
        hash_true=1
        time.sleep(15)

    

    sayac+=1



    if str(json_data['response_code'])=='204':
        print(" \n There was a problem connecting to Virustotal. Please restart scanning.")
        break
    else:
        try:
            if hash_true==1:
                if json_data['results']['response_code'] == 1 and json_data['results']['positives']>0:
                            
                            myFile.write(hash_type_report+'</td><td>')
                            myFile.write(data)
                            myFile.write('</td><td>')
                            if 'Kaspersky' in json_data['results']['scans']:
                                myFile.write(str(json_data['results']['scans']['Kaspersky']['result']))
                            else:
                                myFile.write("Hash Not Found!")

                            myFile.write('</td><td>')
                            if 'Symantec' in json_data['results']['scans']:
                                 myFile.write(str(json_data['results']['scans']['Symantec']['result']))
                            else:
                                myFile.write("Hash Not Found!")
                            myFile.write('</td><td>')
                            myFile.write(str(json_data['results']['positives']))
                            print("[", sayac, "]", data, " Detected. Skor: [ ",str(json_data['results']['positives'])," ]")
                            myFile.write('</td><td>')
                            myFile.write(json_data['results']['scan_date'])
                            myFile.write('</td><td>')
                            myFile.write(' <a href="https://www.virustotal.com/gui/file/%s/details" target="_blank"> <button class ="btn btn-secondary buttons-pdf buttons-html5" tabindex="0" aria-controls="example" type="button" > <span>Click</span> </button> </a>' % type_url)
                            myFile.write('</td></tr><tr><td>')

                elif json_data['results']['response_code'] == 1 and json_data['results']['positives'] == 0:
                    
                    try:
                        myFile.write(hash_type_report+'</td><td>')
                        myFile.write(data)
                        myFile.write('</td><td>N/A</td><td>N/A</td><td>0</td><td>'+json_data['results']['scan_date']+'</td><td>')
                        myFile.write(' <a href="https://www.virustotal.com/gui/file/%s/details" target="_blank"> <button class ="btn btn-secondary buttons-pdf buttons-html5" tabindex="0" aria-controls="example" type="button" > <span>Click</span> </button> </a>' % type_url)
                        myFile.write('</td></tr><tr><td>')
                    except:
                        pass
                else:
                    try:
                        myFile.write(hash_type_report+'</td><td>')
                        myFile.write(data)
                        myFile.write('</td><td>Hash Not Found!</td><td>Hash Not Found!</td><td>N/A</td><td>N/A</td><td>N/A</td></tr><tr><td>')
                    except:
                        pass

            
            elif ip_true==1:

                if str(json_data['results']['detected_urls']) =="[]":

                        myFile.write("IPv4</td><td>")                        
                        myFile.write(data)
                        myFile.write('</td><td>--</td><td>--</td><td>0</td><td>--</td><td>')
                        myFile.write(' <a href="https://www.virustotal.com/gui/ip-address/%s/details" target="_blank"> <button class ="btn btn-secondary buttons-pdf buttons-html5" tabindex="0" aria-controls="example" type="button" > <span>Click</span> </button> </a>' % type_url)
                        myFile.write('</td></tr><tr><td>')
                        pass

                elif json_data['results']['response_code'] == 1 and json_data['results']['detected_urls'][0]['positives']>0:

                            myFile.write("IPv4</td><td>")
                            myFile.write(data)
                            myFile.write('</td><td>--</td><td>--</td><td>'+str(json_data['results']['detected_urls'][0]['positives'])+"</td><td>"+json_data['results']['detected_urls'][0]['scan_date']+"</td><td>")
                            print("[", sayac, "]", data, " Detected. Skor: [ ",str(json_data['results']['detected_urls'][0]['positives'])," ]")
                            myFile.write(' <a href="https://www.virustotal.com/gui/ip-address/%s/details" target="_blank"> <button class ="btn btn-secondary buttons-pdf buttons-html5" tabindex="0" aria-controls="example" type="button" > <span>Click</span> </button> </a>' % type_url)
                            myFile.write('</td></tr><tr><td>')

            elif Domain_true==1:
                
                
                if json_data['results']['response_code'] ==0:
                    myFile.write("URL</td><td>")                        
                    myFile.write(data)
                    myFile.write('</td><td>--</td><td>--</td><td>Domain Not Found!</td><td>--</td><td>')
                    myFile.write('N/A')
                    myFile.write('</td></tr><tr><td>')
                    pass

                elif json_data['results']['response_code'] == 1 and json_data['results']['positives'] == 0:

                    myFile.write("URL</td><td>")                        
                    myFile.write(data)
                    myFile.write('</td><td>--</td><td>--</td><td>0</td><td>'+json_data['results']['scan_date']+'</td><td>')
                    myFile.write(' <a href="%s" target="_blank"> <button class ="btn btn-secondary buttons-pdf buttons-html5" tabindex="0" aria-controls="example" type="button" > <span>Click</span> </button> </a>' % json_data['results']['permalink'])
                    myFile.write('</td></tr><tr><td>')

                elif json_data['results']['response_code'] == 1 and json_data['results']['positives']>0:

                    myFile.write("URL</td><td>")
                    myFile.write(data)
                    myFile.write('</td><td>--</td><td>--</td><td>'+str(json_data['results']['positives'])+"</td><td>"+json_data['results']['scan_date']+"</td><td>")
                    print("[", sayac, "]", data, " Detected. Skor: [ ",str(json_data['results']['positives'])," ]")
                    myFile.write(' <a href="%s" target="_blank"> <button class ="btn btn-secondary buttons-pdf buttons-html5" tabindex="0" aria-controls="example" type="button" > <span>Click</span> </button> </a>' % json_data['results']['permalink'])
                    myFile.write('</td></tr><tr><td>')



            hash_type_report=""

            
        except:
            pass

blglu.close()
if str(json_data['response_code'])!='204':
    print("\n Reported Success. \n Report File Path: ", rapor_adi," ")
html_bitir = """
</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
 </tbody>
    </table>
<br><br><br><div class="footer">
  <p>Copyright &copy; 2020 Malware Checker (VirusTotal)  |   Developer: <a href="http://www.ananas.rs" target="_blank" style=" text-decoration: none;color: white;">Uros Orolicki</a></p>
</div>

<script src="theme_scripts/jquery-3.3.1.js"></script>
    <script src="theme_scripts/jquery.dataTables.min.js"></script>
    <script src="theme_scripts/dataTables.bootstrap4.min.js"></script>
    <script src="theme_scripts/dataTables.buttons.min.js"></script>
    <script src="theme_scripts/buttons.bootstrap4.min.js"></script>
    <script src="theme_scripts/jszip.min.js"></script>
    <script src="theme_scripts/pdfmake.min.js"></script>
    <script src="theme_scripts/vfs_fonts.js"></script>
    <script src="theme_scripts/buttons.html5.min.js"></script>
    <script src="theme_scripts/buttons.print.min.js"></script>
    <script src="theme_scripts/buttons.colVis.min.js"></script>
    <script src="theme_scripts/dataTables.responsive.min.js"></script>
    <script src="theme_scripts/responsive.bootstrap4.min.js"></script>
    <script>
    $(document).ready(function() {
        var table = $('#example').DataTable( {
            lengthChange: false,
            buttons: [ 'copy', 'excel', 'csv', 'pdf', 'colvis' ]
        } );
     
        table.buttons().container()
            .appendTo( '#example_wrapper .col-md-6:eq(0)' );
    } );
     </script>
</body>
</html>
 """
myFile.write(html_bitir)
