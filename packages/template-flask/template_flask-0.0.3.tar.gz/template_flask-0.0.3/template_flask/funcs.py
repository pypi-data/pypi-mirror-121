import os
import venv
import subprocess
from random import choice, randrange
from template_flask.constants import *


def generate_random_secret_key():
    key = ''
    for i in range(0, 32):
        alpha = choice([chr(randrange(65, 91)), chr(randrange(97, 123))])
        num = chr(randrange(48, 58))
        sym = choice([chr(randrange(33, 48)), chr(randrange(58, 65)), chr(randrange(123, 127))])
        key += choice([alpha, num, sym])
    return key


def write_file(file_path, iterable_lines, fill=None):
    with open(file_path, 'w') as f:
        for line_number in iterable_lines:
            line_to_write = iterable_lines[line_number][0]
            needs_fill = iterable_lines[line_number][1]

            if needs_fill:
                f.write(f'{line_to_write.format(fill=fill)}\n')
            else:
                f.write(f'{line_to_write}\n')


def create_dir_and_venv(project_name: str, project_directory: str):
    full_path = os.path.join(project_directory, project_name)
    os.mkdir(full_path)

    venv_path = os.path.join(full_path, 'venv')
    venv.create(venv_path, with_pip=True)

    package_path = os.path.join(full_path, f'{project_name}_app')
    static_path = os.path.join(package_path, 'static')
    templates_path = os.path.join(package_path, 'templates')
    index_path = os.path.join(templates_path, 'index.html')
    config_path = os.path.join(package_path, 'config.py')
    routes_path = os.path.join(package_path, 'routes.py')
    models_path = os.path.join(package_path, 'models.py')
    run_path = os.path.join(package_path, 'run.py')
    init_path = os.path.join(package_path, '__init__.py')

    os.mkdir(package_path)
    os.mkdir(static_path)
    os.mkdir(templates_path)

    write_file(index_path, INDEX_HTML, fill=project_name)
    write_file(config_path, CONFIG, fill=generate_random_secret_key())
    write_file(routes_path, ROUTE, fill=project_name)
    write_file(models_path, MODEL, fill=project_name)
    write_file(run_path, RUN, fill=project_name)
    write_file(init_path, INIT, fill=project_name)


def activate_venv_and_install_reqs(project_name: str, project_directory: str):
    full_path = os.path.join(project_directory, project_name)
    reqs_path = os.path.join(full_path, 'requirements.txt')

    v = os.path.join('venv\Scripts', 'activate.bat')

    os.chdir(full_path)
    cmd1 = f'{v} & pip install {" ".join(REQUIREMENTS)} & deactivate'
    subprocess.check_output(cmd1, shell=True)
    print()

    cmd2 = f'{v} & pip freeze & deactivate'
    reqs = [x.decode('utf-8') for x in subprocess.check_output(cmd2, shell=True).splitlines()]

    print('Completed installing requirements into virtual environment\n')
    print('These packages have been automatically installed into virtual environment...')
    for req in reqs:
        print(req)
    print()

    with open(reqs_path, 'w') as f:
        for req in reqs:
            f.write(f"""{req}\n""")

    print('Completed writing initial "requirements.txt"\n')























