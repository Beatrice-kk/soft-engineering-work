DROP DATABASE IF EXISTS train;
CREATE DATABASE IF NOT EXISTS train;

use train;

-- Table: train
CREATE TABLE train (
    f_id VARCHAR(255) PRIMARY KEY,
    f_s_place VARCHAR(255) DEFAULT NULL,
    f_e_place VARCHAR(255) DEFAULT NULL,
    f_s_airfield VARCHAR(255) DEFAULT NULL,
    f_e_airfield VARCHAR(255) DEFAULT NULL
);

-- Table: arrange
CREATE TABLE arrange (
    a_id VARCHAR(255) PRIMARY KEY,
    f_id VARCHAR(255),
    a_date DATE NOT NULL,
    a_s_time TIME NOT NULL,
    a_e_time TIME NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (f_id) REFERENCES train(f_id) ON DELETE CASCADE
);

-- Table: passenger
CREATE TABLE passenger (
    p_id VARCHAR(255) PRIMARY KEY,
    p_name VARCHAR(255) DEFAULT NULL,
    p_tel VARCHAR(255) DEFAULT NULL,
    p_sex VARCHAR(255) DEFAULT NULL,
    p_age INT DEFAULT NULL,
    p_card VARCHAR(255) DEFAULT NULL
);

-- Table: ticket
CREATE TABLE ticket (
    t_id VARCHAR(255) PRIMARY KEY,
    a_id VARCHAR(255),
    t_seat VARCHAR(255) DEFAULT NULL,
    t_available VARCHAR(255) DEFAULT NULL,
    p_take VARCHAR(255) DEFAULT NULL,
    p_pay VARCHAR(255) DEFAULT NULL,
    t_paytime DATETIME NOT NULL,
    FOREIGN KEY (a_id) REFERENCES arrange(a_id) ON DELETE CASCADE
);

-- Table: relationships
CREATE TABLE relationships (
    r_id VARCHAR(255) PRIMARY KEY,
    p_main VARCHAR(255) DEFAULT NULL,
    p_related VARCHAR(255) DEFAULT NULL
);

-- Table: m_account
CREATE TABLE m_account (
    m_id VARCHAR(255) PRIMARY KEY,
    m_account VARCHAR(255) DEFAULT NULL,
    m_password VARCHAR(255) DEFAULT NULL
);

-- Table: p_account
CREATE TABLE p_account (
    p_id VARCHAR(255) PRIMARY KEY,
    p_account VARCHAR(255) DEFAULT NULL,
    p_password VARCHAR(255) DEFAULT NULL
);


-- Insert data into train
INSERT INTO train (f_id, f_s_place, f_e_place, f_s_airfield, f_e_airfield) VALUES
('F001', 'New York', 'Los Angeles', 'JFK', 'LAX'),
('F002', 'Chicago', 'Miami', 'ORD', 'MIA'),
('F003', 'San Francisco', 'Seattle', 'SFO', 'SEA');

-- Insert data into arrange
INSERT INTO arrange (a_id, f_id, a_date, a_s_time, a_e_time, price) VALUES
('A001', 'F001', '2026-1-20', '10:00:00', '13:30:00', 500.00),
('A002', 'F002', '2026-1-21', '14:00:00', '18:00:00', 350.00),
('A003', 'F003', '2026-1-22', '08:00:00', '10:00:00', 250.00);

-- Insert data into passenger
INSERT INTO passenger (p_id, p_name, p_tel, p_sex, p_age, p_card) VALUES
('P001', 'John Doe', '1234567890', 'Male', 30, 'ID001'),
('P002', 'Jane Smith', '0987654321', 'Female', 25, 'ID002'),
('P003', 'Alice Johnson', '1122334455', 'Female', 35, 'ID003');

-- Insert data into ticket
INSERT INTO ticket (t_id, a_id, t_seat, t_available, p_take, p_pay, t_paytime) VALUES
('T001', 'A001', '12A', 'Yes', 'Yes', 'Yes', '2026-1-13 09:00:00'),
('T002', 'A002', '15B', 'No', 'No', 'Yes', '2026-1-14 15:30:00'),
('T003', 'A003', '7C', 'Yes', 'Yes', 'No', '2026-1-15 10:00:00');

-- Insert data into relationships
INSERT INTO relationships (r_id, p_main, p_related) VALUES
('R001', 'P001', 'P002'),
('R002', 'P002', 'P003'),
('R003', 'P003', 'P001');

-- Insert data into m_account
INSERT INTO m_account (m_id, m_account, m_password) VALUES
('M001', 'manager1', 'password123'),
('M002', 'manager2', 'password456'),
('M003', 'manager3', 'password789');

-- Insert data into p_account
INSERT INTO p_account (p_id, p_account, p_password) VALUES
('P001', 'johndoe', 'johndoe123'),
('P002', 'janesmith', 'janesmith456'),
('P003', 'alicejohnson', 'alicejohnson789');