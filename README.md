# 📄 LegalLens

LegalLens is a full-stack web application that uses AI to help users analyze legal documents. It provides secure authentication, PDF uploading and parsing, clause and risk identification, and an AI-powered chat interface for understanding specific legal texts.

---

## 🚀 Features

### 🌐 Frontend (React + Vite)
- **Authentication**: Login and registration with token-based session management.
- **Dashboard**: View, search, and delete uploaded documents.
- **PDF Upload Modal**: Drag-and-drop interface for uploading and analyzing documents.
- **Chat Panel**: Ask contextual questions about any document with natural-language responses.
- **Responsive Design**: Clean and modern interface built with TailwindCSS.
- **Notification System**: Real-time feedback using `react-hot-toast`.

### 🔙 Backend (FastAPI + SQLModel)
- **User Management**: Secure JWT-based registration and login.
- **Document Parsing**: Extracts content from uploaded PDFs using `PyMuPDF`.
- **AI-Powered Analysis**: Summarizes documents, identifies key clauses and red flags via OpenRouter API.
- **AI Chat Endpoint**: Responds to user questions with contextual legal insight.
- **Role-based Authorization**: Protects routes and ensures users access only their own data.
- **Database Integration**: SQLModel with foreign key relations and proper indexing.

---

## 📁 Tech Stack

| Layer      | Technology                           |
|------------|--------------------------------------|
| Frontend   | React 19, Vite, TypeScript, Zustand  |
| UI/UX      | TailwindCSS, React Icons, Hot Toast  |
| Backend    | FastAPI, SQLModel, PyMuPDF           |
| AI Engine  | OpenRouter API (LLM: mistral-7b)     |
| Auth       | JWT + Bcrypt + Secure Dependencies   |
| Database   | SQL (via SQLModel ORM)               |

---

## 🛠️ Installation

### Prerequisites
- Node.js & npm
- Python 3.11+
- PostgreSQL (or compatible SQL database)

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/legallens.git
cd legallens
```

### 2. Backend Setup
Create a virtual environment and install dependencies:

```bash
cd backend
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
pip install -r requirements.txt
```

Set environment variables (e.g. `.env`):
```
SECRET_KEY=your-secret-key
OPENROUTER_API_KEY=your-api-key
```

Initialize the database:
```bash
uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Access the app at: `http://localhost:5173`

---

## 🔐 API Overview

### Auth Routes (`/auth`)
- `POST /register`: Create a new account.
- `POST /login`: Login and receive JWT token.

### Document Routes (`/document`)
- `POST /upload`: Upload a PDF, extract and analyze.
- `GET /{doc_id}`: Get full details of a document.
- `GET /documents`: List all user documents.
- `DELETE /{doc_id}`: Remove a document.

### AI Routes (`/ai/chat`)
- `POST`: Ask questions about a document using context.

---

## 🧪 Scripts

### Frontend
| Command         | Description                   |
|-----------------|-------------------------------|
| `npm run dev`   | Starts development server     |
| `npm run build` | Builds production assets      |
| `npm run preview` | Preview production build    |
| `npm run lint`  | Lints source code             |

### Backend
Run using:
```bash
uvicorn app.main:app --reload
```

---

## 🎨 UI Structure

- `Home`: Welcome page, login/register access
- `Dashboard`: Document list, actions
- `DocumentDetails`: Clause analysis, red flags
- `UploadModal`: PDF upload with drag-drop
- `ChatPanel`: AI assistant for questions

---

## 🤖 AI Integration

Uses OpenRouter's Mistral-7B model:
- Summarizes content
- Detects clauses
- Flags legal risks
- Answers questions based on context

Ensure you provide an active `OPENROUTER_API_KEY` with domain tracing headers.

---

## 🧾 License

This project is released under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 👏 Contributors

LegalLens is built with ❤️ by Me

---

## 📮 Contact & Feedback

Have ideas or want to report a bug? Start an issue or reach out via email at: `agmzcr@gmail.com`
