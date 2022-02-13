#!/usr/bin/env python3
import pathlib
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mb
import tkinter.ttk as ttk
from lxml.etree import XMLSyntaxError
import logging
import argparse
import os

from MangaManager.MangaTaggerLib.models import LoadedComicInfo
from MangaManager.MangaTaggerLib.cbz_handler import ReadComicInfo, WriteComicInfo
from MangaManager.MangaTaggerLib.errors import *
# logging.getLogger('PIL').setLevel(logging.WARNING)

launch_path =""
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)]
                    # filename='/tmp/myapp.log'
                    )

velog = logging.info
delog = logging.debug


ScriptDir = os.path.dirname(__file__)
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "MangaTagger.ui"

class MangataggerApp():

    def __init__(self,master=None):
        self.master = master
        self.spinbox_1_year_var = tk.IntVar(value=-1,name="year")
        self.spinbox_2_month_var = tk.IntVar(value=-1, name='month')
        self.spinbox_3_volume_var = tk.IntVar(value=-1, name='volume')

        self.spinbox_4_chapter_var = tk.StringVar(value='', name='chapter')
        self.label_14_langIso_var = tk.StringVar(value='Language ISO', name='langIso')
        self.entry_10_langIso_var = tk.StringVar(value='', name='langIso')
        # self.spinbox_5_pageCount_var = tk.IntVar(value='', name='pageCount')
        self.spinbox_5_pageCount_var = tk.IntVar(value=0, name='pageCount')
        self.entry_15_format_var = tk.StringVar(value='', name='format')
        self.entry_18_blackWhite_var = tk.StringVar(value='', name='blackWhite')
        self.entry_19_manga_var = tk.StringVar(value='', name='manga')
        self.entry_1_seriesName_var = tk.StringVar(value='', name='seriesName')
        self.entry_2_title_var = tk.StringVar(value='', name='title')
        self.entry_3_writer_var= tk.StringVar(value='', name='writer')
        self.entry_6_storyArc_var = tk.StringVar(value='', name='storyArc')
        self.entry_7_SeriesGroup_var = tk.StringVar(value='', name='SeriesGroup')
        self.entry_4_penciller_var = tk.StringVar(value='', name='penciller')
        self.entry_5_inker_var = tk.StringVar(value='', name='inker')
        self.entry_8_colorist_var = tk.StringVar(value='', name='colorist')
        self.entry_9_letterer_var = tk.StringVar(value='', name='letterer')
        self.entry_11_coverArtist_var = tk.StringVar(value='', name='coverArtist')
        self.entry_12_editor_var = tk.StringVar(value='', name='editor')
        self.entry_13_publisher_var = tk.StringVar(value='', name='publisher')
        self.entry_14_imprint_var = tk.StringVar(value='', name='imprint')
        self.entry_16_characters_var = tk.StringVar(value='', name='characters')
        self.entry_15_genres_var = tk.StringVar(value='', name='genres')
        self.entry_16_tags_var = tk.StringVar(value='', name='tags')
        self.entry_17_web_var = tk.StringVar(value='', name='web')
        self.entry_20_scanInfo_var = tk.StringVar(value='', name='scanInfo')
        self.widgets_var = [
            self.entry_1_seriesName_var,
            self.entry_2_title_var,
            self.entry_3_writer_var,
            self.entry_4_penciller_var,
            self.entry_5_inker_var,
            self.entry_6_storyArc_var,
            self.entry_7_SeriesGroup_var,
            self.entry_8_colorist_var,
            self.entry_9_letterer_var,
            self.entry_10_langIso_var,
            self.entry_11_coverArtist_var,
            self.entry_12_editor_var,
            self.entry_13_publisher_var,
            self.entry_14_imprint_var,
            self.entry_15_format_var,
            self.entry_16_characters_var,
            self.entry_17_web_var,
            self.entry_18_blackWhite_var,
            self.entry_19_manga_var,
            self.entry_20_scanInfo_var,
            self.spinbox_1_year_var,
            self.spinbox_2_month_var,
            self.spinbox_3_volume_var,
            self.spinbox_4_chapter_var,
            self.spinbox_5_pageCount_var,
            self.entry_16_tags_var,
            self.entry_15_genres_var
        ]
        self.widgets_obj = []
        self.selected_filenames = []
        self.loadedComicInfo_list = list[LoadedComicInfo]()
    def start_ui(self):
        master = self.master
        def makeReadOnly(event: tk.Event = None):
            # <Return>
            if event.widget.cget('state') == "disabled":
                return
            if isinstance(event.widget, tk.Entry):
                event.widget.configure(state="readonly")

        def makeFocused(event: tk.Event = None):
            # <Button-1>
            event.widget.focus()

        def onFocusOut(event: tk.Event = None):
            # <FocusOut>
            makeReadOnly(event)

        def makeEditable(event: tk.Event = None):
            # <Double-Button-1>
            if event.widget.cget('state') == "disabled":
                # if isinstance(event.widget, tk.Entry):
                # if isinstance(event.widget, tk.Spinbox):
                if str(event.widget) in (".!frame.!frame.!spinbox4",".!frame.!frame.!spinbox3"):
                    answer = mb.askyesno("Warning!","Warning: This change will be applied to all files.\
                    Only one file should be selected to change this value.Continue?")
                    if answer:
                        event.widget.configure(state="normal", highlightbackground="#00bfff", highlightcolor="#00bfff",
                                               highlightthickness='2')
                    else:
                        return
            else:
                event.widget.configure(state="normal", highlightbackground="#00bfff", highlightcolor="#00bfff",
                                       highlightthickness='2')

        def ValidateIfNum(s, S):
            # disallow anything but numbers
            valid = S == '' or S.isdigit()
            if not valid:
                self.frame_volumesetter.bell()
                velog("input not valid")
            return valid
        vldt_ifnum_cmd = (self.master.register(ValidateIfNum), '%s', '%S')


        self.edit_warning = False  # We send warning that changing chapter or volume will be set to all files selected
        self.frame1 = ttk.Frame(master)
        self.frame_2 = tk.Frame(self.frame1)
        self.label_1_year = tk.Label(self.frame_2)
        self.label_1_year.configure(text='Year')
        self.label_1_year.grid(column='1', row='0')

        self.spinbox_1_year = tk.Spinbox(self.frame_2, from_=1800, to=99999,  validate='all', validatecommand=vldt_ifnum_cmd)
        self.spinbox_1_year.configure(justify='center', state='readonly', textvariable=self.spinbox_1_year_var)
        self.spinbox_1_year.grid(column='1', row='1')
        self.spinbox_1_year.bind('<Button-1>', makeFocused, add='+')
        self.spinbox_1_year.bind('<Button-1>', makeFocused, add='+')
        self.spinbox_1_year.bind('<Double-Button-1>', makeEditable, add='+')
        self.spinbox_1_year.bind('<Double-Button-1>', makeEditable, add='+')
        self.spinbox_1_year.bind('<FocusOut>', onFocusOut, add='+')
        self.spinbox_1_year.bind('<Return>', makeReadOnly, add='+')
        self.spinbox_1_year.bind('<Return>', makeReadOnly, add='+')
        self.label_2_month = tk.Label(self.frame_2)
        self.label_2_month.configure(text='Month')
        self.label_2_month.grid(column='1', row='2')
        self.spinbox_2_month = tk.Spinbox(self.frame_2, from_=1, to=12, validate='all', validatecommand=vldt_ifnum_cmd)
        self.spinbox_2_month.configure(justify='center', state='readonly', textvariable=self.spinbox_2_month_var)
        self.spinbox_2_month.grid(column='1', row='3')
        self.spinbox_2_month.bind('<Button-1>', makeFocused, add='+')
        self.spinbox_2_month.bind('<Double-Button-1>', makeEditable, add='+')
        self.spinbox_2_month.bind('<FocusOut>', onFocusOut, add='+')
        self.spinbox_2_month.bind('<Return>', makeReadOnly, add='+')
        self.label_3_volume = tk.Label(self.frame_2)
        self.label_3_volume.configure(text='Volume')
        self.label_3_volume.grid(column='1', row='4')
        self.spinbox_3_volume = tk.Spinbox(self.frame_2, validate='all', validatecommand=vldt_ifnum_cmd)
        self.spinbox_3_volume.configure(buttondownrelief='flat', buttonuprelief='flat', font='TkDefaultFont',
                                        justify='center')
        self.spinbox_3_volume.configure(state='readonly', textvariable=self.spinbox_3_volume_var)
        self.spinbox_3_volume.grid(column='1', row='5')
        self.spinbox_3_volume.bind('<Button-1>', makeFocused, add='+')
        self.spinbox_3_volume.bind('<Double-Button-1>', makeEditable, add='+')
        self.spinbox_3_volume.bind('<FocusOut>', onFocusOut, add='+')
        self.spinbox_3_volume.bind('<Return>', makeReadOnly, add='+')
        self.label_4_chapter = tk.Label(self.frame_2)
        self.label_4_chapter.configure(anchor='n', text='Chapter')
        self.label_4_chapter.grid(column='1', row='6')
        self.spinbox_4_chapter = tk.Spinbox(self.frame_2, validate='all', validatecommand=vldt_ifnum_cmd)
        self.spinbox_4_chapter.configure(buttonuprelief='flat', cursor='arrow', justify='center', state='readonly')
        self.spinbox_4_chapter.configure(textvariable=self.spinbox_4_chapter_var)
        self.spinbox_4_chapter.grid(column='1', row='7')
        self.spinbox_4_chapter.bind('<Button-1>', makeFocused, add='+')
        self.spinbox_4_chapter.bind('<Double-Button-1>', makeEditable, add='+')
        self.spinbox_4_chapter.bind('<FocusOut>', onFocusOut, add='+')
        self.spinbox_4_chapter.bind('<Return>', makeReadOnly, add='+')
        self.label_14_langIso = tk.Label(self.frame_2)
        self.label_14_langIso.configure(text='Language ISO', textvariable=self.label_14_langIso_var)
        self.label_14_langIso.grid(column='1', row='8')
        self.label_14_langIso.bind('<Button-1>', makeFocused, add='+')
        self.label_14_langIso.bind('<Double-Button-1>', makeEditable, add='+')
        self.label_14_langIso.bind('<FocusOut>', onFocusOut, add='+')
        self.label_14_langIso.bind('<Return>', makeReadOnly, add='+')
        self.entry_10_langIso = tk.Entry(self.frame_2)
        self.entry_10_langIso.configure(justify='center', state='readonly', textvariable=self.entry_10_langIso_var)
        self.entry_10_langIso.grid(column='1', row='9')
        self.entry_10_langIso.bind('<Button-1>', makeFocused, add='+')
        self.entry_10_langIso.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_10_langIso.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_10_langIso.bind('<Return>', makeReadOnly, add='+')
        self.label_21_pagecount = tk.Label(self.frame_2)
        self.label_21_pagecount.configure(text='Page Count')
        self.label_21_pagecount.grid(column='1', row='10')
        self.spinbox_5_pageCount = tk.Spinbox(self.frame_2, validate='all', validatecommand=vldt_ifnum_cmd)

        self.spinbox_5_pageCount.configure(justify='center', state='readonly',
                                           textvariable=self.spinbox_5_pageCount_var)
        self.spinbox_5_pageCount.grid(column='1', row='11')
        self.spinbox_5_pageCount.bind('<Button-1>', makeFocused, add='+')
        self.spinbox_5_pageCount.bind('<Double-Button-1>', makeEditable, add='+')
        self.spinbox_5_pageCount.bind('<FocusOut>', onFocusOut, add='+')
        self.spinbox_5_pageCount.bind('<Return>', makeReadOnly, add='+')
        self.label_22_format = tk.Label(self.frame_2)
        self.label_22_format.configure(text='Format')
        self.label_22_format.grid(column='1', row='12')
        self.entry_15_format = tk.Entry(self.frame_2)
        self.entry_15_format.configure(justify='center', state='readonly', textvariable=self.entry_15_format_var)
        self.entry_15_format.grid(column='1', row='13')
        self.entry_15_format.bind('<Button-1>', makeFocused, add='+')
        self.entry_15_format.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_15_format.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_15_format.bind('<Return>', makeReadOnly, add='+')
        self.label_25_blackWhite = tk.Label(self.frame_2)
        self.label_25_blackWhite.configure(text='Black and White')
        self.label_25_blackWhite.grid(column='1', row='14')
        self.entry_18_blackWhite = tk.Entry(self.frame_2)
        self.entry_18_blackWhite.configure(state='readonly', textvariable=self.entry_18_blackWhite_var)
        self.entry_18_blackWhite.grid(column='1', row='15')
        self.entry_18_blackWhite.bind('<Button-1>', makeFocused, add='+')
        self.entry_18_blackWhite.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_18_blackWhite.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_18_blackWhite.bind('<Return>', makeReadOnly, add='+')
        self.label_26_manga = tk.Label(self.frame_2)
        self.label_26_manga.configure(text='Manga')
        self.label_26_manga.grid(column='1', row='16')
        self.entry_19_manga = tk.Entry(self.frame_2)
        self.entry_19_manga.configure(textvariable=self.entry_19_manga_var)
        self.entry_19_manga.grid(column='1', row='17')
        self.entry_19_manga.bind('<Button-1>', makeFocused, add='+')
        self.entry_19_manga.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_19_manga.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_19_manga.bind('<Return>', makeReadOnly, add='+')
        self.canvas_1 = tk.Canvas(self.frame_2)
        self.canvas_1.grid(column='0', row='0', rowspan='20')
        self.frame_2.configure(height='200', width='200')
        self.frame_2.grid(column='0', ipadx='10', ipady='10', padx='10', pady='20', row='0')
        self.frame1.columnconfigure('0', pad='0', weight='1')
        self.frame_1 = tk.Frame(self.frame1)
        self.label_5_serieName = tk.Label(self.frame_1)
        self.label_5_serieName.configure(text='Series Name')
        self.label_5_serieName.grid(column='0', row='0')
        self.frame_1.rowconfigure('0', weight='1')
        self.frame_1.columnconfigure('0', weight='1')
        self.entry_1_seriesName = tk.Entry(self.frame_1)
        self.entry_1_seriesName.configure(justify='left', state='readonly', takefocus=False,
                                          textvariable=self.entry_1_seriesName_var)
        self.entry_1_seriesName.grid(pady='10', row='1', sticky='ew')
        self.frame_1.rowconfigure('1', weight='1')
        self.entry_1_seriesName.bind('<Button-1>', makeFocused, add='+')
        self.entry_1_seriesName.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_1_seriesName.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_1_seriesName.bind('<Return>', makeReadOnly, add='+')
        self.label_6_title = tk.Label(self.frame_1)
        self.label_6_title.configure(text='Title')
        self.label_6_title.grid(column='0', row='2')
        self.frame_1.rowconfigure('2', weight='1')
        self.entry_2_title = tk.Entry(self.frame_1)
        self.entry_2_title.configure(font='TkDefaultFont', state='readonly', textvariable=self.entry_2_title_var)
        self.entry_2_title.grid(pady='10', row='3', sticky='ew')
        self.entry_2_title.bind('<Button-1>', makeFocused, add='+')
        self.entry_2_title.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_2_title.bind('<Enter>', makeReadOnly, add='+')
        self.entry_2_title.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_2_title.bind('<Return>', makeReadOnly, add='+')
        self.label_7_summary = tk.Label(self.frame_1)
        self.label_7_summary.configure(text='Summary')
        self.label_7_summary.grid(column='0', row='4')
        self.text_1_summary = tk.Text(self.frame_1)
        self.text_1_summary.configure(cursor='arrow', height='2', state='disabled', width='50')
        self.text_1_summary.grid(pady='10', row='5')
        self.label_5_StoryArc = tk.Label(self.frame_1)
        self.label_5_StoryArc.configure(text='Story Arc')
        self.label_5_StoryArc.grid(column='0', row='6')
        self.entry_6_storyArc = tk.Entry(self.frame_1)
        self.entry_6_storyArc.configure(state='readonly', textvariable=self.entry_6_storyArc_var)
        self.entry_6_storyArc.grid(column='0', row='7', sticky='ew')
        self.entry_6_storyArc.bind('<Button-1>', makeFocused, add='+')
        self.entry_6_storyArc.bind('<Button-1>', makeFocused, add='+')
        self.entry_6_storyArc.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_6_storyArc.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_6_storyArc.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_6_storyArc.bind('<Return>', makeReadOnly, add='+')
        self.entry_6_storyArc.bind('<Return>', makeReadOnly, add='+')
        self.__tkvar = tk.StringVar(value='Unknown')
        __values = []
        self.optionmenu_1 = tk.OptionMenu(self.frame_1, self.__tkvar, 'Unknown', *__values, command=None)
        self.optionmenu_1.grid(column='0', row='10')
        self.label_6_SeriesGroup = tk.Label(self.frame_1)
        self.label_6_SeriesGroup.configure(text='Series Grop')
        self.label_6_SeriesGroup.grid(column='0', row='8')
        self.entry_7_SeriesGroup = tk.Entry(self.frame_1)
        self.entry_7_SeriesGroup.configure(state='readonly', textvariable=self.entry_7_SeriesGroup_var)
        self.entry_7_SeriesGroup.grid(column='0', row='9', sticky='ew')
        self.entry_7_SeriesGroup.bind('<Button-1>', makeFocused, add='+')
        self.entry_7_SeriesGroup.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_7_SeriesGroup.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_7_SeriesGroup.bind('<Return>', makeReadOnly, add='+')
        self.frame_1.configure(height='200', width='200')
        self.frame_1.grid(column='1', ipadx='10', ipady='10', padx='20', pady='20', row='0', sticky='nsew')
        self.frame1.columnconfigure('1', pad='400', weight='1')
        self.frame_3_people = tk.Frame(self.frame1)
        self.label_8_people = tk.Label(self.frame_3_people)
        self.label_8_people.configure(cursor='arrow', font='TkDefaultFont', text='People')
        self.label_8_people.grid(column='0', row='0')
        self.frame_3_people.columnconfigure('0', weight='1')
        self.label_9_writer = tk.Label(self.frame_3_people)
        self.label_9_writer.configure(text='Writer')
        self.label_9_writer.grid(column='0', row='1')
        self.entry_3_writer = tk.Entry(self.frame_3_people)
        self.entry_3_writer.configure(state='readonly', textvariable=self.entry_3_writer_var)
        self.entry_3_writer.grid(column='0', row='2', sticky='ew')
        self.entry_3_writer.bind('<Button-1>', makeFocused, add='+')
        self.entry_3_writer.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_3_writer.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_3_writer.bind('<Return>', makeReadOnly, add='+')
        self.label_10_penciller = tk.Label(self.frame_3_people)
        self.label_10_penciller.configure(cursor='boat', state='disabled', text='Penciller')
        self.label_10_penciller.grid(column='0', row='3')
        self.entry_4_penciller = tk.Entry(self.frame_3_people)
        self.entry_4_penciller.configure(state='readonly', textvariable=self.entry_4_penciller_var)
        self.entry_4_penciller.grid(column='0', row='4', sticky='ew')
        self.entry_4_penciller.bind('<Button-1>', makeFocused, add='+')
        self.entry_4_penciller.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_4_penciller.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_4_penciller.bind('<Return>', makeReadOnly, add='+')
        self.label_11_Inker = tk.Label(self.frame_3_people)
        self.label_11_Inker.configure(compound='top', font='TkFixedFont', text='Inker')
        self.label_11_Inker.grid(column='0', row='5')
        self.entry_5_inker = tk.Entry(self.frame_3_people)
        self.entry_5_inker.configure(state='readonly', textvariable=self.entry_5_inker_var)
        self.entry_5_inker.grid(column='0', row='6', sticky='ew')
        self.entry_5_inker.bind('<Button-1>', makeFocused, add='+')
        self.entry_5_inker.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_5_inker.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_5_inker.bind('<Return>', makeReadOnly, add='+')
        self.label_12_colorist = tk.Label(self.frame_3_people)
        self.label_12_colorist.configure(text='Colorist')
        self.label_12_colorist.grid(column='0', row='7')
        self.entry_8_colorist = tk.Entry(self.frame_3_people)
        self.entry_8_colorist.configure(state='readonly', textvariable=self.entry_8_colorist_var)
        self.entry_8_colorist.grid(column='0', row='8', sticky='ew')
        self.entry_8_colorist.bind('<Button-1>', makeFocused, add='+')
        self.entry_8_colorist.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_8_colorist.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_8_colorist.bind('<Return>', makeReadOnly, add='+')
        self.label_13_letterist = tk.Label(self.frame_3_people)
        self.label_13_letterist.configure(text='Letterer')
        self.label_13_letterist.grid(column='0', row='9')
        self.entry_9_letterer = tk.Entry(self.frame_3_people)
        self.entry_9_letterer.configure(state='readonly', textvariable=self.entry_9_letterer_var)
        self.entry_9_letterer.grid(column='0', row='10', sticky='ew')
        self.entry_9_letterer.bind('<Button-1>', makeFocused, add='+')
        self.entry_9_letterer.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_9_letterer.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_9_letterer.bind('<Return>', makeReadOnly, add='+')
        self.label_14_coverArtist = tk.Label(self.frame_3_people)
        self.label_14_coverArtist.configure(compound='top', text='Cover Artist')
        self.label_14_coverArtist.grid(column='0', row='11')
        self.entry_11_coverArtist = tk.Entry(self.frame_3_people)
        self.entry_11_coverArtist.configure(state='readonly', textvariable=self.entry_11_coverArtist_var)
        self.entry_11_coverArtist.grid(column='0', row='12', sticky='ew')
        self.entry_11_coverArtist.bind('<Button-1>', makeFocused, add='+')
        self.entry_11_coverArtist.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_11_coverArtist.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_11_coverArtist.bind('<Return>', makeReadOnly, add='+')
        self.label_15_editor = tk.Label(self.frame_3_people)
        self.label_15_editor.configure(text='Editor')
        self.label_15_editor.grid(column='0', row='13')
        self.entry_12_editor = tk.Entry(self.frame_3_people)
        self.entry_12_editor.configure(state='readonly', textvariable=self.entry_12_editor_var)
        self.entry_12_editor.grid(column='0', row='14', sticky='ew')
        self.entry_12_editor.bind('<Button-1>', makeFocused, add='+')
        self.entry_12_editor.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_12_editor.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_12_editor.bind('<Return>', makeReadOnly, add='+')
        self.label_16_publisher = tk.Label(self.frame_3_people)
        self.label_16_publisher.configure(text='Publisher')
        self.label_16_publisher.grid(column='0', row='15')
        self.entry_13_publisher = tk.Entry(self.frame_3_people)
        self.entry_13_publisher.configure(state='readonly', textvariable=self.entry_13_publisher_var)
        self.entry_13_publisher.grid(column='0', row='16', sticky='ew')
        self.entry_13_publisher.bind('<Button-1>', makeFocused, add='+')
        self.entry_13_publisher.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_13_publisher.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_13_publisher.bind('<Return>', makeReadOnly, add='+')
        self.label_17_imprint = tk.Label(self.frame_3_people)
        self.label_17_imprint.configure(text='Imprint')
        self.label_17_imprint.grid(column='0', row='17')
        self.entry_14_imprint = tk.Entry(self.frame_3_people)
        self.entry_14_imprint.configure(state='readonly', textvariable=self.entry_14_imprint_var)
        self.entry_14_imprint.grid(column='0', row='18', sticky='ew')
        self.entry_14_imprint.bind('<Button-1>', makeFocused, add='+')
        self.entry_14_imprint.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_14_imprint.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_14_imprint.bind('<Return>', makeReadOnly, add='+')
        self.label_23_characters = tk.Label(self.frame_3_people)
        self.label_23_characters.configure(text='label_6')
        self.label_23_characters.grid(column='0', row='19')
        self.entry_16_characters = tk.Entry(self.frame_3_people)
        self.entry_16_characters.configure(state='readonly', textvariable=self.entry_16_characters_var)
        self.entry_16_characters.grid(column='0', row='20')
        self.entry_16_characters.bind('<Button-1>', makeFocused, add='+')
        self.entry_16_characters.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_16_characters.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_16_characters.bind('<Return>', makeReadOnly, add='+')
        self.frame_3_people.configure(height='200', width='200')
        self.frame_3_people.grid(column='0', ipadx='10', ipady='10', padx='10', row='1', sticky='ew')
        self.frame1.rowconfigure('1', pad='0')
        self.frame_3 = tk.Frame(self.frame1)
        self.label_18_genres = tk.Label(self.frame_3)
        self.label_18_genres.configure(text='Genres')
        self.label_18_genres.grid(column='0', row='0')
        self.frame_3.columnconfigure('0', weight='1')
        self.entry_15_genres = tk.Entry(self.frame_3)

        self.entry_15_genres.configure(state='readonly', textvariable=self.entry_15_genres_var)
        self.entry_15_genres.grid(column='0', row='1', sticky='ew')
        self.entry_15_genres.bind('<Button-1>', makeFocused, add='+')
        self.entry_15_genres.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_15_genres.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_15_genres.bind('<Return>', makeReadOnly, add='+')
        self.label_19_tags = tk.Label(self.frame_3)
        self.label_19_tags.configure(text='Tags')
        self.label_19_tags.grid(column='0', row='2')
        self.entry_16_tags = tk.Entry(self.frame_3)
        self.entry_16_tags.configure(state='readonly', textvariable=self.entry_16_tags_var)
        self.entry_16_tags.grid(column='0', row='3', sticky='ew')
        self.entry_16_tags.bind('<Button-1>', makeFocused, add='+')
        self.entry_16_tags.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_16_tags.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_16_tags.bind('<Return>', makeReadOnly, add='+')
        self.label_20_web = tk.Label(self.frame_3)
        self.label_20_web.configure(text='Web')
        self.label_20_web.grid(column='0', row='4')
        self.entry_17_web = tk.Entry(self.frame_3)
        self.entry_17_web.configure(state='readonly', textvariable=self.entry_17_web_var)
        self.entry_17_web.grid(column='0', row='5', sticky='ew')
        self.entry_17_web.bind('<Button-1>', makeFocused, add='+')
        self.entry_17_web.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_17_web.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_17_web.bind('<Return>', makeReadOnly, add='+')
        self.label_24_scanInfo = tk.Label(self.frame_3)
        self.label_24_scanInfo.configure(text='Scan Information')
        self.label_24_scanInfo.grid(column='0', row='6')
        self.entry_20_scanInfo = tk.Entry(self.frame_3)
        self.entry_20_scanInfo.configure(state='readonly', textvariable=self.entry_20_scanInfo_var)
        self.entry_20_scanInfo.grid(column='0', row='7', sticky='ew')
        self.entry_20_scanInfo.bind('<Button-1>', makeFocused, add='+')
        self.entry_20_scanInfo.bind('<Double-Button-1>', makeEditable, add='+')
        self.entry_20_scanInfo.bind('<FocusOut>', onFocusOut, add='+')
        self.entry_20_scanInfo.bind('<Return>', makeReadOnly, add='+')
        self.frame_3.configure(height='200', width='200')
        self.frame_3.grid(column='1', ipadx='10', ipady='10', padx='20', pady='10', row='1', sticky='ew')
        self.frame1.configure(height='800', padding='20', width='1080')
        self.frame1.grid(column='0', row='0')
        master.rowconfigure('0', minsize='0')
        master.columnconfigure('0', minsize='0', uniform='None')

        def open_files():
            covers_path_list = filedialog.askopenfiles(initialdir=launch_path, title="Select file to apply cover",
                                                       filetypes=(("CBZ Files", ".cbz"),)
                                                       )
            
            for file in covers_path_list:
                self.selected_filenames.append(file.name)

        self.button2_openfile = tk.Button(self.frame1, text="Open", command=open_files, width=15)
        self.button2_openfile.grid(column=1, row=2, pady="5 10", columnspan=2)

        self.button3_read = tk.Button(self.frame1, text="Read", command=self.create_loadedComicInfo_list, width=15)
        self.button3_read.grid(column=1, row=3, pady="5 10", columnspan=2)
        self.button4_save = tk.Button(self.frame1, text="Save", command=self.do_save_UI, width=15)
        self.button4_save.grid(column=1, row=4, pady="5 10", columnspan=2)
        # self.__tkvar.set('Age Rating')
        # self.optionmenu_1 = tk.OptionMenu(self.frame_1, self.__tkvar, "Unknown", *ComicInfo.AgeRating.list(),
        #                                   command=None)
        # Main widget
        self.mainwindow = self.frame1

        self.widgets_obj = [
            self.entry_1_seriesName,
            self.entry_2_title,
            self.entry_3_writer,
            self.entry_4_penciller,
            self.entry_5_inker,
            self.entry_6_storyArc,
            self.entry_7_SeriesGroup,
            self.entry_8_colorist,
            self.entry_9_letterer,
            self.entry_10_langIso,
            self.entry_11_coverArtist,
            self.entry_12_editor,
            self.entry_13_publisher,
            self.entry_14_imprint,
            self.entry_15_format,
            self.entry_16_characters,
            self.entry_17_web,
            self.entry_18_blackWhite,
            self.entry_19_manga,
            self.entry_20_scanInfo,
            self.spinbox_1_year,
            self.spinbox_2_month,
            self.spinbox_3_volume,
            self.spinbox_4_chapter,
            self.spinbox_5_pageCount,
            self.entry_16_tags,
            self.entry_15_genres
        ]


    def run(self):
        self.mainwindow.mainloop()

    def create_loadedComicInfo_list(self, cli_selected_files: list[str] = None):
        self.conflicts={}

        def load_comicinfo_xml(cls, cbz_path) -> LoadedComicInfo:
            """
            Accepts a path string
            Returns a LoadedComicInfo with the ComicInfo class generated from the data contained inside ComicInfo.xml file
            which is taken from the zip-like file type

            :param cls: parent self
            :param string cbz_path: the path to the zip-like file
            :return: LoadedComicInfo: LoadedComicInfo
            """
            velog(f"loading file: '{cbz_path}'")
            try:
                comicinfo = ReadComicInfo(cbz_path).to_ComicInfo(False)
            except NoMetadataFileFound as e:
                logging.error(f"Metadata file 'ComicInfo.xml' not found inside {cbz_path}")
                mb.showerror(f"Metadata file 'ComicInfo.xml' not found inside {cbz_path}.\
                One will be created when saving changes to file")
                return
            except XMLSyntaxError as e:
                logging.error(f"There was an error loading ComicInfo.xml from file: {cbz_path}", exc_info=e)
                mb.showerror("Error loading file", f"Can't loadComicInfo.xml from file: {cbz_path}" + str(e))
                return
            loadedInfo = LoadedComicInfo(cbz_path, comicinfo, comicinfo)
            delog("comicinfo was read and a LoadedComicInfo was created")
            #
            # """
            # Loads LoadedComicInfo.comicInfoObj into StringVar, so it can be modified in the UI.
            # Used for cli mode even if there's no UI present.
            #
            # :param LoadedComicInfo loadedInfo:
            # """

            comicinfo_attrib_get = [
                loadedInfo.comicInfoObj.get_Series,
                loadedInfo.comicInfoObj.get_Title,
                loadedInfo.comicInfoObj.get_Writer,
                loadedInfo.comicInfoObj.get_Penciller,
                loadedInfo.comicInfoObj.get_Inker,
                loadedInfo.comicInfoObj.get_StoryArc,
                loadedInfo.comicInfoObj.get_SeriesGroup,
                loadedInfo.comicInfoObj.get_Colorist,
                loadedInfo.comicInfoObj.get_Letterer,
                loadedInfo.comicInfoObj.get_LanguageISO,
                loadedInfo.comicInfoObj.get_CoverArtist,
                loadedInfo.comicInfoObj.get_Editor,
                loadedInfo.comicInfoObj.get_Publisher,
                loadedInfo.comicInfoObj.get_Imprint,
                loadedInfo.comicInfoObj.get_Format,
                loadedInfo.comicInfoObj.get_Characters,
                loadedInfo.comicInfoObj.get_Web,
                loadedInfo.comicInfoObj.get_BlackAndWhite,
                loadedInfo.comicInfoObj.get_Manga,
                loadedInfo.comicInfoObj.get_ScanInformation,
                loadedInfo.comicInfoObj.get_Year,
                loadedInfo.comicInfoObj.get_Month,
                loadedInfo.comicInfoObj.get_Volume,
                loadedInfo.comicInfoObj.get_Number,
                loadedInfo.comicInfoObj.get_PageCount,
                loadedInfo.comicInfoObj.get_Tags,
                loadedInfo.comicInfoObj.get_Genre
            ]
            comicinfo_attrib_set = [
                loadedInfo.comicInfoObj.set_Series,
                loadedInfo.comicInfoObj.set_Title,
                loadedInfo.comicInfoObj.set_Writer,
                loadedInfo.comicInfoObj.set_Penciller,
                loadedInfo.comicInfoObj.set_Inker,
                loadedInfo.comicInfoObj.set_StoryArc,
                loadedInfo.comicInfoObj.set_SeriesGroup,
                loadedInfo.comicInfoObj.set_Colorist,
                loadedInfo.comicInfoObj.set_Letterer,
                loadedInfo.comicInfoObj.set_LanguageISO,
                loadedInfo.comicInfoObj.set_CoverArtist,
                loadedInfo.comicInfoObj.set_Editor,
                loadedInfo.comicInfoObj.set_Publisher,
                loadedInfo.comicInfoObj.set_Imprint,
                loadedInfo.comicInfoObj.set_Format,
                loadedInfo.comicInfoObj.set_Characters,
                loadedInfo.comicInfoObj.set_Web,
                loadedInfo.comicInfoObj.set_BlackAndWhite,
                loadedInfo.comicInfoObj.set_Manga,
                loadedInfo.comicInfoObj.set_ScanInformation,
                loadedInfo.comicInfoObj.set_Year,
                loadedInfo.comicInfoObj.set_Month,
                loadedInfo.comicInfoObj.set_Volume,
                loadedInfo.comicInfoObj.set_Number,
                loadedInfo.comicInfoObj.set_PageCount,
                loadedInfo.comicInfoObj.set_Tags,
                loadedInfo.comicInfoObj.set_Genre
            ]

            if cls.widgets_obj:  # Initializing UI is optional. If there is no ui then there's no widgets neither.
                widgets_var_zip = zip(cls.widgets_var, comicinfo_attrib_get, comicinfo_attrib_set, cls.widgets_obj)
                initialized_UI = True
            else:
                widgets_var_zip = zip(cls.widgets_var, comicinfo_attrib_get, comicinfo_attrib_set)
                initialized_UI = False

            # Load the comic info into our StringVar and IntVar, so they can be modified in the ui
            cls.processed_chapter = False
            for widgets_var_tuple in widgets_var_zip:

                widgetvar = widgets_var_tuple[0]
                comicinfo_atr_get = widgets_var_tuple[1]()
                # comicinfo_atr_set = widgets_var_tuple[2]
                if widgetvar.get() != comicinfo_atr_get and widgetvar.get() in (-1, 0, ""):
                    if str(widgetvar) == "chapter" and not cls.processed_chapter:
                        continue
                    else:
                        cls.processed_chapter = True

                    delog("Read to variable :"+str(comicinfo_atr_get))
                    delog("widget var ="+str(widgetvar))
                    widgetvar.set(comicinfo_atr_get)

                elif widgetvar.get() != comicinfo_atr_get:
                    if isinstance(widgetvar, tk.StringVar):
                        widgetvar.set("")

                    elif isinstance(widgetvar, tk.IntVar):
                        if str(widgetvar) == "pageCount":
                            widgetvar.set(0)
                        else:
                            widgetvar.set(-1)
                    else:
                        logging.warning(f"Unrecognised type \n{widgetvar=}\n{widgetvar}")
                    if initialized_UI:  # For the items that are different, highlight in orane if ui is initialized
                        widgetobj = widgets_var_tuple[3]  # This is the actual widget, not the variable
                        delog("++#############++")
                        delog(comicinfo_atr_get)
                        delog(widgetvar.get())
                        delog("__#############__")
                        widgetobj.configure(highlightbackground='orange', highlightcolor="orange",
                                            highlightthickness='3')
                else:
                    delog("Content in comicinfo and UI is the same, skipping")
            return loadedInfo
        if not self.selected_filenames:
            if cli_selected_files:
                for file in cli_selected_files:
                    loaded_ComIinf = load_comicinfo_xml(self, file)
                    if loaded_ComIinf:
                        self.loadedComicInfo_list.append(loaded_ComIinf)
                    else:
                        continue
                # self.thiselem, self.nextelem = self.nextelem, next(self.licycle)
            else:
                raise Exception("No files selected")
        else:
            delog("Selected files UI:" + "".join(self.selected_filenames))
            for file_path in self.selected_filenames:
                loaded_ComIinf = load_comicinfo_xml(self,file_path)
                if loaded_ComIinf:
                    self.loadedComicInfo_list.append(loaded_ComIinf)
                else:
                    continue
                # self.thiselem, self.nextelem = self.nextelem, next(self.licycle)

    def parseUI_toComicInfo(self):
        """
        Modifies every ComicInfo loaded with values from the UI
        """
        def parse_UI_toComicInfo(cls, loadedInfo: LoadedComicInfo) -> LoadedComicInfo:
            """
            Accepts a path string
            Returns a LoadedComicInfo with the modified ComicInfo from the modified StringVars

            """
            delog(f"parsing UI to file: '{loadedInfo.path}'")

            comicinfo_attrib_get = [
                loadedInfo.comicInfoObj.get_Series,
                loadedInfo.comicInfoObj.get_Title,
                loadedInfo.comicInfoObj.get_Writer,
                loadedInfo.comicInfoObj.get_Penciller,
                loadedInfo.comicInfoObj.get_Inker,
                loadedInfo.comicInfoObj.get_StoryArc,
                loadedInfo.comicInfoObj.get_SeriesGroup,
                loadedInfo.comicInfoObj.get_Colorist,
                loadedInfo.comicInfoObj.get_Letterer,
                loadedInfo.comicInfoObj.get_LanguageISO,
                loadedInfo.comicInfoObj.get_CoverArtist,
                loadedInfo.comicInfoObj.get_Editor,
                loadedInfo.comicInfoObj.get_Publisher,
                loadedInfo.comicInfoObj.get_Imprint,
                loadedInfo.comicInfoObj.get_Format,
                loadedInfo.comicInfoObj.get_Characters,
                loadedInfo.comicInfoObj.get_Web,
                loadedInfo.comicInfoObj.get_BlackAndWhite,
                loadedInfo.comicInfoObj.get_Manga,
                loadedInfo.comicInfoObj.get_ScanInformation,
                loadedInfo.comicInfoObj.get_Year,
                loadedInfo.comicInfoObj.get_Month,
                loadedInfo.comicInfoObj.get_Volume,
                loadedInfo.comicInfoObj.get_Number,
                loadedInfo.comicInfoObj.get_PageCount,
                loadedInfo.comicInfoObj.get_Tags,
                loadedInfo.comicInfoObj.get_Genre
            ]
            comicinfo_attrib_set = [
                loadedInfo.comicInfoObj.set_Series,
                loadedInfo.comicInfoObj.set_Title,
                loadedInfo.comicInfoObj.set_Writer,
                loadedInfo.comicInfoObj.set_Penciller,
                loadedInfo.comicInfoObj.set_Inker,
                loadedInfo.comicInfoObj.set_StoryArc,
                loadedInfo.comicInfoObj.set_SeriesGroup,
                loadedInfo.comicInfoObj.set_Colorist,
                loadedInfo.comicInfoObj.set_Letterer,
                loadedInfo.comicInfoObj.set_LanguageISO,
                loadedInfo.comicInfoObj.set_CoverArtist,
                loadedInfo.comicInfoObj.set_Editor,
                loadedInfo.comicInfoObj.set_Publisher,
                loadedInfo.comicInfoObj.set_Imprint,
                loadedInfo.comicInfoObj.set_Format,
                loadedInfo.comicInfoObj.set_Characters,
                loadedInfo.comicInfoObj.set_Web,
                loadedInfo.comicInfoObj.set_BlackAndWhite,
                loadedInfo.comicInfoObj.set_Manga,
                loadedInfo.comicInfoObj.set_ScanInformation,
                loadedInfo.comicInfoObj.set_Year,
                loadedInfo.comicInfoObj.set_Month,
                loadedInfo.comicInfoObj.set_Volume,
                loadedInfo.comicInfoObj.set_Number,
                loadedInfo.comicInfoObj.set_PageCount,
                loadedInfo.comicInfoObj.set_Tags,
                loadedInfo.comicInfoObj.set_Genre
            ]

            if cls.widgets_obj:  # Initializing UI is optional. If there is no ui then there's no widgets neither.
                widgets_var_zip = zip(cls.widgets_var, comicinfo_attrib_get, comicinfo_attrib_set, cls.widgets_obj)
                initialized_UI = True
            else:
                widgets_var_zip = zip(cls.widgets_var, comicinfo_attrib_get, comicinfo_attrib_set)
                initialized_UI = False

            # Load the comic info into our StringVar and IntVar, so they can be modified in the ui
            for widgets_var_tuple in widgets_var_zip:
                widgetvar = widgets_var_tuple[0]
                comicinfo_atr_get = widgets_var_tuple[1]
                comicinfo_atr_set = widgets_var_tuple[2]

                if widgetvar.get() != comicinfo_atr_get() and widgetvar.get() not in (-1, 0, ""):
                    comicinfo_atr_set(widgetvar.get())
            return loadedInfo
        modified_loadedComicInfo_list = []
        # modified_loadedComicInfo_XML_list = list[str]()
        for comicObj in self.loadedComicInfo_list:
            modified_loadedComicInfo = parse_UI_toComicInfo(self, comicObj)
            modified_loadedComicInfo_list.append(modified_loadedComicInfo)
        self.loadedComicInfo_list = modified_loadedComicInfo_list

    def saveComicInfo(self):
        for loadedComicObj in self.loadedComicInfo_list:
            WriteComicInfo(loadedComicObj).to_file()

    def do_save_UI(self):
        self.parseUI_toComicInfo()
        self.saveComicInfo()
def run_debug_test():
    velog("Running debug test mode.")
    path_23 = r"I:\Mi unidad\Programacion\Python\ASCRIPT_MANGA_ZIPPER\tests\Sample CBZ Chapter 23.cbz"
    path_24 = r"I:\Mi unidad\Programacion\Python\ASCRIPT_MANGA_ZIPPER\tests\Sample CBZ Chapter 24.cbz"

    root = tk.Tk()
    test_files = [path_23,path_24]
    app = MangataggerApp()
    app.create_loadedComicInfo_list(test_files)

    app.spinbox_1_year_var.set(9870)

    app.parseUI_toComicInfo()



def main():
    velog("Running main")
    root = tk.Tk()

    app = MangataggerApp(root)
    app.start_ui()
    app.run()
if __name__ == '__main__':
    main()