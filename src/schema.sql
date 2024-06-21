DROP TABLE IF EXISTS regions;
DROP TABLE IF EXISTS fragments;
DROP TABLE IF EXISTS tfidf;

CREATE TABLE regions (
    reg_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reg_name TEXT NOT NULL
);

CREATE TABLE fragments (
    frag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    frag_str TEXT NOT NULL
);

CREATE TABLE tfidf (
    reg_id INTEGER,
    frag_id INTEGER,
    tfidf_val FLOAT,
    PRIMARY KEY (reg_id, frag_id)
);
