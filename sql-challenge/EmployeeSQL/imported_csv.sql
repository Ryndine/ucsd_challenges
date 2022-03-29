CREATE TABLE if not exists departments
(
	dept_no VARCHAR(5),
	dept_name VARCHAR(32),
	PRIMARY KEY (dept_no)
);

CREATE TABLE if not exists titles
(
	title_id VARCHAR(7),
	title VARCHAR(32),
	PRIMARY KEY (title_id)
);

CREATE TABLE if not exists employees
(
	emp_no INTEGER,
	emp_title VARCHAR(7),
	birth_date DATE,
	first_name VARCHAR(32),
	last_name VARCHAR(32),
	sex CHAR,
	hire_date DATE,
	PRIMARY KEY (emp_no),
	CONSTRAINT fk_emp_title FOREIGN KEY (emp_title) REFERENCES titles(title_id)
);

CREATE TABLE if not exists dept_manager
(
	dept_no VARCHAR(7),
	emp_no INTEGER,
	PRIMARY KEY (emp_no),
	CONSTRAINT fk_dept_man FOREIGN KEY (dept_no) REFERENCES departments(dept_no),
	CONSTRAINT fk_man_emp FOREIGN KEY (emp_no) REFERENCES employees(emp_no)
);

CREATE TABLE if not exists dept_emp
(
	emp_no INTEGER,
	dept_no VARCHAR(7),
	PRIMARY KEY (emp_no, dept_no),
	CONSTRAINT fk_dept_emp FOREIGN KEY (dept_no) REFERENCES departments(dept_no),
	CONSTRAINT fk_emp_emp FOREIGN KEY (emp_no) REFERENCES employees(emp_no)
);

CREATE TABLE if not exists salaries
(
	emp_no INTEGER,
	salary INTEGER,
	CONSTRAINT fk_sal_emp FOREIGN KEY (emp_no) REFERENCES employees(emp_no)
);