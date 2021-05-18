# открываем файл
import ovito.modifiers as md
import logging
import ovito
import math
import ovito.vis as vis
import math
import numpy as np
from ovito.io import import_file
from ovito.data import *
from ovito.pipeline import *


import matplotlib
matplotlib.use('Agg') # Activate 'agg' backend for off-screen plotting.
import matplotlib.pyplot as plt
import PySide2.QtGui


# pipeline = import_file("short.xyz")
pipeline = import_file("coords.lammpstrj")
# Инициализируем вывод log файла. Необязательно
logging.basicConfig(
    filename="log.txt", level=logging.INFO)
# Модифицируем нашу загруженную систему






arr = []
with open("rdf.txt") as f:
    for line in f:
        if line.split()[0]=='#': continue 
        #print(float(x) for x in coloumn.split())
        arr.append(line.split())

'''
bbonds = []
with open("bonds.txt") as f:
    for line in f:
        if line.split()[0]=='#': continue 
        #print(float(x) for x in coloumn.split())
        bbonds.append([int(line.split()[0]) -1, int(line.split()[1])-1])
'''
pipeline.add_to_scene()
# Меняем цвет и размер ионов и электронов по RGB.
# (Создаем функцию для замены)

data0 = pipeline.compute(0)
wall = data0.cell[0][0]
a = (wall**3.0 / 4000.0);

def modifier_color_radius(frame, data):
    color_property = data.particles_.create_property("Color")
    radius_property = data.particles_.create_property("Radius")
    transparency_property = data.particles_.create_property("Transparency")
    type_property = data.particles['Particle Type']
    id_property = data.particles['Particle Identifier']
    id_property0 = data0.particles['Particle Identifier']
    print(frame)
    for i in range(len(id_property)):
        if type_property[i] == 2:
            color_property.marray[i] = (1, 0, 0)
            radius_property.marray[i] = 0.9
        else:
            color_property.marray[i] = (0, 0, 1)
            radius_property.marray[i] = 0.3


def modify_bonds(frame, data):
    #bond_topology = [[0,1], [1,2], [2,0], [2, 5], [50, 100]]
    data.particles_.bonds = Bonds()
    data.particles_.bonds.create_property('Topology', data=bbonds)




    bond_topology = data.particles.bonds.topology  # array with bond topology
    # Create bonds enumerator object.
    bonds_enum = BondsEnumerator(data.particles.bonds)
    # Loop over atoms.
    for particle_index in range(data.particles.count):
        # Loop over bonds of current atom.
        for bond_index in bonds_enum.bonds_of_particle(particle_index):
            # Obtain the indices of the two particles connected by the bond:
            a,b = bond_topology[bond_index]
#            print(f"Particle Identifiers:{ data.particles['Particle Identifier'][[a,b]] }")
'''
        dr2 = (data.particles_.position[i][0] - data0.particles_.position[i][0])**2 + \
                (data.particles_.position[i][1] - data0.particles_.position[i][1])**2 + \
                (data.particles_.position[i][2] - data0.particles_.position[i][2])**2
        #print(id_property[i], dr2/a)
        radius_property.marray[i] = 0.2
        if dr2/a < 0.1:
            color_property.marray[i] = (0, 0, 1)
        else:
            color_property.marray[i] = (1, 0, 0)




        color_property.marray[i] = (ke_property[i]*100, 0, 1 - ke_property[i]*100)
        if id_property[i] == 300:
            radius_property.marray[i] = 1
            color_property.marray[i] = (1, 0, 0)
        else:
            transparency_property.marray[i] = (frame)*0.008
            if type_property.array[i] == 1:
                radius_property.marray[i] = 0.4    
                color_property.marray[i] = (ke_property[i]*100, 0, 1 - ke_property[i]*100)
            else:
                radius_property.marray[i] = 0.2
                color_property.marray[i] = (0/250, 160/250, 0/250)
'''
# Указываем Ovito какую функцию modifier использовать
pipeline.modifiers.append(md.PythonScriptModifier(function=modifier_color_radius))
#pipeline.modifiers.append(md.PythonScriptModifier(function=modify_bonds))

data = pipeline.compute()


# Создаем видео
# data.particles_.position[300]
# Извлекаем размер ячейки

# Создаем объект визуализации
vp = vis.Viewport()
vp.type = vis.Viewport.Type.Perspective
# Создаем функцию, которая бы по номеру шага выводила бы


def get_pos_dir(frame):
    center = np.array([wall/2, wall/2, wall/2])
    radius = wall*4/3*(105-1.0*frame)/100
    hight = [0, 0, wall*3/4]
    phi = frame/800*2*np.pi
    direction = np.array(
        [np.cos(phi), np.sin(phi), 0])
    position = center + direction*radius
    # direction = [-1,0,-1]
    # position = [34.6, 5.2, 34.6]
    return tuple(position), tuple((center - position))


pos, direction = get_pos_dir(0)
# Задаем начальные данные камеры
vp.camera_pos = pos
vp.camera_dir = direction
vp.fov = math.radians(60.0)
# Создаем функцию, которая будет вызываться на каждом шаге
# создания видео и будет вращать нашу камеру


def render_view(args):
    global wall
    frame = args.frame
    # print (args.frame, end=" ")
    logging.info("frame: {:d}".format(args.frame))
    # text1 = "Frame {}".format(args.frame)
    pos, direction = get_pos_dir(frame)
    args.viewport.camera_pos = pos
    args.viewport.camera_dir = direction
    args.viewport.fov = math.radians(60.0)

    xrdf = []
    rdf = []

    for i in range(1, 1001):
        xrdf.append(float(arr[1001*(frame) + i][1]))
        rdf.append(float(arr[1001*(frame) + i][3]))


    dpi = 80
    plot_width = 0.5 * args.size[0] / dpi
    plot_height = 0.5 * args.size[1] / dpi

    # Create matplotlib figure:
    fig, ax = plt.subplots(figsize=(plot_width,plot_height), dpi=dpi)
    fig.patch.set_alpha(0.5)
    plt.title('Coordination')

    # Plot RDF histogram data
    ax.bar(xrdf, rdf)
    plt.tight_layout()

    # Render figure to an in-memory buffer.
    buf = fig.canvas.print_to_buffer()
    plt.close(fig)

    # Create a QImage from the memory buffer
    res_x, res_y = buf[1]
    img = PySide2.QtGui.QImage(buf[0], res_x, res_y, PySide2.QtGui.QImage.Format_RGBA8888)

    # Paint QImage onto viewport canvas
    args.painter.drawImage(0, 0, img)
	
    #data.particles.bonds.vis.enabled = False
    #data.particles.bonds.vis.shading = BondsVis.Shading.Flat
   # data.particles.bonds.vis.width = 1.0



# Добавляем эту функцию в render
vp.overlays.append(
    vis.PythonViewportOverlay(function=render_view))
# Мы можем создать одно изображение с разрешением 400x300
vp.render_image(size=(400, 300), filename="animation.png",
                renderer=vis.TachyonRenderer())
# Можем создать полную анимацию от 0 до 101 шага
# с разрешением 800x400
vp.render_anim(size=(1280, 720), filename="animation.mp4",
               renderer=vis.TachyonRenderer(), range=(0, 100))
