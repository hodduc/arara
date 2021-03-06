#!/usr/bin/python
# coding: utf-8

import os
import urwid.curses_display
import urwid
from ara_form import *
import widget
from string import Template
from translation import _
from datetime import date

class ara_read_article(ara_form):
    def get_selected_article_id(self):
        return self.thread[self.article_list.get_focus()[1]]['id']

    def is_selected_deleted(self):
        return self.thread[self.article_list.get_focus()[1]]['deleted']

    def keypress(self, size, key):
        key = key.strip()
        if key == 'e':
            if not self.is_selected_deleted():
                self.parent.change_page("post_article", {'session_key':self.session_key, 'board_name':self.board_name,
                    'mode':'modify', 'article_id':self.get_selected_article_id()})
        elif key.lower() == 'r':
            if not self.is_selected_deleted():
                self.parent.change_page("post_article", {'session_key':self.session_key, 'board_name':self.board_name,
                    'mode':'reply', 'article_id':self.get_selected_article_id()})
        elif key == 'q':
            self.parent.change_page("list_article", {'session_key':self.session_key, 'board_name':self.board_name})
        elif key == 'v':
            if not self.is_selected_deleted():
                try:
                    retvalue = self.server.article_manager.vote_article(self.session_key, self.board_name, self.get_selected_article_id())
                    confirm = widget.Dialog(_('Voted.'), [_('OK')], ('menu', 'bg', 'bgf'), 30, 5, self)
                except InvalidOperation, e:
                    confirm = widget.Dialog(e.why, [_('OK')], ('menu', 'bg', 'bgf'), 30, 5, self)
                self.overlay = confirm
                self.parent.run()
                self.overlay = None
                self.parent.run()
        elif key == 'd':
            if not self.is_selected_deleted():
                confirm = widget.Dialog(_('Really delete?'), [_('Yes'), _('No')], ('menu', 'bg', 'bgf'), 30, 5, self)
                self.overlay = confirm
                self.parent.run()
                if confirm.b_pressed == _('Yes'):
                    try:
                        result = self.server.article_manager.delete(self.session_key,self.board_name, self.get_selected_article_id())
                        notice = widget.Dialog(_('Article deleted.'), [_('OK')], ('menu', 'bg', 'bgf'), 30, 5, self)
                    except InvalidOperation, e:
                        notice = widget.Dialog(e.why, [_('OK')], ('menu', 'bg', 'bgf'), 30, 5, self)
                    self.overlay = notice
                    self.parent.run()
                    self.overlay = None
                    self.parent.run()
                else:
                    self.overlay = None
                    self.parent.run()
        elif key == 'g':
            self.article_list.set_focus(0)
        else:
            self.mainpile.keypress(size, key)

    def __init__(self, parent, session_key = None, board_name = None, article_id = None):
        self.board_name = board_name
        self.article_id = article_id

        self.title_template = Template(_('Title: ${TITLE}'))
        self.author_template = Template(_('Author: ${AUTHOR} (${NICKNAME})'))
        self.info_template = Template(_('Date: ${DATE} Hit: ${HIT} Reply: ${REPLY} Vote: ${VOTE}'))
        self.deleted_article_template = _('Deleted article')

        self.reply_template = Template(_('Reply by ${AUTHOR}(${NICKNAME}) on ${DATE} Vote: ${VOTE}'))
        self.deleted_reply_template = Template(_('Deleted reply, written on ${DATE}'))

        self.attach_template = Template(_('Attachment: ${SERVER_ADDRESS}/board/${BOARD_NAME}/${ROOT_ID}/${ARTICLE_ID}/file/${FILE_ID}\n'))
        ara_form.__init__(self, parent, session_key)

    def get_article_body(self):
        article_list = []
        for article in self.thread:
            if article.depth == 1:
                if article.deleted:
                    article_title = urwid.Filler(urwid.Text(self.deleted_article_template))
                    article_info = urwid.Filler(urwid.Text(self.info_template.safe_substitute(
                        HIT=article.hit, REPLY=str(len(self.thread)-1), 
                        DATE=date.fromtimestamp(article.date).strftime("%Y/%m/%d %H:%M"), VOTE=str(article.vote))))
                else:
                    article_title = urwid.Filler(urwid.Text(self.title_template.safe_substitute(
                        TITLE=article.title.decode('utf-8'))))
                    article_author = urwid.Filler(urwid.Text(self.author_template.safe_substitute(
                        AUTHOR=article.author_username.decode('utf-8'), NICKNAME=article.author_nickname.decode('utf-8'))))
                    article_info = urwid.Filler(urwid.Text(self.info_template.safe_substitute(
                        HIT=article.hit, REPLY=str(len(self.thread)-1), 
                        DATE=date.fromtimestamp(article.date).strftime("%Y/%m/%d %H:%M"), VOTE=str(article.vote))))
            else:
                if article.deleted:
                    article_info = urwid.Filler(urwid.Text(self.deleted_reply_template.safe_substitute(
                        DATE=date.fromtimestamp(article.date).strftime("%Y/%m/%d %H:%M"), VOTE=str(article.vote))))
                else:
                    article_title = urwid.Filler(urwid.Text(self.title_template.safe_substitute(TITLE=article.title.decode('utf-8'))))
                    article_info = urwid.Filler(urwid.Text(self.reply_template.safe_substitute(AUTHOR=article.author_username.decode('utf-8'),
                        NICKNAME=article.author_nickname.decode('utf-8'), DATE=date.fromtimestamp(article.date).strftime("%Y/%m/%d %H:%M"),
                        VOTE=str(article.vote))))

            if not article.deleted:
                article_body = article.content
                if article.attach:
                    article_body += '\n\n'
                    for item in article.attach:
                        string = self.attach_template.safe_substitute(SERVER_ADDRESS="http://nan.sparcs.org:8003",
                                BOARD_NAME=self.board_name, ROOT_ID = article.root_id,
                                ARTICLE_ID = article.id, FILE_ID = item.file_id)
                        article_body += string
                article_body = urwid.Text(article_body.rstrip())

            if article.depth == 1:
                if article.deleted:
                    article_pile = urwid.Pile([('fixed',1,article_title),('fixed',1,article_info), ('fixed',1,widget.dash)])
                else:
                    article_pile = urwid.Pile([('fixed',1,article_title),('fixed',1,article_author),
                        ('fixed',1,article_info), ('fixed',1,widget.dash), article_body])
                indented_pile = article_pile
            else:
                if article.deleted:
                    article_pile = urwid.Pile([('fixed',1,article_info)])
                else:
                    article_pile = urwid.Pile([('fixed',1,article_info),('fixed',1,article_title),article_body])
                indented_pile = widget.IndentColumn(article_pile, article.depth)

            indented_pile = widget.MarkedItem('>', indented_pile)
            article_list.append(indented_pile)
        return article_list

    def __initwidgets__(self):
        self.keymap = {
            'j': 'down',
            'k': 'up',
            'b': 'page up',
            'f': 'page down',
        }
        self.thread = self.server.article_manager.read(self.session_key, self.board_name, self.article_id)

        self.article_threads = self.get_article_body()
        assert self.article_threads
        self.article_list = urwid.ListBox(urwid.SimpleListWalker(self.article_threads))

	self.header = urwid.Filler(urwid.Text(_('ARA: Read article'),align='center'))
        functext = urwid.Filler(urwid.Text(_('(n)ext/(p)revious (b)lock (e)dit (d)elete (f)old/retract (r)eply (v)ote (q)uit')))

        content = [self.article_list, ('fixed',1,urwid.AttrWrap(functext, 'reversed'))]
        self.mainpile = urwid.Pile(content)

        return self.mainpile

# vim: set et ts=8 sw=4 sts=4:
