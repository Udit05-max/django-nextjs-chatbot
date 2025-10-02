# 🚀 Quick Start Guide

## One-Command Setup

```bash
# 1. Clone the repo
git clone https://github.com/aparsoft/django-nextjs-chatbot.git
cd django-nextjs-chatbot

# 2. Setup environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Start everything
docker-compose up --build
```

That's it! 🎉

---

## What Happens Automatically?

When you run `docker-compose up`, the backend entrypoint script automatically:

1. **Waits for PostgreSQL** - Ensures database is ready
2. **Runs Migrations** - Creates all database tables
3. **Creates Superuser** - Admin account ready to use
4. **Collects Static Files** - Prepares assets
5. **Starts Server** - Django and Next.js ready

---

## Access Your Application

| Service | URL | Credentials |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | - |
| **Backend API** | http://localhost:8000 | - |
| **Django Admin** | http://localhost:8000/chatbot-admin/ | `admin` / `admin123` |
| **PostgreSQL** | localhost:5433 | `chatbot_user` / `chatbot_pass` |
| **Redis** | localhost:6380 | - |

---

## Default Superuser

- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@aparsoft.com`

⚠️ **Important:** Change this password immediately in production!

To change the password:
```bash
docker-compose exec backend python manage.py changepassword admin
```

---

## First Time Setup Checklist

- [x] Clone repository
- [x] Copy `.env.example` to `.env`
- [x] Add your `OPENAI_API_KEY` to `.env`
- [x] Run `docker-compose up --build`
- [ ] Wait for all services to start (watch the logs)
- [ ] Open http://localhost:3000
- [ ] Login to admin at http://localhost:8000/chatbot-admin/
- [ ] Start building your chatbot! 🤖

---

## Common Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Access Django Shell
```bash
docker-compose exec backend python manage.py shell
```

### Create Another Superuser
```bash
docker-compose exec backend python manage.py createsuperuser
```

### Run Migrations (if needed manually)
```bash
docker-compose exec backend python manage.py migrate
```

### Restart Services
```bash
docker-compose restart
```

### Stop Everything
```bash
docker-compose down
```

### Clean Start (removes data!)
```bash
docker-compose down -v
docker-compose up --build
```

---

## Troubleshooting

### Port Already in Use?

If you see port conflicts, edit `docker-compose.yml`:
- PostgreSQL: Change `5433:5432`
- Redis: Change `6380:6379`
- Backend: Change `8000:8000`
- Frontend: Change `3000:3000`

### Database Connection Issues?

The entrypoint script waits for PostgreSQL. If issues persist:
```bash
docker-compose restart backend
```

### Frontend Not Loading?

Check if all environment variables are set:
```bash
docker-compose exec frontend env | grep NEXT_PUBLIC
```

---

## Need Help?

- **YouTube Tutorials:** [@aparsoft-ai](https://youtube.com/@aparsoft-ai)
- **GitHub Issues:** [Report a bug](https://github.com/aparsoft/django-nextjs-chatbot/issues)
- **Discord:** Ask in our community (link in YouTube description)

---

**Happy coding! 🚀**

*Built with ❤️ by Aparsoft Team*
