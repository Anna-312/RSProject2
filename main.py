from RS import initRS, second_thread
import threading as thr
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import name


def Draw(a, b, n1, n2):
    vertices = (
        (2.0, 0.0, -2.0),
        (-2.0, 4.0, -2.0),
        (-2.0, 0.0, -2.0),
        (-2.0, 0.0, 2.0),
        (-2.0, 4.0, 2.0),
        (2.0, 4.0, -2.0),
        (2.0, 0.0, 2.0)
    )
    edges = (
        (0, 2),
        (1, 2),
        (2, 3),
    )
    surfaces = (
        (2, 1, 5, 0),
        (2, 0, 6, 3),
        (2, 3, 4, 1)
    )
    k1 = 4/a
    k2 = 4/b
    k3 = 4/100
    glColor3f(0.85, 0.85, 0.85)
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(1)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    glBegin(GL_LINES)
    glColor3f(0.6, 0.6, 0.6)
    for i in range(1, 10):
        glVertex3fv((vertices[2][0] + i * 0.4, vertices[2][1], vertices[2][2]))
        glVertex3fv((vertices[3][0] + i * 0.4, vertices[3][1], vertices[3][2]))
        glVertex3fv((vertices[1][0] + i * 0.4, vertices[1][1], vertices[1][2]))
        glVertex3fv((vertices[2][0] + i * 0.4, vertices[2][1], vertices[2][2]))
        glVertex3fv((vertices[2][0], vertices[2][1], vertices[2][2] + i*0.4))
        glVertex3fv((vertices[1][0], vertices[1][1], vertices[1][2] + i*0.4))
        glVertex3fv((vertices[2][0], vertices[2][1] + i*0.4, vertices[2][2]))
        glVertex3fv((vertices[0][0], vertices[0][1] + i*0.4, vertices[0][2]))
        glVertex3fv((vertices[2][0], vertices[2][1] + i * 0.4, vertices[2][2]))
        glVertex3fv((vertices[3][0], vertices[3][1] + i * 0.4, vertices[3][2]))
        glVertex3fv((vertices[2][0], vertices[2][1], vertices[2][2] + i * 0.4))
        glVertex3fv((vertices[0][0], vertices[0][1], vertices[0][2] + i * 0.4))
    glEnd()
    glColor3f(1.0, 0.0, 0.0)
    u = np.empty((n2, n1))
    L = thr.Lock()
    L.acquire()
    for i in range(n1):
        for j in range(n2):
            u[j][i] = name.u[j][i]
    L.release()
    for j in range(n2):
        glBegin(GL_LINE_STRIP)
        for i in range(n1):
            glVertex3fv((name.x[i]*k1 - 2, u[j][i]*k3, name.y[j]*k2 - 2))
        glEnd()
    for j in range(n1):
        glBegin(GL_LINE_STRIP)
        for i in range(n2):
            glVertex3fv((name.x[j]*k1 - 2, u[i][j]*k3, name.y[i]*k2 - 2))
        glEnd()

def main():
    print("Введите имя файла для ввода данных:")
    filename = input()
    with open(filename, "r") as file:
        data = file.read().split()
        name.a = float(data[0])
        name.b = float(data[1])
        name.C1 = float(data[2])
        name.C2 = float(data[3])
        name.alpha = float(data[4])
    initRS()
    print("Для запуска вторичного потока нажмите 1.")
    if int(input()) == 1:
        thread = thr.Thread(target=second_thread)
        thread.start()

        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Главное окно")
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0.0, -1.0, -10)
        glRotatef(20, 10, -10, 0)
        glClearColor(1.0, 1.0, 1.0, 1.1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            Draw(name.a, name.b, name.n1, name.n2)
            pygame.display.flip()
            pygame.time.wait(1)


main()

