import xml.etree.ElementTree as ET
import datetime 
from xml.dom import minidom
import networkx as nx
import configparser
import math
import pkg_resources
from ipey.document import Document, Page
from ipey.primitive import Glyph, Line, Label, Arc, Spline, SplineType


class IpeOptions:

    def __init__(self, settings_path = None):
        config = configparser.ConfigParser()

        if settings_path:
            config.read(settings_path)
        else:
            settings = pkg_resources.resource_filename(__name__, 'static/settings.ini')
            config.read(settings)                                     
        
        self.__dict__['_IPE_VERSION'] = config['IPE']['VERSION']
        self.__dict__['_IPE_CREATOR'] = config['IPE']['CREATOR']
        
        self.__dict__['_DRAWING_UNBOUND'] = config.getboolean('DRAWING', 'UNBOUND')
        self.__dict__['_DRAWING_WIDTH'] = config.getfloat('DRAWING', 'WIDTH')
        self.__dict__['_DRAWING_HEIGHT'] = config.getfloat('DRAWING', 'HEIGHT')
        self.__dict__['_DRAWING_MARGIN'] = config.getfloat('DRAWING','MARGIN')
        self.__dict__['_DRAWING_FLIP_X'] = config.getboolean('DRAWING', 'FLIP_X')
        self.__dict__['_DRAWING_FLIP_Y'] = config.getboolean('DRAWING', 'FLIP_Y')
        self.__dict__['_DRAWING_USE_ARCS'] = config.getboolean('DRAWING', 'USE_ARCS')
        self.__dict__['_DRAWING_SNAP_TO_GRID'] = config.getboolean('DRAWING', 'SNAP_TO_GRID')
        self.__dict__['_DRAWING_GRID_SIZE'] = config.getint('DRAWING', 'GRID_SIZE')
        self.__dict__['_DRAWING_ARC_FACTOR'] = config.getfloat('DRAWING','ARC_FACTOR')

        self.__dict__['_VERTEX_GLYPH'] = config['VERTEX']['GLYPH']
        self.__dict__['_VERTEX_STROKE'] = config['VERTEX']['STROKE']
        self.__dict__['_VERTEX_FILL'] = config['VERTEX']['FILL']
        self.__dict__['_VERTEX_SIZE'] = config['VERTEX']['SIZE']

        self.__dict__['_EDGE_PEN'] = config['EDGE']['PEN']        
        self.__dict__['_EDGE_STROKE'] = config['EDGE']['STROKE']     

        self.__dict__['_LABEL_VALIGN'] = config['LABEL']['VALIGN']
        self.__dict__['_LABEL_HALIGN'] = config['LABEL']['HALIGN']
        self.__dict__['_LABEL_SIZE'] = config['LABEL']['SIZE']
        self.__dict__['_LABEL_STROKE'] = config['LABEL']['STROKE']
        self.__dict__['_LABEL_ISMATH'] = config.getboolean('LABEL', 'MATH')
        self.__dict__['_LABEL_OFFSET_X'] = config.getfloat('LABEL', 'OFFSET_X')
        self.__dict__['_LABEL_OFFSET_Y'] = config.getfloat('LABEL', 'OFFSET_Y')


        self.__dict__['_GRAPH_DIRECTED'] = config.getboolean('GRAPH', 'DIRECTED')
       

