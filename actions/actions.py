import pyodbc # type: ignore 
from rasa_sdk import Action, Tracker # type: ignore
from rasa_sdk.executor import CollectingDispatcher # type: ignore
from typing import Any, Text, Dict, List

class ActionQueryArticles(Action):

    def name(self) -> Text:
        return "action_query_articles"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Cấu hình kết nối với SQL Server
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=ZYOND\SQLEXPRESS;'  # Thay YOUR_SERVER_NAME bằng tên server của bạn
            'DATABASE=JournalDB;'
            'UID=dieu;'  # Thay YOUR_USERNAME bằng tên người dùng của bạn
            'PWD=dieu12345678;'  # Thay YOUR_PASSWORD bằng mật khẩu của bạn
        )

        cursor = connection.cursor()

        # Lấy thông tin từ tracker (ví dụ: tên bài báo hoặc tên tác giả)
        query_type = tracker.get_slot('query_type')
        query_value = tracker.get_slot('query_value')

        # Thực hiện truy vấn dựa trên loại thông tin người dùng yêu cầu
        if query_type == 'title':
            query = "SELECT Title, Abstract, Author, PublishedDate FROM Articles WHERE Title LIKE ?"
        elif query_type == 'author':
            query = "SELECT Title, Abstract, Author, PublishedDate FROM Articles WHERE Author LIKE ?"
        else:
            query = ""

        cursor.execute(query, f'%{query_value}%')
        result = cursor.fetchall()

        if result:
            response = "Kết quả tìm kiếm:\n"
            for row in result:
                response += f"Title: {row.Title}\nAbstract: {row.Abstract}\nAuthor: {row.Author}\nPublished Date: {row.PublishedDate}\n\n"
        else:
            response = "Không tìm thấy thông tin bạn yêu cầu."

        # Đóng kết nối
        connection.close()

        # Trả kết quả về khung chat
        dispatcher.utter_message(text=response)

        return []
