#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess #re, subprocess, simplestyle, os#inkex, os, random, sys, subprocess, shutil

def generate_final_file(isvector, colormode, width, height, strokewidth, bleedsize, marksize, temp_dir):
    if not isvector:

        command = []
        final_command = ['convert']

        for color in colormode:
            command.append('convert')
            command.append('-size')
            command.append(str(width + (marksize*2)) + 'x' + str(height + (marksize*2)))
            command.append('xc:white')
            command.append('-stroke')
            command.append('black')
            command.append('-strokewidth')
            command.append(str(strokewidth))
            command.append('-draw')
            command.append('line ' + str(marksize) + ',' + str(marksize + bleedsize) + ', ' + str(0) + ',' + str(marksize + bleedsize))
            command.append('-draw')
            command.append('line ' + str(marksize + bleedsize) + ',' + str(marksize) + ', ' + str(marksize + bleedsize) + ',' + str(0))
            command.append('-draw')
            command.append('line ' + str(marksize + width - bleedsize) + ',' + str(marksize) + ', ' + str(marksize + width - bleedsize) + ',' + str(0))
            command.append('-draw')
            command.append('line ' + str(marksize + width) + ',' + str(marksize + bleedsize) + ', ' + str(width + (marksize*2)) + ',' + str(marksize + bleedsize))
            command.append('-draw')
            command.append('line ' + str(marksize + width) + ',' + str(height + marksize - bleedsize) + ', ' + str((marksize*2) + width) + ',' + str(height + marksize - bleedsize))
            command.append('-draw')
            command.append('line ' + str(marksize + width - bleedsize) + ',' + str(height + marksize) + ', ' + str(marksize + width - bleedsize) + ',' + str(height + (marksize*2)))
            command.append('-draw')
            command.append('line ' + str(marksize + bleedsize) + ',' + str(height + marksize) + ', ' + str(marksize + bleedsize) + ',' + str(height + (marksize*2)))
            command.append('-draw')
            command.append('line ' + str(marksize) + ',' + str(height + marksize - bleedsize) + ', ' + str(0) + ',' + str(height - bleedsize + marksize))
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
