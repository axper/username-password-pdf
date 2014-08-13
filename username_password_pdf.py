#!/usr/bin/env python
# -*- coding: utf-8


from __future__ import print_function
import Tkinter
import tkFont
import sys
import subprocess
import random
import os


def valid_pass(test_password, all_symbols):
    return all(set(test_password) & set(x) for x in all_symbols)

def get_password():
    length = 10

    all_symbols = 'ABCDEFGHJKLMNPQRSTUVWXYZ',\
                  'abcdefghjklmnpqrstuvwxyz',\
                  '23456789'

    if length < len(all_symbols):
        raise ValueError('must be at least {}'
                         ' characters long!'.format(len(all_symbols)))
    new_password = ''
    while not valid_pass(new_password, all_symbols):
        new_password = ''.join(random.choice(''.join(all_symbols))
                               for _ in xrange(length))

    return new_password


def secure_delete(path, passes=1):
    random.seed()
    with open(path, 'ab') as delfile:
        length = delfile.tell()
        for _ in xrange(passes):
            delfile.seek(0)
            for _ in xrange(length):
                delfile.write(str(random.randrange(256)))

    os.remove(path)


def compile_latex(filename_tex):
    ''' Compiles the filename_tex to PDF using xelatex
        LaTeX distribution is first searched in $PATH.
        If not found, it looks for a local miktex_portable directory.

        Returns True if successful, False otherwise
    '''
    try:
        print('Trying miktex_portable.')
        subprocess.call(['miktex_portable\\miktex\\bin\\xelatex.exe',
                         filename_tex])
        print('Compilation using miktex_portable successful.')
    except OSError:
        print('Did not find miktex_portable. Trying $PATH.')
        try:
            subprocess.call(['xelatex', filename_tex])
            print('Compilation using $PATH successful.')
        except OSError:
            print('Could not find in $PATH either. Aborting')
            return False

    return True


def view_file(filename):
    ''' Opens a file in OS's default file viewer '''
    if sys.platform.startswith('linux'):
        subprocess.call(['xdg-open', filename])
    else:
        os.startfile(filename)


def remove_dangerous_files():
    print('Removing dangerous files')

    secure_delete('username.txt')
    secure_delete('password.txt')

    print('Removed dangerous files')


def get_username():
    return 'username'


def create_pdf(username_entry, password_entry):
    username = username_entry.get()
    if len(username) == 0:
        print('No username! Aborting.')
        return

    password = password_entry.get()
    if len(password) <= 1:
        print('Password too small! Aborting.')
        return

    with open('username.txt', 'w') as file_username:
        file_username.write(username)
    with open('password.txt', 'w') as file_password:
        file_password.write(password)

    if not compile_latex('usernote.tex'):
        print('Aborting...')
        return

    view_file('usernote.pdf')

    remove_dangerous_files()

    print('####### Generation successfully completed. #######')


def update_password(field):
    field.delete(0, Tkinter.END)
    field.insert(0, get_password())


def main():
    top = Tkinter.Tk()
    top.title('Password & PDF generator')

    monospace_font = tkFont.Font(family='monospace', size=11)

    username_label = Tkinter.Label(text='Username:')
    username_label.grid(row=0, column=0)

    username_entry = Tkinter.Entry(top, font=monospace_font)
    username_entry.grid(row=0, column=1)


    password_label = Tkinter.Label(text='Password:')
    password_label.grid(row=1, column=0)

    password_entry = Tkinter.Entry(top, font=monospace_font)
    password_entry.grid(row=1, column=1)


    button_update_password = Tkinter.Button(top,
                                            text='Generate New Password',
                                            command=
                                            lambda:
                                            update_password(password_entry))
    button_update_password.grid(row=1, column=2)

    button_create_pdf = Tkinter.Button(top,
                                       text='Create PDF',
                                       command=lambda:
                                       create_pdf(username_entry,
                                                  password_entry))
    button_create_pdf.grid(row=2, column=0, columnspan=3)


    update_password(password_entry)

    top.mainloop()

if __name__ == '__main__':
    main()
