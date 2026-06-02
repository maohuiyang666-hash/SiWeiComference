# SiWeiComference

上海市思维科学研究会会议网站，后端为 Flask，数据库为 SQL Server。

## Project Layout

- `Conference/Conferences/run.py`: local development entry point.
- `Conference/Conferences/app`: Flask application package.
- `Conference/Conferences/app/home/views.py`: main routes.
- `Conference/Conferences/app/templates/home`: page templates.
- `Conference/Conferences/app/static/home`: CSS, JavaScript, and images.
- `Conference/*.sql`: database table/data scripts.

## Local Setup

```powershell
cd Conference\Conferences
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Use `.env.example` as the reference for the database and email settings. Set these values in your shell or deployment platform before starting the app.

## Run

```powershell
$env:CONFERENCE_DB_PASSWORD="your-password"
python run.py
```

By default the app runs at `http://127.0.0.1:5000` with debug mode disabled. Use `CONFERENCE_DEBUG=true` only for local development.
