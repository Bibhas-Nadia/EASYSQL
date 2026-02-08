#!/bin/bash

# 1. Install MariaDB
echo "Installing MariaDB..."
pacman -Sy --noconfirm mariadb || { echo "Failed to install MariaDB"; exit 1; }

# 2. Initialize the database
echo "Initializing MariaDB data directory..."
mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql || { echo "Failed to initialize DB"; exit 1; }

# 3. Start and enable MariaDB
echo "Starting MariaDB service..."
systemctl start mariadb || { echo "Failed to start MariaDB"; exit 1; }
systemctl enable mariadb

# 4. Secure MariaDB (basic flush, root setup skipped for simplicity)
echo "Securing MariaDB setup..."
mysql -e "DELETE FROM mysql.user WHERE User='';"
mysql -e "DROP DATABASE IF EXISTS test;"
mysql -e "FLUSH PRIVILEGES;"

# 5. Create database and user
echo "Creating database 'SNU' and user 't13'..."
mysql -e "CREATE DATABASE SNU;"
mysql -e "CREATE USER 't13'@'localhost' IDENTIFIED BY 't13';"
mysql -e "GRANT ALL PRIVILEGES ON SNU.* TO 't13'@'localhost';"
mysql -e "FLUSH PRIVILEGES;"

# 6. Import SQL file
echo "Importing file.sql into database SNU..."
if [ ! -f "file.sql" ]; then
  echo "❌ file.sql not found in current directory."
  exit 1
fi
mariadb -u t13 -pt13 SNU < file.sql || { echo "❌ Import failed"; exit 1; }

echo "✅ All done. MariaDB is running, user 't13' and DB 'SNU' are ready."
