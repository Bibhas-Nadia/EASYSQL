-- input.sql
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS teacher;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS college;

CREATE TABLE college (
  c_id INT AUTO_INCREMENT PRIMARY KEY,
  c_name VARCHAR(100) NOT NULL UNIQUE,
  c_city VARCHAR(100) NOT NULL,
  c_state VARCHAR(100) NOT NULL
);

CREATE TABLE department (
  d_id INT AUTO_INCREMENT PRIMARY KEY,
  d_name VARCHAR(100) NOT NULL,
  d_college_name VARCHAR(100) NOT NULL
);

CREATE TABLE student (
  s_id INT AUTO_INCREMENT PRIMARY KEY,
  s_name VARCHAR(100) NOT NULL,
  s_email VARCHAR(100) NOT NULL,
  s_age INT,
  s_city VARCHAR(100),
  s_college_name VARCHAR(100) NOT NULL
);

CREATE TABLE teacher (
  t_id INT AUTO_INCREMENT PRIMARY KEY,
  t_name VARCHAR(100) NOT NULL,
  t_email VARCHAR(100) NOT NULL,
  t_age INT,
  t_city VARCHAR(100),
  t_college_name VARCHAR(100) NOT NULL
);

-- Insert college entries
INSERT INTO college (c_name, c_city, c_state) VALUES ('Indian Institute of Technology Delhi', 'Delhi', 'Delhi');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Indian Institute of Technology Bombay', 'Bombay', 'Maharashtra');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Indian Institute of Technology Madras', 'Madras', 'Tamil Nadu');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Indian Institute of Technology Kharagpur', 'Kharagpur', 'West Bengal');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Indian Institute of Technology Kanpur', 'Kanpur', 'Uttar Pradesh');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Indian Institute of Technology Roorkee', 'Roorkee', 'Uttarakhand');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Indian Institute of Technology Guwahati', 'Guwahati', 'Assam');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Indian Institute of Technology Hyderabad', 'Hyderabad', 'Telangana');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Indian Institute of Technology Bhubaneswar', 'Bhubaneswar', 'Odisha');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Indian Institute of Technology Jodhpur', 'Jodhpur', 'Rajasthan');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Indian Institute of Technology Indore', 'Indore', 'Madhya Pradesh');
INSERT INTO college (c_name, c_city, c_state) VALUES ('National Institute of Technology Warangal', 'Warangal', 'Telangana');
INSERT INTO college (c_name, c_city, c_state) VALUES ('National Institute of Technology Rourkela', 'Rourkela', 'Odisha');
INSERT INTO college (c_name, c_city, c_state) VALUES ('National Institute of Technology Surat', 'Surat', 'Gujarat');
INSERT INTO college (c_name, c_city, c_state) VALUES ('National Institute of Technology Kolkata', 'Kolkata', 'West Bengal');
INSERT INTO college (c_name, c_city, c_state) VALUES ('National Institute of Technology Patna', 'Patna', 'Bihar');
INSERT INTO college (c_name, c_city, c_state) VALUES ('National Institute of Technology Kurukshetra', 'Kurukshetra', 'Haryana');
INSERT INTO college (c_name, c_city, c_state) VALUES ('National Institute of Technology Jammu', 'Jammu', 'Jammu and Kashmir');
INSERT INTO college (c_name, c_city, c_state) VALUES ('National Institute of Technology Agartala', 'Agartala', 'Tripura');
INSERT INTO college (c_name, c_city, c_state) VALUES ('National Institute of Technology Agra', 'Agra', 'Uttar Pradesh');
INSERT INTO college (c_name, c_city, c_state) VALUES ('National Institute of Technology Jalandhar', 'Jalandhar', 'Punjab');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Institute of Technology, Delhi', 'Delhi', 'Delhi');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Institute of Technology, Mumbai', 'Mumbai', 'Maharashtra');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Institute of Technology, Bangalore', 'Bangalore', 'Karnataka');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Institute of Technology, Chennai', 'Chennai', 'Tamil Nadu');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Institute of Technology, Hyderabad', 'Hyderabad', 'Telangana');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Institute of Technology, Ahmedabad', 'Ahmedabad', 'Gujarat');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Institute of Technology, Pune', 'Pune', 'Maharashtra');
INSERT INTO college (c_name, c_city, c_state) VALUES ('University of Delhi', 'Delhi', 'Delhi');
INSERT INTO college (c_name, c_city, c_state) VALUES ('University of Mumbai', 'Mumbai', 'Maharashtra');
INSERT INTO college (c_name, c_city, c_state) VALUES ('University of Kolkata', 'Kolkata', 'West Bengal');
INSERT INTO college (c_name, c_city, c_state) VALUES ('University of Bengaluru', 'Bengaluru', 'Karnataka');
INSERT INTO college (c_name, c_city, c_state) VALUES ('University of Chennai', 'Chennai', 'Tamil Nadu');
INSERT INTO college (c_name, c_city, c_state) VALUES ('University of Bhopal', 'Bhopal', 'Madhya Pradesh');
INSERT INTO college (c_name, c_city, c_state) VALUES ('University of Lucknow', 'Lucknow', 'Uttar Pradesh');
INSERT INTO college (c_name, c_city, c_state) VALUES ('University of Patna', 'Patna', 'Bihar');
INSERT INTO college (c_name, c_city, c_state) VALUES ('University of Hyderabad', 'Hyderabad', 'Telangana');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Dayanand Anglo Vedic College, Delhi', 'Delhi', 'Delhi');
INSERT INTO college (c_name, c_city, c_state) VALUES ('St. Xavier''s College, Mumbai', 'Mumbai', 'Maharashtra');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Loyola College, Chennai', 'Chennai', 'Tamil Nadu');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Madras Christian College, Chennai', 'Chennai', 'Tamil Nadu');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Presidency College, Kolkata', 'Kolkata', 'West Bengal');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Ramjas College, Delhi', 'Delhi', 'Delhi');
INSERT INTO college (c_name, c_city, c_state) VALUES ('National Law School of India University, Bangalore', 'Bangalore', 'Karnataka');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Symbiosis College of Arts & Commerce, Pune', 'Pune', 'Maharashtra');
INSERT INTO college (c_name, c_city, c_state) VALUES ('JSS College of Arts, Commerce and Science, Mysore', 'Mysore', 'Karnataka');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Birla Institute of Technology and Science, Pilani', 'Pilani', 'Rajasthan');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Banaras Hindu University, Varanasi', 'Varanasi', 'Uttar Pradesh');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Jamia Millia Islamia, Delhi', 'Delhi', 'Delhi');
INSERT INTO college (c_name, c_city, c_state) VALUES ('Jadavpur University, Kolkata', 'Kolkata', 'West Bengal');

