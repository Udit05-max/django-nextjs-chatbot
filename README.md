# 🤖 Learn AI Chatbots | Django + Next.js
*Educational Tutorial Series for Developers*

[![YouTube](https://img.shields.io/badge/YouTube-Subscribe-red?style=flat&logo=youtube)](https://youtube.com/@aparsoft)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Follow-blue?style=flat&logo=linkedin)](https://linkedin.com/company/aparsoft)
[![Website](https://img.shields.io/badge/Website-aparsoft.com-green?style=flat)](https://aparsoft.com)

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)
![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue?logo=postgresql)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green)

> **🎓 Educational Tutorial Series for the Developer Community**
>
> Learn how to build conversational AI chatbots from scratch using Django, Django REST Framework, and Next.js. This hands-on tutorial introduces you to LangChain and LangGraph basics while building a real working chatbot.

## 📖 What Is This Project?

This is a **learning-focused repository** designed to teach developers how to integrate AI into full-stack web applications. It's NOT a comprehensive enterprise solution - it's a clear, straightforward tutorial on building your first conversational chatbot.

**What You'll Learn:**
- Setting up Django + Django REST Framework for AI applications
- Building a modern frontend with Next.js
- Creating basic conversational chatbot functionality
- Introduction to LangChain fundamentals
- LangGraph basics for conversation flows
- Connecting Django backend with AI services
- Deploying a simple AI chatbot

---

## ⚡ Quick Start

**New to AI chatbots?** Perfect! This tutorial is designed for you:

1. 🎥 **[Watch the YouTube Tutorial](https://youtube.com/@aparsoft-ai)** - Follow along step-by-step
2. 💻 **Clone this repo** - Get the starter code
3. 🛠️ **Build with us** - Learn by doing
4. 🚀 **Deploy your chatbot** - See it live!

**No prior AI experience needed** - we'll teach you everything from basics to deployment.

---

## 🎯 About Aparsoft

We're an AI solutions company based in **Bengaluru, India**, and we're passionate about teaching developers. This tutorial series is part of our mission to make AI accessible to the Django and broader developer community.

**Why We Created This Tutorial:**
- Share our Django + AI integration knowledge
- Build a supportive developer community
- Demonstrate the power of Django-DRF-Next.js stack
- Make AI less intimidating for backend developers
- Help you build your first AI project

### 📺 Learn With Us on YouTube

We're building in public and teaching everything we know:

- **YouTube:** [@aparsoft-ai](https://youtube.com/@aparsoft-ai) - **Weekly tutorials, live coding, and beginner-friendly content**
- **LinkedIn:** [/company/aparsoft](https://linkedin.com/company/aparsoft) - Articles and tech insights
- **GitHub:** [@aparsoft](https://github.com/aparsoft) - Open-source learning projects
- **Twitter/X:** [@aparsoft](https://twitter.com/aparsoft) - Quick tips and dev updates
- **Website:** [aparsoft.com](https://aparsoft.com) - More about our work

**Subscribe to our YouTube channel** - New tutorials every Wednesday, and Friday!

## 🛠️ Tech Stack (What You'll Learn)

This tutorial uses a modern, beginner-friendly stack:

### Backend
- **Django** - Python web framework (easy to learn!)
- **Django REST Framework** - Building APIs the Django way
- **PostgreSQL** - Reliable database (we'll keep it simple)
- **LangChain** - AI framework basics
- **LangGraph** - Conversation flow management intro

### Frontend
- **Next.js** - React framework with great DX
- **Tailwind CSS** - Utility-first styling (fast to learn)
- **Axios** - API calls made easy

### AI Integration
- **OpenAI API** - GPT models (we'll start simple)
- **Basic conversation memory** - Making chatbots remember context
- **Simple prompt engineering** - Getting good responses

### Development Tools
- **Docker** - Easy local setup (one command!)
- **Git** - Version control basics


## 💡 Why This Repository?

This is a **hands-on learning project** for developers who want to understand AI integration without the overwhelm.

**Perfect for:**
- **Django developers** curious about adding AI to their projects
- **Backend developers** wanting to learn LangChain basics
- **Full-stack developers** exploring Next.js + Django integration
- **Students** learning modern web development with AI
- **Bootcamp grads** building their portfolio with real AI projects
- **Anyone** who's intimidated by AI and wants a friendly introduction

**What makes this tutorial special:**
- No complex enterprise patterns (yet!) - just the essentials
- Clear, commented code you can actually understand
- Step-by-step YouTube videos explaining every decision
- Focus on learning, not production complexity
- Build a real working chatbot you can show off!

## 🚀 What You'll Build

By the end of this tutorial, you'll have a working chatbot with:

### 🤖 Basic Chatbot Features
- **Conversational Interface** - Simple, clean chat UI
- **Message History** - Conversations that remember context
- **AI Responses** - Powered by OpenAI GPT models
- **User Sessions** - Multiple users can chat independently

### 🔧 Technical Implementation
- **Django REST API** - Clean, well-structured backend
- **Next.js Frontend** - Modern React with server-side rendering
- **LangChain Integration** - Your first steps with the AI framework
- **LangGraph Basics** - Simple conversation flow patterns
- **Database Storage** - Saving conversations in PostgreSQL

### 📚 Learning Outcomes
- Understand how to connect Django with AI APIs
- Learn LangChain fundamentals through practice
- See how conversation state management works
- Deploy a full-stack AI application
- Build confidence to explore more complex AI features

## 🛠️ Getting Started

### Prerequisites

Don't worry if you don't have everything - we'll guide you through installation in the tutorial videos!

**Required:**
- Python 3.10+ (we recommend 3.12)
- Node.js 18+
- OpenAI API key (we'll show you how to get one)

**Nice to have:**
- Docker Desktop (makes setup easier, but optional)
- Git basics

### 📦 Quick Setup

**Option 1: Docker (Recommended for Beginners)**
```bash
# Clone the repo
git clone https://github.com/aparsoft/django-nextjs-chatbot.git
cd django-nextjs-chatbot

# Create .env file (we'll guide you)
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# Start everything with one command!
docker-compose up
```

That's it! Open `http://localhost:3000` and start chatting.

**Option 2: Manual Setup (If you want to understand each piece)**

We recommend following our YouTube tutorial "[Setting Up Your Django + Next.js Chatbot](https://youtube.com/@aparsoft)" where we walk through each command. Here are the complete steps:

**Step 1: Clone the Repository**
```bash
git clone https://github.com/aparsoft/django-nextjs-chatbot.git
cd django-nextjs-chatbot
```

**Step 2: Backend Setup (Django)**
```bash
# Navigate to backend folder
cd backend

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Create .env file for backend
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run database migrations
python manage.py migrate

# Create a superuser (optional, for admin access)
python manage.py createsuperuser

# Start the Django development server
python manage.py runserver
# Backend will run on http://localhost:8000
```

**Step 3: Frontend Setup (Next.js with .jsx)**
```bash
# Open a new terminal window
# Navigate to frontend folder
cd frontend

# Install Node.js dependencies
npm install
# or if you prefer yarn:
# yarn install

# Create .env.local file for frontend
cp .env.example .env.local
# Edit .env.local and set:
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Start the Next.js development server
npm run dev
# or with yarn:
# yarn dev
# Frontend will run on http://localhost:3000
```

**Step 4: Test Your Setup**
- Open `http://localhost:3000` in your browser
- You should see the chatbot interface
- Try sending a message - it should connect to your Django backend
- Backend API docs available at `http://localhost:8000/api/docs`

**Troubleshooting Common Issues:**
- **Port already in use?** Change ports in settings
- **Module not found?** Make sure virtual environment is activated
- **Database errors?** Run migrations again
- **API not connecting?** Check CORS settings in Django

### 🔑 Getting Your OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com/)
2. Sign up / Log in
3. Go to API Keys section
4. Create a new key
5. Add $5-10 credit (plenty for learning!)

We have a detailed video guide: "Getting Your First OpenAI API Key"

### ❓ Stuck? We're Here to Help!

- **Watch the setup video** on our YouTube channel
- **Ask in GitHub Discussions** - we respond daily!
- **Join our Discord** (link in YouTube description)
- **Check common issues** in our FAQ section below

## 🤝 Contributing

This is a learning project and we welcome contributions from developers at all levels!

**Ways to contribute:**
- **Improve documentation** - Help us make it clearer
- **Add code comments** - Explain tricky parts
- **Report bugs** - Help us fix issues
- **Share your chatbot** - Show what you built!
- **Suggest features** - What would help you learn?

**Not sure where to start?** Check out our "Good First Issue" labels or ask in Discussions!

## 🎬 YouTube Tutorial Series

This repository is the companion code for our **beginner-friendly video tutorial series** on building AI chatbots!

### 📺 Complete Tutorial Playlist

**Part 1: Setup & Basics** (Start here!)
- "Introduction: What We're Building" - Project overview and goals
- "Django + Next.js Setup from Scratch" - Getting your environment ready
- "Your First API Call to OpenAI" - Hello World for AI

**Part 2: Building the Chatbot**
- "Creating the Django REST API" - Backend fundamentals
- "Next.js Frontend Setup" - Building the chat interface
- "Connecting Frontend to Backend" - Making them talk

**Part 3: Adding Intelligence**
- "Introduction to LangChain" - What it is and why we use it
- "Basic Conversation Memory" - Making the chatbot remember
- "Introduction to LangGraph" - Simple conversation flows

**Part 4: Deployment**
- "Docker Basics for Beginners" - Containerizing your app
- "Deploying Your First Chatbot" - Going live!

### 📅 New Learning Content Every Week

- **Monday:** Technical Tutorials (beginner-friendly!)
- **Wednesday:** Live Coding & Q&A
- **Friday:** Quick Tips & Troubleshooting

### 🎓 What Makes Our Tutorials Different?

- ✅ **No assumptions** - We explain every command
- ✅ **Real code** - Not pseudocode, actual working examples
- ✅ **Mistakes included** - We show bugs and how to fix them
- ✅ **Django focus** - For backend devs learning AI
- ✅ **Community support** - Active Discord and discussions

**[→ Start Learning on YouTube](https://youtube.com/@aparsoft-ai)** - First video teaches absolute basics!

---

## 📞 Get Help & Connect

### 🎓 Learning & Community
- **YouTube:** [@aparsoft-ai](https://youtube.com/@aparsoft-ai) - Main tutorial channel
- **Discord:** [Join our community](https://aparsoft.com/discord) - Get help from fellow learners
- **GitHub Discussions:** Ask questions about the code
- **LinkedIn:** [/company/aparsoft](https://linkedin.com/company/aparsoft) - Articles and tips

### 🐛 Found a Bug?
- **GitHub Issues:** [Report it here](https://github.com/aparsoft/django-nextjs-chatbot/issues)
- **Urgent help:** support@aparsoft.com

### 💼 Want Us to Build For You?
If you need a custom AI solution for your business (beyond learning):
- **Website:** [aparsoft.com](https://aparsoft.com)
- **Email:** contact@aparsoft.com
- **Phone:** +91 8904064878

---

## 📄 License

Copyright © 2024 Aparsoft Private Limited. All rights reserved.

This code is provided for educational purposes. Feel free to learn from it, modify it, and use it in your own projects!

---

## 🌟 Support This Project

**If this helped you learn:**
- ⭐ **Star this repo** - Helps others find it
- 🎥 **Subscribe on YouTube** - [@aparsoft](https://youtube.com/@aparsoft)
- 📢 **Share with friends** - Help others learn too
- 💬 **Join discussions** - Share what you built!
- ☕ **Say thanks** - Tag us when you deploy your chatbot

---

## 🚀 What's Next?

Once you complete this tutorial, you can:

1. **Build on it** - Add features like voice input, file uploads, etc.
2. **Share your version** - Show us what you created!
3. **Learn more** - We have advanced tutorials for RAG, agents, and more
4. **Join our community** - Help other learners on their journey
5. **Build for real** - Use this as foundation for actual projects

---

*"Learning AI Together, One Chatbot at a Time"*

**Built with ❤️ by the Aparsoft Team in Bengaluru, India**

**Ready to start?** [▶️ Watch the first video](https://youtube.com/@aparsoft) and code along!