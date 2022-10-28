DROP TABLE IF EXISTS user_info;
DROP TABLE IF EXISTS course_info;


CREATE TABLE user_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    phonenum INTEGER,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE course_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_name TEXT NOT NULL,
    class_name TEXT NOT NULL,
    class_description TEXT NOT NULL,
    max_students INTEGER,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE course_roster (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    student_email TEXT NOT NULL,
    wait_list BOOLEAN NOT NULL,
    FOREIGN KEY (id) REFERENCES course_info (id)
);

CREATE TABLE course_waitlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    student_email TEXT NOT NULL,
    FOREIGN KEY (id) REFERENCES course_info (id)
);