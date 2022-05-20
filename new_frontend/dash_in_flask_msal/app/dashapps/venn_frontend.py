# 1
# 20
# [{'column_id': 'continent', 'direction': 'asc'}, {'column_id': 'lifeExp', 'direction': 'asc'}]
# {continent} scontains Asia && {lifeExp} s> 50
import requests
import pathlib
import json
import networkx as nx
from pprint import pprint
import pandas as pd
#from venn import * #import venn
import numpy as np

import dash
from dash import Dash
from dash import html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table as dt
import dash_bio as dashbio
import dash_daq as daq

#from plotly.tools import mpl_to_plotly
from matplotlib import pyplot as plt
import io
import base64

from plotly.tools import mpl_to_plotly
from matplotlib import pyplot as plt

from dash_table.Format import Format, Scheme, Group

#flask app adjustment
APP_ID='venn_frontend'
URL_BASE='/dash/venn_frontend/'
MIN_HEIGHT=2000
# external_stylesheets = [dbc.themes.DARKLY]
# app = Dash(__name__, external_stylesheets=external_stylesheets)
# server = app.server

base_url_api = "http://127.0.0.1:4999/"
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()


#############VENN#################################


from itertools import chain
try:
    # since python 3.10
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import colors
import math

default_colors = [
    # r, g, b, a
    [92, 192, 98, 0.5],
    [90, 155, 212, 0.5],
    [246, 236, 86, 0.6],
    [241, 90, 96, 0.4],
    [255, 117, 0, 0.3],
    [82, 82, 190, 0.2],
]
default_colors = [
    [i[0] / 255.0, i[1] / 255.0, i[2] / 255.0, i[3]]
    for i in default_colors
]

def draw_ellipse(fig, ax, x, y, w, h, a, fillcolor):
    e = patches.Ellipse(
        xy=(x, y),
        width=w,
        height=h,
        angle=a,
        color=fillcolor)
    ax.add_patch(e)

def draw_triangle(fig, ax, x1, y1, x2, y2, x3, y3, fillcolor):
    xy = [
        (x1, y1),
        (x2, y2),
        (x3, y3),
    ]
    polygon = patches.Polygon(
        xy=xy,
        closed=True,
        color=fillcolor)
    ax.add_patch(polygon)

def draw_text(fig, ax, x, y, text, color=[0, 0, 0, 1], fontsize=14, ha="center", va="center"):
    ax.text(
        x, y, text,
        horizontalalignment=ha,
        verticalalignment=va,
        fontsize=fontsize,
        color="black")

def draw_annotate(fig, ax, x, y, textx, texty, text, color=[0, 0, 0, 1], arrowcolor=[0, 0, 0, 0.3]):
    plt.annotate(
        text,
        xy=(x, y),
        xytext=(textx, texty),
        arrowprops=dict(color=arrowcolor, shrink=0, width=0.5, headwidth=8),
        fontsize=14,
        color=color,
        xycoords="data",
        textcoords="data",
        horizontalalignment='center',
        verticalalignment='center'
    )

def get_labels(data, fill=["number"]):
    """
    get a dict of labels for groups in data

    @type data: list[Iterable]
    @rtype: dict[str, str]

    input
      data: data to get label for
      fill: ["number"|"logic"|"percent"]

    return
      labels: a dict of labels for different sets

    example:
    In [12]: get_labels([range(10), range(5,15), range(3,8)], fill=["number"])
    Out[12]:
    {'001': '0',
     '010': '5',
     '011': '0',
     '100': '3',
     '101': '2',
     '110': '2',
     '111': '3'}
    """

    N = len(data)

    sets_data = [set(data[i]) for i in range(N)]  # sets for separate groups
    s_all = set(chain(*data))                     # union of all sets

    # bin(3) --> '0b11', so bin(3).split('0b')[-1] will remove "0b"
    set_collections = {}
    for n in range(1, 2**N):
        key = bin(n).split('0b')[-1].zfill(N)
        value = s_all
        sets_for_intersection = [sets_data[i] for i in range(N) if  key[i] == '1']
        sets_for_difference = [sets_data[i] for i in range(N) if  key[i] == '0']
        for s in sets_for_intersection:
            value = value & s
        for s in sets_for_difference:
            value = value - s
        set_collections[key] = value

    labels = {k: "" for k in set_collections}
    if "logic" in fill:
        for k in set_collections:
            labels[k] = k + ": "
    if "number" in fill:
        for k in set_collections:
            labels[k] += str(len(set_collections[k]))
    if "percent" in fill:
        data_size = len(s_all)
        for k in set_collections:
            labels[k] += "(%.1f%%)" % (100.0 * len(set_collections[k]) / data_size)

    return labels

