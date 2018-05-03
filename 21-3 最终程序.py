from urllib.request import urlopen
from reportlab.lib import colors
from reportlab.graphics.shapes import *
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics import renderPDF

data = []
URL = 'ftp://ftp.swpc.noaa.gov/pub/weekly/Predict.txt'
COMMENT_CHARS = '#:'

for line in urlopen(URL).readlines():
    line = line.decode()
    if not isspace(line) and not line[0] in COMMENT_CHARS:
        data.append([float(n) for n in line.split()])

print(data)

'''
import pprint
data = [
    (2007, 8,   113.2,  114.2, 112.2),
    (2007, 9,   112.8,  115.8, 109.8),
    (2007, 10,  111.0,  116.0, 106.0),
    (2007, 11,  109.8,  116.8, 102.8),
    (2007, 12,  107.3,  115.3, 99.3),
    (2008, 1,   105.2,  114.2, 96.2),
    (2008, 2,   104.1,  114.1, 94.1),
    (2008, 3,   99.9,   110.9, 88.9),
    (2008, 4,   94.8,   106.8, 82.8),
    (2008, 5,   91.2,   104.2, 78.2),
    ]
pprint.pprint(data)
'''

if __name__ == '__main__':
    drawing = Drawing(500, 250)

    pred = [row[2]-40 for row in data]      # 提取平均值
    high = [row[3]-40 for row in data]      # 提取最大值
    low  = [row[4]-40 for row in data]      # 提取最小值
    times = [row[0] + row[1]/12.0 for row in data]

    lp = LinePlot()
    lp.x = 50
    lp.y = 50
    lp.height = 125
    lp.width = 300
    lp.data = [list(zip(times, pred)), list(zip(times, high)), list(zip(times, low))]

    lp.lines[0].strokeColor = colors.blue
    lp.lines[1].strokeColor = colors.red
    lp.lines[2].strokeColor = colors.green

    drawing.add(lp)

    drawing.add(String(250, 150, 'Sunspots', fontSize = 14, fillColor = colors.red))

    renderPDF.drawToFile(drawing, 'report2.pdf', 'Sunspots')
