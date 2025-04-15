import json
from datetime import datetime
import streamlit as st


class TaskFlowApp:
    def __init__(self):
        self.setup_navigation()
        self.current_page = st.session_state.get("page", "main")

    def setup_navigation(self):
        # Настройка навигации в сайдбаре

        page = st.sidebar.radio(
            "Выберите страницу:",
            ["Главная", "Админ"],
            key="page_selector"
        )
        st.session_state.page = page

    def main_page(self):
        st.header(":blue[TaskFlowBot] - мини приложение для IT-поддержки", divider="rainbow")

        with st.form("task_form"):
            task_name = st.text_input("Название задачи", placeholder="Опишите кратко проблему")
            task_description = st.text_area("Описание", placeholder="Детали проблемы")

            if st.form_submit_button("Отправить"):
                if task_name != "" and task_description != "":
                    self.save_task(task_name, task_description, "task_flow.json")
                    st.success("Задача отправлена!")
                else:
                    st.error("Заполните все поля!")

    def save_task(self, name, description, file_path):
        try:
            # Загрузка существующих данных
            try:
                with open(file_path, 'r') as f:
                    self.data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                self.data = []

            # Определение следующего ID
            current_increment = max(task['id'] for task in self.data) + 1 if self.data else 1

            # Создание новой записи
            task_dict = {
                "id": current_increment,
                "name": name.strip(),
                "description": description.strip(),
                "timestamp": st.session_state.get("current_time")
            }

            # Сохранение данных
            self.data.append(task_dict)
            with open(file_path, 'w') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            st.error(f"Ошибка: {str(e)}")

    def run(self):
        if st.session_state.page == "Главная":
            self.main_page()
        elif st.session_state.page == "Админ":
            st.switch_page("pages/admin.py")


def main():
    st.set_page_config(
        page_title="TaskFlow",
        page_icon="📋",
        layout="wide"
    )

    # Анимация снега
    with st.spinner("Падающие снежинки..."):
        st.snow()

    # Инициализация времени
    if "current_time" not in st.session_state:
        st.session_state.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Запуск приложения
    TaskFlowApp().run()


if __name__ == "__main__":
    main()