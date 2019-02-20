#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime


agora = datetime.datetime.now()

a = open(r"C:\Users\luiz\PycharmProjects\robos\checklist.txt", 'r').readlines()
if 'bovespa\n' in a:
    os.system(r"python C:\Users\luiz\PycharmProjects\robos\bovespa.py")

if