def venn1(labels, names=['A'], **options):
  '''
  cant believe this wasnt already written
  '''
  colors = options.get('colors', [default_colors[i] for i in range(2)])
  figsize = options.get('figsize', (9, 7))
  dpi = options.get('dpi', 96)
  fontsize = options.get('fontsize', 14)

  fig = plt.figure(0, figsize=figsize, dpi=dpi)
  ax = fig.add_subplot(111, aspect='equal')
  ax.set_axis_off()
  ax.set_ylim(bottom=0.0, top=0.7)
  ax.set_xlim(left=0.0, right=1.0)

  # body
  draw_ellipse(fig, ax, 0.4, 0.4, 0.5, 0.5, 0.0, colors[0])
  #draw_ellipse(fig, ax, 0.625, 0.3, 0.5, 0.5, 0.0, colors[1])
  draw_text(fig, ax, 0.4, 0.4, labels.get('1', ''), fontsize=fontsize)
  #draw_text(fig, ax, 0.26, 0.30, labels.get('10', ''), fontsize=fontsize)
  #draw_text(fig, ax, 0.50, 0.30, labels.get('11', ''), fontsize=fontsize)

  # legend
  draw_text(fig, ax, 0.40, 0.7, names[0], colors[0], fontsize=fontsize, ha="center", va="bottom")
  #draw_text(fig, ax, 0.80, 0.56, names[1], colors[1], fontsize=fontsize, ha="left", va="bottom")
  leg = ax.legend(names, loc='center left', bbox_to_anchor=(0.8, 0.55), fancybox=True)
  leg.get_frame().set_alpha(0.5)

  return fig, ax

