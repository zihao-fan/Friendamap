CREATE TABLE Users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name varchar(25),
    last_name  varchar(25),
    email  varchar(50)
);

CREATE TABLE Likes (
    user_id INT NOT NULL,
    place_id INT NOT NULL,
    PRIMARY KEY (user_id, place_id)
);

CREATE TABLE Visits (
    user_id INT NOT NULL,
    place_id INT NOT NULL,
    PRIMARY KEY (user_id, place_id)
);