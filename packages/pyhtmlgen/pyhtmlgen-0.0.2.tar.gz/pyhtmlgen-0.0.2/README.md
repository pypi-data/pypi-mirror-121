# pyhtml
pyhtml is a little toolbox which allows you to write html content within your
python script into a variable. This variable then can be saved to a .html file
and be opened with any standard browser.

## Where to get it
```sh
# PyPI
pip install pyhtmlgen
```

## supported html objects
* h1, h2, h3
* paragraphs
* line breaks
* tables
* links
* pictures

## supported python objects
* strings
* numpy matrices
* pandas dataframes
* plotly figures

## How to use
* wothin your python code create a variable to store a string
* use generators.start('Title of your page') to add the html head
* add content as needed using the other functions
* use generators.end() to close the html file correctly
* write the variable to a file

Have a look at the example.py script for more information on GitHub https://github.com/danvran/pyhtmlgen
