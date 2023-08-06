import os
from time import sleep
from template_flask.funcs import create_dir_and_venv, activate_venv_and_install_reqs


if __name__ == '__main__':

    p_name = input('\nEnter the name of your project: ')
    p_path = os.getcwd()

    create_dir_and_venv(p_name, p_path)
    print('Created virtual environment and directory structure')

    activate_venv_and_install_reqs(p_name, p_path)

    print('Completed setup')
    print('Exiting...')
    sleep(1)