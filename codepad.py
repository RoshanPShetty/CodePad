import smtplib, ssl
from socket import gaierror
import tkinter as tk
from tkinter import ttk 
from tkinter import font, filedialog, messagebox
import os
import datetime

# create the root, then hide it. The app will create its
# own windows as Toplevels
root = tk.Tk()
root.title('CodePad Text Editor')
root.geometry('1200x800')
root.withdraw()

# This is a global variable needed for the functions: New File and Open File
url = ''

#This is a global variable used for the statusbar and for exit_last_function
text_changed = False

#This is a global variable needed for the functions: hide_statusbar
show_statusbar = tk.BooleanVar()
show_statusbar.set(True)

#This is a global variable needed for the functions: darkmode
dm = tk.BooleanVar()
dm.set(False)

#This is a global variable needed for Fonts
# font family and font size functionality 
current_font_family = 'Arial'
current_font_size = 12

# I created this class in order for me to be able to create new windows with the same features as the original window
class AppWindow(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        self.root = root

        ############################# MAIN MENU #############################
        main_menu = tk.Menu(self)
        #FILE
        file = tk.Menu(main_menu, tearoff = False)

        #EDIT
        edit = tk.Menu(main_menu, tearoff = False)

        #FORMAT
        formating = tk.Menu(main_menu, tearoff = False)

        #VIEW
        view = tk.Menu(main_menu, tearoff = False)

        #HELP
        helping = tk.Menu(main_menu, tearoff = False)
        
        #CASCADE
        main_menu.add_cascade(label='File', menu=file)
        main_menu.add_cascade(label='Edit', menu=edit)
        main_menu.add_cascade(label='Format', menu=formating)
        main_menu.add_cascade(label='View', menu=view)
        main_menu.add_cascade(label='Help', menu=helping)
        ############################# END MAIN MENU #############################

        ############ -------------- TEXT EDITOR -------------- ############
        self.text = tk.Text(self)

        self.vsb = tk.Scrollbar(self)
        self.text.focus_set()
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.pack(fill=tk.BOTH, expand=True)
        self.vsb.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.vsb.set)

        ############ -------------- STATUS BAR -------------- ############
        status_bar = ttk.Label(self, text='Status Bar')
        status_bar.pack(side=tk.BOTTOM)

        def changed(event=None):
            if self.text.edit_modified():
                text_changed = True
                lines = len(self.text.get(1.0, 'end-1c').split('\n'))
                for columns in self.text.get(1.0, 'end-1c').split('\n'):
                    columns = len(columns)
                status_bar.config(text=f'Ln {lines} Col {columns}')
            self.text.edit_modified(False)        
        self.text.bind('<<Modified>>', changed)
        ############ -------------- END STATUS BAR -------------- ############
        ############ -------------- END TEXT EDITOR -------------- ############

        ############################# MAIN MENU FUNCTIONALITY #############################
        #FILE COMMANDS
        #NEW FILE FUNCTIONALITY
        def new_file(event=None):
            global url
            url = ''
            self.text.delete(1.0, tk.END)
        file.add_command(label='New File', compound=tk.LEFT, accelerator='Ctrl+N', command=new_file)
        
         #NEW WINDOW FUNCTIONALITY    
        def new_window(event=None):
            AppWindow(self.root)
        file.add_command(label='New Window', compound=tk.LEFT, accelerator='Ctrl+Alt+N', command=new_window)
        
         #OPEN FUNCTIONALITY
        def open_file(event=None):
            global url
            url = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File', filetypes=(('Text File', '*.text'), ('All Files', '*.*')))
            try:
                with open(url, 'r') as fileReader:
                    self.text.delete(1.0, tk.END)
                    self.text.insert(1.0, fileReader.read())
            except FileNotFoundError:
                return
            except:
                return
            self.title(os.path.basename(url))
        file.add_command(label='Open...', compound=tk.LEFT, accelerator='Ctrl+O', command=open_file)

        #SAVE FUNCTIONALITY
        def save_file(event=None):
            global url
            try:
                if url:
                    content = str(self.text.get(1.0, tk.END))
                    with open(url, 'w', encoding='utf-8') as fileWriter:
                        fileWriter(content)
                else:
                    url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', '*.text'), ('All Files', '*.*')))
                    content2 = self.text.get(1.0, tk.END)
                    url.write(content2)
                    url.close()
            except:
                return
        file.add_command(label='Save', compound=tk.LEFT, accelerator='Ctrl+S', command=save_file)

        #SAVE AS FUNCTIONALITY
        def save_as_file(event=None):
            global url
            try:
                content = self.text.get(1.0, tk.END)
                url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', '*.text'), ('All Files', '*.*')))
                url.write(content)
                url.close()
            except:
                return
        file.add_command(label='Save As...', compound=tk.LEFT, accelerator='Ctrl+Alt+S', command=save_as_file)
        file.add_command(label='Page Setup...', compound=tk.LEFT)
        file.add_command(label='Print...', compound=tk.LEFT, accelerator='Ctrl+P')

        #EXIT LAST WINDOW FUNCTIONALITY
        def exit_on_last_window(event=None):
            global url, text_changed
            try:
                if text_changed is True:                
            # Destroy the root window when no other windows exist
                    self.destroy()
                    if not any([window.winfo_exists() for window in self.root.winfo_children()]):
                        self.root.destroy()
                else:
                    mbox = messagebox.askyesnocancel('Warning', 'Do you want to save the file?')
                    if mbox is True:
                        if url:
                            content = self.text.get(1.0, tk.END)
                            with open(url, 'w', encoding='utf-8') as fileWriter:
                                fileWriter.write(content)
                            self.destroy()
                            if not any([window.winfo_exists() for window in self.root.winfo_children()]):
                                self.root.destroy()
                        else:
                            content2 = self.text.get(1.0, tk.END)
                            url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', '*.text'), ('All Files', '*.*')))
                            url.write(content)
                            url.close()
                            self.destroy()
                            if not any([window.winfo_exists() for window in self.root.winfo_children()]):
                                self.root.destroy()
                    elif mbox is False:
                        self.destroy()
                    if not any([window.winfo_exists() for window in self.root.winfo_children()]):
                        self.root.destroy()
            except:
                return 
        file.add_command(label='Exit', compound=tk.LEFT, accelerator="Ctrl+Q", command=exit_on_last_window)

        #EDIT COMMANDS
        edit.add_command(label='Undo', compound=tk.LEFT, accelerator='Ctrl+Z', command=lambda:self.text.event_generate("<Control z>"))
        edit.add_command(label='Cut', compound=tk.LEFT, accelerator='Ctrl+X', command=lambda:self.text.event_generate("<Control x>"))
        edit.add_command(label='Copy', compound=tk.LEFT, accelerator='Ctrl+C', command=lambda:self.text.event_generate("<Control c>"))
        edit.add_command(label='Paste', compound=tk.LEFT, accelerator='Ctrl+V', command=lambda:self.text.event_generate("<Control v>"))
        edit.add_command(label='Delete', compound=tk.LEFT, accelerator='Del', command=lambda:self.text.delete(1.0, tk.END))
        
        #FIND FUNCTIONALITY
        def find_func(event=None):
            def findAll():
                word = find_input.get()
                self.text.tag_remove('match', '1.0', tk.END)
                matches = 0
                if word:
                    start_position = '1.0'
                    while True:
                        start_position = self.text.search(word, start_position, stopindex=tk.END)
                        if not start_position:
                            break
                        end_position = f'{start_position}+{len(word)}c'
                        self.text.tag_add('match', start_position, end_position)
                        matches += 1
                        start_position = end_position
                        self.text.tag_config('match', foreground='black', background='yellow')
            
            def replace():
                word = find_input.get()
                replace_text = replace_input.get()
                content = self.text.get(1.0, tk.END)
                new_content = content.replace(word, replace_text)
                self.text.delete(1.0, tk.END)
                self.text.insert(1.0, new_content)

            find_dialogue = tk.Toplevel()
            find_dialogue.geometry('300x150')
            find_dialogue.title('Find/Replace')
            find_dialogue.resizable(0,0)

            #FRAME FOR THE DIALOGUE BOX
            find_frame = ttk.LabelFrame(find_dialogue, text='Find/Replace')
            find_frame.pack(pady=30)

            #LABELS
            text_find_label = ttk.Label(find_frame, text='Find : ')
            text_replace_label = ttk.Label(find_frame, text='Replace : ')

            #ENTRY
            find_input = ttk.Entry(find_frame, width=20)
            replace_input = ttk.Entry(find_frame, width=20)

            #BUTTON
            find_button = ttk.Button(find_frame, text='Find All', command=findAll)
            replace_button = ttk.Button(find_frame, text='Replace', command=replace)

            #LABEL GRID
            text_find_label.grid(row=0, column=0, padx=4, pady=4)
            text_replace_label.grid(row=1, column=0, padx=4, pady=4)
            
            #ENTRY GRID
            find_input.grid(row=0, column=1, padx=4, pady=4)
            replace_input.grid(row=1, column=1, padx=4, pady=4)

            #BUTTON GRID
            find_button.grid(row=0, column=2, padx=4, pady=4)
            replace_button.grid(row=1, column=2, padx=4, pady=4)
            find_dialogue.mainloop()

        edit.add_command(label='Find...', compound=tk.LEFT, accelerator='Ctrl+F', command=find_func)
        edit.add_command(label='Find All', compound=tk.LEFT, accelerator='Fn+F3', command=find_func)
        edit.add_command(label='Replace...', compound=tk.LEFT, accelerator='Ctrl+H', command=find_func)
        edit.add_command(label='Select All', compound=tk.LEFT, accelerator='Ctrl+A', command=lambda:self.text.event_generate("<Control a>"))
        def date_time(event=None):
            self.text.insert(1.0, str(datetime.datetime.now()))
        edit.add_command(label='Time/Date', compound=tk.LEFT, accelerator='Fn+F5', command=date_time)

        #FORMAT COMMANDS
        def wrapping(event=None):
            self.text.config(wrap='word', relief=tk.FLAT)
        formating.add_checkbutton(label='Word Wrap', onvalue=1, offvalue=False, compound=tk.LEFT, command=wrapping)
        
        #FONTS FUNCTIONALITY
        def fonts(event=None):
            Font = tk.font.Font()
            mainfont = Font
            #CONFIGURING THE TEXT TO THE FONT
            self.text.config(font=Font)
            #VARIABLES
            f = tk.StringVar()
            f.set(mainfont.actual('family'))
            s = tk.IntVar()
            s.set(mainfont.actual('size'))
            w = tk.StringVar()
            w.set(mainfont.actual('weight'))
            itls = tk.StringVar()
            itls.set(mainfont.actual('slant'))
            u = tk.IntVar()
            u.set(mainfont.actual('underline'))
            o = tk.IntVar()
            o.set(mainfont.actual('overstrike'))
            
            #FONT SAMPLE
            font_sample = tk.font.Font()
            for i in ['family', 'weight', 'slant', 'overstrike', 'underline', 'size']:
                font_sample[i] = mainfont.actual(i)
            
            #FUNCTIONS
            def checkface(event):
                try:
                    f.set(str(listbox.get(listbox.curselection())))
                    font_sample.config(family=f.get(), size=s.get(), weight=w.get(), slant=itls.get(), underline=u.get(), overstrike=o.get())
                except:
                    pass
            def checksize(event):
                try:
                    s.set(int(sizebox.get(sizebox.curselection())))
                    font_sample.config(family=f.get(), size=s.get(), weight=w.get(), slant=itls.get(), underline=u.get(), overstrike=o.get())
                except:
                    pass

            def applied():
                result = (f.get(), s.get(), w.get(), itls.get(), u.get(), o.get())
                mainfont['family'] = f.get()
                mainfont['size'] = s.get()
                mainfont['weight'] = w.get()
                mainfont['slant'] = itls.get()
                mainfont['underline'] = u.get()
                mainfont['overstrike'] = o.get()
            
            def out():
                result = (f.get(), s.get(), w.get(), itls.get(), u.get(), o.get())
                mainfont['family'] = f.get()
                mainfont['size'] = s.get()
                mainfont['weight'] = w.get()
                mainfont['slant'] = itls.get()
                mainfont['underline'] = u.get()
                mainfont['overstrike'] = o.get()
                font_dialogue.destroy()
            
            def end():
                result = None
                font_dialogue.destroy()

            #DIALOGUE BOX
            font_dialogue = tk.Toplevel()
            font_dialogue.title('Font')

            #MAINWINDOW
            mainwindow = ttk.Frame(font_dialogue)
            mainwindow.pack(padx=10, pady=10)

            #MAIN LABEL FRAME
            mainframe = ttk.Frame(mainwindow)
            mainframe.pack(side='top',ipady=30, ipadx=30,expand='no', fill='both')
            mainframe0 = ttk.Frame(mainwindow)
            mainframe0.pack(side='top', expand='yes', fill='x', padx=10, pady=10)
            mainframe1 = ttk.Frame(mainwindow)
            mainframe1.pack(side='top',expand='no', fill='both')
            mainframe2 = ttk.Frame(mainwindow)
            mainframe2.pack(side='top',expand='yes', fill='x', padx=10, pady=10)
            
            #FRAME IN MAIN LABEL FRAME
            font_frame = ttk.LabelFrame(mainframe, text='Select Font Face')
            font_frame.pack(side='left', padx=10, pady=10, ipadx=20, ipady=20, expand='yes', fill='both')
            size_frame = ttk.LabelFrame(mainframe, text='Select Font Size')
            size_frame.pack(side='left', padx=10, pady=10, ipadx=20, ipady=20, expand='yes', fill='both')
            ttk.Entry(font_frame, textvariable=f).pack(side='top', padx=5, pady=5, expand='yes', fill='x')
            listbox = tk.Listbox(font_frame)
            listbox.pack(side='top', padx=5, pady=5, expand='yes', fill='both')
            for i in tk.font.families():
                listbox.insert(tk.END, i)
            
            #FRAME IN MAIN LABEL FRAME 0
            bold = ttk.Checkbutton(mainframe0, text='Bold', onvalue='bold', offvalue='normal', variable=w)
            bold.pack(side='left',expand='yes', fill='x')
            italic = ttk.Checkbutton(mainframe0, text='Italic', onvalue='italic', offvalue='roman', variable=itls)
            italic.pack(side='left',expand='yes', fill='x')
            underline = ttk.Checkbutton(mainframe0, text='Underline', onvalue=1, offvalue=0, variable=u)
            underline.pack(side='left',expand='yes', fill='x')
            overstrike = ttk.Checkbutton(mainframe0, text='Overstrike', onvalue=1, offvalue=0, variable=o)
            overstrike.pack(side='left',expand='yes', fill='x')
            
            #FRAME IN MAIN LABEL FRAME 1 
            ttk.Entry(size_frame, textvariable=s).pack(side='top', padx=5, pady=5, expand='yes', fill='x')
            sizebox = tk.Listbox(size_frame)
            sizebox.pack(side='top', padx=5, pady=5, expand='yes', fill='both')
            for i in range(100):
                sizebox.insert(tk.END, 2*i)

            #SAMPLE BOX THAT IS STILL IN LABEL FRAME 1
            tk.Label(mainframe1, bg='white',text='''ABCDEabcde12345''', font=font_sample).pack(expand='no', padx=10,pady=10)
            
            #FRAME IN MAIN LABEL FRAME 2
            ttk.Button(mainframe2, text='   OK   ', command=out).pack(side='left', expand='yes', fill='x', padx=5, pady=5)
            ttk.Button(mainframe2, text=' Cancel ', command=end).pack(side='left', expand='yes', fill='x', padx=5, pady=5)
            ttk.Button(mainframe2, text=' Apply  ', command=applied).pack(side='left', expand='yes', fill='x', padx=5, pady=5)

            listbox.bind('<<ListboxSelect>>', checkface)
            sizebox.bind('<<ListboxSelect>>', checksize)

        formating.add_command(label='Font..', compound=tk.LEFT, accelerator='Ctrl+F1', command=fonts)
        formating.add_command(label='Format Document', compound=tk.LEFT, accelerator='Ctrl+Alt+F')
        
        #DARK MODE COMMANDS
        def darkmode(event=None):
            global dm
            if dm:
                self.text.config(bg='black', fg='white')
                dm = False
            else:
                self.text.config(bg='white', fg='black')
                dm = True
        formating.add_checkbutton(label='Dark Mode', onvalue=0, offvalue=1, variable=True, compound=tk.LEFT, accelerator='Ctrl+D', command=darkmode)

        #VIEW COMMANDS
        #ZOOMIN
        def zoomin(event=None):
            self.state('zoomed')
        view.add_command(label='Zoom In', compound=tk.LEFT, accelerator='Ctrl+Plus', command=zoomin)
        def zoomout(event=None):
            self.state('iconic')
        view.add_command(label='Zoom Out', compound=tk.LEFT, accelerator='Ctrl+1', command=zoomout)
        def zoomnorm(event=None):
            self.state('normal')
        view.add_command(label='Restore Default Zoom', compound=tk.LEFT, accelerator='Ctrl+0', command=zoomnorm)

        #HIDE STATUS BAR
        def hide_statusbar():
            global show_statusbar
            if show_statusbar:
                status_bar.pack_forget()
                show_statusbar = False
            else:
                status_bar.pack(side=tk.BOTTOM)
                show_statusbar = True
        view.add_checkbutton(label='Status Bar', onvalue=1, offvalue=False, variable=show_statusbar, compound=tk.LEFT, command=hide_statusbar)

        #HELP COMMANDS
        def view_help(event=None):
            find_dialogue = tk.Toplevel()
            # find_dialogue.geometry('300x150')
            find_dialogue.title('Help')
            find_dialogue.resizable(0,0)
            
            #FRAME FOR THE DIALOGUE BOX
            about_frame = ttk.LabelFrame(find_dialogue, text='Navigation Within CodePad')
            about_frame.pack(pady=30)

            #LABELS
            text_a_label = ttk.Label(about_frame, text='This is an exact replica of Notepad, implying the functions are the same of that of Notepad.\nThere are 5 menu options, each with a command that either has a shortcut or you must select it.\nYou can write anything on this text editor and it has new features such as dark mode and format document.\nThis makes it better than notepad due to its uniqueness.\nThe Help section contains 3 commands which are View Help, Send Feedback, and About CodePad.\nAny feedback you send it appreciated and would be tended to.\nThe details about the software is available in the About Codepad section.')

            #LABEL GRID
            text_a_label.grid(row=3, column=0, padx=4, pady=4)
                        
        helping.add_command(label='View Help', command=view_help)
        
        def feedback(event=None):
            def sendemail():
                port = 587  # For starttls
                smtp_server = "smtp.gmail.com"
                sender_email = find_email.get()  # Enter your address
                receiver_email = "youreverydaycoder@gmail.com"  # Enter receiver address
                password = "juxtaposephotos"
                message = find_message.get()

                context = ssl.create_default_context()
                try:
                    with smtplib.SMTP(smtp_server, port) as server:
                        server.ehlo()  # Can be omitted
                        server.starttls(context=context)
                        server.ehlo()  # Can be omitted
                        server.login(receiver_email, password)
                        server.sendmail(sender_email, receiver_email, message)
                        server.close()
                except (gaierror, ConnectionRefusedError):
                      messagebox.showerror('Failed to connect to the server.', 'Bad connection settings?')
                except smtplib.SMTPServerDisconnected:
                        messagebox.showerror('Failed to connect to the server.', 'Wrong user/password?')
                except smtplib.SMTPException as e:
                        messagebox.showerror('SMTP error occurred: ', str(e))
                else:
                    messagebox.showinfo('Sent','Your feedback has been sent.')
                    feedback_dialogue.destroy()

            feedback_dialogue = tk.Toplevel()
            feedback_dialogue.geometry('400x230')
            feedback_dialogue.title('Send Feedback')
            feedback_dialogue.resizable(0,0)

            #FRAME FOR THE DIALOGUE BOX
            feedback_frame = ttk.LabelFrame(feedback_dialogue, text='Email and Feedback')
            feedback_frame.pack(pady=30)

            #LABELS
            text_a_label = ttk.Label(feedback_frame, text='Email id: ')
            text_b_label = ttk.Label(feedback_frame, text='Feedback: ')
            # text_c_label = ttk.Label(feedback_frame, text='Password: ')

            #ENTRY
            find_email = ttk.Entry(feedback_frame, width=20)
            find_message = ttk.Entry(feedback_frame, width=20)
            # find_password = ttk.Entry(feedback_frame, width=20)

            #BUTTON
            send_button = ttk.Button(feedback_frame, text='Send', command=sendemail)

            #LABEL GRID
            text_a_label.grid(row=0, column=0, padx=4, pady=4)
            text_b_label.grid(row=2, column=0, padx=4, pady=4)
            # text_c_label.grid(row=1, column=0, padx=4, pady=4)
            
            #ENTRY GRID
            find_email.grid(row=0, column=1, padx=4, pady=4)
            find_message.grid(row=2, column=1, padx=4, pady=4)
            # find_password.grid(row=1, column=1, padx=4, pady=4)

            #BUTTON GRID
            send_button.grid(row=3, column=1, padx=4, pady=4)
            feedback_dialogue.mainloop()

        helping.add_command(label='Send Feedback', command=feedback)

        def aboutsection(event=None):
            about_dialogue = tk.Toplevel()
            about_dialogue.geometry('400x230')
            about_dialogue.title('About CodePad')
            about_dialogue.resizable(0,0)

            #FRAME FOR THE DIALOGUE BOX
            about_frame = ttk.LabelFrame(about_dialogue, text='About CodePad')
            about_frame.pack(pady=30)

            #LABELS
            text_a_label = ttk.Label(about_frame, text='RPS Softwares')
            text_b_label = ttk.Label(about_frame, text='Version 1')
            text_c_label = ttk.Label(about_frame, text='© 2020 RPS Softwares. All rights reserved')
            text_e_label = ttk.Label(about_frame, text='This software was created by Roshan Praveen Shetty.\nIt is the exact replica of Notepad but with new features such as dark mode and format document.')

            #LABEL GRID
            text_a_label.grid(row=3, column=0, padx=4, pady=4)
            text_b_label.grid(row=4, column=0, padx=4, pady=4)
            text_c_label.grid(row=5, column=0, padx=4, pady=4)
            text_e_label.grid(row=6, column=0, padx=4, pady=4)
            
        helping.add_command(label='About CodePad', command=aboutsection)
        ############ -------------- END MAIN MENU FUNCTIONALITY -------------- ############
        self.configure(menu=main_menu)
        # call a function to destroy the root window when the last
        # instance of AppWindow is destroyed
        self.wm_protocol("WM_DELETE_WINDOW", exit_on_last_window)
        
        #BINDS FOR SHORTCUT KEYS
        self.bind("<Control-n>", new_file)
        self.bind("<Control-Alt-n>", new_window)
        self.bind("<Control-o>", open_file)
        self.bind("<Control-s>", save_file)
        self.bind("<Control-Alt-s>", save_as_file)
        self.bind("<Control-f>", find_func)
        self.bind("<Control-q>", exit_on_last_window)
        self.bind("<Control-Alt-f>", find_func)
        self.bind("<Control-d>", darkmode)
        self.bind("<Control-=>", zoomin)
        self.bind("<Control-2>", zoomout)
        self.bind("<Control-0>", zoomnorm)
        self.bind("<F5>", date_time)
        self.bind("<Control-F1>", fonts)
        self.bind("<Control-h>", find_func)
        self.bind("<F3>", find_func)

# create the first window, then start the event loop
AppWindow(root)
root.mainloop()