class IpeConverter:

    def __init__(self, settings_path = None, styles = []):
        self._options = IpeOptions(settings_path)
        self._styles = styles

    def createDrawing(self, G, path):
        G = G.copy()

        self.scaleGraph(G)

        document = Document(styles=self._styles)
        page = document.createPage()

        self.drawEdges(page, G)
        self.drawNodes(page, G)
        self.drawNodeLabels(page, G)
        self.drawEdgeLabels(page, G)

        if not self._options._DRAWING_UNBOUND:
            document.crop = True

        document.write(path)



    def drawNodes(self, page : Page, G):
        for n, data in G.nodes(data=True):

            if 'Glyph' in data:
                glyph = data['Glyph']
            else:
                glyph = self._options._VERTEX_GLYPH

            node = Glyph((data['X'], data['Y']), type = glyph)
            
            if 'Size' in data:
                node.size = data['Size']
            else:
                node.size = self._options._VERTEX_SIZE

            if 'Fill' in data:
                node.fill = data['Fill']
            else:
                node.fill = self._options._VERTEX_FILL

            if 'Stroke' in data:
                node.stroke = data['Stroke']
            else:
                node.stroke = self._options._VERTEX_STROKE

            if 'Layer' in data:
                node.layer = data['Layer']
            else:
                node.layer = 'nodes'

            page.add(node)

    def drawEdges(self, page, G):
        for u, v, data in G.edges(data=True):
            x1 = G.nodes[u]['X']
            y1 = G.nodes[u]['Y']
            x2 = G.nodes[v]['X']
            y2 = G.nodes[v]['Y']

            if 'Spline' in data:
                spline = data['Spline']
                if type(spline) == SplineC:
                    points = [(x1, y1)]
                    points.extend(spline.points)
                    points.append((x2, y2))
                    edge = Spline(points, spline.type)
            elif self._options._DRAWING_USE_ARCS:
                xx = x1 - x2
                yy = y1 - y2
                cx = (x1+x2)/2
                cy = (y1+y2)/2
                l = math.sqrt(xx**2 + yy**2)
                nx = xx / l
                ny = yy / l
                px = -ny
                py = nx

                p3x = cx + px * self._options._DRAWING_ARC_FACTOR * l
                p3y = cy + py * self._options._DRAWING_ARC_FACTOR * l
                edge = Arc((x1,y1), (p3x, p3y), (x2,y2))
            else:
                points = [(x1,y1), (x2,y2)]
                edge = Line(points)
            
            
            if 'Stroke' in data:
                edge.stroke = data['Stroke']
            else:
                edge.stroke = self._options._EDGE_STROKE


            if 'Pen' in data:
                edge.pen = data['Pen']
            else:
                edge.pen = self._options._EDGE_PEN


            if 'Layer' in data:
                edge.layer = data['Layer']
            else:
                edge.layer = 'edges'

            if self._options._GRAPH_DIRECTED:
                edge.arrow = 'normal/normal'

            page.add(edge)

    def drawNodeLabels(self, page, G):

        for n, data in G.nodes(data=True):
            if 'Label' in data:
                offset_x = self._options._LABEL_OFFSET_X
                offset_y = self._options._LABEL_OFFSET_Y
                if 'Label_Offset_X' in data:
                    offset_x = data['Label_Offset_X']
                if 'Label_Offset_Y' in data:
                    offset_y = data['Label_Offset_Y']

                x = offset_x + data['X']
                y = offset_y + data['Y']

                label = Label(data['Label'], (x,y))

                label.stroke = self._options._LABEL_STROKE
                label.vAlign = self._options._LABEL_VALIGN
                label.hAlign = self._options._LABEL_HALIGN
                label.isMath = self._options._LABEL_ISMATH
                label.size = self._options._LABEL_SIZE
                label.layer = 'node_labels'

                page.add(label)
    
    def drawEdgeLabels(self, page, G):
        for u, v, data in G.edges(data=True):
            if 'Label' in data:
                x1 = G.nodes[u]['X']
                y1 = G.nodes[u]['Y']
                x2 = G.nodes[v]['X']
                y2 = G.nodes[v]['Y']

                if 'Spline' in data:
                    spline = data['Spline']
                    if type(spline) == SplineC:
                        if len(spline.points) < 1:
                            lx = (x1 + x2) / 2
                            ly = (y1 + y2) / 2
                        else:
                            lx = spline.points[int(len(spline.points) / 2)][0]
                            ly = spline.points[int(len(spline.points) / 2)][1]
                elif self._options._DRAWING_USE_ARCS:
                    xx = x1 - x2
                    yy = y1 - y2
                    cx = (x1+x2)/2
                    cy = (y1+y2)/2
                    l = math.sqrt(xx**2 + yy**2)
                    nx = xx / l
                    ny = yy / l
                    px = -ny
                    py = nx

                    lx = cx + px * self._options._DRAWING_ARC_FACTOR * l
                    ly = cy + py * self._options._DRAWING_ARC_FACTOR * l
                else:
                    lx = (x1 + x2) / 2
                    ly = (y1 + y2) / 2

                label = Label(data['Label'], (lx, ly))

                page.add(label)


    def scaleGraph(self, G):
        '''
        Scale the graph to be either in the range [0, xmax], [0, ymax] or [0, width],[0, height].
        '''
        minX = 100000
        maxX = -100000
        minY = 100000
        maxY = -100000  
        for n, data in G.nodes(data=True):
            if not ('X' in data and 'Y' in data):
                raise Exception(f'Coordinate missing for {n}')

            data['X'] = float(data['X'])
            data['Y'] = float(data['Y'])

            if data['X'] < minX: minX = data['X']
            if data['Y'] < minY: minY = data['Y']
            if data['X'] > maxX: maxX = data['X']
            if data['Y'] > maxY: maxY = data['Y']

        if self._options._DRAWING_FLIP_X:
            for n, data in G.nodes(data=True):
                data['X'] = maxX - data['X']
        if self._options._DRAWING_FLIP_Y:
            for n, data in G.nodes(data=True):
                data['Y'] = maxY - data['Y']

        if self._options._DRAWING_SNAP_TO_GRID:
            data['X'] = round(data['X'] / self._options._DRAWING_GRID_SIZE) * self._options._DRAWING_GRID_SIZE
            data['Y'] = round(data['Y'] / self._options._DRAWING_GRID_SIZE) * self._options._DRAWING_GRID_SIZE


    def findCircle(self, x1, y1, x2, y2, x3, y3):
        x12 = x1 - x2
        x13 = x1 - x3
    
        y12 = y1 - y2
        y13 = y1 - y3
    
        y31 = y3 - y1
        y21 = y2 - y1

        x31 = x3 - x1
        x21 = x2 - x1
    
        # x1^2 - x3^2
        sx13 = pow(x1, 2) - pow(x3, 2)
    
        # y1^2 - y3^2
        sy13 = pow(y1, 2) - pow(y3, 2)
    
        sx21 = pow(x2, 2) - pow(x1, 2)
        sy21 = pow(y2, 2) - pow(y1, 2)
    
        f = (((sx13) * (x12) + (sy13) * (x12) + (sx21) * (x13) + (sy21) * (x13)) // (2 * ((y31) * (x12) - (y21) * (x13))))
                
        g = (((sx13) * (y12) + (sy13) * (y12) + (sx21) * (y13) + (sy21) * (y13)) // (2 * ((x31) * (y12) - (x21) * (y13))))
    
        c = (-pow(x1, 2) - pow(y1, 2) - 2 * g * x1 - 2 * f * y1)
    
        # eqn of circle be x^2 + y^2 + 2*g*x + 2*f*y + c = 0
        # where centre is (h = -g, k = -f) and
        # radius r as r^2 = h^2 + k^2 - c
        cx = -g
        cy = -f
        sqr_of_r = cx**2 + cy ** 2 - c
    
        # r is the radius
        r = math.sqrt(sqr_of_r)
    
        return cx, cy, r


class SplineC:

    def __init__(self, points = [], type = SplineType.BSPLINE):
        self.points = points
        self.type = type

    