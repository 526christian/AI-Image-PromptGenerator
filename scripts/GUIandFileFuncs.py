import random as rn
import gradio as gr
from subprocess import check_call
import json
import re
import os

scriptdir = os.path.dirname(os.path.abspath(__file__))

head, tail = os.path.split(scriptdir)

promptpath = os.path.join(head, 'prompts')

#putting log files in their own folder
log = os.path.join(head, 'outputs', 'log.txt')
outputdir = os.path.join(head, 'outputs')

#templates file
templatefile = os.path.join(head, 'jsons', 'templates.json')

#blacklists file
blacklistfile = os.path.join(head, 'jsons', 'blacklists.json')

#settings file
settingsfile = os.path.join(head, 'jsons', 'settings.json')

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
    with open(settingsfile, 'r') as f:
        settings = json.load(f)
    return settings


def loadlog():
    with open(log, 'r') as promptlog:
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
    with open(templatefile, 'r') as openfile:
        templates = json.load(openfile)
    return templates

def blacklistlist():
    with open(blacklistfile, "r") as keys:
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
    with open(blacklistfile, 'r') as bl:
        blacklists = json.load(bl)
    return blacklists

def updatetemplatebox(name):
    template = templates[name]
    return gr.update(value=template)

def updateblacklistbox(name):
    blacklist = blacklists[name]
    return gr.update(value=blacklist)

def hideA1111output(a1111):
    if not a1111:
        return gr.update(visible=False)

def hideinvokeoutput(invoke):
    if not invoke:
        return gr.update(visible=False)