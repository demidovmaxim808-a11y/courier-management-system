"""View-функции главной страницы и общий каркас HTML-страниц."""

from django.http import HttpResponse

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/"
    "bootstrap.min.css"
)


def page(title: str, content: str) -> str:
    """Единый HTML-каркас всех страниц проекта."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link href="{BOOTSTRAP_CSS}" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">Курьеры</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/couriers/">Курьеры</a>
                <a class="nav-link" href="/orders/">Заказы</a>
            </div>
        </div>
    </nav>
    <div class="container">
        {content}
    </div>
</body>
</html>"""


def index(request):
    """Главная страница."""
    content = """
    <h1 class="display-4">Система управления курьерами</h1>
    <p class="lead">Управление курьерами и заказами службы доставки.</p>
    <p>Основные разделы:</p>
    <a href="/couriers/" class="btn btn-primary me-2">Курьеры</a>
    <a href="/orders/" class="btn btn-secondary">Заказы</a>
    """
    return HttpResponse(page("Система управления курьерами", content))


def page_not_found(request, exception):
    """Обработчик ошибки 404."""
    content = """
    <h1 class="text-danger">404 - страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 - страница не найдена", content),
        status=404,
    )
