#!/usr/bin/python
# coding: utf-8

import os
import urwid.curses_display
import urwid
from ara_forms import *
from widget import *
import listview

class boardlist_rowitem(FieldRow):
    fields = [
        ('new', 1, 'right'),
        ('name',12, 'left'),
        ('desc',0, 'left'),
    ]

class ara_list_boards(ara_forms):
    def __initwidgets__(self):
        self.keymap = {
            'j': 'down',
            'k': 'up',
        }
        boardlist = self.server.article_manager.board_list(self.session_key)
        if boardlist[0] == False:
            # TODO: 폴백 위젯 구현
            return
	self.header = urwid.Filler(urwid.Text(u"ARA: List boards",align='center'))
        self.boardnameedit = urwid.Filler(urwid.Edit(caption=" * Enter board name: ", wrap='clip'))
        boardcounttext = urwid.Filler(urwid.Text(' * There are %s boards.' % len(boardlist[1].keys())))

        itemlist = []
        for data in boardlist[1].keys():
            itemlist += [{'new':'N', 'name':data, 'desc':u'설명'}]
        header = {'new':'N', 'name':'Name', 'desc':'Description'}

        boardlist = listview.get_view(itemlist, header, boardlist_rowitem)

        content = [('fixed',1, self.header),('fixed',1,self.boardnameedit),('fixed',1,boardcounttext),boardlist]
        self.mainpile = urwid.Pile(content)

        return self.mainpile

if __name__=="__main__":
    ara_list_boards().main()

# vim: set et ts=8 sw=4 sts=4: