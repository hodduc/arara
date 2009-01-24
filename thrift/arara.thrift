namespace py arara

exception DatabaseError {
    1: string why
}

exception InvalidOperation {
    1: string why
}

typedef i32 id_t

struct VisitorCount {
    1: i32 total_visitor_count,
    2: i32 today_visitor_count,
}

struct Session {
    1: string username,
    2: string user_ip,
    3: i64 login_time,
}

struct LoggedUser {
    1: string username,
    2: string ip,
    3: string current_action,
    4: string nickname,
    5: i64 logintime,
}

service LoginManager {
    string guest_login(1:string guest_ip)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    VisitorCount total_visitor()
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    string login(1:string username, 2:string password, 3:string user_ip)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    void logout(1:string session_key)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    void update_session(1:string session_key)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    Session get_session(1:string session_key)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    LoggedUser get_current_online(1:string session_key)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    bool is_logged_in(1:string session_key)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
}

struct WrittenArticle {
    1: string title,
    2: string content
}

struct Article {
    1:  id_t id,
    2:  string title,
    3:  string content,
    4:  i64 date,
    5:  i32 hit = 0,
    6:  i32 vote,
    7:  bool deleted = 0,
    8:  i32 root_id,
    9:  string author_username,
    10: string author_nickname,
    11: bool blacklisted = 0,
    12: bool is_searchable,
    13: i64 last_modified_date,
    14: optional i32 depth,  // Only used in the 'read' function
    15: optional string read_status,
    16: optional i32 reply_count,
    17: optional string type
}

struct ArticleList {
    1: i32 last_page,
    2: i32 results,
    3: list<Article> hit
}

service ArticleManager {
    list<Article> get_today_best_list(1:i32 count=5)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    list<Article> get_today_best_list_specific(1:string board_name, 2:i32 count=5)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    list<Article> get_weekly_best_list(1:i32 count=5)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    list<Article> get_weekly_best_list_specific(1:string board_name, 2:i32 count=5)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    ArticleList not_read_article_list(1:string session_key,
                                      2:i32 page=1,
                                      3:i32 page_length=20)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    ArticleList not_article_list(1:string session_key,
                                 2:i32 page=1,
                                 3:i32 page_length=20)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    ArticleList article_list(1:string session_key,
                             2:string board_name,
                             3:i32 page=1,
                             4:i32 page_length=20)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    list<Article> read(1:string session_key, 2:string board_name, 3:id_t no)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    ArticleList article_list_below(1:string session_key,
                                   2:string board_name,
                                   3:id_t no,
                                   4:i32 page_length=20)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    void vote_article(1:string session_key, 2:string board_name,
                      3:id_t article_no)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    i32 write_article(1:string session_key, 2:string board_name,
                      3:WrittenArticle article)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    i32 write_reply(1:string session_key, 2:string board_name,
                      3:id_t article_no, 4:WrittenArticle article)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    i32 modify(1:string session_key, 2:string board_name,
               3:id_t no, 4:WrittenArticle article)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
    void delete_(1:string session_key,
                2:string board_name,
                3:id_t no)
        throws (1:InvalidOperation ouch, 2:DatabaseError ouch),
}
