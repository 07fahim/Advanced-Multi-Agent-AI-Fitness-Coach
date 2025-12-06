# 🏋️ AI-Powered Fitness Coach

<div align="center">

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.0+-FF6B6B?style=for-the-badge)
![AstraDB](https://img.shields.io/badge/AstraDB-Database-FF6B6B?style=for-the-badge)

**Your Personal Trainer & Nutritionist in One**

An intelligent fitness coaching application powered by AI that provides personalized workout plans, nutrition guidance, and real-time fitness advice.

[🚀 Live Demo](https://fitness-coach-wsipw4fnqsa9zkrdej4cjh.streamlit.app) • [🐛 Report Bug](#) • [💡 Request Feature](#)

</div>

---

## 📹 Project Demo

<!-- TODO: Add project video here -->
<div align="center">

**🎥 Project Demo Video Coming Soon!**

*[Video will be embedded here]*

</div>

---

## ✨ Features

### 🤖 AI-Powered Coaching
- **Intelligent Chat Assistant**: Get personalized fitness and nutrition advice powered by Groq AI
- **Context-Aware Responses**: AI remembers your conversation history and profile
- **Multi-Agent System**: Smart routing between general fitness advice and math-based calculations

### 👤 Personalized Profiles
- **User Management**: Multiple user support with name-based profiles
- **Comprehensive Data**: Track age, weight, height, gender, and activity level
- **Goal Setting**: Set and track fitness goals (Muscle Gain, Fat Loss, Stay Active)

### 🥗 Nutrition & Macros
- **AI-Generated Macros**: Get personalized daily macronutrient recommendations
- **Custom Tracking**: Manually set and track calories, protein, fat, and carbs
- **Smart Calculations**: AI considers your profile and goals for accurate recommendations

### 📋 Fitness Journal
- **Notes & Tracking**: Document your fitness journey, workouts, and insights
- **Vector Search**: AI uses your notes for personalized advice (AstraDB integration)
- **Progress Tracking**: Keep a detailed log of your fitness journey

### 💬 Interactive Chat Interface
- **Conversation History**: Full chat history with context-aware responses
- **Personalized Responses**: AI addresses you by name and uses your profile data
- **Real-Time Advice**: Get instant answers to fitness and nutrition questions

---

## 🛠️ Tech Stack

### Core Technologies
- **Frontend**: [Streamlit](https://streamlit.io/) - Interactive web app framework
- **Backend**: Python 3.8+
- **AI/ML**: 
  - [LangChain](https://www.langchain.com/) - LLM framework
  - [Groq AI](https://groq.com/) - Fast inference engine (FREE tier available)
- **Database**: 
  - [AstraDB](https://www.datastax.com/products/datastax-astra) - Vector database for notes storage
  - Vector search capabilities for personalized recommendations

### Key Libraries
- `langchain-groq` - Groq AI integration
- `langchain-community` - Community tools and integrations
- `langchain-classic` - Backward compatibility
- `astrapy` - AstraDB Python driver
- `python-dotenv` - Environment variable management

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed
- **Git** for version control
- **API Keys**:
  - [Groq API Key](https://console.groq.com/) (FREE tier available)
  - [AstraDB](https://astra.datastax.com/) account and credentials

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/fitness-app.git
cd fitness-app
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Setup

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
ASTRA_DB_APPLICATION_TOKEN=your_astra_token_here
ASTRA_ENDPOINT=your_astra_endpoint_here
```

**⚠️ Important**: Never commit your `.env` file to version control!

### 5. Run the Application

```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📖 Usage Guide

### Getting Started

1. **Select or Create User Profile**
   - Enter your name to create a new profile
   - Or select from existing users if you've used the app before

2. **Fill Personal Information**
   - Complete your profile: age, weight, height, gender, activity level
   - All fields use placeholders for easy input

3. **Set Fitness Goals**
   - Choose from: Muscle Gain, Fat Loss, or Stay Active
   - You can select multiple goals

4. **Generate Macros (Optional)**
   - Click "Generate Macros with AI" for personalized recommendations
   - Or manually enter your daily targets

5. **Add Notes**
   - Document your workouts, progress, or insights
   - AI uses these notes for personalized advice

6. **Chat with AI Coach**
   - Ask any fitness or nutrition questions
   - AI uses your profile and notes for personalized responses
   - Conversation history is maintained for context

### Example Questions

- "Can you create a leg day workout routine for me?"
- "What should I eat to meet my protein goal?"
- "How many calories should I consume for fat loss?"
- "Create a meal plan for muscle gain"

---

## 🏗️ Project Structure

```
fitness-app/
│
├── main.py                 # Main Streamlit application
├── langchain_agents.py    # AI agents and LLM integration
├── profiles.py            # User profile management
├── form_submit.py         # Form handling and database operations
├── db.py                  # Database connection and setup
│
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in repo)
├── .gitignore            # Git ignore rules
│
├── README.md             # This file
├── DEPLOYMENT_GUIDE.md   # Deployment instructions
└── QUICK_DEPLOY.md       # Quick deployment checklist
```

### Key Files

- **`main.py`**: Main application entry point with Streamlit UI
- **`langchain_agents.py`**: AI agent implementations (MacroAgent, AskAISystem)
- **`profiles.py`**: User profile CRUD operations
- **`form_submit.py`**: Form submission handlers
- **`db.py`**: AstraDB connection and collection management

---

## 🌐 Deployment

### Streamlit Cloud (Recommended)

The easiest way to deploy this app is using [Streamlit Cloud](https://share.streamlit.io/):

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" and select your repository
4. Add environment variables in Settings → Secrets
5. Deploy! 🚀

**Detailed instructions**: See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

### Other Platforms

This app can also be deployed on:
- **Heroku**
- **Railway**
- **Render**
- **AWS/GCP/Azure**
- **Docker** (with containerization)

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq AI API key | ✅ Yes |
| `ASTRA_DB_APPLICATION_TOKEN` | AstraDB authentication token | ✅ Yes |
| `ASTRA_ENDPOINT` | Your AstraDB API endpoint | ✅ Yes |

### API Setup

#### Groq AI (FREE)
1. Sign up at [console.groq.com](https://console.groq.com/)
2. Create an API key
3. Free tier includes generous limits

#### AstraDB (FREE)
1. Sign up at [astra.datastax.com](https://astra.datastax.com/)
2. Create a database
3. Get your application token and endpoint
4. Create collections: `personal_data` and `notes`

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - For the amazing framework
- [LangChain](https://www.langchain.com/) - For LLM integration tools
- [Groq AI](https://groq.com/) - For fast, free AI inference
- [AstraDB](https://www.datastax.com/products/datastax-astra) - For vector database capabilities

---

## 📊 Features Roadmap

- [ ] Workout plan generator
- [ ] Meal plan creator
- [ ] Progress tracking charts
- [ ] Social features
- [ ] Mobile app version
- [ ] Integration with fitness trackers

---

## 🐛 Known Issues

- Vector search requires AstraDB vectorization service configuration
- Some LangChain imports may vary by version (handled with fallbacks)

---

## 💬 Support

If you have any questions or need help:

- 📧 Open an issue on GitHub
- 💬 Check the [Discussions](https://github.com/YOUR_USERNAME/fitness-app/discussions) section
- 📖 Read the [Documentation](./DEPLOYMENT_GUIDE.md)

---

## ⭐ Show Your Support

If you find this project helpful, please give it a ⭐ on GitHub!

---

<div align="center">

**Made with ❤️ using Streamlit, LangChain, and Groq AI**

[⬆ Back to Top](#-ai-powered-fitness-coach)

</div>

