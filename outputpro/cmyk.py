#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, subprocess, simplestyle, os#inkex, os, random, sys, subprocess, shutil

def calculateCMYK(red, green, blue):
    C = float()
    M = float()
    Y = float()
    K = float()

    if 1.00 - red < 1.00 - green:
        K = 1.00 - red
    else:
        K = 1.00 - green

    if 1.00 - blue < K:
        K = 1.00 - blue

    if K != 1.00:
        C = ( 1.00 - red   - K ) / ( 1.00 - K )
        M = ( 1.00 - green - K ) / ( 1.00 - K )
        Y = ( 1.00 - blue  - K ) / ( 1.00 - K )

    return [C, M, Y, K]

def clean_svg_color_definitions(svg):
    def change_colors(origin, tipo_cor):
        for i in range(len(str(origin).split(tipo_cor + ':'))):
            if str(str(origin).split(tipo_cor + ':')[i].split(';')[0]) in simplestyle.svgcolors.keys():
                numeros_da_cor = simplestyle.formatColoria(simplestyle.parseColor(str(str(origin).split(tipo_cor + ':')[i].split(';')[0])))
                origin = str(origin).replace(':' + str(str(origin).split(tipo_cor + ':')[i].split(';')[0]) + ';', ':' + numeros_da_cor + ';')
        return origin

    colortypes = ['fill', 'stop-color', 'flood-color', 'lighting-color', 'stroke']
    for i in range(len(colortypes)):
        svg = change_colors(svg, colortypes[i])

    return svg

def removeK(origem):
    def zerar_opacidade(valor):
        return str(valor.group()).split('opacity:')[0] + "opacity:0;"
    #return re.sub("#000000;fill-opacity:[0-9.]+;", zerar_opacidade, re.sub("#000000;stop-opacity:[0-9.]+;", zerar_opacidade, re.sub("#000000;stroke-opacity:[0-9.]+;", zerar_opacidade, re.sub("#000000;flood-opacity:[0-9.]+;", zerar_opacidade, re.sub("#000000;lighting-opacity:[0-9.]+;", zerar_opacidade, origem)))))
    return re.sub("#000000;fill-opacity:[0-9.?]+", zerar_opacidade, re.sub("#000000;stop-opacity:[0-9.?]+", zerar_opacidade, re.sub("#000000;stroke-opacity:[0-9.?]+", zerar_opacidade, re.sub("#000000;flood-opacity:[0-9.?]+", zerar_opacidade, re.sub("#000000;lighting-opacity:[0-9.?]+", zerar_opacidade, origem)))))

def representC(value):
    # returns CMS color if available
    if (re.search("icc-color", value.group()) ):
        return simplestyle.formatColor3f(float(1.00 - float(re.split('[,\)\s]+',value.group())[2])), float(1.00), float(1.00))
    else:
        red =   float(simplestyle.parseColor(str(value.group()))[0]/255.00)
        green = float(simplestyle.parseColor(str(value.group()))[1]/255.00)
        blue =  float(simplestyle.parseColor(str(value.group()))[2]/255.00)
        return simplestyle.formatColor3f(float(1.00 - calculateCMYK(red, green, blue)[0]), float(1.00), float(1.00))

def representM(value):
    # returns CMS color if available
    if ( re.search("icc-color", value.group()) ):
        return simplestyle.formatColor3f(float(1.00), float(1.00 - float(re.split('[,\)\s]+',value.group())[3])), float(1.00))
    else:
        red =   float(simplestyle.parseColor(str(value.group()))[0]/255.00)
        green = float(simplestyle.parseColor(str(value.group()))[1]/255.00)
        blue =  float(simplestyle.parseColor(str(value.group()))[2]/255.00)
        return simplestyle.formatColor3f(float(1.00), float(1.00 - calculateCMYK(red, green, blue)[1]), float(1.00))

def representY(value):
    # returns CMS color if available
    if (re.search("icc-color", value.group()) ):
        return simplestyle.formatColor3f(float(1.00), float(1.00), float(1.00 - float(re.split('[,\)\s]+',value.group())[4])))
    else:
        red =   float(simplestyle.parseColor(str(value.group()))[0]/255.00)
        green = float(simplestyle.parseColor(str(value.group()))[1]/255.00)
        blue =  float(simplestyle.parseColor(str(value.group()))[2]/255.00)
        return simplestyle.formatColor3f(float(1.00), float(1.00), float(1.00 - calculateCMYK(red, green, blue)[2]))

def representK(value):
    # returns CMS color if available
    if (re.search("icc-color", value.group()) ):
        return simplestyle.formatColor3f(float(1.00 - float(re.split('[,\)\s]+',value.group())[5])), float(1.00 - float(re.split('[,\)\s]+',value.group())[5])), float(1.00 - float(re.split('[,\)\s]+',value.group())[5])))
    else:
        red =   float(simplestyle.parseColor(str(value.group()))[0]/255.00)
        green = float(simplestyle.parseColor(str(value.group()))[1]/255.00)
        blue =  float(simplestyle.parseColor(str(value.group()))[2]/255.00)
        return simplestyle.formatColor3f(float(1.00 - calculateCMYK(red, green, blue)[3]), float(1.00 - calculateCMYK(red, green, blue)[3]), float(1.00 - calculateCMYK(red, green, blue)[3]))


def generate_svg_separations(temp_dir, original_source, overblack):
    svg_ready = clean_svg_color_definitions(original_source)

    open(temp_dir + "separationK.svg","w").write(re.sub("#[a-fA-F0-9]{6}( icc-color\(.*?\))?", representK, svg_ready))

    if overblack:
        svg_ready = removeK(svg_ready)

    open(temp_dir + "separationC.svg","w").write(re.sub("#[a-fA-F0-9]{6}( icc-color\(.*?\))?", representC, svg_ready))
    open(temp_dir + "separationM.svg","w").write(re.sub("#[a-fA-F0-9]{6}( icc-color\(.*?\))?", representM, svg_ready))
    open(temp_dir + "separationY.svg","w").write(re.sub("#[a-fA-F0-9]{6}( icc-color\(.*?\))?", representY, svg_ready))

def generate_png_separations(temp_dir, area_to_export, resolution, alpha):
    if alpha:
        alpha_command = ""
    else:
        alpha_command = " --export-background=white "
    string_inkscape_exec = ''
    for color in ['C', 'M', 'Y', 'K']:
        string_inkscape_exec += temp_dir + "separation" + color + ".svg " + area_to_export + ' --export-png=' + temp_dir + "separated" + area_to_export.replace(' ', '') + color + ".png" + alpha_command + ' --export-dpi=' + str(resolution) + "\n"

    open('/tmp/teste.txt', 'w').write(string_inkscape_exec)

    inkscape_exec = subprocess.Popen(['inkscape -z --shell'], shell=True, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'), stdin=subprocess.PIPE)
    inkscape_exec.communicate(input=string_inkscape_exec)



