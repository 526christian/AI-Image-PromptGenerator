import random as rn
import gradio as gr
from subprocess import check_call
from dicts import prompts
import promptgen as pr
import json
import re

def createprompt(template, blacklist, adj, sty, qual, matrix):
    global numadjectives
    global numstyles
    global numquality
    global usepromptmatrix
    global promptlog
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
    outputprompt = give_output(prompts, template, blacklist)
    print(f'\n{outputprompt}\n')
    previousprompts.append(outputprompt)
    promptlog = loadpreviousprompts(previousprompts)
    return outputprompt

previousprompts = []

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


def loadsettings():
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    return settings


def A1111export(a1111, a1111neg, a1111steps, a1111cfg, a1111sampler, a1111seed, a1111width,
                                           a1111height):
    if a1111:
        if a1111seed == 1:
            a1111seed = rn.randint(1, 1999999999)
        A1111output = (f'--prompt "{outputprompt}" --negative_prompt "{a1111neg}" '
                       f'--steps {a1111steps} --cfg_scale {a1111cfg} '
                       f'--sampler_name "{a1111sampler}" --seed {a1111seed}'
                       f' --width {a1111width} --height {a1111height}')
        with open('A1111list.txt', 'a') as file:
            saveout = A1111output + (f'\n\n')
            file.write(saveout)
        with open('A1111recent.txt', 'w') as file:
            file.write(A1111output)
        return gr.update(value=A1111output, visible=True)

def invokeexport(invoke, invneg, invwidth, invheight, inviter, invsteps, invcfg, invseed, invsampler,
                 invoutputdir, invhires, invgrid):
    if invoke:
        if invseed == 1:
            invseed = rn.randint(1, 1999999999)

        invoutput = (f'{outputprompt} [{invneg}] -W{invwidth} '
                     f'-H{invheight} -n{inviter} '
                     f'-s{invsteps} -C{invcfg} '
                     f'-S{invseed} -A{invsampler} '
                     f'-o{invoutputdir}')
        if invhires:
            invoutput += (f' --hires_fix')
        if invgrid:
            invoutput += (f' -g')
        with open('Invokelist.txt', 'a') as file:
            saveinvout = invoutput + (f'\n\n')
            file.write(saveinvout)
        with open('Invokerecent.txt', 'w') as file:
            file.write(invoutput)
        return gr.update(value=invoutput, visible=True)


def copy2clip(txt): #Only works on windows, if it were mac '|clip' would be replaced with '|pbcopy' .
    cmd='echo '+txt.strip()+'|clip'
    return check_call(cmd, shell=True)


def loadpreviousprompts(previousprompts):
    log = ""
    for p in previousprompts:
        log += p + ' \n '
    return log

def getList(d):
    return [*d]


def templatelist():
    with open("templates.json", "r") as file:
        templates = json.load(file)
    key_list = list(templates.keys())
    return key_list

def createtemplate(template, tempname):
    templates[tempname] = template
    with open("templates.json", "w") as savedtemps:
        json.dump(templates, savedtemps)

def openTemplates():
    with open('templates.json', 'r') as openfile:
        templates = json.load(openfile)
    return templates

def blacklistlist():
    with open("blacklists.json", "r") as keys:
        b = json.load(keys)
    key_blacks = list(b.keys())
    return key_blacks

def createblacklist(blacklist, blacklistname):
    blacklists[blacklistname] = blacklist
    with open("blacklists.json", "w") as savedblack:
        json.dump(blacklists, savedblack)

def openblacklist():
    with open('blacklists.json', 'r') as bl:
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

