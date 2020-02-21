# coding: utf-8

from cx_Freeze import setup, Executable

exe = executables = [Executable('main.py')]
build_options = dict(excludes = ["tkinter"], includes =["idna.idnadata"], optimize=1)

setup(name='GGC',
      version='1.0.0.1',
      description='Genetic Algorithm Technologies',
      executables=executables,
      options =dict(build_exe = build_options))