import random as rn
import gradio as gr
from subprocess import check_call
import json
import re
import os
import sys
scriptdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(scriptdir, "scripts"))
import main as gen
import GUIandFileFuncs as guifi

def main():
    guifi.createblankmissingfiles()
    guifi.openTemplates()
    guifi.openblacklist()
    key_blacks = guifi.blacklistlist()
    key_list = guifi.templatelist()
    gen.build_dictionary(guifi.promptpath)
    with gr.Blocks() as demo:
        with gr.Tab("Generate"):
            with gr.Row():
                with gr.Column(scale=1, min_width=300):
                    type = gr.Dropdown(guifi.getList(key_list))
                    count = gr.Number(value=1, label="Number of prompts", precision=0)
                    template = gr.Textbox(label="Template", interactive=True, placeholder="Input text and bracketed references to lists, "
                                                                        "see default templates for examples")
                    adj = gr.Slider(label="Adjectives to list", minimum=0, maximum=10, value=4, step=1)
                    sty = gr.Slider(label="Styles to list", minimum=0, maximum=10, value=4, step=1)
                    qual = gr.Slider(label="Quality phrases to list", minimum=0, maximum=10, value=4, step=1)
                    matrix = gr.Checkbox(value=False, label="Prompt matrix for lists of phrases")
                    btn = gr.Button(value="Generate", variant="primary")
                    with gr.Accordion("Blacklists", open=False):
                        presetblacklist = gr.Dropdown(guifi.getList(key_blacks))
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
                    with gr.Accordion("Log", open=False):
                        logTextBox = gr.Textbox(label="Log", lines=30, max_lines=75)
                        clearLog = gr.Button(value= "Clear Log")

                    # log = gr.Textbox(loadpreviousprompts(previousprompts=), label="Log")
        with gr.Tab("Export Options"):
            with gr.Row():
                    with gr.Column(scale=1, min_width=350):
                        a1111 = gr.Checkbox(label="Save prompts in .txt for import in A1111 WebUI")
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
                        invoke = gr.Checkbox(label="Save prompts in .txt for import in InvokeAI / use InvokeAI CLI commands")
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
        type.change(fn=guifi.updatetemplatebox, inputs=type, outputs=template)
        presetblacklist.change(fn=guifi.updateblacklistbox, inputs=presetblacklist, outputs=blacklist)
        if template and tempname != "":
            savetemp.click(fn=guifi.createtemplate,inputs=[template, tempname], outputs=None)
        if blacklist and blackname != "":
            saveblack.click(fn=guifi.createblacklist, inputs=[blacklist, blackname], outputs=None)
        btn.click(gen.createprompt, inputs=[template, blacklist, adj, sty, qual, matrix, count], outputs=prompt)
        clearLog.click(fn=guifi.clearlog, inputs=None, outputs=None)
        a1111.change(fn=guifi.hideA1111output, inputs=a1111, outputs=a1111rec)
        invoke.change(fn=guifi.hideinvokeoutput, inputs=invoke, outputs=invokerec)
        prompt.change(fn=guifi.loadlog, inputs=None, outputs=logTextBox)
        prompt.change(fn=gen.a1111export, inputs=[a1111, a1111neg, a1111steps, a1111cfg, a1111sampler, a1111seed, a1111width,
                                        a1111height], outputs=a1111rec)
        prompt.change(fn=gen.invokeexport, inputs=[invoke, invneg, invwidth, invheight, inviter, invsteps,
                                           invcfg, invseed, invsampler, invoutputdir, invhires, invgrid], outputs=invokerec)
    demo.launch()

if __name__ == "__main__":
    main()
