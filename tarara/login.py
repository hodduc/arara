#!/usr/bin/python
# coding: utf-8

import os
import urwid.curses_display
import urwid

keymap = {
    'j': 'down',
    'k': 'up',
}

class ara_login(object):
    def get_login_message(self):
        basedir = os.path.dirname(__file__)
        banner = os.path.join(basedir, 'login.txt')
        f = open(banner, 'r')
        return f.read().decode('utf-8')

    def __init__(self):
        utf8decode = urwid.escape.utf8decode
        dash = urwid.SolidFill(utf8decode('─'))
        blank = urwid.SolidFill(u" ")
        blanktext = urwid.Filler(urwid.Text(' '))

        self.message = urwid.Filler(urwid.Text(self.get_login_message(), align="center"))
        self.message_ko = urwid.Filler(urwid.Text(u"[Tab] 키를 누르면 항목간을 전환할 수 있습니다", align='center'))
        self.message_en = urwid.Filler(urwid.Text(u"Press [Tab] key to jump between each items", align='center'))

        idedit = urwid.Filler(urwid.Edit(caption="ID:", wrap='clip'))
        pwedit = urwid.Filler(urwid.Edit(caption="Password:", wrap='clip'))
        self.idpwpile = urwid.Pile([idedit, pwedit])

        langitems = [urwid.Text('Korean'), urwid.Text('English'), urwid.Text('Chinese')]
        self.langlist = urwid.LineBox(urwid.ListBox(urwid.SimpleListWalker(langitems)))

        joinitems = [urwid.Text('Join'), urwid.Text('Guest')]
        self.joinlist = urwid.LineBox(urwid.ListBox(urwid.SimpleListWalker(joinitems)))

#        self.bottomcolumn = urwid.Columns([urwid.Padding(self.idpwpile,'left', ('relative', 40)), urwid.Padding(self.langlist, 'center', ('relative', 30)), urwid.Padding(self.joinlist, 'right',('relative', 30))])
        self.bottomcolumn = urwid.Columns([('weight',40,self.idpwpile),('weight',30,self.langlist),('weight',30,self.joinlist)])

        content = [self.message,('fixed',1, dash), ("fixed", 1, self.message_ko), ('fixed',1,self.message_en), ('fixed',1,blank), ('fixed',4,self.bottomcolumn)]
        self.mainpile = urwid.Pile(content)

        self.frame = self.mainpile

    def main(self):
        self.ui = urwid.curses_display.Screen()
        self.ui.run_wrapper(self.run)

    def run(self):
        size = self.ui.get_cols_rows()
        quit = False
        while not quit:
            self.draw_screen(size)
            keys = self.ui.get_input()
            for key in keys:
                if key == 'tab':
                    quit = True
                    break
                if key in keymap:
                    key = keymap[key]
                self.frame.keypress(size, key)
   
    def draw_screen(self, size):
        canvas = self.frame.render(size, focus=True)
        self.ui.draw_screen(size, canvas)

ara_login().main()

# vim: set et ts=8 sw=4 sts=4