-- Insert department entries
INSERT INTO department (d_name, d_college_name) VALUES ('English', 'Indian Institute of Technology Delhi');
INSERT INTO department (d_name, d_college_name) VALUES ('Environmental Science', 'Indian Institute of Technology Bombay');
INSERT INTO department (d_name, d_college_name) VALUES ('Electronics and Communication', 'Indian Institute of Technology Madras');
INSERT INTO department (d_name, d_college_name) VALUES ('Anthropology', 'Indian Institute of Technology Kharagpur');
INSERT INTO department (d_name, d_college_name) VALUES ('Music', 'Indian Institute of Technology Kanpur');
INSERT INTO department (d_name, d_college_name) VALUES ('Pharmacy', 'Indian Institute of Technology Roorkee');
INSERT INTO department (d_name, d_college_name) VALUES ('Biotechnology', 'Indian Institute of Technology Guwahati');
INSERT INTO department (d_name, d_college_name) VALUES ('Law Enforcement', 'Indian Institute of Technology Hyderabad');
INSERT INTO department (d_name, d_college_name) VALUES ('Nursing', 'Indian Institute of Technology Bhubaneswar');
INSERT INTO department (d_name, d_college_name) VALUES ('Data Science', 'Indian Institute of Technology Jodhpur');
INSERT INTO department (d_name, d_college_name) VALUES ('Agriculture', 'Indian Institute of Technology Indore');
INSERT INTO department (d_name, d_college_name) VALUES ('Biomedical Engineering', 'National Institute of Technology Warangal');
INSERT INTO department (d_name, d_college_name) VALUES ('Education', 'National Institute of Technology Rourkela');
INSERT INTO department (d_name, d_college_name) VALUES ('Psychology', 'National Institute of Technology Surat');
INSERT INTO department (d_name, d_college_name) VALUES ('Astrophysics', 'National Institute of Technology Kolkata');
INSERT INTO department (d_name, d_college_name) VALUES ('Mathematics', 'National Institute of Technology Patna');
INSERT INTO department (d_name, d_college_name) VALUES ('Mechanical Engineering', 'National Institute of Technology Kurukshetra');
INSERT INTO department (d_name, d_college_name) VALUES ('Civil Engineering', 'National Institute of Technology Jammu');
INSERT INTO department (d_name, d_college_name) VALUES ('Sports Science', 'National Institute of Technology Agartala');
INSERT INTO department (d_name, d_college_name) VALUES ('Accounting', 'National Institute of Technology Agra');
INSERT INTO department (d_name, d_college_name) VALUES ('Electrical Engineering', 'National Institute of Technology Jalandhar');
INSERT INTO department (d_name, d_college_name) VALUES ('Architecture', 'Institute of Technology, Delhi');
INSERT INTO department (d_name, d_college_name) VALUES ('Pharmacy', 'Institute of Technology, Mumbai');
INSERT INTO department (d_name, d_college_name) VALUES ('Astrophysics', 'Institute of Technology, Bangalore');
INSERT INTO department (d_name, d_college_name) VALUES ('Psychology', 'Institute of Technology, Chennai');
INSERT INTO department (d_name, d_college_name) VALUES ('Environmental Science', 'Institute of Technology, Hyderabad');
INSERT INTO department (d_name, d_college_name) VALUES ('Electronics and Communication', 'Institute of Technology, Ahmedabad');
INSERT INTO department (d_name, d_college_name) VALUES ('Law', 'Institute of Technology, Pune');
INSERT INTO department (d_name, d_college_name) VALUES ('Business Administration', 'University of Delhi');
INSERT INTO department (d_name, d_college_name) VALUES ('Civil Engineering', 'University of Mumbai');
INSERT INTO department (d_name, d_college_name) VALUES ('Medicine', 'University of Kolkata');
INSERT INTO department (d_name, d_college_name) VALUES ('Marine Biology', 'University of Bengaluru');
INSERT INTO department (d_name, d_college_name) VALUES ('Information Technology', 'University of Chennai');
INSERT INTO department (d_name, d_college_name) VALUES ('Nanotechnology', 'University of Bhopal');
INSERT INTO department (d_name, d_college_name) VALUES ('Data Science', 'University of Lucknow');
INSERT INTO department (d_name, d_college_name) VALUES ('Astronomy', 'University of Patna');
INSERT INTO department (d_name, d_college_name) VALUES ('Business Administration', 'University of Hyderabad');
INSERT INTO department (d_name, d_college_name) VALUES ('Aeronautical Engineering', 'Dayanand Anglo Vedic College, Delhi');
INSERT INTO department (d_name, d_college_name) VALUES ('History', 'St. Xavier''s College, Mumbai');
INSERT INTO department (d_name, d_college_name) VALUES ('Computer Science', 'Loyola College, Chennai');
INSERT INTO department (d_name, d_college_name) VALUES ('Medicine', 'Madras Christian College, Chennai');
INSERT INTO department (d_name, d_college_name) VALUES ('Journalism', 'Presidency College, Kolkata');
INSERT INTO department (d_name, d_college_name) VALUES ('Physics', 'Ramjas College, Delhi');
INSERT INTO department (d_name, d_college_name) VALUES ('Nanotechnology', 'National Law School of India University, Bangalore');
INSERT INTO department (d_name, d_college_name) VALUES ('Chemistry', 'Symbiosis College of Arts & Commerce, Pune');
INSERT INTO department (d_name, d_college_name) VALUES ('Mathematics', 'JSS College of Arts, Commerce and Science, Mysore');
INSERT INTO department (d_name, d_college_name) VALUES ('Law', 'Birla Institute of Technology and Science, Pilani');
INSERT INTO department (d_name, d_college_name) VALUES ('Information Technology', 'Banaras Hindu University, Varanasi');
INSERT INTO department (d_name, d_college_name) VALUES ('History', 'Jamia Millia Islamia, Delhi');
INSERT INTO department (d_name, d_college_name) VALUES ('Information Technology', 'Jadavpur University, Kolkata');

