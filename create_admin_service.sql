-- Create a new table for student service admins
CREATE TABLE IF NOT EXISTS student_service_admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'admin',
    department TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some initial admin users
INSERT INTO student_service_admin (email, password, full_name, role, department)
VALUES 
    ('admin@example.com', 'pbkdf2:sha256:150000$aBcDeFgH$c6a7030e0c8caadb85cb3403a0739886e9ad001fa8a6262a47083c62bc2f0b48', 'System Administrator', 'super_admin', 'IT'),
    ('academic@example.com', 'pbkdf2:sha256:150000$aBcDeFgH$c6a7030e0c8caadb85cb3403a0739886e9ad001fa8a6262a47083c62bc2f0b48', 'Academic Admin', 'admin', 'Academic Affairs'),
    ('finance@example.com', 'pbkdf2:sha256:150000$aBcDeFgH$c6a7030e0c8caadb85cb3403a0739886e9ad001fa8a6262a47083c62bc2f0b48', 'Finance Admin', 'admin', 'Finance');



