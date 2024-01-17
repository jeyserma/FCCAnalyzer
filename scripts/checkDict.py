
import os
import glob
import json


def get_directory_size(path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size


def export(datadict, basePath):

    table_rows = ""
    size_tot = 0.
    for d in datadict:
        tmp = [entry for entry in d.split("_") if entry.startswith("ecm")][0]
        ecm = float(tmp.replace("p", ".").replace("ecm", ""))
        if ecm < 100:
            cat = "Z"
        elif ecm > 100 and ecm < 200:
            cat = "WW"
        elif ecm > 200 and ecm < 300:
            cat = "Higgs"
        else:
            cat = "Top"
        size = get_directory_size(basePath + datadict[d]['path']) / 1024.0 / 1024.0 / 1024.0 # GB
        size_tot += size

        table_rows += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(d, cat, datadict[d]['xsec'], size, datadict[d]['path'])

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
    
    
    for datasetName in datadict:
        if not os.path.isdir(f"{basePath}/{datadict[datasetName]['path']}"):
            print(f"Directory {datadict[datasetName]['path']} does not exist")
    
    samples = [s.split("/")[-1] for s in samples]
    for s in samples:
        if not s in datadict:
            print(f"Datadict entry {s} does not exist")

    export(datadict, basePath)

if __name__ == '__main__':
    main()