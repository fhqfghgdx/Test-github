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
    if not line.isspace() and not line[0] in COMMENT_CHARS:
        data.append([float(n) for n in line.split()])

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

    drawing.add(String(180, 200, 'Sunspots', fontSize = 14, fillColor = colors.red))

    renderPDF.drawToFile(drawing, 'report3.pdf', 'Sunspots')
