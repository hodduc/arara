#!/usr/bin/python
# coding: utf-8

import sys
import urwid.curses_display
import urwid
from ara_form import *
import widget

class ara_main(ara_form):
    menu = [
        "(N)ew article",
        "(S)elect board",
        "(P)rivate message",
        "(U)ser preferences",
        "User (I)nformation",
        "(H)elp",
        "(A)bout ARA",
        "(W)elcome screen",
        "(Q)uit",
    ]

    def keypress(self, size, key):
        if key in self.keymap:
            key = self.keymap[key]
        if key == "tab":
            if self.maincolumn.get_focus() == self.menulist:
                self.maincolumn.set_focus(self.bests)
            elif self.maincolumn.get_focus() == self.bests:
                self.maincolumn.set_focus(self.menulist)
        elif key == "enter":
            maincolumn_focus = self.maincolumn.get_focus()
            if maincolumn_focus == self.menulist:
                pos = self.menulist.get_focus()[1]
                if pos == 0:
                    # TODO: 새 글 읽기로 가기
                    pass
                elif pos == 1:
                    self.parent.change_page("list_boards", {'session_key':self.session_key})
                elif pos == 2:
                    self.parent.change_page("list_pm", {'session_key':self.session_key})
                elif pos == 3:
                    self.parent.change_page("user_preferences", {'session_key':self.session_key})
                elif pos == 4:
                    self.parent.change_page("user_information", {'session_key':self.session_key})
                elif pos == 5:
                    self.parent.change_page("helpviewer",{'session_key':self.session_key,'topic':'ara_help', 'caller':'main', 'caller_args':{'session_key':self.session_key}})
                elif pos == 6:
                    self.parent.change_page("helpviewer",{'session_key':self.session_key,'topic':'about', 'caller':'main', 'caller_args':{'session_key':self.session_key}})
                elif pos == 7:
                    self.parent.change_page("welcome", {'session_key':self.session_key})
                elif pos == 8:
                    confirm = widget.Dialog("Really quit?", ["Yes", "No"], ('menu', 'bg', 'bgf'), 30, 5, self)
                    self.overlay = confirm
                    self.parent.run()
                    if confirm.b_pressed == "Yes":
                        self.server.login_manager.logout(self.session_key)
                        sys.exit(0)
                    else:
                        self.overlay = None
                        self.parent.run()
            elif maincolumn_focus == self.bests:
                bests_focus = self.bests.get_focus()
                if bests_focus == self.todaybest:
                    selected = self.tblist_raw[self.tblist.get_focus()[1]]
                    self.parent.change_page("read_article", {'session_key':self.session_key,
                        'board_name':selected['board_name'], 'article_id':selected['id']})
                elif bests_focus == self.weeklybest:
                    selected = self.wblist_raw[self.wblist.get_focus()[1]]
                    self.parent.change_page("read_article", {'session_key':self.session_key,
                        'board_name':selected['board_name'], 'article_id':selected['id']})
        else:
            self.mainpile.keypress(size, key)

    def __initwidgets__(self):
        self.keymap = {
            'j':'down',
            'k':'up',
        }
	self.header = urwid.Filler(urwid.Text(u"ARA: Main Menu", align='center'))
        self.header = urwid.AttrWrap(self.header, 'reversed')
        menuitems = [widget.Item(" * "+w+"\n", None, 'selected') for w in self.menu]
        self.menulist = urwid.ListBox(urwid.SimpleListWalker(menuitems))

	tbtext = urwid.Filler(urwid.Text(u"Today Best", align='center'))
        retvalue, self.tblist_raw = self.server.article_manager.get_today_best_list()
        assert retvalue
	tbitems = ["%(title)s (%(nickname)s, %(date)s)" % {"title":text['title'],
            'nickname':text['author_nickname'],'date':text['date'].strftime("%Y/%m/%d")} for text in self.tblist_raw]
        tbitems = [widget.Item(w, None, 'selected') for w in tbitems]
        self.tblist = urwid.ListBox(urwid.SimpleListWalker(tbitems))
	self.todaybest = urwid.Pile([('fixed',1,tbtext), self.tblist])

	wbtext = urwid.Filler(urwid.Text(u"Weekly Best", align='center'))
        retvalue, self.wblist_raw = self.server.article_manager.get_weekly_best_list()
        assert retvalue
	wbitems = ["%(title)s (%(nickname)s, %(date)s)" % {"title":text['title'],
            'nickname':text['author_nickname'],'date':text['date'].strftime("%Y/%m/%d")} for text in self.wblist_raw]
        wbitems = [widget.Item(w, None, 'selected') for w in wbitems]
        self.wblist = urwid.ListBox(urwid.SimpleListWalker(wbitems))
	self.weeklybest = urwid.Pile([('fixed',1,wbtext), self.wblist])

	self.bests = urwid.Pile([self.todaybest, self.weeklybest])
	self.copyrightnotice = urwid.Filler(urwid.Text(
u"""  * Press [Tab] to jump between menu, today best, weekly best
 ARAra Release 1.0                                Copyright (C) 2008, SPARCS"""))

        self.maincolumn = urwid.Columns([('weight',40,self.menulist),('weight',60,self.bests)])

        content = [('fixed',1, self.header),('fixed',1,widget.blanktext),
                self.maincolumn, ('fixed',1,widget.dash),
                ('fixed',2,self.copyrightnotice)]
        self.mainpile = urwid.Pile(content)

        self.keymap = {
            "left":"",
            "right":"",
            "j":"down",
            "k":"up",
            }

if __name__=="__main__":
    ara_main().main()

# vim: set et ts=8 sw=4 sts=4:
