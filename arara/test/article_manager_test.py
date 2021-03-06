#-*- coding: utf-8 -*-
import unittest
import os
import sys
import time

THRIFT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../gen-py/'))
sys.path.append(THRIFT_PATH)
ARARA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(ARARA_PATH)

from arara.test.test_common import AraraTestBase
from arara_thrift import ttypes
from arara_thrift.ttypes import *
import arara.model

from etc import arara_settings

class ArticleManagerTest(AraraTestBase):

    def register_extra_users(self):
        '''
        6명의 사용자를 추가로 등록하고, 1번사용자 (sysop) 부터의 session key 반환

        @rtype: list<str>
        @return: 총 9명의 사용자의 Login Session
        '''
         
        return [self.session_key_sysop,
                self.session_key_mikkang,
                self.session_key_serialx,
                self.register_and_login(u'hodduc'),
                self.register_and_login(u'sillo'),
                self.register_and_login(u'bbashong'),
                self.register_and_login(u'panda'),
                self.register_and_login(u'koolvibes'),
                self.register_and_login(u'wiki')]

    def setUp(self):
        # Common preparation for all tests
        super(ArticleManagerTest, self).setUp(stub_time=True, stub_time_initial=31536000.1)

        # SYSOP will appear.
        self.session_key_sysop = self.engine.login_manager.login(u'SYSOP', u'SYSOP', u'123.123.123.123')
        # Register two users
        self.session_key_mikkang = self.register_and_login(u'mikkang')
        self.session_key_serialx = self.register_and_login(u'serialx')

        # Create default board
        self.engine.board_manager.add_board(self.session_key_sysop, u'board', u'테스트보드', u'Test Board', [])
        self.engine.board_manager.add_board(self.session_key_sysop, u'board_h', u'글머리가 있는 보드', u'Test Board with heading', [u'head1', u'head2'])

        self.engine.board_manager.add_board(self.session_key_sysop, u'board_del', u'지워질 보드', u'Test Board for deleting board test', [])
        self.engine.board_manager.add_board(self.session_key_sysop, u'board_hide', u'숨겨질 보드', u'Test Board for hiding board test', [])

    def test_read_only_board(self):
        # Add a read-only board. Try to write an article. Must fail.
        self.engine.board_manager.add_read_only_board(self.session_key_sysop, u'board')

        article = Article(**{'title': u'serialx is...', 'content': u'polarbear'})
        try:
            self.engine.article_manager.write_article(self.session_key_sysop, u'board', article)
            self.fail()
        except InvalidOperation:
            pass

    def _dummy_article_write(self, session_key, title_append = u"", board_name=u'board', heading=u''):
        time.time.elapse(1.0)
        article_dic = {'title': u'TITLE' + title_append, 'content': u'CONTENT', 'heading': heading}
        return self.engine.article_manager.write_article(session_key, board_name, Article(**article_dic))

    def _to_dict(self, article_object):
        '''
        이런 식으로 온 객체를 

        Article(attach=None, board_name=None, author_username=u'mikkang', hit=1, blacklisted=False, title=u'TITLE', deleted=False, read_status=None, root_id=1, is_searchable=True, author_nickname=u'mikkang', content=u'CONTENT', vote=0, depth=1, reply_count=None, last_modified_date=31536001.100000001, date=31536001.100000001, author_id=2, type=None, id=1)

        이런 식으로 고친다

        {'attach': None, 'board_name': None, 'author_username': u'mikkang', 'hit': 1, 'blacklisted': False, 'title': ...}
        '''
        FIELD_LIST = ['attach', 'board_name', 'author_username', 'hit', 'blacklisted', 'title', 'deleted', 'read_status', 'root_id', 'is_searchable', 'author_nickname', 'content', 'positive_vote', 'negative_vote', 'depth', 'reply_count', 'last_modified_date', 'date', 'author_id', 'type', 'id', 'heading']
        result_dict = {}
        for field in FIELD_LIST:
            result_dict[field] = article_object.__dict__[field]
        return result_dict

    def test_write_and_read_basic(self):
        # Write an article.
        article_id = self._dummy_article_write(self.session_key_mikkang)
        # Checking the article id
        self.assertEqual(1, article_id)
        # Now read, and check the contents.
        result = self.engine.article_manager.read_article(self.session_key_mikkang, u'board', 1)
        expected_result = {'negative_vote': 0, 'positive_vote': 0, 'last_modified_date': 31536001.100000001, 'is_searchable': True, 'author_nickname': u'mikkang', 'reply_count': None, 'id': 1, 'title': u'TITLE', 'content': u'CONTENT', 'attach': None, 'type': None, 'author_username': u'mikkang', 'hit': 1, 'root_id': 1, 'deleted': False, 'board_name': u'board', 'date': 31536001.100000001, 'blacklisted': False, 'read_status': None, 'depth': 1, 'author_id': 2, 'heading': u''} 
        self.assertEqual(1, len(result))
        self.assertEqual(expected_result, self._to_dict(result[0]))

    def test_write_and_read_with_heading(self):
        # Write an article
        article_id = self._dummy_article_write(self.session_key_mikkang, u"", u"board_h", u"head1")
        result = self.engine.article_manager.read_article(self.session_key_mikkang, u'board_h', 1)
        expected_result = {'negative_vote': 0, 'positive_vote': 0, 'last_modified_date': 31536001.100000001, 'is_searchable': True, 'author_nickname': u'mikkang', 'reply_count': None, 'id': 1, 'title': u'TITLE', 'content': u'CONTENT', 'attach': None, 'type': None, 'author_username': u'mikkang', 'hit': 1, 'root_id': 1, 'deleted': False, 'board_name': u'board_h', 'date': 31536001.100000001, 'blacklisted': False, 'read_status': None, 'depth': 1, 'author_id': 2, 'heading': u'head1'} 
        self.assertEqual(1, len(result))
        self.assertEqual(expected_result, self._to_dict(result[0]))
        # Can't write an article with nonexist heading
        try:
            self._dummy_article_write(self.session_key_mikkang, u"", u"board_h", u"head3")
            self.fail("must not be able to write an article with nonexisting heading")
        except InvalidOperation:
            pass

    def test_read_recent_article(self):
        # Test 1. Board에 게시물이 하나도 없을 때 에러를 발생시키는가?
        try:
            self.engine.article_manager.read_recent_article(self.session_key_mikkang, u'board')
            self.fail("Get article from empty board!")
        except InvalidOperation:
            pass

        # Test 2. Board에 게시물이 여러 개 있을 때 과연 최근 게시물을 읽어 오는가?
        article_id1 = self._dummy_article_write(self.session_key_mikkang)
        article_id2 = self._dummy_article_write(self.session_key_mikkang)
        recent_article = self.engine.article_manager.read_recent_article(self.session_key_mikkang, u'board')
        if recent_article[0].id != article_id2:
            self.fail("Not recent article!")

        article_id3 = self._dummy_article_write(self.session_key_mikkang)
        more_recent_article = self.engine.article_manager.read_recent_article(self.session_key_mikkang, u'board')
        if more_recent_article[0].id != article_id3:
            self.fail("Not recent article!")

        # Test 3. 존재하지 않는 보드에 접근할 때 에러를 발생시키는가?
        try:
            self.engine.article_manager.read_recent_article(self.session_key_mikkang, u'ghost_board')
            self.fail("Get article from non-exist board")
        except InvalidOperation:
            pass
            
    def test_reply(self):
        # Test fail to reply on a nonexisting article
        reply_dic = WrittenArticle(**{'title':u'dummy', 'content': u'asdf', 'heading': u''})
        try:
            self.engine.article_manager.write_reply(self.session_key_mikkang, u'board', 24, reply_dic)
            self.fail()
        except InvalidOperation:
            pass
        # Test successfully reply on an existing article.
        article_id = self._dummy_article_write(self.session_key_mikkang)
        time.time.elapse(1.0)
        reply_id   = self.engine.article_manager.write_reply(self.session_key_mikkang, u'board', 1, reply_dic)
        self.assertEqual(2, reply_id)
        # Test read original article again.
        result = self.engine.article_manager.read_article(self.session_key_mikkang, u'board', 1)
        expected_result1 = {'negative_vote': 0, 'positive_vote': 0, 'last_modified_date': 31536001.100000001, 'is_searchable': True, 'author_nickname': u'mikkang', 'reply_count': None, 'id': 1, 'title': u'TITLE', 'content': u'CONTENT', 'attach': None, 'type': None, 'author_username': u'mikkang', 'hit': 1, 'root_id': 1, 'deleted': False, 'board_name': u'board', 'date': 31536001.100000001, 'blacklisted': False, 'read_status': None, 'depth': 1, 'author_id': 2, 'heading': u''} 
        
        expected_result2 = {'negative_vote': 0, 'positive_vote': 0, 'last_modified_date': 31536002.100000001, 'is_searchable': True, 'author_nickname': u'mikkang', 'reply_count': None, 'id': 2, 'title': u'dummy', 'content': u'asdf', 'attach': None, 'type': None, 'author_username': u'mikkang', 'hit': 0, 'root_id': 1, 'deleted': False, 'board_name': u'board', 'date': 31536002.100000001, 'blacklisted': False, 'read_status': None, 'depth': 2, 'author_id': 2, 'heading': u''}
        self.assertEqual(2, len(result))
        self.assertEqual(expected_result1, self._to_dict(result[0]))
        self.assertEqual(expected_result2, self._to_dict(result[1]))
        # List the article (should only be one article in the list
        # XXX It shouldn't be a repr!!! Please replace it.
        result = self.engine.article_manager.article_list(self.session_key_mikkang, u'board', u'')
        self.assertEqual(1, result.last_page)
        self.assertEqual(1, result.results)
        self.assertEqual(1, result.current_page)
        self.assertEqual(1, len(result.hit))

        expected_result = expected_result1
        expected_result['reply_count'] = 1
        expected_result['content'] = None
        expected_result['read_status'] = 'R'
        expected_result['type'] = 'normal'
        expected_result['depth'] = None
        expected_result['root_id'] = None
        expected_result['board_name'] = u'board'
        self.assertEqual(expected_result, self._to_dict(result.hit[0]))

    def test_reply_with_heading(self):
        # Write an article
        article_id = self._dummy_article_write(self.session_key_mikkang, u'', u'board_h')
        time.time.elapse(1.0)
        reply_dic = WrittenArticle(**{'title':u'dummy', 'content': u'asdf', 'heading': u'head1'})
        reply_id1 = self.engine.article_manager.write_reply(self.session_key_serialx, u'board_h', article_id, reply_dic)
        time.time.elapse(1.0)
        reply_dic = WrittenArticle(**{'title':u'dummy', 'content': u'asdf', 'heading': u'head2'})
        reply_id2 = self.engine.article_manager.write_reply(self.session_key_mikkang, u'board_h', article_id, reply_dic)

        result = self.engine.article_manager.read_article(self.session_key_mikkang, u'board_h', 1)
        expected_result2 = {'negative_vote': 0, 'positive_vote': 0, 'last_modified_date': 31536002.100000001, 'is_searchable': True, 'author_nickname': u'serialx', 'reply_count': None, 'id': 2, 'title': u'dummy', 'content': u'asdf', 'attach': None, 'type': None, 'author_username': u'serialx', 'hit': 0, 'root_id': 1, 'deleted': False, 'board_name': u'board_h', 'date': 31536002.100000001, 'blacklisted': False, 'read_status': None, 'depth': 2, 'author_id': 3, 'heading': u'head1'} 
        expected_result3 = {'negative_vote': 0, 'positive_vote': 0, 'last_modified_date': 31536003.100000001, 'is_searchable': True, 'author_nickname': u'mikkang', 'reply_count': None, 'id': 3, 'title': u'dummy', 'content': u'asdf', 'attach': None, 'type': None, 'author_username': u'mikkang', 'hit': 0, 'root_id': 1, 'deleted': False, 'board_name': u'board_h', 'date': 31536003.100000001, 'blacklisted': False, 'read_status': None, 'depth': 2, 'author_id': 2, 'heading': u'head2'}

        self.assertEqual(3, len(result))
        self.assertEqual(expected_result2, self._to_dict(result[1]))
        self.assertEqual(expected_result3, self._to_dict(result[2]))

        # Can't write an article with nonexist heading
        try:
            self._dummy_article_write(self.session_key_mikkang, u"", u"board_h", u"head3")
            self.fail("must not be able to write an article with nonexisting heading")
        except InvalidOperation:
            pass



    def test_reply_changes_list(self):
        # Preparation
        article_1_id = self._dummy_article_write(self.session_key_mikkang)
        article_2_id = self._dummy_article_write(self.session_key_serialx)
        time.time.elapse(1.0)
        reply_dic    = WrittenArticle(**{'title':u'dummy', 'content': u'asdf', 'heading': u''})
        reply_id     = self.engine.article_manager.write_reply(self.session_key_mikkang, u'board', 1, reply_dic)
        # Without reply, listing order must be [article 2, article 1].
        # But since new reply was found on article 1, listing order must be [article 1, article 2].
        result = self.engine.article_manager.article_list(self.session_key_mikkang, u'board', u'')
        self.assertEqual(1, result.last_page)
        self.assertEqual(2, result.results)
        self.assertEqual(1, result.current_page)

        expected_result1 = {'negative_vote': 0, 'positive_vote': 0, 'last_modified_date': 31536001.100000001, 'is_searchable': True, 'author_nickname': u'mikkang', 'reply_count': 1, 'id': 1, 'title': u'TITLE', 'content': None, 'attach': None, 'type': 'normal', 'author_username': u'mikkang', 'hit': 0, 'root_id': None, 'deleted': False, 'board_name': u'board', 'date': 31536001.100000001, 'blacklisted': False, 'read_status': 'N', 'depth': None, 'author_id': 2, 'heading': u''}

        expected_result2 = {'negative_vote': 0, 'positive_vote': 0, 'last_modified_date': 31536002.100000001, 'is_searchable': True, 'author_nickname': u'serialx', 'reply_count': 0, 'id': 2, 'title': u'TITLE', 'content': None, 'attach': None, 'type': 'normal', 'author_username': u'serialx', 'hit': 0, 'root_id': None, 'deleted': False, 'board_name': u'board', 'date': 31536002.100000001, 'blacklisted': False, 'read_status': 'N', 'depth': None, 'author_id': 3, 'heading': u''}

        self.assertEqual(expected_result2, self._to_dict(result.hit[0]))
        self.assertEqual(expected_result1, self._to_dict(result.hit[1]))

    def test_pagination(self):
        # Write some articles
        for i in range(1, 105):
            self._dummy_article_write(self.session_key_mikkang, unicode(i))
        # Check some articles
        l = self.engine.article_manager.article_list(self.session_key_mikkang, u'board', u'')
        self.assertEqual(u'TITLE104', l.hit[0].title)
        self.assertEqual(u'TITLE103', l.hit[1].title)
        self.assertEqual(u'TITLE85', l.hit[19].title)
        l = self.engine.article_manager.article_list(self.session_key_mikkang, u'board', u'', page=2)
        self.assertEqual(u'TITLE84', l.hit[0].title)
        self.assertEqual(6, l.last_page)

    def testReadStatus(self):
        # XXX : ReadStatusManager 가 잘 작동되어서 그 결과가
        #       ArticleManager 에 잘 반영되었는지 점검하는 것.

        # Write some articles
        article_id1 = self._dummy_article_write(self.session_key_mikkang)
        article_id2 = self._dummy_article_write(self.session_key_mikkang)
        article_id3 = self._dummy_article_write(self.session_key_mikkang)
        # Test that everything is New
        l = self.engine.article_manager.article_list(self.session_key_serialx, u'board', u'')
        self.assertEqual('N', l.hit[2].read_status)
        self.assertEqual('N', l.hit[1].read_status)
        self.assertEqual('N', l.hit[0].read_status)
        # Now Read some article and test if it is changed as read
        article_1 = self.engine.article_manager.read_article(self.session_key_serialx, u'board', article_id3)
        article_2 = self.engine.article_manager.read_article(self.session_key_serialx, u'board', article_id2)
        l = self.engine.article_manager.article_list(self.session_key_serialx, u'board', u'')
        self.assertEqual('N', l.hit[2].read_status)
        self.assertEqual('R', l.hit[1].read_status)
        self.assertEqual('R', l.hit[0].read_status)

    def test_update_read_status(self):
        # Case 1. 루트 글은 읽었으나 답글은 읽지 않았다
        # Case 2. 루트 글도 안 읽었고 답글도 안 읽었다
        # Case 3. 루트 글도 답글도 읽었다.

        # Preparation
        article_1_id = self._dummy_article_write(self.session_key_mikkang) # 루트글만 읽음
        article_2_id = self._dummy_article_write(self.session_key_mikkang) # 루트글도 안읽음
        article_3_id = self._dummy_article_write(self.session_key_mikkang) # 루트글도 답글도 읽음
        self.engine.article_manager.read_article(self.session_key_serialx, u'board', article_1_id)
        self.engine.article_manager.read_article(self.session_key_serialx, u'board', article_3_id)
        time.time.elapse(1.0)
        reply_dic    = WrittenArticle(**{'title':u'dummy', 'content': u'asdf', 'heading': u''})
        reply_1_id   = self.engine.article_manager.write_reply(self.session_key_mikkang, u'board', 1, reply_dic)
        time.time.elapse(1.0)
        reply_dic    = WrittenArticle(**{'title':u'dummy', 'content': u'asdf', 'heading': u''})
        reply_2_id   = self.engine.article_manager.write_reply(self.session_key_mikkang, u'board', 2, reply_dic)
        time.time.elapse(1.0)
        reply_dic    = WrittenArticle(**{'title':u'dummy', 'content': u'asdf', 'heading': u''})
        reply_3_id   = self.engine.article_manager.write_reply(self.session_key_mikkang, u'board', 3, reply_dic)
        self.engine.article_manager.read_article(self.session_key_serialx, u'board', reply_3_id)

        # Article_3 번에게는 R
        # Article_2 번에게는 N
        # Article_1 번에게는 U <새로 도입하는 기호, 루트글은 읽고 답글은 안읽었을 때>

        result = self.engine.article_manager.article_list(self.session_key_serialx, u'board', u'')
        self.assertEqual('R', result.hit[0].read_status)
        self.assertEqual('N', result.hit[1].read_status)
        self.assertEqual('U', result.hit[2].read_status)

        # 이제 다시 한번 위의 글을 읽어주면 U->R 으로.
        self.engine.article_manager.read_article(self.session_key_serialx, u'board', article_1_id)
        result = self.engine.article_manager.article_list(self.session_key_serialx, u'board', u'')
        self.assertEqual('R', result.hit[2].read_status)

    def test_deletion(self):
        # Write some articles
        article1_id = self._dummy_article_write(self.session_key_mikkang)
        article2_id = self._dummy_article_write(self.session_key_mikkang)
        article3_id = self._dummy_article_write(self.session_key_mikkang)
        # Delete these!
        self.assertEqual(True, self.engine.article_manager.delete_article(self.session_key_mikkang, u'board', article1_id))
        self.assertEqual(True, self.engine.article_manager.read_article(self.session_key_mikkang, u'board', article1_id)[0].deleted)
        # XXX: Well.. It will be safe to check all the other information remain
        # Can't delete which not exist
        try:
            self.engine.article_manager.delete_article(self.session_key_mikkang, u'board', 1241252)
            self.fail()
        except InvalidOperation:
            pass
        # Can't delete which I didn't write
        try:
            self.engine.article_manager.delete_article(self.session_key_serialx, u'board', article2_id)
            self.fail()
        except InvalidOperation:
            pass
        # Can't delete which I already deleted
        try:
            self.engine.article_manager.delete_article(self.session_key_mikkang, u"board", article1_id)
            self.fail()
        except InvalidOperation:
            pass

    def test_destroy(self):
        # Write some articles
        article1_id = self._dummy_article_write(self.session_key_mikkang)
        article2_id = self._dummy_article_write(self.session_key_mikkang)
        article3_id = self._dummy_article_write(self.session_key_mikkang)
        # Delete one.
        self.engine.article_manager.delete_article(self.session_key_mikkang, u'board', article1_id)
        try:
            self.assertEqual(True, self.engine.article_manager.destroy_article(self.session_key_sysop, u'board', article1_id))
            self.fail('Destroy one. Must fail, because delete automatically destroy article...')
        except InvalidOperation:
            pass

        try:
            self.engine.article_manager.destroy_article(self.session_key_sysop, u'board', 1241252)
            self.fail("Can't destroy which do not exist.")
        except InvalidOperation:
            pass
        
        try:
            self.engine.article_manager.destroy_article(self.session_key_mikkang, u'board', article2_id)
            self.fail("Anyone other tha SYSOP can't do destroy article")
        except InvalidOperation:
            pass

        try:
            self.engine.article_manager.destroy_article(self.session_key_sysop, u"board", article1_id)
            self.fail("Can't destroy which already destroyed.")
        except InvalidOperation:
            pass
        # TODO : Check whether it is marked as destroyed

    def test_modification(self):
        # XXX combacsa 20090805 1905
        # Write an articles
        article_no = self._dummy_article_write(self.session_key_mikkang)
        # Modify its contents
        article_dic = {'title': u'MODIFIED TITLE', 'content': u'MODIFIED CONTENT', 'heading': u''}
        result = self.engine.article_manager.modify_article(self.session_key_mikkang, u'board', article_no, WrittenArticle(**article_dic))
        self.assertEqual(article_no, result)
        # Now check it is modified or not
        result = self.engine.article_manager.read_article(self.session_key_mikkang, u'board', 1)
        expected_result = {'negative_vote': 0, 'positive_vote': 0, 'last_modified_date': 31536001.100000001, 'is_searchable': True, 'author_nickname': u'mikkang', 'reply_count': None, 'id': 1, 'title': u'MODIFIED TITLE', 'content': u'MODIFIED CONTENT', 'attach': None, 'type': None, 'author_username': u'mikkang', 'hit': 1, 'root_id': 1, 'deleted': False, 'board_name': u'board', 'date': 31536001.100000001, 'blacklisted': False, 'read_status': None, 'depth': 1, 'author_id': 2, 'heading': u''} 
        self.assertEqual(1, len(result))
        self.assertEqual(expected_result, self._to_dict(result[0]))
        # XXX : 수정된 글의 경우 ... 
        #       이미 읽은 유저가 읽을 때 조회수가 올라가야 할까?

    def test_modification_with_heading(self):
        # 위의 것과 똑같은데 heading 의 변화만 관찰한다
        # Write an articles
        article_no = self._dummy_article_write(self.session_key_mikkang, u"", u"board_h", u"head1")
        # Modify its contents
        article_dic = {'title': u'MODIFIED TITLE', 'content': u'MODIFIED CONTENT', 'heading': u'head2'}
        result = self.engine.article_manager.modify_article(self.session_key_mikkang, u'board_h', article_no, WrittenArticle(**article_dic))
        self.assertEqual(article_no, result)
        # Now check it is modified or not
        result = self.engine.article_manager.read_article(self.session_key_mikkang, u'board_h', 1)
        expected_result = {'negative_vote': 0, 'positive_vote': 0, 'last_modified_date': 31536001.100000001, 'is_searchable': True, 'author_nickname': u'mikkang', 'reply_count': None, 'id': 1, 'title': u'MODIFIED TITLE', 'content': u'MODIFIED CONTENT', 'attach': None, 'type': None, 'author_username': u'mikkang', 'hit': 1, 'root_id': 1, 'deleted': False, 'board_name': u'board_h', 'date': 31536001.100000001, 'blacklisted': False, 'read_status': None, 'depth': 1, 'author_id': 2, 'heading': u'head2'} 
        self.assertEqual(1, len(result))
        self.assertEqual(expected_result, self._to_dict(result[0]))

    def test_nickname_modification(self):
        # 유저가 SYSOP일 경우에 nickname이 제대로 변화하는지 확인
        # Write two articles
        article_no0 = self._dummy_article_write(self.session_key_mikkang)
        article_no1 = self._dummy_article_write(self.session_key_mikkang)
        # Modify nickname of first article when the User is a sysop
        result = self.engine.article_manager.modify_nickname_in_article(self.session_key_sysop, u'board', article_no0, u'MODIFIED NICKNAME')
        self.assertEqual(article_no0, result)
        # Now check it is modified or not
        result = self.engine.article_manager.read_article(self.session_key_mikkang, u'board', 1)
        expected_result = {'negative_vote': 0, 'positive_vote': 0, 'last_modified_date': 31536001.100000001, 'is_searchable': True, 'author_nickname': u'MODIFIED NICKNAME', 'reply_count': None, 'id': 1, 'title': u'TITLE', 'content': u'CONTENT', 'attach': None, 'type': None, 'author_username': u'mikkang', 'hit': 1, 'root_id': 1, 'deleted': False, 'board_name': u'board', 'date': 31536001.100000001, 'blacklisted': False, 'read_status': None, 'depth': 1, 'author_id': 2, 'heading': u''}
        self.assertEqual(1, len(result))
        self.assertEqual(expected_result, self._to_dict(result[0]))
        result = self.engine.article_manager.read_article(self.session_key_mikkang, u'board', 2)
        expected_result = {'negative_vote': 0, 'positive_vote': 0, 'last_modified_date': 31536002.100000001, 'is_searchable': True, 'author_nickname': u'mikkang', 'reply_count': None, 'id': 2, 'title': u'TITLE', 'content': u'CONTENT', 'attach': None, 'type': None, 'author_username': u'mikkang', 'hit': 1, 'root_id': 2, 'deleted': False, 'board_name': u'board', 'date': 31536002.100000001, 'blacklisted': False, 'read_status': None, 'depth': 1, 'author_id': 2, 'heading': u''}
        self.assertEqual(1, len(result))
        self.assertEqual(expected_result, self._to_dict(result[0]))

    def test_read_and_hit_goes_up(self):
        # Write an article
        article_no = self._dummy_article_write(self.session_key_mikkang)
        # Author read the article
        self.engine.article_manager.read_article(self.session_key_mikkang, u'board', 1)
        # Another person read the article, and check hit goes up.
        result = self.engine.article_manager.read_article(self.session_key_serialx, u'board', 1)
        expected_result = {'negative_vote': 0, 'positive_vote': 0, 'last_modified_date': 31536001.100000001, 'is_searchable': True, 'author_nickname': u'mikkang', 'reply_count': None, 'id': 1, 'title': u'TITLE', 'content': u'CONTENT', 'attach': None, 'type': None, 'author_username': u'mikkang', 'hit': 2, 'root_id': 1, 'deleted': False, 'board_name': u'board', 'date': 31536001.100000001, 'blacklisted': False, 'read_status': None, 'depth': 1, 'author_id': 2, 'heading': u''}
        self.assertEqual(1, len(result))
        self.assertEqual(expected_result, self._to_dict(result[0]))
        # If author read the article again, it should not goes up.
        result = self.engine.article_manager.read_article(self.session_key_mikkang, u'board', 1)
        self.assertEqual(expected_result, self._to_dict(result[0]))
        # XXX : 제 3의 인물이 또 읽으면 hit 이 올라가는 거.

    def test_vote(self):
        session_keys = self.register_extra_users()

        # Writel an article
        article_no = self._dummy_article_write(self.session_key_mikkang)
        # Mikkang now positive vote
        self.engine.article_manager.vote_article(self.session_key_mikkang, u'board', article_no, True)
        # So the vote status must be updated.
        result = self.engine.article_manager.read_article(self.session_key_mikkang, u'board', 1)
        expected_result = {'negative_vote': 0, 'positive_vote': 1, 'last_modified_date': 31536001.100000001, 'is_searchable': True, 'author_nickname': u'mikkang', 'reply_count': None, 'id': 1, 'title': u'TITLE', 'content': u'CONTENT', 'attach': None, 'type': None, 'author_username': u'mikkang', 'hit': 1, 'root_id': 1, 'deleted': False, 'board_name': u'board', 'date': 31536001.100000001, 'blacklisted': False, 'read_status': None, 'depth': 1, 'author_id': 2, 'heading': u''} 
        self.assertEqual(1, len(result))
        self.assertEqual(expected_result, self._to_dict(result[0]))
        # Serialx now negative vote
        self.engine.article_manager.vote_article(self.session_key_serialx, u'board', article_no)
        # So the vote status must be updated again.
        result = self.engine.article_manager.read_article(self.session_key_mikkang, u'board', 1)
        expected_result = {'negative_vote': 0, 'positive_vote': 2, 'last_modified_date': 31536001.100000001, 'is_searchable': True, 'author_nickname': u'mikkang', 'reply_count': None, 'id': 1, 'title': u'TITLE', 'content': u'CONTENT', 'attach': None, 'type': None, 'author_username': u'mikkang', 'hit': 1, 'root_id': 1, 'deleted': False, 'board_name': u'board', 'date': 31536001.100000001, 'blacklisted': False, 'read_status': None, 'depth': 1, 'author_id': 2, 'heading': u''}
        self.assertEqual(1, len(result))
        self.assertEqual(expected_result, self._to_dict(result[0]))
        # But he can't vote again.
        try:
            self.engine.article_manager.vote_article(self.session_key_serialx, u'board', article_no)
            self.fail()
        except InvalidOperation:
            pass

        #Now, SYSOP is trying to vote the article without board name.
        self.engine.article_manager.vote_article(self.session_key_sysop, u'', article_no, True)
        # Then. the vote status must be updated AGAIN!
        result = self.engine.article_manager.read_article(self.session_key_mikkang, u'board', 1)
        expected_result['positive_vote'] = 3
        self.assertEqual(1, len(result))
        self.assertEqual(expected_result, self._to_dict(result[0]))

    def _vote(self, article_num, vote_num, board_name, session_keys):
        '''
        넉넉한 갯수의 session_key 를 받아 특정 게시물을 주어진만큼 추천한다

        @type  article_num: int
        @param article_num: 추천할 게시물의 번호
        @type  vote_num: int
        @param vote_num: 추천할 횟수 ( < len(session_keys))
        @type  board_name: str
        @param board_name: 추천할 게시물이 있는 board 이름
        @type  session_keys: list<str>
        @param session_keys: 추천에 사용할 session key 의 목록
        '''
        for session_key in session_keys[:vote_num]:
            self.engine.article_manager.vote_article(session_key, board_name, article_num)

    def _read(self, article_num, read_num, board_name, session_keys):
        '''
        넉넉한 갯수의 session_key 를 받아 특정 게시물을 주어진만큼 읽는다

        @type  article_num: int
        @param article_num: 읽을 게시물의 번호
        @type  read_num: int
        @param read_num: 읽을 횟수 ( < len(session_keys))
        @type  board_name: str
        @param board_name: 읽을 게시물이 있는 board 이름
        @type  session_keys: list<str>
        @param session_keys: 글읽기에 사용할 session key 의 목록
        '''
        for session_key in session_keys[:read_num]:
            self.engine.article_manager.read_article(session_key, board_name, article_num)

    def test_todays_best_and_weekly_best(self):
        session_keys = self.register_extra_users()

        # Phase 1.
        # Preparation - Step 1. Writing articles
        self._dummy_article_write(self.session_key_mikkang, u"", u"board")      #1
        self._dummy_article_write(self.session_key_mikkang, u"", u"board_hide") #2
        self._dummy_article_write(self.session_key_mikkang, u"", u"board_del")  #3
        self._dummy_article_write(self.session_key_mikkang, u"", u"board_hide") #4
        self._dummy_article_write(self.session_key_mikkang, u"", u"board")      #5
        self._dummy_article_write(self.session_key_mikkang, u"", u"board")      #6
        self._dummy_article_write(self.session_key_mikkang, u"", u"board_del")  #7
        self._dummy_article_write(self.session_key_mikkang, u"", u"board_hide") #8
        self._dummy_article_write(self.session_key_mikkang, u"", u"board_del")  #9

        # Preparation - Step 2. Vote (article no, vote num, board name)
        self._vote(4, 8, u"board_hide", session_keys)
        self._vote(9, 7, u"board_del", session_keys)
        self._vote(2, 6, u"board_hide", session_keys)
        self._vote(6, 5, u"board", session_keys)
        self._vote(7, 4, u"board_del", session_keys)
        self._vote(8, 3, u"board_hide", session_keys)
        self._vote(5, 2, u"board", session_keys)
        self._vote(3, 1, u"board_del", session_keys)

        # 추천한 대로 잘 뽑히는가?
        result = self.engine.article_manager.get_weekly_best_list(5)
        self.assertEqual(len(result), 5)
        self.assertEqual([4, 9, 2, 6, 7], [x.id for x in result])

        result = self.engine.article_manager.get_today_best_list(5)
        self.assertEqual(len(result), 5)
        self.assertEqual([4, 9, 2, 6, 7], [x.id for x in result])

        # 특정 게시판만 뽑을때는 잘 뽑히는가?
        result = self.engine.article_manager.get_weekly_best_list_specific('board_del')
        self.assertEqual(len(result), 3)
        self.assertEqual([9, 7, 3], [x.id for x in result])

        result = self.engine.article_manager.get_today_best_list_specific('board_del')
        self.assertEqual(len(result), 3)
        self.assertEqual([9, 7, 3], [x.id for x in result])

        # 게시판을 숨기면 잘 갱신되는가?
        self.engine.board_manager.hide_board(self.session_key_sysop, u'board_hide')
        result = self.engine.article_manager.get_weekly_best_list(5)
        self.assertEqual(len(result), 5)
        self.assertEqual([9, 6, 7, 5, 3], [x.id for x in result])

        result = self.engine.article_manager.get_today_best_list(5)
        self.assertEqual(len(result), 5)
        self.assertEqual([9, 6, 7, 5, 3], [x.id for x in result])

        # 보드를 지우면 잘 갱신되는가?
        self.engine.board_manager.delete_board(self.session_key_sysop, u'board_del')
        result = self.engine.article_manager.get_weekly_best_list(5)
        self.assertEqual(len(result), 3)
        self.assertEqual([6, 5, 1], [x.id for x in result])

        result = self.engine.article_manager.get_today_best_list(5)
        self.assertEqual(len(result), 3)
        self.assertEqual([6, 5, 1], [x.id for x in result])

        # 게시판을 숨김해제하면 잘 갱신되는가?
        self.engine.board_manager.return_hide_board(self.session_key_sysop, u'board_hide')
        result = self.engine.article_manager.get_weekly_best_list(5)
        self.assertEqual(len(result), 5)
        self.assertEqual([4, 2, 6, 8, 5], [x.id for x in result])

        result = self.engine.article_manager.get_today_best_list(5)
        self.assertEqual(len(result), 5)
        self.assertEqual([4, 2, 6, 8, 5], [x.id for x in result])

        # 게시물을 지우면 잘 갱신되는가?
        self.engine.article_manager.delete_article(self.session_key_mikkang, u'board_hide', 2)
        result = self.engine.article_manager.get_weekly_best_list(5)
        self.assertEqual(len(result), 5)
        self.assertEqual([4, 6, 8, 5, 1], [x.id for x in result])

        # 하루가 지났다. 새로운 글이 하나 올라왔다
        time.time.elapse(86400)
        self._dummy_article_write(self.session_key_mikkang, u"", u"board_hide") #10
        self._vote(10, 7, u"board_hide", session_keys)

        # Weekly Best 와 Today's Best 를 구해봐!
        result = self.engine.article_manager.get_weekly_best_list(5)
        self.assertEqual(len(result), 5)
        self.assertEqual([4, 10, 6, 8, 5], [x.id for x in result])

        result = self.engine.article_manager.get_today_best_list(5)
        self.assertEqual(len(result), 1)
        self.assertEqual([10], [x.id for x in result])

    def test_todays_most_and_weekly_most(self):
        session_keys = self.register_extra_users()

        # Phase 1.
        # Preparation - Step 1. Writing articles
        self._dummy_article_write(self.session_key_mikkang, u"", u"board")      #1
        self._dummy_article_write(self.session_key_mikkang, u"", u"board_hide") #2
        self._dummy_article_write(self.session_key_mikkang, u"", u"board_del")  #3
        self._dummy_article_write(self.session_key_mikkang, u"", u"board_hide") #4
        self._dummy_article_write(self.session_key_mikkang, u"", u"board")      #5
        self._dummy_article_write(self.session_key_mikkang, u"", u"board")      #6
        self._dummy_article_write(self.session_key_mikkang, u"", u"board_del")  #7
        self._dummy_article_write(self.session_key_mikkang, u"", u"board_hide") #8
        self._dummy_article_write(self.session_key_mikkang, u"", u"board_del")  #9

        # Preparation - Step 2. Vote (article no, vote num, board name)
        self._read(4, 8, u"board_hide", session_keys)
        self._read(9, 7, u"board_del", session_keys)
        self._read(2, 6, u"board_hide", session_keys)
        self._read(6, 5, u"board", session_keys)
        self._read(7, 4, u"board_del", session_keys)
        self._read(8, 3, u"board_hide", session_keys)
        self._read(5, 2, u"board", session_keys)
        self._read(3, 1, u"board_del", session_keys)

        # 추천한 대로 잘 뽑히는가?
        result = self.engine.article_manager.get_weekly_most_list(5)
        self.assertEqual(len(result), 5)
        self.assertEqual([4, 9, 2, 6, 7], [x.id for x in result])

        result = self.engine.article_manager.get_today_most_list(5)
        self.assertEqual(len(result), 5)
        self.assertEqual([4, 9, 2, 6, 7], [x.id for x in result])

        # 특정 게시판만 뽑을때는 잘 뽑히는가?
        result = self.engine.article_manager.get_weekly_most_list_specific('board_del')
        self.assertEqual(len(result), 3)
        self.assertEqual([9, 7, 3], [x.id for x in result])

        result = self.engine.article_manager.get_today_most_list_specific('board_del')
        self.assertEqual(len(result), 3)
        self.assertEqual([9, 7, 3], [x.id for x in result])

        # 게시판을 숨기면 잘 갱신되는가?
        self.engine.board_manager.hide_board(self.session_key_sysop, u'board_hide')
        result = self.engine.article_manager.get_weekly_most_list(5)
        self.assertEqual(len(result), 5)
        self.assertEqual([9, 6, 7, 5, 3], [x.id for x in result])

        result = self.engine.article_manager.get_today_most_list(5)
        self.assertEqual(len(result), 5)
        self.assertEqual([9, 6, 7, 5, 3], [x.id for x in result])

        # 보드를 지우면 잘 갱신되는가?
        self.engine.board_manager.delete_board(self.session_key_sysop, u'board_del')
        result = self.engine.article_manager.get_weekly_most_list(5)
        self.assertEqual(len(result), 3)
        self.assertEqual([6, 5, 1], [x.id for x in result])

        result = self.engine.article_manager.get_today_most_list(5)
        self.assertEqual(len(result), 3)
        self.assertEqual([6, 5, 1], [x.id for x in result])

        # 게시판을 숨김해제하면 잘 갱신되는가?
        self.engine.board_manager.return_hide_board(self.session_key_sysop, u'board_hide')
        result = self.engine.article_manager.get_weekly_most_list(5)
        self.assertEqual(len(result), 5)
        self.assertEqual([4, 2, 6, 8, 5], [x.id for x in result])

        result = self.engine.article_manager.get_today_most_list(5)
        self.assertEqual(len(result), 5)
        self.assertEqual([4, 2, 6, 8, 5], [x.id for x in result])

        # 게시물을 지우면 잘 갱신되는가?
        self.engine.article_manager.delete_article(self.session_key_mikkang, u'board_hide', 2)
        result = self.engine.article_manager.get_weekly_most_list(5)
        self.assertEqual(len(result), 5)
        self.assertEqual([4, 6, 8, 5, 1], [x.id for x in result])

        # 하루가 지났다. 새로운 글이 하나 올라왔다
        time.time.elapse(86400)
        self._dummy_article_write(self.session_key_mikkang, u"", u"board_hide") #10
        self._read(10, 7, u"board_hide", session_keys)

        # Weekly Best 와 Today's Best 를 구해봐!
        result = self.engine.article_manager.get_weekly_most_list(5)
        self.assertEqual(len(result), 5)
        self.assertEqual([4, 10, 6, 8, 5], [x.id for x in result])

        result = self.engine.article_manager.get_today_most_list(5)
        self.assertEqual(len(result), 1)
        self.assertEqual([10], [x.id for x in result])


    def test_many_replies(self):
        article_id = self._dummy_article_write(self.session_key_mikkang)
        reply_dic = WrittenArticle(**{'title':u'dummy', 'content': u'asdf', 'heading': u''})
        article_reply_id_1 = self.engine.article_manager.write_reply(self.session_key_mikkang, u'board', article_id, reply_dic)
        article_reply_id_2 = self.engine.article_manager.write_reply(self.session_key_mikkang, u'board', article_reply_id_1, reply_dic)
        article_reply_id_3 = self.engine.article_manager.write_reply(self.session_key_mikkang, u'board', article_reply_id_2, reply_dic)
        article_reply_id_4 = self.engine.article_manager.write_reply(self.session_key_mikkang, u'board', article_id, reply_dic)
        # Now check some
        article = self.engine.article_manager.read_article(self.session_key_mikkang, u'board', article_id)
        self.assertEqual(article_id, article[0].root_id)
        self.assertEqual(article_id, article[1].root_id)
        self.assertEqual(article_id, article[2].root_id)
        self.assertEqual(article_id, article[3].root_id)
        self.assertEqual(article_id, article[4].root_id)
        self.assertEqual(1, article[0].depth)
        self.assertEqual(2, article[1].depth)
        self.assertEqual(3, article[2].depth)
        self.assertEqual(4, article[3].depth)
        self.assertEqual(2, article[4].depth)
        # And check reply_count
        list = self.engine.article_manager.article_list(self.session_key_mikkang, u'board', u'', 1, 5)
        self.assertEqual(4, list.hit[0].reply_count)

    def test_blacklist(self):
        # mikkang write an article. mikkang was in serialx's blacklist.
        # Then mikkang's article should be marked as blacklisted.
        # XXX 아라라 프로젝트 생각 :
        # 장기적으로는 Middleware 가 Frontend 에게 보내는 정보량을
        # 어떻게 최소화할 지에 대해서도 생각해야한다 ... (combacsa)
        self.engine.blacklist_manager.add_blacklist(self.session_key_serialx, u'mikkang')
        article_id = self._dummy_article_write(self.session_key_mikkang)
        expected_result = {'negative_vote': 0, 'positive_vote': 0, 'last_modified_date': 31536001.100000001, 'is_searchable': True, 'author_nickname': u'mikkang', 'reply_count': None, 'id': 1, 'title': u'TITLE', 'content': u'CONTENT', 'attach': None, 'type': None, 'author_username': u'mikkang', 'hit': 1, 'root_id': 1, 'deleted': False, 'board_name': u'board', 'date': 31536001.100000001, 'blacklisted': True, 'read_status': None, 'depth': 1, 'author_id': 2, 'heading': u''}
        result = self.engine.article_manager.read_article(self.session_key_serialx, u'board', 1)
        self.assertEqual(1, len(result))
        self.assertEqual(expected_result, self._to_dict(result[0]))

    def test_get_article_list_and_article_list_and_article_list_below(self):
        # ArticleManager.get_article_list 와 article_list, article_list_below 테스트가 목적이다.
        # 게시판에 적당한 갯수의 글을 쓰고 적당한 page 의 상황을 확인한다
        for i in range(55):
            if i % 2 == 1:
                self._dummy_article_write(self.session_key_mikkang, u"", u"board_h")
            else:
                self._dummy_article_write(self.session_key_mikkang, u"", u"board_h", u"head1")

        # TEST 1 : 모든 heading 을 불러와보자
        article_list, _ = self.engine.article_manager.get_article_list(u'board_h', u"", 1, 5)
        self.assertEqual([55, 54, 53, 52, 51], [x.id for x in article_list.hit])
        self.assertEqual(11, article_list.last_page)
        self.assertEqual(55, article_list.results)

        # 관심 있는 것은 글의 id 와 heading 이다.
        result = self.engine.article_manager.article_list(self.session_key_serialx, u"board_h", u"", 1, 5)
        self.assertEqual(55, result.results)
        self.assertEqual(11, result.last_page)
        self.assertEqual([55, 54, 53, 52, 51], [x.id for x in result.hit])
        self.assertEqual([u'head1', u'', u'head1', u'', u'head1'], [x.heading for x in result.hit])

        result = self.engine.article_manager.article_list_below(self.session_key_serialx, u"board_h", u"", 55, 5)
        self.assertEqual(55, result.results)
        self.assertEqual(11, result.last_page)
        self.assertEqual([55, 54, 53, 52, 51], [x.id for x in result.hit])
        self.assertEqual([u'head1', u'', u'head1', u'', u'head1'], [x.heading for x in result.hit])

        # TEST 2 : heading 이 없는 것만
        article_list, _ = self.engine.article_manager.get_article_list(u'board_h', u"", 1, 5, False)
        self.assertEqual([54, 52, 50, 48, 46], [x.id for x in article_list.hit])
        self.assertEqual(6,  article_list.last_page)
        self.assertEqual(27, article_list.results)

        result = self.engine.article_manager.article_list(self.session_key_serialx, u"board_h", u"", 1, 5, False)
        self.assertEqual(27, result.results)
        self.assertEqual(6, result.last_page)
        self.assertEqual([54, 52, 50, 48, 46], [x.id for x in result.hit])
        self.assertEqual([u'', u'', u'', u'', u''], [x.heading for x in result.hit])

        result = self.engine.article_manager.article_list_below(self.session_key_serialx, u"board_h", u"", 54, 5, False)
        self.assertEqual(27, result.results)
        self.assertEqual(6, result.last_page)
        self.assertEqual([54, 52, 50, 48, 46], [x.id for x in result.hit])
        self.assertEqual([u'', u'', u'', u'', u''], [x.heading for x in result.hit])

        # TEST 3 : heading == head1
        article_list, _ = self.engine.article_manager.get_article_list(u'board_h', u"head1", 1, 5, False)
        self.assertEqual([55, 53, 51, 49, 47], [x.id for x in article_list.hit])
        self.assertEqual(6, article_list.last_page)
        self.assertEqual(28, article_list.results)

        result = self.engine.article_manager.article_list(self.session_key_serialx, u"board_h", u"head1", 1, 5, False)
        self.assertEqual(28, result.results)
        self.assertEqual(6, result.last_page)
        self.assertEqual([55, 53, 51, 49, 47], [x.id for x in result.hit])
        self.assertEqual([u'head1', u'head1', u'head1', u'head1', u'head1'], [x.heading for x in result.hit])

        result = self.engine.article_manager.article_list_below(self.session_key_serialx, u"board_h", u"head1", 55, 5, False)
        self.assertEqual(28, result.results)
        self.assertEqual(6, result.last_page)
        self.assertEqual([55, 53, 51, 49, 47], [x.id for x in result.hit])
        self.assertEqual([u'head1', u'head1', u'head1', u'head1', u'head1'], [x.heading for x in result.hit])

    def test_article_list_below(self):
        for i in range(100):
            self._dummy_article_write(self.session_key_mikkang)

        l = self.engine.article_manager.article_list_below(self.session_key_mikkang, u'board', u'', 75, 10)
        self.assertEqual(l.hit[0].id, 80)
        self.assertEqual(l.last_page, 10)
        l = self.engine.article_manager.article_list_below(self.session_key_mikkang, u'board', u'', 84, 10)
        self.assertEqual(l.hit[0].id, 90)
        l = self.engine.article_manager.article_list_below(self.session_key_mikkang, u'board', u'', 95, 10)
        self.assertEqual(l.hit[0].id, 100)

        # 경계값 테스트
        l = self.engine.article_manager.article_list_below(self.session_key_mikkang, u'board', u'', 71, 10)
        self.assertEqual(l.hit[0].id, 80)
        l = self.engine.article_manager.article_list_below(self.session_key_mikkang, u'board', u'', 70, 10)
        self.assertEqual(l.hit[0].id, 70)

    def test_article_list_for_all_board(self):
        # 테스트용 게시판을 두 개 만들자.
        self.engine.board_manager.add_board(self.session_key_sysop, u'total1', u'total1', u'Test Board', [])
        self.engine.board_manager.add_board(self.session_key_sysop, u'total2', u'total2', u'Test Board', [])

        # 게시판 2개에 섞어서 글을 쓰자.
        for i in range(55):
            if i % 2 == 1:
                self._dummy_article_write(self.session_key_mikkang, unicode(i), u"total1")
            else:
                self._dummy_article_write(self.session_key_mikkang, unicode(i), u"total2")

        # 검사!
        l = self.engine.article_manager.article_list(self.session_key_mikkang, u'', u'', 1, 20, True)
        self.assertEqual(u'TITLE54', l.hit[0].title)
        self.assertEqual(u'total2',  l.hit[0].board_name)
        self.assertEqual(u'TITLE53', l.hit[1].title)
        self.assertEqual(u'total1',  l.hit[1].board_name)
        self.assertEqual(u'TITLE35', l.hit[19].title)
        self.assertEqual(u'total1',  l.hit[19].board_name)
        self.assertEqual(3, l.last_page)

        # article_list_below 에 대해서도!
        l = self.engine.article_manager.article_list_below(self.session_key_mikkang, u'', u'', 34, 20, True)
        self.assertEqual(u'TITLE34', l.hit[0].title)
        self.assertEqual(u'total2',  l.hit[0].board_name)
        self.assertEqual(u'TITLE33', l.hit[1].title)
        self.assertEqual(u'total1',  l.hit[1].board_name)
        self.assertEqual(u'TITLE15', l.hit[19].title)
        self.assertEqual(u'total1',  l.hit[19].board_name)
        self.assertEqual(3, l.last_page)

        # 게시판 'total1'을 숨겼을 때 제대로 나타나는지 검사!
        self.engine.board_manager.hide_board(self.session_key_sysop, u'total1')
        l = self.engine.article_manager.article_list(self.session_key_mikkang, u'', u'', 1, 20, True)
        self.assertEqual(u'TITLE54', l.hit[0].title)
        self.assertEqual(u'total2',  l.hit[0].board_name)
        self.assertEqual(u'TITLE52', l.hit[1].title)
        self.assertEqual(u'total2',  l.hit[1].board_name)
        self.assertEqual(u'TITLE16', l.hit[19].title)
        self.assertEqual(u'total2',  l.hit[19].board_name)
        self.assertEqual(2, l.last_page)
        
        l = self.engine.article_manager.article_list_below(self.session_key_mikkang, u'', u'', 14, 20, True)
        self.assertEqual(u'TITLE14', l.hit[0].title)
        self.assertEqual(u'total2',  l.hit[0].board_name)
        self.assertEqual(u'TITLE12', l.hit[1].title)
        self.assertEqual(u'total2',  l.hit[1].board_name)
        self.assertEqual(u'TITLE0', l.hit[7].title)
        self.assertEqual(u'total2',  l.hit[7].board_name)
        self.assertEqual(2, l.last_page)

        # 게시판 'total1'을 숨김 해제하고 'total2'를 지웠을 때 제대로 나타나는지 검사!
        self.engine.board_manager.return_hide_board(self.session_key_sysop, u'total1')
        self.engine.board_manager.delete_board(self.session_key_sysop, u'total2')
        l = self.engine.article_manager.article_list(self.session_key_mikkang, u'', u'', 1, 20, True)
        self.assertEqual(u'TITLE53', l.hit[0].title)
        self.assertEqual(u'total1',  l.hit[0].board_name)
        self.assertEqual(u'TITLE51', l.hit[1].title)
        self.assertEqual(u'total1',  l.hit[1].board_name)
        self.assertEqual(u'TITLE15', l.hit[19].title)
        self.assertEqual(u'total1',  l.hit[19].board_name)
        self.assertEqual(2, l.last_page)
        
        l = self.engine.article_manager.article_list_below(self.session_key_mikkang, u'', u'', 13, 20, True)
        self.assertEqual(u'TITLE13', l.hit[0].title)
        self.assertEqual(u'total1',  l.hit[0].board_name)
        self.assertEqual(u'TITLE11', l.hit[1].title)
        self.assertEqual(u'total1',  l.hit[1].board_name)
        self.assertEqual(u'TITLE1', l.hit[6].title)
        self.assertEqual(u'total1',  l.hit[6].board_name)
        self.assertEqual(2, l.last_page)

    def test__get_article(self):
        # 두 개의 서로 다른 게시판에 글을 쓴다.
        self._dummy_article_write(self.session_key_mikkang, u"1", u"board")
        self._dummy_article_write(self.session_key_mikkang, u"a", u"board_h")
        # SQLAlchemy Session 을 열고 테스트해보자.
        session = arara.model.Session()
        result11 = self.engine.article_manager._get_article(session, 1, 1)
        result12 = self.engine.article_manager._get_article(session, 2, 2)
        result21 = self.engine.article_manager._get_article(session, None, 1)
        result22 = self.engine.article_manager._get_article(session, None, 2)
        self.assertEqual(1, result11.id)
        self.assertEqual(1, result21.id)
        self.assertEqual(2, result12.id)
        self.assertEqual(2, result22.id)
        # 세션을 닫는다.
        session.close()

    def test_move_article(self):
        #유저가 SYSOP 일 경우 글을 선택해서 다른 게시판으로 옮길 수 있는지 테스트 한다.
        # Write an article, reply to the article, and create board2
        article_no1 = self._dummy_article_write(self.session_key_mikkang)
        reply_dic = WrittenArticle(**{'title':u'dummy', 'content': u'asdf', 'heading': u''})
        time.time.elapse(1)
        reply_no2 = self.engine.article_manager.write_reply(self.session_key_mikkang, u'board', 1, reply_dic)
        time.time.elapse(1)
        reply_no3 = self.engine.article_manager.write_reply(self.session_key_mikkang, u'board', 2, reply_dic)
        self.engine.board_manager.add_board(self.session_key_sysop, u'board2', u'board2', u'Test Board2', [])
        # Vote for article
        self.engine.article_manager.vote_article(self.session_key_mikkang, u'board', article_no1, True)
        # Move articles from board to board2
        self.engine.article_manager.move_article(self.session_key_sysop, u'board', article_no1, u'board2')
        # Check if an article is moved well
        result = self.engine.article_manager.read_article(self.session_key_mikkang, u'board2', 1)
        expected_result = {'negative_vote': 0, 'positive_vote': 1, 'last_modified_date': 31536001.100000001, 'is_searchable': True, 'author_nickname': u'mikkang', 'reply_count': None, 'id': 1, 'title': u'TITLE', 'content': u'CONTENT', 'attach': None, 'type': None, 'author_username': u'mikkang', 'hit': 1, 'root_id': 1, 'deleted': False, 'board_name': u'board2', 'date': 31536001.100000001, 'blacklisted': False, 'read_status': None, 'depth': 1, 'author_id': 2, 'heading': u''}
        self.assertEqual(expected_result, self._to_dict(result[0]))
        expected_result = {'negative_vote': 0, 'positive_vote': 0, 'last_modified_date': 31536002.100000001, 'is_searchable': True, 'author_nickname': u'mikkang', 'reply_count': None, 'id': 2, 'title': u'dummy', 'content': u'asdf', 'attach': None, 'type': None, 'author_username': u'mikkang', 'hit': 0, 'root_id': 1, 'deleted': False, 'board_name': u'board2', 'date': 31536002.100000001, 'blacklisted': False, 'read_status': None, 'depth': 2, 'author_id': 2, 'heading': u''}
        self.assertEqual(expected_result, self._to_dict(result[1]))
        expected_result = {'negative_vote': 0, 'positive_vote': 0, 'last_modified_date': 31536003.100000001, 'is_searchable': True, 'author_nickname': u'mikkang', 'reply_count': None, 'id': 3, 'title': u'dummy', 'content': u'asdf', 'attach': None, 'type': None, 'author_username': u'mikkang', 'hit': 0, 'root_id': 1, 'deleted': False, 'board_name': u'board2', 'date': 31536003.100000001, 'blacklisted': False, 'read_status': None, 'depth': 3, 'author_id': 2, 'heading': u''}
        self.assertEqual(expected_result, self._to_dict(result[2]))
        # TODO: article_vote_status table 의 board_id가 바뀌는 것 확인하기? files 의 board_id가 바뀌는 것 확인하기?

    def test_change_article_heading(self):
        session_keys = self.register_extra_users()

        # 테스트를 위해 말머리가 2개 있는 보드를 생성한다.
        self.engine.board_manager.add_board(self.session_key_sysop, u'testboard', u'글머리가 있는 테스트보드', u'Test Board with heading', [u'heading1', u'heading2'])

        # 글을 2개의 말머리를 섞어서 작성한다.
        article1 = self._dummy_article_write(session_keys[0], board_name = 'testboard', heading = 'heading1')
        article2 = self._dummy_article_write(session_keys[1], board_name = 'testboard', heading = 'heading1')
        article3 = self._dummy_article_write(session_keys[3], board_name = 'testboard', heading = 'heading2')
        article4 = self._dummy_article_write(session_keys[4], board_name = 'testboard', heading = 'heading2')
        article5 = self._dummy_article_write(session_keys[8], board_name = 'testboard', heading = 'heading1')

        # 말머리 1의 글을 모두 말머리 2로 옮기고, 전부 옮겨지는지 확인한다.
        self.engine.article_manager.change_article_heading(self.session_key_sysop, 'testboard', 'heading1', 'heading2')
        self.assertEqual(ArticleList(last_page=1, hit=[], results=0, current_page=1), self.engine.article_manager.article_list(self.session_key_sysop, 'testboard', 'heading1', include_all_headings = False))
        articleListOfHeading2 = self.engine.article_manager.article_list(self.session_key_sysop, 'testboard', 'heading2', include_all_headings = False).hit 
        self.assertEqual(5, len(articleListOfHeading2))
        self.assertEqual(Article(negative_vote=0, positive_vote=0, last_modified_date=31536005.100000001, is_searchable=True, author_nickname=u'wiki', reply_count=0, id=5, title=u'TITLE', content=None, attach=None, type='normal', author_username=u'wiki', hit=0, root_id=None, deleted=False, board_name=u'testboard', date=31536005.100000001, blacklisted=False, read_status='N', depth=None, author_id=9, heading=u'heading2', anonymous=False), articleListOfHeading2[0])

        # TODO: 말머리 1의 글이 전부 없어진 것 확인
        # TODO: 변수 이름 camelcase 에서 소문자와 언더바로 바꾸기
        # 말머리 2의 글의 말머리를 전부 없앤다.
        self.engine.article_manager.change_article_heading(self.session_key_sysop, 'testboard', 'heading2', '')
        articleListOfNoHeading = self.engine.article_manager.article_list(self.session_key_sysop, 'testboard', '', include_all_headings = False).hit 
        self.assertEqual(5, len(articleListOfNoHeading))

    def test_remaining_article_count(self):
        # 글 10개를 쓰고 테스트해보자.
        for idx in xrange(10):
            self._dummy_article_write(self.session_key_sysop)
        session = arara.model.Session()
        self.assertEqual(9, self.engine.article_manager._get_remaining_article_count(session, None, None, 1, True, 0))
        self.assertEqual(8, self.engine.article_manager._get_remaining_article_count(session, None, None, 2, True, 0))
        self.assertEqual(7, self.engine.article_manager._get_remaining_article_count(session, None, None, 3, True, 0))
        self.assertEqual(6, self.engine.article_manager._get_remaining_article_count(session, None, None, 4, True, 0))
        self.assertEqual(5, self.engine.article_manager._get_remaining_article_count(session, None, None, 5, True, 0))
        self.assertEqual(4, self.engine.article_manager._get_remaining_article_count(session, None, None, 6, True, 0))
        self.assertEqual(3, self.engine.article_manager._get_remaining_article_count(session, None, None, 7, True, 0))
        self.assertEqual(2, self.engine.article_manager._get_remaining_article_count(session, None, None, 8, True, 0))
        self.assertEqual(1, self.engine.article_manager._get_remaining_article_count(session, None, None, 9, True, 0))
        self.assertEqual(0, self.engine.article_manager._get_remaining_article_count(session, None, None, 10, True, 0))

        # 답글을 달고 Listing Method 를 바꿔 보자.
        reply_dic = WrittenArticle(**{'title':u'dummy', 'content': u'asdf', 'heading': u''})
        time.time.elapse(1)
        reply_id   = self.engine.article_manager.write_reply(self.session_key_mikkang, u'board', 1, reply_dic)
        time.time.elapse(1)
        reply_id   = self.engine.article_manager.write_reply(self.session_key_mikkang, u'board', 3, reply_dic)
        time.time.elapse(1)
        reply_id   = self.engine.article_manager.write_reply(self.session_key_mikkang, u'board', 6, reply_dic)

        self.assertEqual(9, self.engine.article_manager._get_remaining_article_count(session, None, None, 2, True, 1))
        self.assertEqual(8, self.engine.article_manager._get_remaining_article_count(session, None, None, 4, True, 1))
        self.assertEqual(7, self.engine.article_manager._get_remaining_article_count(session, None, None, 5, True, 1))
        self.assertEqual(6, self.engine.article_manager._get_remaining_article_count(session, None, None, 7, True, 1))
        self.assertEqual(5, self.engine.article_manager._get_remaining_article_count(session, None, None, 8, True, 1))
        self.assertEqual(4, self.engine.article_manager._get_remaining_article_count(session, None, None, 9, True, 1))
        self.assertEqual(3, self.engine.article_manager._get_remaining_article_count(session, None, None, 10, True, 1))
        self.assertEqual(2, self.engine.article_manager._get_remaining_article_count(session, None, None, 1, True, 1))
        self.assertEqual(1, self.engine.article_manager._get_remaining_article_count(session, None, None, 3, True, 1))
        self.assertEqual(0, self.engine.article_manager._get_remaining_article_count(session, None, None, 6, True, 1))
        session.close()

    def test_article_listing_order_concurrency(self):
        article1 = self._dummy_article_write(self.session_key_sysop, board_name = 'board')
        article2 = self._dummy_article_write(self.session_key_sysop, board_name = 'board')
        article3 = self._dummy_article_write(self.session_key_sysop, board_name = 'board')
        reply_dic = WrittenArticle(**{'title':u'dummy', 'content': u'asdf', 'heading': u''})
        article4 = self.engine.article_manager.write_reply(self.session_key_mikkang, u'board', 1, reply_dic)

        # 이러한 상황에서 article_list 와 article_list_below 는 3, 2, 1 순으로 글을 보여준다.
        list1 = self.engine.article_manager.article_list(self.session_key_mikkang, u'board', u'', 1, 10).hit
        list2 = self.engine.article_manager.article_list_below(self.session_key_mikkang, u'board', u'', 1, 10).hit
        self.assertEqual(list1, list2)

        # mikkang 의 글 목록 방식을 바꾼다.
        self.engine.member_manager.change_listing_mode(self.session_key_mikkang, 1)

        # 그래도 여전히 article_list 와 article_list_below 는 같다.
        list1 = self.engine.article_manager.article_list(self.session_key_mikkang, u'board', u'', 1, 10).hit
        list2 = self.engine.article_manager.article_list_below(self.session_key_mikkang, u'board', u'', 1, 10).hit
        self.assertEqual(list1, list2)
 
    def test_get_page_no_of_article(self):
        # 1개의 글은 1번째 페이지에 위치
        self._dummy_article_write(self.session_key_mikkang)
        self.assertEqual(1, self.engine.article_manager.get_page_no_of_article(u'board', u'', 1, 5))

        # 게시물이 6개가 되면 2-6번 글은 1페이지, 1번 글은 2페이지에 위치해야 한다
        for _ in xrange(5):
            self._dummy_article_write(self.session_key_mikkang)
        self.assertEqual(1, self.engine.article_manager.get_page_no_of_article(u'board', u'', 2, 5))
        self.assertEqual(2, self.engine.article_manager.get_page_no_of_article(u'board', u'', 1, 5))

    def test_put_user_specific_info(self):
        # 사용자에 따른 정보가 바르게 입혀지는지 확인
        self.engine.read_status_manager.mark_as_read_list(self.session_key_mikkang, [1, 3, 5])
        article_list = ttypes.ArticleList(hit=[ttypes.Article(id=1),
                                               ttypes.Article(id=2),
                                               ttypes.Article(id=3),
                                               ttypes.Article(id=4),
                                               ttypes.Article(id=5)])
        self.engine.article_manager.put_user_specific_info(2, article_list, [1, 2, 3, 4, 5])
        self.assertEqual(['R', 'N', 'R', 'N', 'R'], [x.read_status for x in article_list.hit])

        # 로그인하지 않은 사용자의 경우 모든 글이 새 글
        self.engine.article_manager.put_user_specific_info(-1, article_list, [1, 2, 3, 4, 5])
        self.assertEqual(['N', 'N', 'N', 'N', 'N'], [x.read_status for x in article_list.hit])

    def test_article_list_by_user(self):
        id_list = []
        for x in xrange(10):
            id_list.append(self._dummy_article_write(self.session_key_mikkang))

        article_list = self.engine.article_manager.get_article_list_by_username(self.engine.login_manager.get_session(self.session_key_mikkang).username)
        self.assertEqual(sorted(id_list), sorted([article.id for article in article_list]))

        id_list = []
        for x in xrange(10):
            id_list.append(self._dummy_article_write(self.session_key_serialx))

        article_list = self.engine.article_manager.get_article_list_by_username(self.engine.login_manager.get_session(self.session_key_serialx).username)
        self.assertEqual(sorted(id_list), sorted([article.id for article in article_list]))
        

    def get_get_page_info(self):
        self.assertEqual((2, 6, 2), self.engine.article_manager.get_page_info(6, 1, 5))
        self.assertEqual((3, 11, 7), self.engine.article_manager.get_page_info(11, 1, 5))

        try:
            self.engine.article_manager.get_page_info(6, 3, 5)
            self.fail("Getting page info of nonexisting page must fail.")
        except ValueError as e:
            self.assertEqual("WRONG_PAGENUM", str(e))

    def test_get_last_article_no(self):
        self.assertEqual(self.engine.article_manager._get_last_article_no(), None)
        self._dummy_article_write(self.session_key_mikkang)
        self._dummy_article_write(self.session_key_mikkang)
        self.assertEqual(self.engine.article_manager._get_last_article_no(), 2)

    def test_scrap_and_unscrap_article(self):
        session_keys = self.register_extra_users()
        # Write two articles
        article_no1 = self._dummy_article_write(session_keys[3])
        article_no2 = self._dummy_article_write(self.session_key_serialx)

        # Mikkang now scrap hodduc's article
        self.engine.article_manager.scrap_article(self.session_key_mikkang, article_no1)

        # So the mikkang's scrapped_article will be updated.
        session = arara.model.Session()
        article1 = session.query(arara.model.Article).filter_by(id=article_no1).one()
        mikkang_instance = session.query(arara.model.User).filter_by(username=u'mikkang').one()
        scraplist = mikkang_instance.scrapped_articles
        self.assertEqual(len(scraplist), 1)
        self.assertEqual(scraplist[0].article.id, article1.id)
        session.close()

        # Mikkang now scrap serialx's article
        self.engine.article_manager.scrap_article(self.session_key_mikkang, article_no2)

        # So the mikkang's scrapped_article will be updated again.
        session = arara.model.Session()
        article2 = session.query(arara.model.Article).filter_by(id=article_no2).one()
        mikkang_instance = session.query(arara.model.User).filter_by(username=u'mikkang').one()
        scraplist = mikkang_instance.scrapped_articles
        self.assertEqual(len(scraplist), 2)
        self.assertEqual(scraplist[0].article.id, article1.id)
        self.assertEqual(scraplist[1].article.id, article2.id)
        session.close()

        # But he can't scrap again.
        try:
            self.engine.article_manager.scrap_article(self.session_key_mikkang, article_no1)
            self.fail()
        except InvalidOperation:
            pass

        # Try Scrap without article number.
        try:
            self.engine.article_manager.scrap_article(self.session_key_mikkang, -1)
            self.fail()
        except InvalidOperation:
            pass

        # Now, Try Unscrap one.
        try:
            self.engine.article_manager.unscrap_article(self.session_key_serialx, article_no1)
            self.fail()
        except InvalidOperation:
            pass
        try:
            self.engine.article_manager.unscrap_article(self.session_key_mikkang, -1)
            self.fail()
        except InvalidOperation:
            pass

        self.engine.article_manager.unscrap_article(self.session_key_mikkang, article_no1)
        session = arara.model.Session()
        mikkang_instance = session.query(arara.model.User).filter_by(username=u'mikkang').one()
        scraplist = mikkang_instance.scrapped_articles
        self.assertEqual(len(scraplist), 1)
        self.assertEqual(scraplist[0].article.id, article_no2)
        session.close()

        # He can't unscrap again
        try:
            self.engine.article_manager.unscrap_article(self.session_key_mikkang, article_no1)
            self.fail()
        except InvalidOperation:
            pass

    def test_scrapped_article_list_and_below(self):
        # 테스트용 게시판 만들자.
        self.engine.board_manager.add_board(self.session_key_sysop, u'scrap1', u'Test Board', u'')

        # 게시판에 글을 쓰자. 짝수 번째 게시물은 특별히 스크랩 해준다
        for i in xrange(1, 101):
            no = self._dummy_article_write(self.session_key_mikkang, unicode(i), u"scrap1")
            if not i % 2:
                self.engine.article_manager.scrap_article(self.session_key_mikkang, no)

        # 1 페이지를 가져와 보자
        l = self.engine.article_manager.scrapped_article_list(self.session_key_mikkang, 1)
        self.assertEqual(u'TITLE100', l.hit[0].title)
        self.assertEqual(u'TITLE98', l.hit[1].title)
        self.assertEqual(u'TITLE62', l.hit[19].title)
        self.assertEqual(3, l.last_page)
        self.assertEqual(50, l.results)
        self.assertEqual(1, l.current_page)

        # 2 페이지를 가져와 보자
        l = self.engine.article_manager.scrapped_article_list(self.session_key_mikkang, 2)
        self.assertEqual(u'TITLE60', l.hit[0].title)
        self.assertEqual(u'TITLE58', l.hit[1].title)
        self.assertEqual(u'TITLE22', l.hit[19].title)
        self.assertEqual(3, l.last_page)
        self.assertEqual(50, l.results)
        self.assertEqual(2, l.current_page)

        # 3 페이지를 가져와 보자
        l = self.engine.article_manager.scrapped_article_list(self.session_key_mikkang, 3)
        self.assertEqual(u'TITLE20', l.hit[0].title)
        self.assertEqual(u'TITLE18', l.hit[1].title)
        self.assertEqual(u'TITLE2', l.hit[9].title)
        self.assertEqual(10, len(l.hit))
        self.assertEqual(3, l.last_page)
        self.assertEqual(50, l.results)
        self.assertEqual(3, l.current_page)

        # 100번 글을 읽었을 때 below 확인
        l = self.engine.article_manager.scrapped_article_list_below(self.session_key_mikkang, 100, 20)
        self.assertEqual(u'TITLE100', l.hit[0].title)
        self.assertEqual(u'TITLE62', l.hit[19].title)
        self.assertEqual(1, l.current_page)

        # 62번 글을 읽었을 때 below 확인
        l = self.engine.article_manager.scrapped_article_list_below(self.session_key_mikkang, 62, 20)
        self.assertEqual(u'TITLE100', l.hit[0].title)
        self.assertEqual(u'TITLE62', l.hit[19].title)
        self.assertEqual(1, l.current_page)

        # 60번 글을 읽었을 때 below 확인
        l = self.engine.article_manager.scrapped_article_list_below(self.session_key_mikkang, 60, 20)
        self.assertEqual(u'TITLE60', l.hit[0].title)
        self.assertEqual(u'TITLE22', l.hit[19].title)
        self.assertEqual(2, l.current_page)

        # 2번 글을 읽었을 때 below 확인
        l = self.engine.article_manager.scrapped_article_list_below(self.session_key_mikkang, 2, 20)
        self.assertEqual(u'TITLE20', l.hit[0].title)
        self.assertEqual(u'TITLE2', l.hit[9].title)
        self.assertEqual(10, len(l.hit))
        self.assertEqual(3, l.current_page)

    def test_notice(self):
        article_id = self._dummy_article_write(self.session_key_mikkang)
        self.assertEqual(0, self.engine.article_manager.notice_list(u'board').results)
        # 1. 시삽 권한 없이 공지로 만든다
        try:
            self.engine.article_manager.register_notice(self.session_key_mikkang, article_id)
            self.fail('register with notice by normal user must fail.')
        except InvalidOperation:
            pass
        # 2. 시삽이 공지로 만든다
        self.engine.article_manager.register_notice(self.session_key_sysop, article_id)
        self.assertEqual(1, self.engine.article_manager.notice_list(u'board').results)
        # 3. 다른 글도 공지로 만든다
        article_id2 = self._dummy_article_write(self.session_key_mikkang)
        self.engine.article_manager.register_notice(self.session_key_sysop, article_id2)
        self.assertEqual(2, self.engine.article_manager.notice_list(u'board').results)
        # 4. 이미 있는 글을 공지로 만들어본다
        try:
            self.engine.article_manager.register_notice(self.session_key_sysop, article_id)
            self.fail('Register notice to notice must fail.')
        except InvalidOperation:
            pass
        # 5. 시삽 권한 없이 공지에서 내린다
        try:
            self.engine.article_manager.unregister_notice(self.session_key_mikkang, article_id)
            self.fail('unregister with notice by normal user must fail.')
        except InvalidOperation:
            pass
        # 6. 시삽이 공지에서 내린다
        self.engine.article_manager.unregister_notice(self.session_key_sysop, article_id)
        self.assertEqual(1, self.engine.article_manager.notice_list(u'board').results)

        # 6. 공지가 아닌 글을 공지에서 내려본다
        try:
            self.engine.article_manager.unregister_notice(self.session_key_sysop, article_id)
            self.fail('Unregistering an article that is not a notice must fail.')
        except InvalidOperation:
            pass

        self.assertEqual(0, self.engine.article_manager.notice_list(u'board_h').results)

    def test_recent_articles(self):
        # 글을 쓴다. 두 게시판에 5개씩.
        self.engine.board_manager.add_board(self.session_key_sysop, u'board2', u'테스트보드2', u'Test Board2', [])
        for i in range(5):
            self._dummy_article_write(self.session_key_mikkang, title_append=str(i), board_name='board')
        for i in range(5):
            self._dummy_article_write(self.session_key_serialx, title_append=str(i+5), board_name='board2')

        # 최근 게시물을 가져와본다.
        recent_of_board = self.engine.article_manager.recent_article_list('board')
        recent_of_board2 = self.engine.article_manager.recent_article_list('board2')
        self.assertEqual(['TITLE4', 'TITLE3', 'TITLE2', 'TITLE1', 'TITLE0'], [a.title for a in recent_of_board])
        self.assertEqual(['TITLE9', 'TITLE8', 'TITLE7', 'TITLE6', 'TITLE5'], [a.title for a in recent_of_board2])

        recent_of_board = self.engine.article_manager.recent_article_list('board', count=3)
        recent_of_board2 = self.engine.article_manager.recent_article_list('board2', count=3)
        self.assertEqual(['TITLE4', 'TITLE3', 'TITLE2'], [a.title for a in recent_of_board])
        self.assertEqual(['TITLE9', 'TITLE8', 'TITLE7'], [a.title for a in recent_of_board2])

        # OK
 
    def tearDown(self):
        super(ArticleManagerTest, self).tearDown()
 
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(ArticleManagerTest)

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
