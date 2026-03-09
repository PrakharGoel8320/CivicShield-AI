import { useRouter } from 'next/router'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { 
  BarChart3, 
  Database, 
  Brain, 
  TrendingUp, 
  Shield, 
  Sparkles,
  ArrowRight,
  CheckCircle2,
  Zap
} from 'lucide-react'

export default function Home() {
  const router = useRouter()

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Navigation */}
      <nav className="backdrop-blur-md bg-white/70 dark:bg-gray-900/70 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <Shield className="w-8 h-8 text-primary-600" />
              <span className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
                CivicShield AI
              </span>
            </div>
            <Link 
              href="/dashboard"
              className="btn-primary flex items-center space-x-2"
            >
              <span>Get Started</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-28">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="inline-flex items-center space-x-2 bg-primary-100 dark:bg-primary-900/30 px-4 py-2 rounded-full mb-6"
            >
              <Sparkles className="w-4 h-4 text-primary-600" />
              <span className="text-sm font-semibold text-primary-600">Powered by AI & Machine Learning</span>
            </motion.div>

            <h1 className="text-5xl md:text-7xl font-extrabold mb-6">
              <span className="bg-gradient-to-r from-primary-600 via-secondary-600 to-primary-600 bg-clip-text text-transparent">
                Urban Solutions
              </span>
              <br />
              <span className="text-gray-900 dark:text-white">Made Intelligent</span>
            </h1>

            <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-10 max-w-3xl mx-auto">
              Transform your data into actionable insights with our advanced AI platform. 
              Analyze, predict, and optimize urban solutions effortlessly.
            </p>

            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <button
                onClick={() => router.push('/dashboard')}
                className="btn-primary text-lg px-8 py-4 flex items-center justify-center space-x-2"
              >
                <span>Launch Dashboard</span>
                <ArrowRight className="w-5 h-5" />
              </button>
              <button
                onClick={() => router.push('/upload')}
                className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white border-2 border-gray-300 dark:border-gray-600 hover:border-primary-600 dark:hover:border-primary-500 font-semibold text-lg px-8 py-4 rounded-lg transition-all duration-200"
              >
                Upload Data
              </button>
            </div>
          </motion.div>

          {/* Animated Feature Cards */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-20"
          >
            <FeatureCard
              icon={<Database className="w-8 h-8" />}
              title="Data Management"
              description="Upload, clean, and preprocess your datasets with powerful tools"
              color="blue"
            />
            <FeatureCard
              icon={<Brain className="w-8 h-8" />}
              title="AI Models"
              description="Train multiple ML models and compare performance metrics"
              color="purple"
            />
            <FeatureCard
              icon={<TrendingUp className="w-8 h-8" />}
              title="Visualizations"
              description="Interactive charts, maps, and dashboards for insights"
              color="green"
            />
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Everything You Need
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              Comprehensive tools for data science and machine learning
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="card"
              >
                <div className="flex items-center space-x-3 mb-4">
                  <CheckCircle2 className="w-6 h-6 text-green-500" />
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    {feature.title}
                  </h3>
                </div>
                <p className="text-gray-600 dark:text-gray-300">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-primary-600 to-secondary-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <Zap className="w-16 h-16 text-white mx-auto mb-6" />
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Ready to Get Started?
            </h2>
            <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
              Join the future of urban data analysis. Start analyzing your data in minutes.
            </p>
            <button
              onClick={() => router.push('/dashboard')}
              className="bg-white text-primary-600 hover:bg-gray-100 font-bold text-lg px-10 py-4 rounded-lg transition-colors duration-200 inline-flex items-center space-x-2"
            >
              <span>Access Dashboard</span>
              <ArrowRight className="w-5 h-5" />
            </button>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <Shield className="w-6 h-6 text-primary-400" />
            <span className="text-xl font-bold">CivicShield AI</span>
          </div>
          <p className="text-gray-400">
            © 2026 CivicShield AI. Built for Circuit Minds Hackathon.
          </p>
        </div>
      </footer>
    </div>
  )
}

function FeatureCard({ icon, title, description, color }: any) {
  const colorClasses = {
    blue: 'from-blue-500 to-blue-600',
    purple: 'from-purple-500 to-purple-600',
    green: 'from-green-500 to-green-600',
  }

  return (
    <motion.div
      whileHover={{ y: -8, scale: 1.02 }}
      className="card cursor-pointer"
    >
      <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${colorClasses[color as keyof typeof colorClasses]} flex items-center justify-center text-white mb-4`}>
        {icon}
      </div>
      <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
        {title}
      </h3>
      <p className="text-gray-600 dark:text-gray-300">
        {description}
      </p>
    </motion.div>
  )
}

const features = [
  {
    title: 'Data Upload & Parsing',
    description: 'Support for CSV, Excel, and JSON formats with automatic schema detection',
  },
  {
    title: 'Data Cleaning',
    description: 'Handle missing values, outliers, and duplicates automatically',
  },
  {
    title: 'Feature Engineering',
    description: 'Create new features from existing data with advanced transformations',
  },
  {
    title: 'Multiple ML Models',
    description: 'Linear Regression, Random Forest, Decision Tree, and more',
  },
  {
    title: 'Model Comparison',
    description: 'Compare model performance with detailed metrics and visualizations',
  },
  {
    title: 'Interactive Dashboards',
    description: 'Beautiful, responsive dashboards with real-time updates',
  },
  {
    title: 'Data Visualization',
    description: 'Charts, graphs, and plots powered by Plotly and Chart.js',
  },
  {
    title: 'Map Integration',
    description: 'Visualize geographical data with interactive Leaflet maps',
  },
  {
    title: 'Export Results',
    description: 'Download processed data and predictions in multiple formats',
  },
]
