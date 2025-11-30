# Resume Management System - Frontend

Vue 3 + Vite frontend for the Resume Management System.

## Features

- Vue 3 with Composition API
- Pinia for state management
- Vue Router for routing
- Element Plus UI framework
- Vue I18n for internationalization (Chinese/English)
- Axios for HTTP requests
- Responsive design

## Setup

### 1. Install dependencies

```bash
cd frontend
npm install
```

### 2. Configure environment variables

```bash
# Create .env file (already created)
# Edit if needed to change API URL
VITE_API_BASE_URL=http://localhost:8000/api
```

### 3. Run development server

```bash
npm run dev
```

The application will be available at http://localhost:5173

## Build for Production

```bash
npm run build
```

Built files will be in the `dist/` directory.

## Project Structure

```
src/
├── api/              # API services
├── assets/           # Static assets
├── components/       # Reusable components
├── locales/          # i18n translations
├── router/           # Vue Router configuration
├── stores/           # Pinia stores
├── views/            # Page components
│   ├── admin/        # Admin panel views
│   └── ResumeView.vue # Public resume view
├── App.vue           # Root component
└── main.js           # Application entry point
```

## Routes

### Public Routes
- `/` - Resume display page

### Admin Routes (Requires Authentication)
- `/admin/login` - Admin login
- `/admin/dashboard` - Admin dashboard
- `/admin/personal-info` - Edit personal information
- `/admin/work-experience` - Manage work experiences

## Language Switching

The application supports Chinese (Traditional) and English. Users can switch languages using the button in the top-right corner.

Languages are stored in `localStorage` and persisted across sessions.

## Default Admin Credentials

- Username: `admin`
- Password: `admin123`

**Important**: Change these credentials in production!
