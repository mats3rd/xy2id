import sys
import re
import csv
from sympy.geometry import Point, Polygon

PID = []        # Product ID
PDummy = []     # Dummy info for the product
PPoly = []      # Polygon data for the product



def main():
    argv = sys.argv
    argc = len(argv)

    # Usage...
    if (argc != 3):
        print("    Usage: # python xy2id.py <Polygon+ID.csv> <points.csv>")
        print()
        quit()

#    xy2id("用賀_View.txt", "用賀_IN.txt")      #DEBUG
    xy2id("ProdView2ID.txt", "用賀_IN.txt")    #DEBUG


def readCameraView(fname):              # Read camera view file to setup PID[]/PDummy[]/PPoly[]
    with open(fname, 'r', encoding="ShiftJIS") as f:
        reader = csv.reader(f, delimiter='\t', quotechar='"')

        row = next(reader)              # Camera name
        row = next(reader)              # Date
        row = next(reader)              # Memo
        row = next(reader)              # Image W/H
        row = next(reader)              # Header

        points = []
        for row in reader:
            if row[2] == "":
                break
            PID.append(row[0])                  # ID[]
            PDummy.append(row[1])               # Dummy[]
            row = row[2:]
            points.clear()
            for pos in row:
                pos = pos.strip('()"\n')
                if (pos != ""):
                    xy = re.split(",", pos)
                    points.append(Point(int(xy[0]), int(xy[1])))
            PPoly.append(Polygon(*points))      # Polygon[]


def getIDfromPosition(point, polygons, ids):    # Returns polygon ID which includes the specified point
    i = 0
    pid = "<no match found>"
    for poly in polygons:                       # for each polygon
        if poly.encloses_point(point) == True:  # YES!  Inside the polygon!
            pid = ids[i]
            break
        i = i + 1
    return pid



def addPIDtoOperationFile(fname):           # Read operation file and add PID based on XY
    with open(fname, 'r', encoding="ShiftJIS") as f:
        reader = csv.reader(f, delimiter='\t', quotechar='"')

        # next(reader)      # Header?

        for row in reader:
            pos = row[1]                                                            #CSV次第！
            pos = pos.strip('()"\n')
            xy = re.split(",", pos)
            point = Point(int(xy[0]), int(xy[1]))

            pid = getIDfromPosition(point, PPoly, PID)

            #row = row + pid
            print("\t", point, "\t", pid)                                           #出力方法要検討
        print("...done!")


def xy2id(fnameView, fnameIN):

    # Init
    PID.clear()
    PDummy.clear()
    PPoly.clear()

    readCameraView(fnameView)           # Setup PID[]/PDummy[]/PPoly[]

    addPIDtoOperationFile(fnameIN)      # Append PID into the Operation file





if __name__ == "__main__":
    main()
