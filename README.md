# AI-Image-PromptGenerator
A flexible UI script to help create and expand on prompts for generative AI art models, such as Stable Diffusion and MidJourney. Get inspired, and create. Multi-platform, and completely independent.

## Features

### Keyword-based system with configurable templates
![Peek 2023-01-28 05-09](https://user-images.githubusercontent.com/122599135/215260744-5788b9fc-0265-40a4-b783-0d8cac4d7ed3.gif)

Input names of lists in the phrase dictionary to get a random selection, and use the special keywords [listadj], [liststy], and [listqual] to get a list of random visual adjectives, styles, and image quality tokens. Fill in random phrases to add some flavor to your prompts, or come up with new ones entirely.

### Automatic1111 and InvokeAI export support
![Peek 2023-01-28 05-18](https://user-images.githubusercontent.com/122599135/215261325-180534af-7b4c-4469-8271-715ff2957752.gif)
![Selection_234](https://user-images.githubusercontent.com/122599135/215261452-fb5ad457-0277-4a77-a254-a4452cb2feba.png)

Get prompts generated in command-line format for Automatic1111 and InvokeAI to easily queue up lists of prompts to be generated with Stable Diffusion, and with logs to import from text file.

### Custom prompt template saving
![Peek 2023-01-28 05-30](https://user-images.githubusercontent.com/122599135/215261786-af3404f2-0bf4-4a3d-abbc-f0ef3bfa6551.gif)

Save whatever you type in the template box to conveniently access in the dropdown later, text and keywords and all.

### Phrase blacklisting
![Peek 2023-01-28 05-24](https://user-images.githubusercontent.com/122599135/215261561-ff030bf9-0f4e-4778-b68b-4ea5fc57b656.gif)

Don't want certain phrases in your outputs, but don't want to delete them completely? Add them to the blacklist, and they'll be automatically yoinked out without affecting the random selections (as long as you don't blacklist every single word in the lists!)

### And more to come...

Some planned features include:

* Settings / state saving
* New, and more specific phrase lists and categories
* A complete restructure of the phrase selection system to add your own lists and categories easier
* A prompt log box

## Install & startup

### Prerequisites
To run this script all you need is:

*[Python3 installed](https://www.python.org/downloads/) on your system

That's it. You'll also need a web browser, but presumably, you already have one if you're reading this. To install Python3 if you haven't already, pick a version for your OS, and run the provided installer.

With Python3 out-of-the-way, open up a terminal / command prompt window, and type pip install gradio
![Peek 2023-01-28 05-45](https://user-images.githubusercontent.com/122599135/215262432-5c6b48d1-1caa-4f13-bb1a-310c2f47e54c.gif)

## Running the script
And now you're ready to run the script whenever you please. All you'll have to do is access the script with a single command, 
`python path/to/promptgen.py`:
![Peek 2023-01-28 05-54](https://user-images.githubusercontent.com/122599135/215262858-05419e00-0618-4553-bb19-1a8868b721b8.gif)

It's best to keep the script and its dependent files in a folder that you can access easily. That'll make it easier to cd to the directory, or simply just drag-and-drop the script into the CLI.

