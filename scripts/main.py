import random as rn
import gradio as gr
from subprocess import check_call
import json
import re
import os
import GUIandFileFuncs as guifi

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

def createprompt(template, blacklist, adj, sty, qual, matrix, count):
    global numadjectives
    global numstyles
    global numquality
    global usepromptmatrix
    numadjectives = adj
    numstyles = sty
    numquality = qual
    usepromptmatrix = matrix
    template = template
    blacklist = blacklist
    global specialkeys
    specialkeys = {
        "listadj": {"selectedlist": prompts["Adjectives"]["VisAdjs"],
                    "numsamples": numadjectives},
        "liststy": {"selectedlist": prompts["VisualModifiers"]["Styles"],
                    "numsamples": numstyles},
        "listqual": {"selectedlist": prompts["VisualModifiers"]["Qualities"],
                     "numsamples": numquality},
    }
    global outputprompt
    global outputs
    # from now on, any repetitive/large I/O actions should be saved outside of loops after completing them
    # to avoid bottlenecks
    outputs = []
    with open(log, 'r+') as logfile:
        for c in range(count):
            outputprompt = give_output(prompts, template, blacklist)
            outputs.append(outputprompt)
        existing_text = logfile.read()
        logfile.seek(0)
        logfile.write('\n\n'.join(reversed(outputs)) + '\n\n' + existing_text)
    return outputs[-1]

def build_dictionary(promptpath):
    global prompts
    prompts = {}
    for dirpath, dirnames, filenames in os.walk(promptpath):
        for filename in filenames:
            if filename.endswith(".txt"):
                with open(os.path.join(dirpath, filename), "r") as f:
                    content = f.readlines()
                    content = [line for line in content if not line.startswith("#")]
                    content = [line.strip() for line in content]
                    sub_dict = prompts
                    for subdir in os.path.relpath(dirpath, promptpath).split(os.sep):
                        sub_dict = sub_dict.setdefault(subdir, {})
                    keyname = filename.replace(".txt", "")
                    sub_dict[keyname] = content
    return prompts


def give_output(prompts, template, blacklist):
    keywords = re.findall(r'\[(.*?)\]', template)
    for word in keywords:
        if word in specialkeys:
            matchedlist = specialkeys[word]
            selection = list(filter(lambda i: i not in blacklist, matchedlist["selectedlist"]))
            if usepromptmatrix:
                output = ' | '.join(rn.sample(selection, matchedlist["numsamples"]))
            else:
                output = ', '.join(rn.sample(selection, matchedlist["numsamples"]))
        else:
            matchedlist = search_dict(prompts, word)
            selection = list(filter(lambda i: i not in blacklist, matchedlist))
            output = rn.choice(selection)
        template = re.sub(f'\[{word}\]', output, template, count=1)
    return template

def search_dict(prompts, target):
    if target in specialkeys:
        return specialkeys[target]
    for key, value in prompts.items():
        if key == target:
            if isinstance(value, dict):
                newout = search_dict(value, rn.choice(list(value.keys())))
                return newout
            else:
                return value
        if isinstance(value, dict):
            result = search_dict(value, target)
            if result:
                return result


def a1111export(a1111, a1111neg, a1111steps, a1111cfg, a1111sampler, a1111seed, a1111width,
                                           a1111height):
    filepath1 = os.path.join(outputdir, 'A1111list.txt')
    filepath2 = os.path.join(outputdir, 'A1111recent.txt')
    if not os.path.exists(filepath1):
        with open(filepath1, 'w') as file:
            file.write("\n")
    if not os.path.exists(filepath2):
        with open(filepath2, 'w') as file:
            file.write("\n")
    if a1111 == True:
        with open(filepath1, 'r+') as a1111log, open(filepath2, 'w') as a1111rec:
            #from now on, any repetitive/large I/O actions should be saved outside of loops after completing them
            #to avoid bottlenecks
            tosavea1111log = []
            initialseed = a1111seed
            for output in outputs:
                if initialseed == 1:
                    a1111seed = rn.randint(1, 1999999999)
                A1111output = (f'--prompt "{output}" --negative_prompt "{a1111neg}" '
                               f'--steps {a1111steps} --cfg_scale {a1111cfg} '
                               f'--sampler_name "{a1111sampler}" --seed {a1111seed}'
                               f' --width {a1111width} --height {a1111height}')
                tosavea1111log.append(A1111output)
            existing_text = a1111log.read()
            a1111log.seek(0)
            a1111log.write('\n\n'.join(reversed(tosavea1111log)) + '\n\n' + existing_text)
            a1111rec.write(A1111output)
            return gr.update(value=A1111output, visible=True)


def invokeexport(invoke, invneg, invwidth, invheight, inviter, invsteps, invcfg, invseed, invsampler,
                 invoutputdir, invhires, invgrid):
    filepath1 = os.path.join(outputdir, 'Invokelist.txt')
    filepath2 = os.path.join(outputdir, 'Invokerecent.txt')
    if not os.path.exists(filepath1):
        with open(filepath1, 'w') as file:
            file.write("\n")
    if not os.path.exists(filepath2):
        with open(filepath2, 'w') as file:
            file.write("\n")
    if invoke == True:
        with open(filepath1, 'r+') as invokelog, open(filepath2, 'w') as invokerec:
            #from now on, any repetitive/large I/O actions should be saved outside of loops after completing them
            #to avoid bottlenecks
            tosaveinvokelog = []
            initialseed = invseed
            for output in outputs:
                if initialseed == 1:
                    invseed = rn.randint(1, 1999999999)
                invoutput = (f'{output} [{invneg}] -W{invwidth} '
                             f'-H{invheight} -n{inviter} '
                             f'-s{invsteps} -C{invcfg} '
                             f'-S{invseed} -A{invsampler} '
                             f'-o{invoutputdir}')
                if invhires:
                    invoutput += (f' --hires_fix')
                if invgrid:
                    invoutput += (f' -g')
                tosaveinvokelog.append(invoutput)
            existing_text = invokelog.read()
            invokelog.seek(0)
            invokelog.write('\n\n'.join(reversed(tosaveinvokelog)) + '\n\n' + existing_text)
            invokerec.write(invoutput)
            return gr.update(value=invoutput, visible=True)
