from dicts import prompts
from dicts import print_dict_structure
import os

scriptdir = os.path.dirname(os.path.abspath(__file__))

expprompts = os.path.join(scriptdir, 'ExportedPrompts')

def main():
    print()
    cont = input(f'This script is for users who downloaded the prompt generator before the phrases were moved to .txt files.'
          f' If you have the old dicts.py and modified it, this will automatically export your existing dictionary into .txts.'
          f' Make sure this file is in the same folder as dicts.py, and press enter to continue.')
    if not cont:
        print()
        print_dict_structure(prompts)
        print()
        os.makedirs(expprompts, exist_ok=True)
        dict_to_files(prompts, expprompts)
        print(f'All done! Your phrase dictionary should be in a similar structure as seen above, inside a "Exported'
              f'Prompts" folder. You can now do whatever you wish with them, just make sure your files are put in the'
              f' "prompts" folder if you want to use them.')

def dict_to_files(prompts, expprompts):
    for key, value in prompts.items():
        path = os.path.join(expprompts, key)
        if isinstance(value, dict):
            os.makedirs(path, exist_ok=True)
            dict_to_files(value, path)
        elif isinstance(value, list):
            with open(os.path.join(expprompts, key + ".txt"), "w") as f:
                f.writelines([line + '\n' for line in value])
        else:
            with open(os.path.join(path, key + ".txt"), "w") as f:
                f.write(value)


if __name__ == "__main__":
    main()