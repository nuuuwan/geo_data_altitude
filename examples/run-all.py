import os

def main():
    for file_name in os.listdir('examples'):
        if not (file_name.endswith('.py') and file_name.startswith('example')):
            continue    

        path = os.path.join('examples', file_name)
        os.system(f'python {path}')


if __name__ == '__main__':
    main()