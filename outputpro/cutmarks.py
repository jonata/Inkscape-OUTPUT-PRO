#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess #re, subprocess, simplestyle, os#inkex, os, random, sys, subprocess, shutil

def generate_final_file(isvector, colormode, width, height, strokewidth, temp_dir):
    if not isvector:

        command = []
        final_command = ['convert']

        for color in colormode:
            command.append('convert')
            command.append('-size')
            command.append(str(width + 40) + 'x' + str(height + 40))
            command.append('xc:white')
            command.append('-stroke')
            command.append('black')
            command.append('-strokewidth')
            command.append(str(strokewidth))
            command.append('-draw')
            command.append('line ' + str(20) + ',' + str(20) + ', ' + str(0) + ',' + str(20))
            command.append('-draw')
            command.append('line ' + str(20) + ',' + str(20) + ', ' + str(20) + ',' + str(0))
            command.append('-draw')
            command.append('line ' + str(width + 20) + ',' + str(20) + ', ' + str(width + 20) + ',' + str(0))
            command.append('-draw')
            command.append('line ' + str(width + 20) + ',' + str(20) + ', ' + str(width + 40) + ',' + str(20))
            command.append('-draw')
            command.append('line ' + str(20) + ',' + str(height + 20) + ', ' + str(0) + ',' + str(height + 20))
            command.append('-draw')
            command.append('line ' + str(20) + ',' + str(height + 20) + ', ' + str(20) + ',' + str(height + 40))
            command.append('-draw')
            command.append('line ' + str(width + 20) + ',' + str(height + 20) + ', ' + str(width + 40) + ',' + str(height + 20))
            command.append('-draw')
            command.append('line ' + str(width + 20) + ',' + str(height + 20) + ', ' + str(width + 20) + ',' + str(height + 40))
            command.append(temp_dir + '/cut_mark_' + color + '.png')
            subprocess.Popen(command).wait()
            del command[:]

            command.append('convert')
            command.append(temp_dir + '/cut_mark_' + color + '.png')
            command.append('-colorspace')
            command.append(str(colormode).lower())
            command.append('-channel')
            command.append('K')
            command.append('-separate')
            command.append(temp_dir + '/cut_mark_' + color + '.png')
            subprocess.Popen(command).wait()
            del command[:]

            final_command.append(temp_dir + '/cut_mark_' + color + '.png')

        final_command.extend(['-set', 'colorspace', colormode, '-combine', temp_dir + '/cut_mark.tiff'])
        subprocess.Popen(final_command).wait()
