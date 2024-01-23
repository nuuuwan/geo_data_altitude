import os

import matplotlib.pyplot as plt
from utils import Log

log = Log('examples')


class Example:
    DPI = 300

    @staticmethod
    def write(py_file_name: str):
        base_name = os.path.basename(py_file_name)
        image_path = os.path.join('examples', f'{base_name}.png')

        ax = plt.gca()
        # Hide grid lines
        ax.grid(False)

        # Hide axes ticks
        ax.set_xticks([])
        ax.set_yticks([])

        plt.savefig(image_path, dpi=Example.DPI)
        log.info(f'Wrote {image_path}.')
        os.startfile(image_path)
        plt.close()

        print(
            f'''
### [{base_name}](examples/{base_name})

![{base_name}](examples/{base_name}.png)
        '''
        )
