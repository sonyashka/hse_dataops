#!/bin/bash

# Создание пользователей в системе
echo "Creating system users for JupyterHub..."

# Создание администратора
if id "admin" &>/dev/null; then
    echo "User admin already exists"
else
    sudo useradd -m -s /bin/bash admin
    echo "admin:admin123" | sudo chpasswd
    echo "Created user: admin (password: admin123)"
fi

# Создание дополнительных пользователей
for user in user1 user2; do
    if id "$user" &>/dev/null; then
        echo "User $user already exists"
    else
        sudo useradd -m -s /bin/bash "$user"
        echo "$user:pass123" | sudo chpasswd
        echo "Created user: $user (password: pass123)"
    fi
done

echo "Users created successfully"