-- Insert student entries
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Raj Verma', 'rverma56@example.com', 20, 'Mumbai', 'Indian Institute of Technology Delhi');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Anjali Rao', 'arao84@gmail.com', 19, 'Kolkata', 'Indian Institute of Technology Bombay');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Deepa Nair', 'dnair29@gmail.com', 22, 'Chennai', 'Indian Institute of Technology Madras');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Sunil Gupta', 'sgupta41@gmail.com', 21, 'New Delhi', 'Indian Institute of Technology Kharagpur');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Priya Singh', 'psingh34@hotmail.com', 18, 'Bangalore', 'Indian Institute of Technology Kanpur');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Amit Sharma', 'asharma67@gmail.com', 24, 'Mumbai', 'Indian Institute of Technology Roorkee');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Sunita Mehta', 'smehta90@yahoo.com', 23, 'Patna', 'Indian Institute of Technology Guwahati');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Rohan Singh', 'rsingh12@gmail.com', 20, 'Ahmedabad', 'Indian Institute of Technology Hyderabad');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Pooja Gupta', 'pgupta88@gmail.com', 19, 'Lucknow', 'Indian Institute of Technology Bhubaneswar');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Ravi Joshi', 'rjoshi22@example.com', 21, 'Jaipur', 'Indian Institute of Technology Jodhpur');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Meena Patel', 'mpatel13@gmail.com', 18, 'Surat', 'Indian Institute of Technology Indore');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Rahul Khan', 'rkhan74@example.com', 22, 'Noida', 'National Institute of Technology Warangal');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Sneha Kapoor', 'skapoor45@gmail.com', 20, 'Lucknow', 'National Institute of Technology Rourkela');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Arun Nair', 'anair38@gmail.com', 19, 'Mumbai', 'National Institute of Technology Surat');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Preeti Iyer', 'piyer53@gmail.com', 21, 'Chennai', 'National Institute of Technology Kolkata');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Vijay Kapoor', 'vkapoor17@gmail.com', 22, 'Pune', 'National Institute of Technology Patna');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Rita Kumar', 'rkumar80@yahoo.com', 20, 'Hyderabad', 'National Institute of Technology Kurukshetra');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Suresh Jain', 'sjain26@gmail.com', 23, 'Lucknow', 'National Institute of Technology Jammu');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Anita Mehta', 'amehta97@gmail.com', 20, 'Mumbai', 'National Institute of Technology Agartala');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Rahul Sharma', 'rsharma73@gmail.com', 19, 'Mumbai', 'National Institute of Technology Agra');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Sunita Verma', 'sverma64@gmail.com', 21, 'Lucknow', 'National Institute of Technology Jalandhar');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Arjun Singh', 'asingh29@gmail.com', 22, 'Jaipur', 'Institute of Technology, Delhi');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Sonia Mehta', 'smehta77@gmail.com', 21, 'Patna', 'Institute of Technology, Mumbai');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Neha Rao', 'nrao50@gmail.com', 18, 'Chennai', 'Institute of Technology, Bangalore');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Rohit Das', 'rdas81@yahoo.com', 20, 'Hyderabad', 'Institute of Technology, Chennai');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Anjali Patel', 'apatel34@gmail.com', 19, 'Patna', 'Institute of Technology, Hyderabad');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Sachin Mehta', 'smehta59@example.com', 22, 'Mumbai', 'Institute of Technology, Ahmedabad');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Sunita Das', 'sdas11@gmail.com', 23, 'Jaipur', 'Institute of Technology, Pune');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Amit Joshi', 'ajoshi92@gmail.com', 20, 'New Delhi', 'University of Delhi');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Rekha Verma', 'rverma65@gmail.com', 18, 'Ahmedabad', 'University of Mumbai');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Sunil Singh', 'ssingh29@gmail.com', 20, 'Chennai', 'University of Kolkata');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Priya Sharma', 'psharma16@gmail.com', 21, 'Mumbai', 'University of Bengaluru');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Vijay Kumar', 'vkumar89@gmail.com', 22, 'Bengaluru', 'University of Chennai');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Rita Singh', 'rsingh47@gmail.com', 19, 'Surat', 'University of Bhopal');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Anil Mehta', 'amehta10@gmail.com', 20, 'Mumbai', 'University of Lucknow');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Rekha Nair', 'rnair23@gmail.com', 21, 'Mumbai', 'University of Patna');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Ravi Gupta', 'rgupta55@gmail.com', 22, 'Pune', 'University of Hyderabad');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Meena Sharma', 'msharma35@gmail.com', 19, 'Bengaluru', 'Dayanand Anglo Vedic College, Delhi');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Sanjay Jain', 'sjain68@gmail.com', 20, 'Chennai', 'St. Xavier''s College, Mumbai');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Pooja Kapoor', 'pkapoor46@gmail.com', 21, 'Lucknow', 'Loyola College, Chennai');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Rahul Gupta', 'rgupta77@gmail.com', 20, 'Bangalore', 'Madras Christian College, Chennai');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Kiran Singh', 'ksingh25@gmail.com', 18, 'Pune', 'Presidency College, Kolkata');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Anita Sharma', 'asharma62@gmail.com', 22, 'Chennai', 'Ramjas College, Delhi');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Vijay Nair', 'vnair33@gmail.com', 21, 'Chennai', 'National Law School of India University, Bangalore');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Sangeeta Das', 'sdas49@gmail.com', 19, 'Bangalore', 'Symbiosis College of Arts & Commerce, Pune');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Naveen Joshi', 'njoshi28@example.com', 20, 'Mumbai', 'JSS College of Arts, Commerce and Science, Mysore');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Shweta Iyer', 'siyer66@gmail.com', 21, 'Mumbai', 'Birla Institute of Technology and Science, Pilani');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Ritu Jain', 'rjain58@gmail.com', 18, 'New Delhi', 'Banaras Hindu University, Varanasi');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Suresh Mehta', 'smehta42@gmail.com', 20, 'Lucknow', 'Jamia Millia Islamia, Delhi');
INSERT INTO student (s_name, s_email, s_age, s_city, s_college_name) VALUES ('Preeti Sharma', 'psharma84@gmail.com', 22, 'Ahmedabad', 'Jadavpur University, Kolkata');

