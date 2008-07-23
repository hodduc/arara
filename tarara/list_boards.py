#!/usr/bin/python
# coding: utf-8

import os
import urwid.curses_display
import urwid
from ara_forms import *
from widget import *
from list_article import *
import listview

class boardlist_rowitem(FieldRow):
    fields = [
        ('new', 1, 'right'),
        ('name',12, 'left'),
        ('desc',0, 'left'),
    ]

class ara_list_boards(ara_forms):
    def __keypress__(self, size, key):
        key = key.strip().lower()
        mainpile_focus = self.mainpile.get_focus()
        if mainpile_focus == self.boardlist:
            if key == "enter":
                # self.boardlist.get_body().get_focus()[0].w.w.widget_list : 현재 활성화된 항목
                boardname = self.boardlist.get_body().get_focus()[0].w.w.widget_list[1].get_text()[0]
                ara_list_article(session_key = self.session_key, board_name = boardname).main()
            else:
                self.frame.keypress(size, key)
        else:
            self.frame.keypress(size, key)

    def __initwidgets__(self):
        self.keymap = {
            'j': 'down',
            'k': 'up',
        }
        boardlist = self.server.article_manager.board_list(self.session_key)
        if boardlist[0] == False:
            assert("Not logged in")
        boards = boardlist[1]#.keys()
	self.header = urwid.Filler(urwid.Text(u"ARA: List boards",align='center'))
        self.boardnameedit = urwid.Filler(urwid.Edit(caption=" * Enter board name: ", wrap='clip'))
        itemlist = []
        if len(boards) > 0:
            boardcounttext = urwid.Filler(urwid.Text(' * There are %s boards.' % len(boards)))
            for data in boards:
                itemlist += [{'new':'N', 'name':data, 'desc':u'설명'}]
        else:
            boardcounttext = urwid.Filler(urwid.Text(' * No boards found. Have a nice day.'))
            itemlist = [{'new':' ','name':'', 'desc':u'No boards found. Have a nice day.'}]

        header = {'new':'N', 'name':'Name', 'desc':'Description'}
        self.boardlist = listview.get_view(itemlist, header, boardlist_rowitem)

        content = [('fixed',1, self.header),('fixed',1,self.boardnameedit),('fixed',1,boardcounttext),self.boardlist]
        self.mainpile = urwid.Pile(content)

        return self.mainpile

if __name__=="__main__":
    ara_list_boards().main()

# vim: set et ts=8 sw=4 sts=4:
