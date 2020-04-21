# coding:utf-8

import os
import logging
import threading
import subprocess


class MayaPy(threading.Thread):
    logging.basicConfig()

    def __init__(self, __template_file, __language, __maya_log=True, **kwargs):
        threading.Thread.__init__(self)

        with open(__template_file, 'r') as file_handle:
            script_text = file_handle.read().format(**kwargs)

        if __language == 'mel':
            temp_script_text = ''
            for script in script_text.split('\n'):
                temp_script_text += "mel.eval('{mel}')\n".format(
                    mel=script.replace('\\', r'\\').replace('\r', '')
                )
            script_text = temp_script_text

        self.script = '{core_script}\n{script_text}'.format(
            core_script='import maya.standalone as standalone\n'
                        'standalone.initialize()\n'
                        'import maya.mel as mel\n',
            script_text=script_text
        )

        self.__logger = None

        self.__maya_log = __maya_log

    def run(self):
        self.__logger = logging.getLogger('[MayaPy] - ID({id})'.format(
            id=str(self.ident)
        ))
        self.__logger.info('Task Is Running...')

        file_path = r'{maya_path}\{thread_id}.py'.format(
            maya_path=os.getcwd(),
            thread_id=str(self.ident)
        )
        with open(file_path, 'w') as temp_file:
            temp_file.write(self.script)
        self.__logger.info('Temp Script Has Finished Writing...')

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        process = subprocess.Popen(
            r"{maya_path}\bin\mayapy.exe {temp_script_file_path}".format(
                maya_path=os.getcwd(),
                temp_script_file_path=file_path
            ),
            startupinfo=startupinfo,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        self.__logger.info('Program Is Open...')

        if self.__maya_log:
            while process.poll() is None:
                line = process.stdout.readline().strip()
                if line:
                    self.__logger.info(line)

        process.wait()

        if process.returncode == 0:
            self.__logger.info('Program Success')
        else:
            self.__logger.info('Program Failed')

        os.remove(file_path)
