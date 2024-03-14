
import os
import glob
import json
import ROOT
from concurrent.futures import ThreadPoolExecutor

def analyze(datasetName, dataDict, basePath):
    print("START", datasetName)
    
    path = f"{basePath}/{dataDict['path']}"
    total_size = 0
    total_files = 0
    chain = ROOT.TChain("events")
    files = []
    
    filenames = glob.glob(f"{path}/*.root")
    for filename in filenames:
        filepath = os.path.join(path, filename)
        #total_size += os.path.getsize(filepath)
        total_files += 1
        #chain.Add(filepath)
        files.append(filepath)
    '''
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if not ".root" in filepath:
                continue
            total_size += os.path.getsize(filepath)
            total_files += 1
            chain.Add(filepath)
    '''
    js = f"{path}/meta.json"
    if os.path.isfile(path):
        f = open(js)
        d = json.load(f)
        total_size_ = d['total_size']
        total_files_ = d['total_files']
        total_events_ = d['total_events']
        if total_files_ == total_files:
            dataDict['total_size'] = total_size_
            dataDict['total_files'] = total_files_
            dataDict['total_events'] = total_events_
            print("DONE (meta available)", datasetName)
            return datasetName, dataDict

    for f in files:
        total_size += os.path.getsize(filepath)
        chain.Add(filepath)
    df = ROOT.ROOT.RDataFrame(chain)
    dataDict['total_size'] = total_size / 1024.0 / 1024.0 / 1024.0 # GB
    dataDict['total_files'] = total_files
    dataDict['total_events'] = df.Count().GetValue() #chain.GetEntries()
    print("DONE (meta parsed)", datasetName)
    with open(js, 'w') as fp:
        json.dump(dataDict, fp)
    return datasetName, dataDict


def export(datadict):

    table_rows = ""
    size_tot = 0.
    for d in datadict:
        name, ddict = d[0], d[1]
        tmp = [entry for entry in name.split("_") if entry.startswith("ecm")][0]
        ecm = float(tmp.replace("p", ".").replace("ecm", ""))
        if ecm < 100:
            cat = "Z"
        elif ecm > 100 and ecm < 200:
            cat = "WW"
        elif ecm > 200 and ecm < 300:
            cat = "Higgs"
        else:
            cat = "Top"
        size, nfiles, nevents = ddict['total_size'], ddict['total_files'], ddict['total_events']
        size_tot += size

        table_rows += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(name, cat, ddict['xsec'], size, nfiles, nevents, ddict['path'])

    # HTML template with the dynamic table rows
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FCCee samples at SubMIT</title>
        <!-- choose a theme file -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.31.3/css/theme.blue.css">
        <!-- load jQuery and tablesorter scripts -->
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.0/jquery.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.31.3/js/jquery.tablesorter.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.31.3/js/widgets/widget-math.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.31.3/js/widgets/widget-filter.min.js"></script>

        <style>
        body {{
            font: 12px Arial;
        }}
        table, th, td {{
            font: 12px Arial;
        }}
        </style>

        <script>

        $(function() {{
          $("#myTable").tablesorter({{
              theme: 'blue',
              delayInit: true,
              headers: {{ 2: {{ filter: false}} }},
              widgets: ['zebra', 'filter'],
              widgetOptions: {{
              }},
          }});
        }});

        </script>

    </head>
    <body>
        <h1>FCCee samples at SubMIT</h1>
        Storage path: /data/submit/cms/store/fccee/samples/winter2023/ <br />
        Total size: {} TB
        <table id="myTable" class="tablesorter">
            <thead>
                <tr>
                    <th data-placeholder="Name">Name</th>
                    <th data-placeholder="Name">Category</th>
                    <th data-placeholder="Cross-section (pb)">Cross-section (pb)</th>
                    <th data-placeholder="Size">Size (GB)</th>
                    <th data-placeholder="Size">Number of files</th>
                    <th data-placeholder="Size">Number of events</th>
                    <th data-placeholder="Path">Path</th>
                </tr>
            </thead>
            <tbody>
                {}
            </tbody>
        </table>
    </body>
    </html>
    """.format(size_tot/1024., table_rows)

    # Write the HTML content to a file
    with open('/home/submit/jaeyserm/public_html/fccee/samples.html', 'w') as file:
        file.write(html_content)


def main():

    dictPath = "/data/submit/cms/store/fccee/samples/winter2023/catalog.json"
    basePath = "/data/submit/cms/store/fccee/samples/winter2023/"
    f = open(dictPath)
    datadict = json.load(f)

    samples = glob.glob(f"{basePath}/IDEA/*") + glob.glob(f"{basePath}/IDEA_2E/*") + glob.glob(f"{basePath}/IDEA_3T/*") + glob.glob(f"{basePath}/CLD/*")

    with ThreadPoolExecutor(max_workers=64) as executor:
        futures = [executor.submit(analyze, d, datadict[d], basePath) for d in datadict.keys()]
        results = [future.result() for future in futures]

    export(results)


if __name__ == '__main__':
    main()