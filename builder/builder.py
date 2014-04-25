#!/usr/bin/env python
# coding=utf-8

import re
import os
from sources.config import AseConfig
from sources.log import AseLog
from sources.renderer import AseRenderer
from sources.builder import AseBuilder

renderer = AseRenderer('/home/fike/Documents/Exams/builder/templates')
data = {
    'answer_number':12,
    'answer_title':'Whatta',
    'questions_path':'../../questions/acoustics.md'
}
print renderer.render('empty_answer', data)
