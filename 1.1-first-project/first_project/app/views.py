from django.shortcuts import render, reverse
from django.http import HttpResponse
import datetime
import os

def home_view(request):
    """Домашняя страница со списком доступных страниц"""
    context = {
        'pages': [
            {'name': 'Текущее время', 'url': '/current_time/'},
            {'name': 'Содержимое рабочей директории', 'url': '/workdir/'},
        ]
    }
    return render(request, 'home.html', context)

def current_time_view(request):
    """Показывает текущее время"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return HttpResponse(f"""
        <h1>🕐 Текущее время</h1>
        <p style="font-size: 32px; color: #4CAF50; font-weight: bold;">{current_time}</p>
        <br>
        <a href="/" style="color: #4CAF50; text-decoration: none; font-size: 18px;">← На главную</a>
    """)

def workdir_view(request):
    """Выводит содержимое рабочей директории"""
    try:
        # Получаем список файлов и папок в текущей директории
        items = os.listdir('.')
        
        # Разделяем файлы и папки
        files = []
        dirs = []
        
        for item in items:
            if os.path.isdir(item):
                dirs.append(item)
            else:
                files.append(item)
        
        # Сортируем списки
        dirs.sort()
        files.sort()
        
        # Формируем HTML-ответ
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Содержимое рабочей директории</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                h1 { color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }
                h2 { color: #555; margin-top: 20px; }
                .back-link { display: inline-block; margin-top: 20px; color: #4CAF50; text-decoration: none; font-size: 18px; }
                .back-link:hover { text-decoration: underline; }
                ul { list-style: none; padding: 0; }
                li { padding: 8px 12px; margin: 5px 0; background: #f5f5f5; border-radius: 4px; }
                .dir { color: #2196F3; font-weight: bold; }
                .file { color: #333; }
            </style>
        </head>
        <body>
            <h1>📂 Содержимое рабочей директории</h1>
        """
        
        if dirs:
            html += "<h2>📁 Папки:</h2><ul>"
            for dir_name in dirs:
                html += f'<li class="dir">📁 {dir_name}/</li>'
            html += "</ul>"
        else:
            html += "<p>Нет папок</p>"
        
        if files:
            html += "<h2>📄 Файлы:</h2><ul>"
            for file_name in files:
                html += f'<li class="file">📄 {file_name}</li>'
            html += "</ul>"
        else:
            html += "<p>Нет файлов</p>"
        
        html += """
            <br>
            <a href="/" class="back-link">← На главную</a>
        </body>
        </html>
        """
        
        return HttpResponse(html)
        
    except Exception as e:
        return HttpResponse(f"""
            <h1>❌ Ошибка при чтении директории</h1>
            <p style="color: red;">{e}</p>
            <br>
            <a href="/" style="color: #4CAF50; text-decoration: none; font-size: 18px;">← На главную</a>
        """)
