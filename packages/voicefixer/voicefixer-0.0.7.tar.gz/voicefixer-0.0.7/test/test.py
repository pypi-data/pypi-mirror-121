#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test.py
@Contact :   haoheliu@gmail.com
@License :   (C)Copyright 2020-2100

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
9/14/21 11:02 AM   Haohe Liu      1.0         None
'''

from voicefixer import VoiceFixer

voicefixer = VoiceFixer()

voicefixer.restore(input="/Users/liuhaohe/Desktop/test_song.wav",
                   output="/Users/liuhaohe/Desktop/test_song_out_2.wav",
                   cuda=False,mode=1)