def main():
    global templates
    global settings
    global blacklists
    settings = loadsettings()
    templates = openTemplates()
    blacklists = openblacklist()
    key_blacks = blacklistlist()
    key_list = templatelist()
    with gr.Blocks() as demo:
        with gr.Tab("Generate"):
            with gr.Row():
                with gr.Column(scale=1, min_width=300):
                    type = gr.Dropdown(getList(key_list))
                    template = gr.Textbox(label="Template", interactive=True, placeholder="Input text and bracketed references to lists, "
                                                                        "see default templates for examples")
                    adj = gr.Slider(label="Adjectives to list", minimum=0, maximum=10, value=4, step=1)
                    sty = gr.Slider(label="Styles to list", minimum=0, maximum=10, value=4, step=1)
                    qual = gr.Slider(label="Quality phrases to list", minimum=0, maximum=10, value=4, step=1)
                    matrix = gr.Checkbox(value=False, label="Prompt matrix for lists of phrases")
                    btn = gr.Button(value="Generate", variant="primary")
                    with gr.Accordion("Blacklists", open=False):
                        presetblacklist = gr.Dropdown(getList(key_blacks))
                        blacklist = gr.Textbox(label="Blacklist",
                                               placeholder="Input words separated with commas you want "
                                                           "to omit")
                with gr.Column(scale=1, min_width=350):
                    prompt = gr.Textbox(label="Prompt")
                    a1111rec = gr.Textbox(label="A1111 prompt", visible=False)
                    invokerec = gr.Textbox(label="InvokeAI CLI prompt", visible=False)
                    with gr.Accordion("Template/blacklist savers", open=False):
                        tempname = gr.Textbox(label="Template name", placeholder="Hint: Use existing name to overwrite "
                                                                                 "that template. Restart to have template "
                                                                                 "in dropdown menu.")
                        savetemp = gr.Button(value="Save current template")
                        blackname = gr.Textbox(label="Blacklist name", placeholder="Hint: Use existing name to overwrite "
                                                                                 "that blacklist. Restart to have blacklist "
                                                                                 "in dropdown menu.")
                        saveblack = gr.Button(value="Save current blacklist")
                    # log = gr.Textbox(loadpreviousprompts(previousprompts=), label="Log")
        with gr.Tab("Export Options"):
            with gr.Row():
                    with gr.Column(scale=1, min_width=350):
                        a1111 = gr.Checkbox(value=False, label="Save prompts in .txt for import in A1111 WebUI")
                        a1111neg = gr.Textbox(label="Negative prompt", placeholder="Reminder: parentheses around ((tokens))"
                                                                                   " for extra emphasis")
                        a1111steps = gr.Slider(label="Sampling steps", minimum=5, maximum=150, value=30, step=1)
                        a1111cfg = gr.Slider(label="CFG scale", minimum=0, maximum=100, value=8.0, step=0.5)
                        a1111sampler = gr.Dropdown(["Euler a", "Euler", "LMS", "Heun", "DPM2", "DPM2 a", "DPM++ 2S a",
                                                    "DPM++ 2M", "DPM++ SDE", "DPM fast", "DPM adaptive", "LMS Karras",
                                                    "DPM2 Karras", "DPM2 a Karras", "DPM++ 2S a Karras",
                                                    "DPM++ 2M Karras", "DPM++ SDE Karras", "DDIM", "PLMS"],
                                                   label="Sampler (hint: _a 'ancestral' "
                                                                            "samplers add noise to change image"
                                                                                       " with more steps)",  value="DPM2 Karras")
                        a1111seed = gr.Number(value=1, label="Seed (leave at 1 for random seed)")
                        a1111width = gr.Slider(label="Image width", minimum=64, maximum=2048, value=512, step=64)
                        a1111height = gr.Slider(label="Image height", minimum=64, maximum=2048, value=704, step=64)
                    with gr.Column(scale=1, min_width=350):
                        invoke = gr.Checkbox(value=False,
                                         label="Save prompts in .txt for import in InvokeAI / use InvokeAI CLI commands")
                        invneg = gr.Textbox(label="Negative prompt", placeholder="Reminder: + next to token or "
                                                                                      "phrase in parentheses for more emphasis,"
                                                                                      " - for less emphasis")
                        invwidth = gr.Slider(label="Image width", minimum=64, maximum=2048, value=512, step=64)
                        invheight = gr.Slider(label="Image height", minimum=64, maximum=2048, value=704, step=64)
                        inviter = gr.Number(label="Images to generate per prompt", value=1)
                        invsteps = gr.Slider(label="Sampling steps", minimum=5, maximum=150, value=30, step=1)
                        invcfg = gr.Slider(label="CFG scale", minimum=0, maximum=100, value=8.0, step=0.5)
                        invseed = gr.Number(label="Seed (set at 1 for random seed)", value=1)
                        invsampler = gr.Dropdown(["DDIM", "PLMS", "k_lms", "k_dpm_2", "k_dpm_2_a", "k_dpmpp_2", "k_dpmpp_2_a",
                                                  "k_euler", "k_euler_a", "k_heun"], label="Sampler (hint: _a 'ancestral' "
                                                                                       "samplers add noise to change image"
                                                                                       " with more steps)", value="k_dpmpp_2")
                        invoutputdir = gr.Textbox(label="Image output directory (from /invokeai/)",
                                                  placeholder="Default: outputs/promptgen", value="outputs/promptgen")
                        invhires = gr.Checkbox(label="Toggle hires fix to improve coherence beyond 512x512 resolution",
                                               value=True)
                        invgrid = gr.Checkbox(label="Toggle placing images in a series in a grid", value=False)
        type.change(fn=updatetemplatebox, inputs=type, outputs=template)
        presetblacklist.change(fn=updateblacklistbox, inputs=presetblacklist, outputs=blacklist)
        if template and tempname != "":
            savetemp.click(fn=createtemplate,inputs=[template, tempname], outputs=None)
        if blacklist and blackname != "":
            saveblack.click(fn=createblacklist, inputs=[blacklist, blackname], outputs=None)
        a1111.change(fn=hideA1111output, inputs=a1111, outputs=a1111rec)
        invoke.change(fn=hideinvokeoutput, inputs=invoke, outputs=invokerec)
        btn.click(createprompt, inputs=[template, blacklist, adj, sty, qual, matrix], outputs=prompt)
        #if conditions necessary to avoid Gradio causing a race condition from executing invokeexport and A1111export
        #in parallel with createprompt
        if a1111:
            btn.click(fn=A1111export, inputs=[a1111, a1111neg, a1111steps, a1111cfg, a1111sampler, a1111seed, a1111width,
                                            a1111height], outputs=a1111rec)
        if invoke:
            btn.click(fn=invokeexport, inputs=[invoke, invneg, invwidth, invheight, inviter, invsteps,
                                               invcfg, invseed, invsampler, invoutputdir, invhires, invgrid], outputs=invokerec)
    demo.launch()

if __name__ == "__main__":
    main()
