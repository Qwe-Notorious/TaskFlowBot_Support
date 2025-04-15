import os
import json
import streamlit as st
import bcrypt


def auto_admin():
    # Проверяем статус авторизации в session_state
    if 'is_authenticated' not in st.session_state:
        st.session_state.is_authenticated = False

    if not st.session_state.is_authenticated:
        # Показываем форму авторизации только если не авторизованы
        current_dir = os.path.dirname(os.path.abspath(__file__))
        users_path = os.path.join(current_dir, "..", "users.json")

        with st.form("admin_login"):
            admin_login = st.text_input("Login", placeholder="Login")
            admin_password = st.text_input("Password", type="password", placeholder="Password")

            if st.form_submit_button("Отправить"):
                if admin_login and admin_password:
                    try:
                        if not os.path.exists(users_path):
                            raise FileNotFoundError("Файл users.json не найден")

                        with open(users_path, "r", encoding="utf-8") as file:
                            users = json.load(file)

                            for user in users:
                                password = user.get("password").encode('utf-8')

                                check = bcrypt.checkpw(
                                    password=admin_password.encode('utf-8'),
                                    hashed_password=password
                                )

                                if user.get("login") == admin_login and check:
                                    st.session_state.is_authenticated = True
                                    st.rerun()  # Перезагружаем страницу
                                    return

                            st.error("Неверные учетные данные")

                    except json.JSONDecodeError:
                        st.error("Ошибка формата файла users.json")
                    except Exception as e:
                        st.error(f"Ошибка: {str(e)}")
                else:
                    st.error("Заполните все поля!")
    else:
        # Показываем админ-панель и кнопку выхода
        admin_page()

        if st.button("Выйти"):
            st.session_state.is_authenticated = False
            st.rerun()


def admin_page():
    st.header("Admin-Panel")
    st.write("Добро пожаловать в админ-панель!")
    data = []
    container = st.container(border=True)

    try:
        with open("task_flow.json", 'r') as file:
            data = json.load(file)
            for datas in data:
                container.write(f"{datas.get('name')}")
                container.write(f"{datas.get('description')}")
                container.write(f"{datas.get('timestamp')}")
                if container.button(f"{datas.get('id')}", icon="✅", use_container_width=True):
                    delete_json_date(datas.get("id"))

    except (FileNotFoundError, json.JSONDecodeError):
        data = []
        st.error("Данных пока что нет!")


def delete_json_date(id: int) -> None:
    import json

    try:
        # Чтение файла
        with open('task_flow.json', 'r') as file:
            tasks = json.load(file)

        # Проверка формата данных
        if not isinstance(tasks, list):
            raise ValueError("Некорректный формат файла")

        # Удаление элемента
        original_count = len(tasks)
        filtered_tasks = [task for task in tasks if task.get('id') != id]

        # Проверка изменений
        if len(filtered_tasks) == original_count:
            st.error(f"Элемент с {id} не найден")
        else:
            # Запись изменений
            with open('task_flow.json', 'w') as file:
                json.dump(filtered_tasks, file, ensure_ascii=False, indent=2)

    except FileNotFoundError:
        print("Файл task_flow.json не найден")
    except json.JSONDecodeError:
        print("Ошибка чтения JSON")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


# Пример использования
if __name__ == "__main__":
    auto_admin()
