def start_styled_html(site_title: str):
    """
    :param site_title: string to be the title of the HTML page, the default is eqaul to no page name
    :return: string containing HTML content to start a styled site
    """
    if not isinstance(site_title, str):
        raise TypeError("input must be a string")

    html_start = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <title>""" + site_title + """</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Roboto'>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <style>
    html,body,h1,h2,h3,h4,h5,h6 {font-family: "Roboto", sans-serif; color: #a3978f}
    body {background-color: #f3f2f1;}
    table, th, td {color:#a3978f; border: 1px solid #a3978f; border-collapse: collapse; text-align: center}
    tr:nth-child(odd) {background-color: #f3f2f1;}
    tr:nth-child(even) {background-color: #f3f2f1;}
    </style>
    </head>
    <body class="w3-light-grey">

    <!-- Page Container -->
    <div class="w3-content w3-margin-top" style="max-width:1400px;">
    """
    return html_start


def start_basic_html(site_title: str):
    """
    :param site_title: string to be the title of the HTML page, the default is eqaul to no page name
    :return: string containing HTML content to start a basic site
    """
    if not isinstance(site_title, str):
        raise TypeError("input must be a string")

    html_start = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <title>""" + site_title + """</title>
    <body>
    """
    return html_start

def h1(text: str):
    """
    :param h1: string with text for HTML header
    :return:  string containing HTML header 1
    """
    if not isinstance(text, str):
        raise TypeError("input must be a string")
    local_text = ("""<h1>""" + text + """</h1>
    """)
    return local_text


def h2(text: str):
    """
    :param h2: string with text for HTML header
    :return:  string containing HTML header 2
    """
    if not isinstance(text, str):
        raise TypeError("input must be a string")
    local_text = ("""<h2>""" + text + """</h2>
    """)
    return local_text


def h3(text: str):
    """
    :param h3: string with text for HTML header
    :return:  string containing HTML header 3
    """
    if not isinstance(text, str):
        raise TypeError("input must be a string")
    local_text = ("""<h3>""" + text + """</h3>
    """)
    return local_text


def para(text: str):
    """
    :param para: string with text for HTML paragraph
    :return:  string containing HTML paragraph

    the function will automatically replace textual new lines with html syntax
    to display the text accordingly
    """
    if not isinstance(text, str):
        raise TypeError("input must be a string")
    local_text = ("""<p>""" + text + """</p>
    """)
    local_text = local_text.replace("\n", "</p><p>")  # replace textual new lines with html line breaks
    return local_text


def line_break():
    """
    :return:  string containing HTML content representing a line break
    """
    line_break = ("""<hr>
    """)
    return line_break


def end_styled_html():
    """
    :return: string containing html to end a styled html site
    """
    html_end = """
    </body>
    <!-- End Page Container -->
    </div>
    </html>"""
    return html_end


def np_matrix_as_table(np_array, headers=[], sides=[], size='50'):
    """
    :param array: numpy array to be displayed as a HTML table
    :param headers: table headers for columns, default is no headers
    :param sides: table headers for rows, default is no headers
    :param size: string to set realtive table size in percent standard 50%
    :return: string containing a html table
    """
    n_cols = np_array.shape[1]
    n_rows = np_array.shape[0]
    local_text = "<table style=\"width:"+size+"%\">"
    if headers != []:
        if sides != []:
            headers.insert(0, "-")
        local_text += "<tr>"
        for element in headers:
            local_text += "<th>"+element+"</th>"
        local_text += "</tr>"
    for i in range(n_rows):
        local_text += "<tr>"
        if sides != []:
            local_text += "<th>" + str(sides[i]) + "</th>"
        for j in range(n_cols):
            local_text += "<td>" + str(np_array[i][j]) + "</td>"
        local_text += "</tr>"
    local_text += "</table>"
    return local_text

def df_as_table(dataframe, size='50'):
    """
    :param dataframe: pandas dataframe to be displayed as a HTML table
    :param size: string to set realtive table size in percent standard 50%
    :return: string containing a html table
    """
    shape = dataframe.shape
    n_cols = shape[1]
    n_rows = shape[0]
    headers = list(dataframe.columns)
    sides = list(dataframe.index.values)
    local_text = "<table style=\"width:"+size+"%\">"
    if headers != []:
        if sides != []:
            headers.insert(0, "-")
        local_text += "<tr>"
        for element in headers:
            local_text += "<th>"+element+"</th>"
        local_text += "</tr>"
    for i in range(n_rows):
        local_text += "<tr>"
        if sides != []:
            local_text += "<th>" + str(sides[i]) + "</th>"
        for j in range(n_cols):
            local_text += "<td>" + str(dataframe.iloc[i][j]) + "</td>"
        local_text += "</tr>"
    local_text += "</table>"
    return local_text



def plotly_figure(figure, id: str):
    """
    :param figure: plotly graph object or px figure
    :param id: unique id string of format 'id_xxx' with x representin a number
    :return: html style string containing a plotly figure
    """
    json_figure = figure.to_json()
    html = """
        <div id="""+id+"""></div>
        <script>
            var plotly_data = {}
            Plotly.react("""+id+""", plotly_data.data, plotly_data.layout);
        </script>
    """
    local_text = html.format(json_figure)
    return local_text

def single_plotly_figure(site_title: str, figure):
    """
    :param figure: plotly graph object or px figure
    :return: html style string to generate a site from a single figure
    """
    if not isinstance(site_title, str):
        raise TypeError("input must be a string")

    json_figure = figure.to_json()
    html = """
        <div id="id_1"></div>
        <script>
            var plotly_data = {}
            Plotly.react("id_1", plotly_data.data, plotly_data.layout);
        </script>
    """
    graph_content = html.format(json_figure)

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <title>""" + site_title + """</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Roboto'>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <style>
    html,body,h1,h2,h3,h4,h5,h6 {font-family: "Roboto", sans-serif; color: #a3978f}
    body {background-color: #f3f2f1;}
    table, th, td {color:#e8e5e3; border: 1px solid black; border-collapse: collapse;}
    tr:nth-child(odd) {background-color: #990030;}
    tr:nth-child(even) {background-color: #a3978f;}
    </style>
    </head>
    <body class="w3-light-grey">

    <!-- Page Container -->
    <div class="w3-content w3-margin-top" style="max-width:1600px;">
    """
    html += graph_content
    html += """
    </body>
    <!-- End Page Container -->
    </div>
    </html>"""
    return html

def end_basic_html():
    """
    :return: html style string to end a basic html site
    """
    html = """
    </body>
    </html>
    """
    return html

def add_image_by_ref(reference: str, name: str, height: str, width: str):
    html="""
    <img src=\""""+reference+"""\" alt=\""""+name+"""\" style=\"width:"""+width+"""px;height:"""+height+"""px;\">
    """
    return html

def add_link(link: str, text: str):
    """
    :param link: string containing a web reference
    :param text: string containing text to be displayed on website
    :return htlm style string to add text with a link
    """
    html = """
    <a href=\""""+link+"""\">"""+text+"""</a>
    """
    return html
