# AI Playground

Минимальный AI Playground: страница в браузере отправляет текст на FastAPI, backend вызывает Ollama Cloud через OpenAI-compatible API и возвращает ответ на страницу.

Цепочка: **Frontend → FastAPI → Ollama Cloud → FastAPI → Frontend**.

## Подготовка

1. Создайте виртуальное окружение в этой папке:

   ```bash
   python -m venv .venv
   ```

2. Активируйте его:

   - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
   - macOS / Linux: `source .venv/bin/activate`

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Скопируйте шаблон окружения и добавьте ключ **только** в локальный файл `.env` (этот файл не коммитится):

   ```bash
   copy .env.example .env
   ```

   На macOS / Linux: `cp .env.example .env`

   Для текущего провайдера нужна переменная `OLLAMA_API_KEY` (шаблон без настоящего ключа есть в `.env.example`). Строку `OPENAI_API_KEY` в `.env` оставляем: она не используется этим этапом, но не удаляется. Ключ нужен только backend-у. Его не следует вставлять во frontend или в Git.

## Запуск

Из папки проекта, с активированным `.venv`:

```bash
uvicorn app:app --reload
```

Откройте в браузере: http://127.0.0.1:8000

## Файлы

- `app.py` — FastAPI: отдаёт страницу и проксирует запрос в Ollama Cloud (`https://ollama.com/v1/`).
- `static/index.html` — простой интерфейс без фреймворков.
- `.env.example` — шаблон `OPENAI_API_KEY` и `OLLAMA_API_KEY` без настоящих ключей.
- `.gitignore` — скрывает `.env`, `.venv` и Python-кэш от Git.
- `requirements.txt` — зависимости Python.
