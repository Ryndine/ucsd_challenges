-- 1) Employee Salaries
SELECT e.emp_no, e.last_name, e.first_name, e.sex, s.salary
FROM employees AS e
INNER JOIN salaries AS s 
ON (e.emp_no = s.emp_no);

-- 2) Hired 1986
SELECT e.first_name, e.last_name, e.hire_date
FROM employees AS e
WHERE EXTRACT(YEAR FROM e.hire_date) = 1986;

-- 3) Manager Departments
SELECT d.dept_no, d.dept_name, mn.emp_no, e.first_name, e.last_name
FROM departments AS d
LEFT JOIN dept_manager AS mn 
ON (d.dept_no = mn.dept_no)
LEFT JOIN employees AS e 
ON (mn.emp_no = e.emp_no);

-- 4) Employee Departments
SELECT e.emp_no, e.last_name, e.first_name, d.dept_name
FROM employees AS e
INNER JOIN dept_emp AS de 
ON e.emp_no = de.emp_no
INNER JOIN departments AS d 
ON de.dept_no = d.dept_no;

-- 5) Hercules & B's
SELECT first_name, last_name, sex
FROM employees
WHERE first_name = 'Hercules' 
AND last_name LIKE 'B%';

-- 6) Sales Department
SELECT e.emp_no, e.last_name, e.first_name, d.dept_name
FROM employees AS e 
INNER JOIN dept_emp AS de
ON e.emp_no = de.emp_no
INNER JOIN departments AS d 
ON d.dept_no = de.dept_no
WHERE d.dept_name = 'Sales';

--  7) Sales and Development Departments
SELECT e.emp_no, e.last_name, e.first_name, d.dept_name
FROM employees AS e 
INNER JOIN dept_emp AS de 
ON e.emp_no = de.emp_no
INNER JOIN departments AS d 
ON d.dept_no = de.dept_no
WHERE d.dept_name = 'Sales' 
OR d.dept_name = 'Development';

-- 8) Similar Last Names
SELECT last_name, COUNT(last_name) AS "last_name_count"
FROM employees 
GROUP BY last_name
ORDER BY "last_name_count" DESC;