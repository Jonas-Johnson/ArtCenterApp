DROP TABLE IF EXISTS user_info;
DROP TABLE IF EXISTS class_info;


CREATE TABLE user_info (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      email TEXT UNIQUE NOT NULL,
                      password TEXT NOT NULL,
                      firstname TEXT NOT NULL,
                      lastname TEXT NOT NULL,
                      phonenum INTEGER,
                      created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE class_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    teacher_name TEXT NOT NULL,
                    class_name TEXT NOT NULL,
                    class_description TEXT NOT NULL,
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);