def venn2(labels, names=['A', 'B'], **options):
    """
    plots a 2-set Venn diagram

    @type labels: dict[str, str]
    @type names: list[str]
    @rtype: (Figure, AxesSubplot)

    input
      labels: a label dict where keys are identified via binary codes ('01', '10', '11'),
              hence a valid set could look like: {'01': 'text 1', '10': 'text 2', '11': 'text 3'}.
              unmentioned codes are considered as ''.
      names:  group names
      more:   colors, figsize, dpi, fontsize

    return
      pyplot Figure and AxesSubplot object
    """
    colors = options.get('colors', [default_colors[i] for i in range(2)])
    figsize = options.get('figsize', (9, 7))
    dpi = options.get('dpi', 96)
    fontsize = options.get('fontsize', 14)

    fig = plt.figure(0, figsize=figsize, dpi=dpi)
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_axis_off()
    ax.set_ylim(bottom=0.0, top=0.7)
    ax.set_xlim(left=0.0, right=1.0)

    # body
    draw_ellipse(fig, ax, 0.375, 0.3, 0.5, 0.5, 0.0, colors[0])
    draw_ellipse(fig, ax, 0.625, 0.3, 0.5, 0.5, 0.0, colors[1])
    draw_text(fig, ax, 0.74, 0.30, labels.get('01', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.26, 0.30, labels.get('10', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.50, 0.30, labels.get('11', ''), fontsize=fontsize)

    # legend
    draw_text(fig, ax, 0.20, 0.56, names[0], colors[0], fontsize=fontsize, ha="right", va="bottom")
    draw_text(fig, ax, 0.80, 0.56, names[1], colors[1], fontsize=fontsize, ha="left", va="bottom")
    leg = ax.legend(names, loc='center left', bbox_to_anchor=(1.0, 0.5), fancybox=True)
    leg.get_frame().set_alpha(0.5)

    return fig, ax

def venn3(labels, names=['A', 'B', 'C'], **options):
    """
    plots a 3-set Venn diagram

    @type labels: dict[str, str]
    @type names: list[str]
    @rtype: (Figure, AxesSubplot)

    input
      labels: a label dict where keys are identified via binary codes ('001', '010', '100', ...),
              hence a valid set could look like: {'001': 'text 1', '010': 'text 2', '100': 'text 3', ...}.
              unmentioned codes are considered as ''.
      names:  group names
      more:   colors, figsize, dpi, fontsize

    return
      pyplot Figure and AxesSubplot object
    """
    colors = options.get('colors', [default_colors[i] for i in range(3)])
    figsize = options.get('figsize', (9, 9))
    dpi = options.get('dpi', 96)
    fontsize = options.get('fontsize', 14)

    fig = plt.figure(0, figsize=figsize, dpi=dpi)
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_axis_off()
    ax.set_ylim(bottom=0.0, top=1.0)
    ax.set_xlim(left=0.0, right=1.0)

    # body
    draw_ellipse(fig, ax, 0.333, 0.633, 0.5, 0.5, 0.0, colors[0])
    draw_ellipse(fig, ax, 0.666, 0.633, 0.5, 0.5, 0.0, colors[1])
    draw_ellipse(fig, ax, 0.500, 0.310, 0.5, 0.5, 0.0, colors[2])
    draw_text(fig, ax, 0.50, 0.27, labels.get('001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.73, 0.65, labels.get('010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.61, 0.46, labels.get('011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.27, 0.65, labels.get('100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.39, 0.46, labels.get('101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.50, 0.65, labels.get('110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.50, 0.51, labels.get('111', ''), fontsize=fontsize)

    # legend
    draw_text(fig, ax, 0.15, 0.87, names[0], colors[0], fontsize=fontsize, ha="right", va="bottom")
    draw_text(fig, ax, 0.85, 0.87, names[1], colors[1], fontsize=fontsize, ha="left", va="bottom")
    draw_text(fig, ax, 0.50, 0.02, names[2], colors[2], fontsize=fontsize, va="top")
    leg = ax.legend(names, loc='center left', bbox_to_anchor=(1.0, 0.5), fancybox=True)
    leg.get_frame().set_alpha(0.5)

    return fig, ax

def venn4(labels, names=['A', 'B', 'C', 'D'], **options):
    """
    plots a 4-set Venn diagram

    @type labels: dict[str, str]
    @type names: list[str]
    @rtype: (Figure, AxesSubplot)

    input
      labels: a label dict where keys are identified via binary codes ('0001', '0010', '0100', ...),
              hence a valid set could look like: {'0001': 'text 1', '0010': 'text 2', '0100': 'text 3', ...}.
              unmentioned codes are considered as ''.
      names:  group names
      more:   colors, figsize, dpi, fontsize

    return
      pyplot Figure and AxesSubplot object
    """
    colors = options.get('colors', [default_colors[i] for i in range(4)])
    figsize = options.get('figsize', (12, 12))
    dpi = options.get('dpi', 96)
    fontsize = options.get('fontsize', 14)

    fig = plt.figure(0, figsize=figsize, dpi=dpi)
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_axis_off()
    ax.set_ylim(bottom=0.0, top=1.0)
    ax.set_xlim(left=0.0, right=1.0)

    # body
    draw_ellipse(fig, ax, 0.350, 0.400, 0.72, 0.45, 140.0, colors[0])
    draw_ellipse(fig, ax, 0.450, 0.500, 0.72, 0.45, 140.0, colors[1])
    draw_ellipse(fig, ax, 0.544, 0.500, 0.72, 0.45, 40.0, colors[2])
    draw_ellipse(fig, ax, 0.644, 0.400, 0.72, 0.45, 40.0, colors[3])
    draw_text(fig, ax, 0.85, 0.42, labels.get('0001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.68, 0.72, labels.get('0010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.77, 0.59, labels.get('0011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.32, 0.72, labels.get('0100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.71, 0.30, labels.get('0101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.50, 0.66, labels.get('0110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.65, 0.50, labels.get('0111', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.14, 0.42, labels.get('1000', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.50, 0.17, labels.get('1001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.29, 0.30, labels.get('1010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.39, 0.24, labels.get('1011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.23, 0.59, labels.get('1100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.61, 0.24, labels.get('1101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.35, 0.50, labels.get('1110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.50, 0.38, labels.get('1111', ''), fontsize=fontsize)

    # legend
    draw_text(fig, ax, 0.13, 0.18, names[0], colors[0], fontsize=fontsize, ha="right")
    draw_text(fig, ax, 0.18, 0.83, names[1], colors[1], fontsize=fontsize, ha="right", va="bottom")
    draw_text(fig, ax, 0.82, 0.83, names[2], colors[2], fontsize=fontsize, ha="left", va="bottom")
    draw_text(fig, ax, 0.87, 0.18, names[3], colors[3], fontsize=fontsize, ha="left", va="top")
    leg = ax.legend(names, loc='center left', bbox_to_anchor=(1.0, 0.5), fancybox=True)
    leg.get_frame().set_alpha(0.5)

    return fig, ax

def venn5(labels, names=['A', 'B', 'C', 'D', 'E'], **options):
    """
    plots a 5-set Venn diagram

    @type labels: dict[str, str]
    @type names: list[str]
    @rtype: (Figure, AxesSubplot)

    input
      labels: a label dict where keys are identified via binary codes ('00001', '00010', '00100', ...),
              hence a valid set could look like: {'00001': 'text 1', '00010': 'text 2', '00100': 'text 3', ...}.
              unmentioned codes are considered as ''.
      names:  group names
      more:   colors, figsize, dpi, fontsize

    return
      pyplot Figure and AxesSubplot object
    """
    colors = options.get('colors', [default_colors[i] for i in range(5)])
    figsize = options.get('figsize', (13, 13))
    dpi = options.get('dpi', 96)
    fontsize = options.get('fontsize', 14)

    fig = plt.figure(0, figsize=figsize, dpi=dpi)
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_axis_off()
    ax.set_ylim(bottom=0.0, top=1.0)
    ax.set_xlim(left=0.0, right=1.0)

    # body
    draw_ellipse(fig, ax, 0.428, 0.449, 0.87, 0.50, 155.0, colors[0])
    draw_ellipse(fig, ax, 0.469, 0.543, 0.87, 0.50, 82.0, colors[1])
    draw_ellipse(fig, ax, 0.558, 0.523, 0.87, 0.50, 10.0, colors[2])
    draw_ellipse(fig, ax, 0.578, 0.432, 0.87, 0.50, 118.0, colors[3])
    draw_ellipse(fig, ax, 0.489, 0.383, 0.87, 0.50, 46.0, colors[4])
    draw_text(fig, ax, 0.27, 0.11, labels.get('00001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.72, 0.11, labels.get('00010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.55, 0.13, labels.get('00011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.91, 0.58, labels.get('00100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.78, 0.64, labels.get('00101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.84, 0.41, labels.get('00110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.76, 0.55, labels.get('00111', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.51, 0.90, labels.get('01000', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.39, 0.15, labels.get('01001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.42, 0.78, labels.get('01010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.50, 0.15, labels.get('01011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.67, 0.76, labels.get('01100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.70, 0.71, labels.get('01101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.51, 0.74, labels.get('01110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.64, 0.67, labels.get('01111', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.10, 0.61, labels.get('10000', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.20, 0.31, labels.get('10001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.76, 0.25, labels.get('10010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.65, 0.23, labels.get('10011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.18, 0.50, labels.get('10100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.21, 0.37, labels.get('10101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.81, 0.37, labels.get('10110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.74, 0.40, labels.get('10111', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.27, 0.70, labels.get('11000', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.34, 0.25, labels.get('11001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.33, 0.72, labels.get('11010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.51, 0.22, labels.get('11011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.25, 0.58, labels.get('11100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.28, 0.39, labels.get('11101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.36, 0.66, labels.get('11110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.51, 0.47, labels.get('11111', ''), fontsize=fontsize)

    # legend
    draw_text(fig, ax, 0.02, 0.72, names[0], colors[0], fontsize=fontsize, ha="right")
    draw_text(fig, ax, 0.72, 0.94, names[1], colors[1], fontsize=fontsize, va="bottom")
    draw_text(fig, ax, 0.97, 0.74, names[2], colors[2], fontsize=fontsize, ha="left")
    draw_text(fig, ax, 0.88, 0.05, names[3], colors[3], fontsize=fontsize, ha="left")
    draw_text(fig, ax, 0.12, 0.05, names[4], colors[4], fontsize=fontsize, ha="right")
    leg = ax.legend(names, loc='center left', bbox_to_anchor=(1.0, 0.5), fancybox=True)
    leg.get_frame().set_alpha(0.5)

    return fig, ax

def venn6(labels, names=['A', 'B', 'C', 'D', 'E'], **options):
    """
    plots a 6-set Venn diagram

    @type labels: dict[str, str]
    @type names: list[str]
    @rtype: (Figure, AxesSubplot)

    input
      labels: a label dict where keys are identified via binary codes ('000001', '000010', '000100', ...),
              hence a valid set could look like: {'000001': 'text 1', '000010': 'text 2', '000100': 'text 3', ...}.
              unmentioned codes are considered as ''.
      names:  group names
      more:   colors, figsize, dpi, fontsize

    return
      pyplot Figure and AxesSubplot object
    """
    colors = options.get('colors', [default_colors[i] for i in range(6)])
    figsize = options.get('figsize', (20, 20))
    dpi = options.get('dpi', 96)
    fontsize = options.get('fontsize', 14)

    fig = plt.figure(0, figsize=figsize, dpi=dpi)
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_axis_off()
    ax.set_ylim(bottom=0.230, top=0.845)
    ax.set_xlim(left=0.173, right=0.788)

    # body
    # See https://web.archive.org/web/20040819232503/http://www.hpl.hp.com/techreports/2000/HPL-2000-73.pdf
    draw_triangle(fig, ax, 0.637, 0.921, 0.649, 0.274, 0.188, 0.667, colors[0])
    draw_triangle(fig, ax, 0.981, 0.769, 0.335, 0.191, 0.393, 0.671, colors[1])
    draw_triangle(fig, ax, 0.941, 0.397, 0.292, 0.475, 0.456, 0.747, colors[2])
    draw_triangle(fig, ax, 0.662, 0.119, 0.316, 0.548, 0.662, 0.700, colors[3])
    draw_triangle(fig, ax, 0.309, 0.081, 0.374, 0.718, 0.681, 0.488, colors[4])
    draw_triangle(fig, ax, 0.016, 0.626, 0.726, 0.687, 0.522, 0.327, colors[5])
    draw_text(fig, ax, 0.212, 0.562, labels.get('000001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.430, 0.249, labels.get('000010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.356, 0.444, labels.get('000011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.609, 0.255, labels.get('000100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.323, 0.546, labels.get('000101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.513, 0.316, labels.get('000110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.523, 0.348, labels.get('000111', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.747, 0.458, labels.get('001000', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.325, 0.492, labels.get('001001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.670, 0.481, labels.get('001010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.359, 0.478, labels.get('001011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.653, 0.444, labels.get('001100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.344, 0.526, labels.get('001101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.653, 0.466, labels.get('001110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.363, 0.503, labels.get('001111', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.750, 0.616, labels.get('010000', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.682, 0.654, labels.get('010001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.402, 0.310, labels.get('010010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.392, 0.421, labels.get('010011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.653, 0.691, labels.get('010100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.651, 0.644, labels.get('010101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.490, 0.340, labels.get('010110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.468, 0.399, labels.get('010111', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.692, 0.545, labels.get('011000', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.666, 0.592, labels.get('011001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.665, 0.496, labels.get('011010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.374, 0.470, labels.get('011011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.653, 0.537, labels.get('011100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.652, 0.579, labels.get('011101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.653, 0.488, labels.get('011110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.389, 0.486, labels.get('011111', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.553, 0.806, labels.get('100000', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.313, 0.604, labels.get('100001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.388, 0.694, labels.get('100010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.375, 0.633, labels.get('100011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.605, 0.359, labels.get('100100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.334, 0.555, labels.get('100101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.582, 0.397, labels.get('100110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.542, 0.372, labels.get('100111', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.468, 0.708, labels.get('101000', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.355, 0.572, labels.get('101001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.420, 0.679, labels.get('101010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.375, 0.597, labels.get('101011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.641, 0.436, labels.get('101100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.348, 0.538, labels.get('101101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.635, 0.453, labels.get('101110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.370, 0.548, labels.get('101111', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.594, 0.689, labels.get('110000', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.579, 0.670, labels.get('110001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.398, 0.670, labels.get('110010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.395, 0.653, labels.get('110011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.633, 0.682, labels.get('110100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.616, 0.656, labels.get('110101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.587, 0.427, labels.get('110110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.526, 0.415, labels.get('110111', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.495, 0.677, labels.get('111000', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.505, 0.648, labels.get('111001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.428, 0.663, labels.get('111010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.430, 0.631, labels.get('111011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.639, 0.524, labels.get('111100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.591, 0.604, labels.get('111101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.622, 0.477, labels.get('111110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.501, 0.523, labels.get('111111', ''), fontsize=fontsize)

    # legend
    draw_text(fig, ax, 0.674, 0.824, names[0], colors[0], fontsize=fontsize)
    draw_text(fig, ax, 0.747, 0.751, names[1], colors[1], fontsize=fontsize)
    draw_text(fig, ax, 0.739, 0.396, names[2], colors[2], fontsize=fontsize)
    draw_text(fig, ax, 0.700, 0.247, names[3], colors[3], fontsize=fontsize)
    draw_text(fig, ax, 0.291, 0.255, names[4], colors[4], fontsize=fontsize)
    draw_text(fig, ax, 0.203, 0.484, names[5], colors[5], fontsize=fontsize)
    leg = ax.legend(names, loc='center left', bbox_to_anchor=(1.0, 0.5), fancybox=True)
    leg.get_frame().set_alpha(0.5)

    return fig, ax
##############################################################


############### LOAD HIERARCHIES ##############

###########################################


######### HELPER FUNCTIONS ################
def make_venn_figure_from_panda(temp_panda):
    '''
    for each column make a set of items, up to 6
    '''
    print('~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(temp_panda)
    column_membership_list=list()
    column_name_list=list()
    for i,temp_column in enumerate(temp_panda.columns):
        if temp_column=='bin' or i>7:
            continue
        else:
            temp_set={x for x in temp_panda[temp_column].to_list() if x==x}
            column_membership_list.append(temp_set)
            column_name_list.append(temp_column)


    pprint(column_membership_list)
    labels = get_labels(column_membership_list, fill=['number', 'logic'])
    fig, ax = eval('venn'+str(len(column_membership_list))+'(labels, names=column_name_list)')
    #plotly_fig = mpl_to_plotly(fig)
    buf = io.BytesIO() # in-memory files
    #plt.scatter(x, y)
    plt.savefig(buf, format = "png") # save to the above file object
    plt.close()
    data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
    plotly_fig="data:image/png;base64,{}".format(data)

    return plotly_fig

    #for i,temp_column in enumerate(temp_panda.columns):
    
########################################


#############Load pandas for data selection options ##########
unique_sod_combinations_address = DATA_PATH.joinpath("unique_sod_combinations.bin")

unique_sod_combinations_panda = pd.read_pickle(unique_sod_combinations_address)
unique_sod_combinations_dict = {
    temp:temp for temp in unique_sod_combinations_panda.keys().to_list()
}
pprint(unique_sod_combinations_dict)
########################################


#####Read in panda for filtering options after one is selected######

####################################################################


############Update pandas for data selection#################

#############################################

################create temp mpl fig####################

# labels = venn.get_labels([range(20), range(5, 15), range(3, 8)], fill=['number', 'logic'])
# fig, ax = venn.venn3(labels, names=['Human Plasma No', 'a;lskdjfa;lskjdfafs', 'b'])
# #plotly_fig = mpl_to_plotly(fig)
# buf = io.BytesIO() # in-memory files
# #plt.scatter(x, y)
# plt.savefig(buf, format = "png") # save to the above file object
# plt.close()
# data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
# plotly_fig="data:image/png;base64,{}".format(data)
######################################################

def add_dash(server):

    external_stylesheets = [dbc.themes.DARKLY]
    app = dash.Dash(
        server=server,
        url_base_pathname=URL_BASE,
        suppress_callback_exceptions=True,
        external_stylesheets=external_stylesheets
    )

    #####################Structure of app#################
    app.layout=dbc.Container(#html.Div(
        children=[
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            html.H2("Venn Comparator", className='text-center'),
                            html.Br(),
                        ],
                        width={'size':6}
                    )
                ],
                justify='center'
            ),
            html.Br(),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            dbc.Card(
                                dbc.CardBody(
                                    children=[
                                        html.H6('Select one or more groups'),
                                        dcc.Dropdown(
                                            id='dropdown_triplet_selection',
                                            options=[
                                                #{'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in species_network_dict_from['elements']['nodes']
                                                {'label': temp, 'value':unique_sod_combinations_dict[temp]} for temp in unique_sod_combinations_dict
                                            ],
                                            multi=True,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#3EB489',
                                            }
                                        ),         
                                        html.Br(),                               
                                        html.H6("Minimum Percent Present", className='text-center'),
                                        dcc.Slider(
                                            id='slider_percent_present',
                                            #label='Minimum Percent Present',
                                            min=0,
                                            max=100,
                                            step=1,
                                            value=80,   
                                            marks=None,
                                            tooltip={"placement": "bottom", "always_visible": True}       
                                        ),
                                        html.Br(),
                                        html.H6("Median or Average", className='text-center'),
                                        daq.ToggleSwitch(
                                            id='toggle_average_true',
                                            value=True,
                                            #label='Median - Average'
                                        ),
                                        html.Br(),
                                        html.H6("Bin Filters"),
                                        dcc.RadioItems(
                                            id='radio_items_filter',
                                            options=[
                                                {'label': 'No Filter', 'value': 'no_filter'},
                                                {'label': 'Common', 'value': 'common'},
                                                #{'label': 'Unique', 'value': 'unique'},
                                            ],         
                                            value='no_filter'                                   
                                        )
                                    ]
                                )
                            ),
                        ],
                        width={'size':4}
                    ),
                    dbc.Col(
                        children=[
                            dbc.Card(
                                dbc.CardBody(
                                    # children=[
                                    #     html.H6("Minimum Percent Present", className='text-center'),
                                    #     dcc.Slider(
                                    #         id='slider_percent_present',
                                    #         #label='Minimum Percent Present',
                                    #         min=0,
                                    #         max=100,
                                    #         step=1,
                                    #         value=80,   
                                    #         marks=None,
                                    #         tooltip={"placement": "bottom", "always_visible": True}       
                                    #     ),
                                    #     html.H6("Median or Average", className='text-center'),
                                    #     daq.ToggleSwitch(
                                    #         id='toggle_average_true',
                                    #         value=True,
                                    #         #label='Median - Average'
                                    #     )
                                    # ]
                                    # dcc.Graph(
                                    #     id='figure_venn',
                                    #     figure=plotly_fig
                                    # )
                                    html.Img(
                                        id='Img_venn',
                                        #src=plotly_fig,
                                        height=200,
                                        width=200
                                    )
                                )
                            ),
                        ],
                        width={'size':4}
                    )
                ],
                justify='around'
            ),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            html.Br(),
                            html.H2("Results", className='text-center'),
                            dbc.Card(
                                dbc.CardBody(
                                    children=[
                                        html.Button(
                                            'Get Results',
                                            id='button_query',
                                        )
                                    ]
                                )
                            )
                        ],
                        width={'size':3}
                    )
                ],
                justify='center'
            ),
            dbc.Row(
                children=[
                    dbc.Card(
                        dt.DataTable(
                            id='table',
                            columns=[
                                {"name": "Bin ID", "id": "bin_id"},
                                {"name": "Compound Name", "id": "compound_name"},
                                {"name": "Group 1", "id": "group_1"},
                            ],
                            data=[],
                            page_current=0,
                            page_size=50,
                            page_action='custom',
                            style_header={
                                'backgroundColor': 'rgb(30, 30, 30)',
                                'color': 'white'
                            },
                            style_data={
                                'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'white'
                            },

                            sort_action='custom',
                            sort_mode='multi',
                            sort_by=[],

                            filter_action='custom',
                            filter_query=''
                        )
                    ),
                ],
                justify='center'
            ),
            dbc.Modal(
                dbc.ModalBody(
                    html.Img(
                        id='modal_Img_venn',
                        #src=plotly_fig,
                        height=700,
                        width=700
                    )
                ),
                id='modal',
                is_open=False
            )
        ]
    )
    ######################################################

    # #generates the datatable
    @app.callback(
        [
            Output(component_id="table", component_property="columns"),
            Output(component_id="table", component_property="data"),
            #Output(component_id="volcano_average_welch", component_property="figure"),
            #Output(component_id="volcano_median_mw", component_property="figure"),
        ],
        [
            Input(component_id="button_query", component_property="n_clicks"),
            Input(component_id="table", component_property="page_current"),
            Input(component_id="table", component_property="page_size"),
            Input(component_id="table", component_property="sort_by"),
            Input(component_id="table", component_property="filter_query"),
        ],
        [
            State(component_id="dropdown_triplet_selection",component_property="value"),
            State(component_id="slider_percent_present", component_property="value"),
            State(component_id="toggle_average_true", component_property="value"),
            State(component_id="radio_items_filter",component_property="value")
            # State(component_id="dropdown_from_disease", component_property="value"),
            # State(component_id="dropdown_to_species", component_property="value"),
            # State(component_id="dropdown_to_organ", component_property="value"),
            # State(component_id="dropdown_to_disease", component_property="value"),
        ],
        prevent_initial_call=True
    )
    def perform_query_table(
        query,
        page_current,
        page_size,
        sort_by,
        filter_query,
        dropdown_triplet_selection_value,
        slider_percent_present_value,
        toggle_average_true_value,
        radio_items_filter_value
    #     checklist_query,
    #     from_species_value,
    #     from_organ_value,
    #     from_disease_value,
    #     to_species_value,
    #     to_organ_value,
    #     to_disease_value,
        ):
            """
            """
            # print(page_current)
            # print(page_size)
            # print(sort_by)
            # print(filter_query)


        #     print('before json')

        #     if "Classes" in checklist_query:
        #         include_classes='Yes'
        #     else:
        #         include_classes='No'
        #     if "Knowns" in checklist_query:
        #         include_knowns='Yes'
        #     else:
        #         include_knowns='No'
        #     if "Unknowns" in checklist_query:
        #         include_unknowns='Yes'
        #     else:
        #         include_unknowns='No'

        #     ##################volcano query######################
            #prepare json for api
            venn_data_table_output={
                "page_current":page_current,
                "page_size":page_size,
                "sort_by":sort_by,
                "filter_query":filter_query,
                "dropdown_triplet_selection_value":dropdown_triplet_selection_value,
                "slider_percent_present_value":slider_percent_present_value,
                "toggle_average_true_value":toggle_average_true_value,
                "radio_items_filter_value":radio_items_filter_value
            }

            pprint(venn_data_table_output)
        #     volcano_json_output = {
        #         "from_species": from_species_value,
        #         "from_organ": from_organ_value,
        #         "from_disease": from_disease_value,
        #         "to_species": to_species_value,
        #         "to_organ": to_organ_value,
        #         "to_disease": to_disease_value,
        #         "include_classes": include_classes,
        #         "include_knowns": include_knowns,
        #         "include_unknowns": include_unknowns,
        #         "page_current":page_current,
        #         "page_size":page_size,
        #         "sort_by":sort_by,
        #         "filter_query":filter_query,
        #     }

        #     print('after json before api')
        #     #call api
            response = requests.post(base_url_api + "/venntableresource/", json=venn_data_table_output)
            print(response)
            total_panda = pd.read_json(response.json(), orient="records")
            print(total_panda)

        #     #prepare columns and data for the table
            column_list = [
                {"name": "bin", "id": "bin"},
                {"name": "English Name", "id":"compound"}
            ]
            sod_column_list=[
                {"name": temp_column, "id": temp_column,"type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)} for temp_column in total_panda.columns 
                if (temp_column != "bin" and temp_column!="compound")
            ]
            #     {"name": "Fold Average", "id": "fold_average","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
            #     {"name": "Significance Welch", "id": "sig_welch","type": "numeric","format": Format(group=Group.yes, precision=4, scheme=Scheme.exponent)},
            #     {"name": "Fold Median", "id": "fold_median","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
            #     {"name": "Significance MWU", "id": "sig_mannwhit","type": "numeric","format": Format(group=Group.yes, precision=4, scheme=Scheme.exponent)}
            # ]
            column_list+=sod_column_list
            data = total_panda.to_dict(orient='records')

        #     #prepare figures for volcano plots
        #     volcano_average = dashbio.VolcanoPlot(
        #         dataframe=total_panda,#bins_panda,
        #         snp="english_name",
        #         p="sig_welch",
        #         effect_size="fold_average",
        #         gene=None,
        #         xlabel='log2 Fold Change',
        #         genomewideline_value=1e-2,
        #     )
        #     volcano_median = dashbio.VolcanoPlot(
        #         dataframe=total_panda,#bins_panda,
        #         snp="english_name",
        #         p="sig_mannwhit",
        #         effect_size="fold_median",
        #         gene=None,
        #         xlabel='log2 Fold Change',
        #         genomewideline_value=1e-2,
        #     )
        #     #################################################3

            return (
                column_list,
                data
        #         volcano_average,
        #         volcano_median,
            )



    #generates the venn diagram
    @app.callback(
        [
            Output(component_id="Img_venn", component_property="src"),
            Output(component_id='modal_Img_venn',component_property="src")
            #Output(component_id="table", component_property="columns"),
            #Output(component_id="table", component_property="data"),
            #Output(component_id="volcano_average_welch", component_property="figure"),
            #Output(component_id="volcano_median_mw", component_property="figure"),
        ],
        [
            Input(component_id="button_query", component_property="n_clicks"),
            #Input(component_id="table", component_property="page_current"),
            #Input(component_id="table", component_property="page_size"),
            #Input(component_id="table", component_property="sort_by"),
            #Input(component_id="table", component_property="filter_query"),
        ],
        [
            State(component_id="dropdown_triplet_selection",component_property="value"),
            State(component_id="slider_percent_present", component_property="value"),
            #State(component_id="toggle_average_true", component_property="value"),
            #State(component_id="radio_items_filter",component_property="value")
            # State(component_id="dropdown_from_disease", component_property="value"),
            # State(component_id="dropdown_to_species", component_property="value"),
            # State(component_id="dropdown_to_organ", component_property="value"),
            # State(component_id="dropdown_to_disease", component_property="value"),
        ],
        prevent_initial_call=True
    )
    def perform_query_diagram(
        query,
        #page_current,
        #page_size,
        #sort_by,
        #filter_query,
        dropdown_triplet_selection_value,
        slider_percent_present_value,
        #toggle_average_true_value,
        #radio_items_filter_value
        #     checklist_query,
        #     from_species_value,
        #     from_organ_value,
        #     from_disease_value,
        #     to_species_value,
        #     to_organ_value,
        #     to_disease_value,
        ):
            """
            """
            # print(page_current)
            # print(page_size)
            # print(sort_by)
            # print(filter_query)


        #     print('before json')

        #     if "Classes" in checklist_query:
        #         include_classes='Yes'
        #     else:
        #         include_classes='No'
        #     if "Knowns" in checklist_query:
        #         include_knowns='Yes'
        #     else:
        #         include_knowns='No'
        #     if "Unknowns" in checklist_query:
        #         include_unknowns='Yes'
        #     else:
        #         include_unknowns='No'

        #     ##################volcano query######################
            #prepare json for api
            venn_diagram_output={
                #"page_current":page_current,
                #"page_size":page_size,
                #"sort_by":sort_by,
                #"filter_query":filter_query,
                "dropdown_triplet_selection_value":dropdown_triplet_selection_value,
                "slider_percent_present_value":slider_percent_present_value,
                #"toggle_average_true_value":toggle_average_true_value,
                #"radio_items_filter_value":radio_items_filter_value
            }

            #pprint(venn_data_table_output)
        #     volcano_json_output = {
        #         "from_species": from_species_value,
        #         "from_organ": from_organ_value,
        #         "from_disease": from_disease_value,
        #         "to_species": to_species_value,
        #         "to_organ": to_organ_value,
        #         "to_disease": to_disease_value,
        #         "include_classes": include_classes,
        #         "include_knowns": include_knowns,
        #         "include_unknowns": include_unknowns,
        #         "page_current":page_current,
        #         "page_size":page_size,
        #         "sort_by":sort_by,
        #         "filter_query":filter_query,
        #     }

        #     print('after json before api')
        #     #call api
            response = requests.post(base_url_api + "/venndiagramresource/", json=venn_diagram_output)
            print(response)
            total_panda = pd.read_json(response.json(), orient="records")
            print(total_panda)

            temp_img=make_venn_figure_from_panda(total_panda)




        #     #prepare columns and data for the table
            # column_list = [
            #     {"name": "bin", "id": "bin"},
            #     {"name": "English Name", "id":"compound"}
            # ]
            # sod_column_list=[
            #     {"name": temp_column, "id": temp_column,"type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)} for temp_column in total_panda.columns 
            #     if (temp_column != "bin" and temp_column!="compound")
            # ]
            #     {"name": "Fold Average", "id": "fold_average","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
            #     {"name": "Significance Welch", "id": "sig_welch","type": "numeric","format": Format(group=Group.yes, precision=4, scheme=Scheme.exponent)},
            #     {"name": "Fold Median", "id": "fold_median","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
            #     {"name": "Significance MWU", "id": "sig_mannwhit","type": "numeric","format": Format(group=Group.yes, precision=4, scheme=Scheme.exponent)}
            # ]
            # column_list+=sod_column_list
            # data = total_panda.to_dict(orient='records')

        #     #prepare figures for volcano plots
        #     volcano_average = dashbio.VolcanoPlot(
        #         dataframe=total_panda,#bins_panda,
        #         snp="english_name",
        #         p="sig_welch",
        #         effect_size="fold_average",
        #         gene=None,
        #         xlabel='log2 Fold Change',
        #         genomewideline_value=1e-2,
        #     )
        #     volcano_median = dashbio.VolcanoPlot(
        #         dataframe=total_panda,#bins_panda,
        #         snp="english_name",
        #         p="sig_mannwhit",
        #         effect_size="fold_median",
        #         gene=None,
        #         xlabel='log2 Fold Change',
        #         genomewideline_value=1e-2,
        #     )
        #     #################################################3

            return [temp_img,temp_img]
                # column_list,
                # data
        #         volcano_average,
        #         volcano_median,
            #)

    @app.callback(
        [
            Output(component_id='modal', component_property='is_open'),
        ],
        [
            Input(component_id='Img_venn', component_property='n_clicks'),
        ],
        prevent_initial_call=True
    )
    def open_modal(Img_venn_n_clicks):
        # if n % 2 == 0:
        #     return {'display': 'none'}
        # else:
        #     return {
        #         'display': 'block',
        #         'z-index': '1',
        #         'padding-top': '100',
        #         'left': '0',
        #         'top': '0',
        #         'width': '100%',
        #         'height': '100%',
        #         'overflow': 'auto'
        #         }
        print('hi')
        return [True]
  

    return server

# if __name__ == "__main__":
#     app.run_server(debug=True)
if __name__ == '__main__':
    from flask import Flask, render_template
    from flask_bootstrap import Bootstrap

    bootstrap = Bootstrap()
    app = Flask(__name__)
    bootstrap.init_app(app)

    # inject Dash
    app = add_dash(app) #, login_req=False)

    @app.route(URL_BASE)
    def dash_app():
        return render_template('dashapps/dash_app_debug.html', dash_url=URL_BASE,
                               min_height=MIN_HEIGHT)

    app_port = 8050
    print(f'http://localhost:{app_port}{URL_BASE}')
    app.run(debug=True, port=app_port)