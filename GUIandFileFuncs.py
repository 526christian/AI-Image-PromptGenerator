import json
import os

import gradio as gr

root = os.path.dirname(os.path.abspath(__file__))

promptpath = os.path.join(root, 'prompts')

#putting log files in their own folder
log = os.path.join(root, 'outputs', 'log.txt')
outputdir = os.path.join(root, 'outputs')

#templates file
templatefile = os.path.join(root, 'jsons', 'templates.json')

#blacklists file
blacklistfile = os.path.join(root, 'jsons', 'blacklists.json')

#settings file
settingsfile = os.path.join(root, 'jsons', 'settings.json')

def createblankmissingfiles():
    if not os.path.exists(log):
        with open(log, 'w') as file:
            file.write("\n")
    if not os.path.exists(templatefile):
        with open(templatefile,'w') as file:
            d = {}
            json.dump(d, file)
    if not os.path.exists(blacklistfile):
        with open(blacklistfile, 'w') as file:
            d = {}
            json.dump(d, file)


def loadsettings():
    with open(settingsfile) as f:
        return json.load(f)


def loadlog():
    with open(log) as promptlog:
        return promptlog.read()

def clearlog():
    with open(log, 'w') as promptlog:
        promptlog.close()

def getList(d):
    return [*d]

def templatelist():
    with open(templatefile, "r") as file:
        try:
            templates = json.load(file)
            key_list = list(templates.keys())
        except KeyError:
            key_list = "PlaceholderIfNoTemplatesFound"
    return key_list

def createtemplate(template, tempname):
    templates[tempname] = template
    with open(templatefile, "w") as savedtemps:
        json.dump(templates, savedtemps)

def openTemplates():
    global templates
    with open(templatefile) as openfile:
        templates = json.load(openfile)
    return templates

def blacklistlist():
    with open(blacklistfile) as keys:
        try:
            b = json.load(keys)
            key_blacks = list(b.keys())
        except KeyError:
            key_blacks = "PlaceholderIfNoBlacklistsFound"
    return key_blacks

def createblacklist(blacklist, blacklistname):
    blacklists[blacklistname] = blacklist
    with open(blacklistfile, "w") as savedblack:
        json.dump(blacklists, savedblack)

def openblacklist():
    global blacklists
    with open(blacklistfile) as bl:
        return json.load(bl)

def updatetemplatebox(name):
    return gr.update(value=templates[name])

def updateblacklistbox(name):
    return gr.update(value=blacklists[name])

def hideA1111output(a1111):
    if not a1111:
        return gr.update(visible=False)

def hideinvokeoutput(invoke):
    if not invoke:
        return gr.update(visible=False)