-- Insert teacher entries
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Sachin Das', 'sdas674@example.com', 45, 'Mumbai', 'National Institute of Technology Surat');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Shweta Bose', 'sbose274@hotmail.com', 38, 'New Delhi', 'Indian Institute of Technology Delhi');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Amit Iyer', 'aiyer579@gmail.com', 52, 'Chennai', 'Indian Institute of Technology Roorkee');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Priya Nair', 'pnair613@gmail.com', 41, 'Bengaluru', 'Indian Institute of Technology Madras');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Ravi Rao', 'rrao297@gmail.com', 49, 'Bangalore', 'Indian Institute of Technology Kharagpur');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Sneha Patel', 'spatel359@gmail.com', 37, 'Mumbai', 'Indian Institute of Technology Hyderabad');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Rohit Sharma', 'rsharma488@yahoo.com', 55, 'Chennai', 'Indian Institute of Technology Guwahati');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Sonia Singh', 'ssingh634@gmail.com', 42, 'Kolkata', 'Indian Institute of Technology Kanpur');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Vijay Gupta', 'vgupta104@gmail.com', 46, 'Pune', 'Indian Institute of Technology Bombay');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Sunita Khan', 'skhan715@gmail.com', 50, 'Hyderabad', 'Indian Institute of Technology Jodhpur');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Rajesh Mehta', 'rmehta295@gmail.com', 39, 'Kolkata', 'Indian Institute of Technology Bhubaneswar');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Anjali Verma', 'averma467@gmail.com', 35, 'Pune', 'National Institute of Technology Warangal');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Manish Kumar', 'mkumar950@gmail.com', 59, 'Delhi', 'National Institute of Technology Rourkela');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Ritu Joshi', 'rjoshi159@gmail.com', 43, 'Chennai', 'National Institute of Technology Agra');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Deepak Singh', 'dsingh738@gmail.com', 47, 'Chennai', 'National Institute of Technology Patna');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Meena Patel', 'mpatel345@hotmail.com', 36, 'Mumbai', 'Institute of Technology, Delhi');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Arun Nair', 'anair264@gmail.com', 58, 'New Delhi', 'Institute of Technology, Chennai');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Preeti Kapoor', 'pkapoor593@gmail.com', 40, 'Chennai', 'Institute of Technology, Bangalore');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Amit Singhania', 'asinghania214@gmail.com', 50, 'Mumbai', 'Institute of Technology, Mumbai');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Sunita Bose', 'sbose821@yahoo.com', 48, 'Delhi', 'Institute of Technology, Hyderabad');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Neha Das', 'ndas768@gmail.com', 37, 'Bangalore', 'Institute of Technology, Ahmedabad');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Raj Verma', 'rverma874@gmail.com', 44, 'Hyderabad', 'Institute of Technology, Pune');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Sunil Mehta', 'smehta695@gmail.com', 39, 'Ahmedabad', 'University of Delhi');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Priya Jain', 'pjain923@gmail.com', 49, 'Noida', 'University of Mumbai');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Rohit Gupta', 'rgupta781@gmail.com', 51, 'Jaipur', 'University of Kolkata');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Shweta Sharma', 'ssharma672@gmail.com', 46, 'Mumbai', 'University of Bengaluru');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Vijay Das', 'vdas905@example.com', 53, 'Mumbai', 'University of Chennai');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Anita Joshi', 'ajoshi317@gmail.com', 38, 'Mumbai', 'University of Bhopal');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Rahul Menon', 'rmenon446@gmail.com', 55, 'Ahmedabad', 'University of Lucknow');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Pooja Shah', 'pshah505@gmail.com', 43, 'Hyderabad', 'University of Patna');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Arun Kumar', 'akumar662@gmail.com', 52, 'Mumbai', 'University of Hyderabad');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Sneha Verma', 'sverma432@gmail.com', 39, 'Pune', 'Dayanand Anglo Vedic College, Delhi');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Ritesh Nair', 'rnair231@gmail.com', 41, 'Patna', 'St. Xavier''s College, Mumbai');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Anjali Kapoor', 'akapoor654@gmail.com', 47, 'Lucknow', 'Loyola College, Chennai');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Deepak Jain', 'djain781@gmail.com', 54, 'Mumbai', 'Madras Christian College, Chennai');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Neha Sharma', 'nsharma229@gmail.com', 49, 'Bangalore', 'Presidency College, Kolkata');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Amit Mehta', 'amehta390@gmail.com', 45, 'Mumbai', 'Ramjas College, Delhi');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Priya Nair', 'pnair838@gmail.com', 42, 'Mumbai', 'National Law School of India University, Bangalore');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Vijay Kapoor', 'vkapoor097@gmail.com', 50, 'Chennai', 'Symbiosis College of Arts & Commerce, Pune');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Arun Das', 'adas157@gmail.com', 53, 'Hyderabad', 'JSS College of Arts, Commerce and Science, Mysore');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Ritu Verma', 'rverma416@gmail.com', 44, 'Mumbai', 'Birla Institute of Technology and Science, Pilani');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Meena Rao', 'mrao708@gmail.com', 59, 'Bengaluru', 'Banaras Hindu University, Varanasi');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Raj Gupta', 'rgupta372@gmail.com', 57, 'Mumbai', 'Jamia Millia Islamia, Delhi');
INSERT INTO teacher (t_name, t_email, t_age, t_city, t_college_name) VALUES ('Anita Singh', 'asingh814@gmail.com', 40, 'Pune', 'Jadavpur University, Kolkata');
