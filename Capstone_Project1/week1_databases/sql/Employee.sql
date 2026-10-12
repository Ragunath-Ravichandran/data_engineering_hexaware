CREATE DATABASE IF NOT EXISTS attendance_tracker;
USE attendance_tracker;

CREATE TABLE employees (
    employee_id   INT AUTO_INCREMENT PRIMARY KEY,
    first_name    VARCHAR(50)  NOT NULL,
    last_name     VARCHAR(50)  NOT NULL,
    email         VARCHAR(100) UNIQUE NOT NULL,
    department    VARCHAR(50)  NOT NULL,
    designation   VARCHAR(50),
    hire_date     DATE         NOT NULL
);

CREATE TABLE attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id   INT  NOT NULL,
    work_date     DATE NOT NULL,
    clock_in      DATETIME,
    clock_out     DATETIME,
    status        ENUM('PRESENT','ABSENT','LEAVE','LATE') DEFAULT 'PRESENT',
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
    UNIQUE (employee_id, work_date)
);

CREATE TABLE tasks (
    task_id        INT AUTO_INCREMENT PRIMARY KEY,
    employee_id    INT          NOT NULL,
    task_title     VARCHAR(150) NOT NULL,
    assigned_date  DATE         NOT NULL,
    due_date       DATE,
    completed_date DATE,
    status         ENUM('PENDING','IN_PROGRESS','COMPLETED') DEFAULT 'PENDING',
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
);

-- indexes
CREATE INDEX idx_attendance_employee ON attendance(employee_id);
CREATE INDEX idx_attendance_date     ON attendance(work_date);
CREATE INDEX idx_employees_dept      ON employees(department);
CREATE INDEX idx_tasks_employee      ON tasks(employee_id);

--sample records
INSERT INTO employees (first_name, last_name, email, department, designation, hire_date) VALUES
('Arun',   'Kumar',  'arun.kumar@company.com',  'Engineering', 'Developer',  '2022-03-15'),
('Priya',  'Sharma', 'priya.sharma@company.com','HR',          'HR Manager', '2021-07-01'),
('Karthik','Raj',    'karthik.raj@company.com', 'Engineering', 'Tester',     '2023-01-10'),
('Divya',  'Menon',  'divya.menon@company.com', 'Finance',     'Analyst',    '2022-09-20');

INSERT INTO tasks (employee_id, task_title, assigned_date, due_date, completed_date, status) VALUES
(1, 'Build login module',  '2025-01-06', '2025-01-10', '2025-01-09', 'COMPLETED'),
(1, 'Fix API bugs',        '2025-01-07', '2025-01-12', NULL,         'IN_PROGRESS'),
(2, 'Prepare HR report',   '2025-01-06', '2025-01-08', '2025-01-08', 'COMPLETED'),
(3, 'Write test cases',    '2025-01-06', '2025-01-11', '2025-01-10', 'COMPLETED'),
(4, 'Monthly reconciliation','2025-01-08','2025-01-15', NULL,        'PENDING');

--clocking in.
INSERT INTO attendance (employee_id, work_date, clock_in, status)
VALUES (1, '2025-01-06', '2025-01-06 09:02:00', 'PRESENT');

INSERT INTO attendance (employee_id, work_date, clock_in, status)
VALUES (2, '2025-01-06', '2025-01-06 09:45:00', 'LATE');


--clock-out.
UPDATE attendance
SET clock_out = '2025-01-06 18:05:00'
WHERE employee_id = 1 AND work_date = '2025-01-06';

UPDATE attendance
SET clock_out = '2025-01-06 17:50:00'
WHERE employee_id = 2 AND work_date = '2025-01-06';


INSERT INTO attendance (employee_id, work_date, clock_in, clock_out, status) VALUES
(1, '2025-01-07', '2025-01-07 09:00:00', '2025-01-07 18:00:00', 'PRESENT'),
(1, '2025-01-08', '2025-01-08 09:10:00', '2025-01-08 17:40:00', 'PRESENT'),
(3, '2025-01-06', '2025-01-06 09:30:00', '2025-01-06 18:30:00', 'LATE'),
(3, '2025-01-07', NULL, NULL, 'ABSENT'),
(4, '2025-01-06', '2025-01-06 08:55:00', '2025-01-06 17:30:00', 'PRESENT');


UPDATE tasks
SET status = 'COMPLETED', completed_date = CURDATE()
WHERE task_id = 2;


SELECT * FROM employees;

SELECT e.employee_id, e.first_name, e.department, a.work_date, a.clock_in, a.clock_out, a.status
FROM attendance a
JOIN employees e ON e.employee_id = a.employee_id
WHERE a.work_date = '2025-01-06';

SELECT department, COUNT(*) AS headcount
FROM employees
GROUP BY department;


DELETE FROM tasks WHERE task_id = 5;

DROP PROCEDURE IF EXISTS calc_total_working_hours;

DELIMITER //
CREATE PROCEDURE calc_total_working_hours(
    IN p_employee_id INT,      
    IN p_start_date  DATE,
    IN p_end_date    DATE
)
BEGIN
    SELECT
        e.employee_id,
        CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
        e.department,
        COUNT(a.attendance_id) AS days_worked,
        ROUND(SUM(TIMESTAMPDIFF(MINUTE, a.clock_in, a.clock_out)) / 60, 2) AS total_working_hours
    FROM employees e
    JOIN attendance a ON a.employee_id = e.employee_id
    WHERE a.clock_in  IS NOT NULL
      AND a.clock_out IS NOT NULL
      AND a.work_date BETWEEN p_start_date AND p_end_date
      AND (p_employee_id IS NULL OR e.employee_id = p_employee_id)
    GROUP BY e.employee_id, e.first_name, e.last_name, e.department
    ORDER BY total_working_hours DESC;
END //
DELIMITER ;


CALL calc_total_working_hours(1, '2025-01-01', '2025-01-31');
CALL calc_total_working_hours(NULL, '2025-01-01', '2025-01-31');