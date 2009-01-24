typedef i32 id_t

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
    list<Article> get_today_best_list(1:i32 count=5),
    list<Article> get_today_best_list_specific(1:string board_name, 2:i32 count=5),
    list<Article> get_weekly_best_list(1:i32 count=5),
    list<Article> get_weekly_best_list_specific(1:string board_name, 2:i32 count=5),
    ArticleList not_read_article_list(1:string session_key,
                                      2:i32 page=1,
                                      3:i32 page_length=20),
    ArticleList not_article_list(1:string session_key,
                                 2:i32 page=1,
                                 3:i32 page_length=20),
    ArticleList article_list(1:string session_key,
                             2:string board_name,
                             3:i32 page=1,
                             4:i32 page_length=20),
    list<Article> read(1:string session_key, 2:string board_name, 3:id_t no),
    ArticleList article_list_below(1:string session_key,
                                   2:string board_name,
                                   3:id_t no,
                                   4:i32 page_length=20),
    void vote_article(1:string session_key, 2:string board_name,
                      3:id_t article_no),
    i32 write_article(1:string session_key, 2:string board_name,
                      3:WrittenArticle article),
    i32 write_reply(1:string session_key, 2:string board_name,
                      3:id_t article_no, 4:WrittenArticle article),
    i32 modify(1:string session_key, 2:string board_name,
               3:id_t no, 4:WrittenArticle article),
    void delete_(1:string session_key,
                2:string board_name,
                3:id_t no),
}
