#!/bin/bash

# Функции для работы с юнитами
get_units() {
    systemctl list-units --type=service | grep 'foobar-' | awk '{print $1}' | sed 's/.service$//'
}

stop_unit() {
    local unit="$1"
    echo "Останавливаю юнит $unit..."
    systemctl stop "$unit.service"
}

move_service_files() {
    local unit="$1"
    local service_name="${unit##*-}"
    local old_dir="/opt/misc/$service_name"
    local new_dir="/srv/data/$service_name"
    echo "Перемещаю файлы из $old_dir в $new_dir..."
    mv "$old_dir" "$new_dir"
}

update_unit_file() {
    local unit="$1"
    local service_name="${unit##*-}"
    local old_dir="/opt/misc/$service_name"
    local new_dir="/srv/data/$service_name"
    local unit_file="/etc/systemd/system/${unit}.service"
    echo "Редактирую юнит-файл $unit_file..."
    sed -i "s|$old_dir|$new_dir|g" "$unit_file"
}

restart_unit() {
    local unit="$1"
    echo "Перезапускаю юнит $unit..."
    systemctl restart "$unit.service"
}

# Основная программа
echo "Получение списка юнитов foobar-*..."
units=$(get_units)

for unit in $units; do
    echo "Обрабатывается юнит $unit:"
    stop_unit "$unit"
    move_service_files "$unit"
    update_unit_file "$unit"
    restart_unit "$unit"
done

echo "Завершение работы скрипта."