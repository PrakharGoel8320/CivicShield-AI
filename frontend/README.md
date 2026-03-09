# CivicShield AI - Frontend

Modern React/Next.js frontend for CivicShield AI platform.

## Features

- 🎨 Modern SaaS-style dashboard with Tailwind CSS
- 📊 Interactive data visualizations with Chart.js and Plotly
- 🗺️ Map visualization with Leaflet
- 🤖 ML model training interface
- 📈 Real-time predictions
- 📱 Fully responsive design
- 🌙 Dark mode support
- ⚡ Fast and optimized with Next.js

## Tech Stack

- **Framework**: Next.js 14
- **UI**: React 18, Tailwind CSS
- **Charts**: Chart.js, React-Chartjs-2, Plotly
- **Maps**: Leaflet, React-Leaflet
- **Animations**: Framer Motion
- **HTTP Client**: Axios
- **Icons**: Lucide React

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env.local` file:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Run development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000)

## Pages

- **/** - Landing page with hero and features
- **/dashboard** - Main dashboard with stats and quick actions
- **/upload** - Dataset upload interface
- **/analytics** - Data statistics and analysis
- **/visualizations** - Interactive charts and correlation heatmap
- **/train** - ML model training interface
- **/predictions** - Make predictions with trained models
- **/map** - Geographical visualization

## Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── pages/           # Next.js pages
├── components/      # React components
├── styles/          # Global styles
├── public/          # Static assets
└── package.json     # Dependencies
```

## Environment Variables

- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)

## Development

The application connects to the FastAPI backend for all data operations. Make sure the backend is running on port 8000.
