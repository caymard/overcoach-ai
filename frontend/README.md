# Overcoach AI - Frontend

React + TypeScript + Vite frontend for Overcoach AI.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🏗️ Architecture

- **React 18** with TypeScript
- **Vite** for fast HMR
- **Tailwind CSS** for styling
- **Lucide React** for icons

## 📁 Structure

```
src/
├── components/        # React components
│   ├── HeroSlot.tsx
│   ├── HeroSearch.tsx
│   ├── HeroSelector.tsx
│   ├── MapSelector.tsx
│   ├── DifficultyInput.tsx
│   ├── CoachButton.tsx
│   ├── TeamRecommendation.tsx
│   └── StrategyDisplay.tsx
├── services/          # API clients
│   ├── overfastApi.ts
│   └── overcoachApi.ts
├── types/             # TypeScript types
│   └── overwatch.ts
├── App.tsx            # Main app
└── main.tsx           # Entry point
```

## 🎨 Features

- **Team Composition Builder**: Select enemy and friendly team (5 heroes each)
- **Map Selection**: Searchable dropdown with map thumbnails
- **Difficulty Input**: Describe the problem you're facing
- **AI Suggestions**: Get team recommendations from Coach AI
- **Real-time Loading**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages

## 🔌 API Integration

### OverFast API
- `GET /heroes` - Fetch all heroes
- `GET /maps` - Fetch all maps

### Overcoach AI API (localhost:8000)
- `POST /suggest` - Get team composition suggestions

## 🎮 Usage

1. Select enemy team heroes (at least 1 required)
2. Optionally select your current team
3. Optionally select the map
4. Describe the difficulty (optional)
5. Click "Help!" button
6. Wait for AI coach suggestions

## 🛠️ Development

Backend must be running on `http://localhost:8000`:

```bash
# In backend directory
./start.sh
```

Then start the frontend:

```bash
npm run dev
```

Open http://localhost:5173

## 🎨 Theming

Tailwind custom colors in `tailwind.config.js`:

- `overwatch-orange`: #F99E1A
- `overwatch-blue`: #00CCFF
- `overwatch-tank`: #FAA528
- `overwatch-damage`: #F6475D
- `overwatch-support`: #FCBD42
