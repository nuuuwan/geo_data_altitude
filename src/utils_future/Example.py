from utils import Log
import os
import matplotlib.pyplot as plt

log = Log('examples')

class Example:
    @staticmethod 
    def write(py_file_name: str):
        base_name = os.path.basename(py_file_name)
        image_path = os.path.join('examples', f'{base_name}.png')
        plt.savefig(image_path)
        log.info(f'Wrote {image_path}.')
        plt.close()

        print(f'''
[examples/{base_name}](examples/{base_name})

![{base_name}]({base_name}.png)
        ''')