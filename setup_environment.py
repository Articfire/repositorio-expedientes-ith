import os

def isWindows():
    if os.name == 'nt':
        return True
    return False

def main():
    run = os.system

    if isWindows():
        run('py -m venv venv')
        run('venv/Scripts/activate.bat')
        run('pip install -r librerias_necesarias.txt')
    else:
        run('python3 -m venv venv')
        run('source venv/bin/activate')
        run('pip install -r librerias_necesarias.txt')
    run('deactivate')

if __name__ == '__main__':
    main()
