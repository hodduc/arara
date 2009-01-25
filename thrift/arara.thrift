namespace py arara_thrift

exception InternalError {
    1: string why
}

exception InvalidOperation {
    1: string why
}

exception NotLoggedIn {

}

typedef i32 id_t

struct VisitorCount {
    1: i32 total_visitor_count,
    2: i32 today_visitor_count,
}

struct Session {
    1: string username,
    2: string ip,
    3: string current_action,
    4: string nickname,
    5: i64 logintime,
}

service LoginManager {
    string guest_login(1:string guest_ip)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    VisitorCount total_visitor()
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    string login(1:string username, 2:string password, 3:string user_ip)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    void logout(1:string session_key)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    void update_session(1:string session_key)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    Session get_session(1:string session_key)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    list<Session> get_current_online(1:string session_key)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    bool is_logged_in(1:string session_key)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
}

struct UserRegistration {
    1: string username,
    2: string password,
    3: string nickname,
    4: string email,
    5: string signature,
    6: string self_introduction,
    7: string default_language
}

struct UserInformation {
    1 : string username,
    2 : string nickname,
    3 : string email,
    4 : string last_login_ip,
    5 : i64 last_logout_time,
    6 : string signature,
    7 : string self_introduction,
    8 : string default_language
    9 : bool activated,
    10: i32 widget,
    11: string layout,
}

struct UserPasswordInfo {
    1: string username,
    2: string current_password,
    3: string new_password,
}

struct UserModification {
    1: string nickname,
    2: string signature,
    3: string self_introduction,
    4: string default_language,
    5: i32 widget,
    6: string layout,
}

struct PublicUserInformation {
    1: string username,
    2: string nickname,
    3: string signature,
    4: string self_introduction,
    5: string last_login_ip,
}

struct SearchUserResult {
    1: string username,
    2: string nickname,
}

service MemberManager {
    void register(1:UserRegistration user_reg)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    void backdoor_confirm(1:string session_key, 2:string username)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    void confirm(1:string username_to_confirm, 2:string confirm_key)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    bool is_registered(1:string username)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    bool is_registered_nickname(1:string nickname)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    bool is_registered_email(1:string email)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    UserInformation get_info(1:string session_key)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    string modify_password(1:string session_key,
                           2:UserPasswordInfo user_password_info)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    string modify(1:string session_key,
                  2:UserModification user_modification_info)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    PublicUserInformation query_by_username(1:string session_key,
                                            2:string username)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    PublicUserInformation query_by_nick(1:string session_key,
                                        2:string username)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    void remove_user(1:string session_key),
    SearchUserResult search_user(1:string session_key,
                                 2:string search_user,
                                 3:string search_key="")
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    bool is_sysop(1:string session_key)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
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
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    list<Article> get_today_best_list_specific(1:string board_name, 2:i32 count=5)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    list<Article> get_weekly_best_list(1:i32 count=5)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    list<Article> get_weekly_best_list_specific(1:string board_name, 2:i32 count=5)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    ArticleList not_read_article_list(1:string session_key,
                                      2:i32 page=1,
                                      3:i32 page_length=20)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    ArticleList not_article_list(1:string session_key,
                                 2:i32 page=1,
                                 3:i32 page_length=20)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    ArticleList article_list(1:string session_key,
                             2:string board_name,
                             3:i32 page=1,
                             4:i32 page_length=20)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    list<Article> read(1:string session_key, 2:string board_name, 3:id_t no)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    ArticleList article_list_below(1:string session_key,
                                   2:string board_name,
                                   3:id_t no,
                                   4:i32 page_length=20)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    void vote_article(1:string session_key, 2:string board_name,
                      3:id_t article_no)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    i32 write_article(1:string session_key, 2:string board_name,
                      3:WrittenArticle article)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    i32 write_reply(1:string session_key, 2:string board_name,
                      3:id_t article_no, 4:WrittenArticle article)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    i32 modify(1:string session_key, 2:string board_name,
               3:id_t no, 4:WrittenArticle article)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
    void delete_(1:string session_key,
                2:string board_name,
                3:id_t no)
        throws (1:InvalidOperation invalid,
                2:InternalError ouch, 3:NotLoggedIn not_logged_in),
}
