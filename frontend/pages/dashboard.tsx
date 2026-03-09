import { useState, useEffect } from 'react'
import Layout from '../components/Layout'
import { motion } from 'framer-motion'
import {
  Database,
  TrendingUp,
  Activity,
  Zap,
  FileText,
  CheckCircle2,
  AlertCircle,
  BarChart3
} from 'lucide-react'

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalRows: 0,
    totalColumns: 0,
    modelsTrained: 0,
    predictions: 0
  })

  return (
    <Layout>
      <div className="space-y-6">
        {/* Welcome Banner */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-primary-600 to-secondary-600 rounded-xl p-8 text-white"
        >
          <h1 className="text-3xl font-bold mb-2">Welcome to CivicShield AI</h1>
          <p className="text-white/90 text-lg">
            Your intelligent platform for urban data analysis and predictions
          </p>
        </motion.div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            icon={<Database className="w-8 h-8" />}
            title="Dataset Rows"
            value={stats.totalRows.toLocaleString()}
            color="blue"
            trend="+12%"
          />
          <StatCard
            icon={<BarChart3 className="w-8 h-8" />}
            title="Features"
            value={stats.totalColumns.toString()}
            color="green"
            trend="+5%"
          />
          <StatCard
            icon={<Activity className="w-8 h-8" />}
            title="Models Trained"
            value={stats.modelsTrained.toString()}
            color="purple"
            trend="+3"
          />
          <StatCard
            icon={<Zap className="w-8 h-8" />}
            title="Predictions"
            value={stats.predictions.toLocaleString()}
            color="orange"
            trend="+24%"
          />
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="card"
          >
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
              Quick Actions
            </h2>
            <div className="space-y-3">
              <QuickActionButton
                icon={<FileText className="w-5 h-5" />}
                title="Upload New Dataset"
                description="Import CSV, Excel, or JSON files"
                href="/upload"
              />
              <QuickActionButton
                icon={<Activity className="w-5 h-5" />}
                title="Train ML Model"
                description="Start training your models"
                href="/train"
              />
              <QuickActionButton
                icon={<BarChart3 className="w-5 h-5" />}
                title="View Analytics"
                description="Explore data insights"
                href="/analytics"
              />
              <QuickActionButton
                icon={<TrendingUp className="w-5 h-5" />}
                title="Open Visualizations"
                description="Correlation heatmap and distributions"
                href="/visualizations"
              />
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="card"
          >
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
              Recent Activity
            </h2>
            <div className="space-y-3">
              <ActivityItem
                icon={<CheckCircle2 className="w-5 h-5 text-green-500" />}
                title="Dataset Uploaded"
                time="2 minutes ago"
              />
              <ActivityItem
                icon={<CheckCircle2 className="w-5 h-5 text-green-500" />}
                title="Model Training Complete"
                time="15 minutes ago"
              />
              <ActivityItem
                icon={<AlertCircle className="w-5 h-5 text-yellow-500" />}
                title="Data Cleaning Required"
                time="1 hour ago"
              />
            </div>
          </motion.div>
        </div>

        {/* System Status */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="card"
        >
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
            System Status
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <StatusItem label="API Server" status="operational" />
            <StatusItem label="ML Pipeline" status="operational" />
            <StatusItem label="Data Storage" status="operational" />
          </div>
        </motion.div>
      </div>
    </Layout>
  )
}

function StatCard({ icon, title, value, color, trend }: any) {
  const colorClasses = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    purple: 'from-purple-500 to-purple-600',
    orange: 'from-orange-500 to-orange-600',
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ scale: 1.02 }}
      className="card"
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
            {title}
          </p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white">
            {value}
          </p>
          <p className="text-sm text-green-600 dark:text-green-400 mt-1">
            {trend} from last month
          </p>
        </div>
        <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${colorClasses[color as keyof typeof colorClasses]} flex items-center justify-center text-white`}>
          {icon}
        </div>
      </div>
    </motion.div>
  )
}

function QuickActionButton({ icon, title, description, href }: any) {
  return (
    <a
      href={href}
      className="flex items-center p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors cursor-pointer"
    >
      <div className="flex-shrink-0 w-10 h-10 bg-primary-100 dark:bg-primary-900/30 rounded-lg flex items-center justify-center text-primary-600 mr-4">
        {icon}
      </div>
      <div className="flex-1">
        <h3 className="font-semibold text-gray-900 dark:text-white">{title}</h3>
        <p className="text-sm text-gray-600 dark:text-gray-400">{description}</p>
      </div>
    </a>
  )
}

function ActivityItem({ icon, title, time }: any) {
  return (
    <div className="flex items-center p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
      <div className="flex-shrink-0 mr-3">
        {icon}
      </div>
      <div className="flex-1">
        <p className="text-sm font-medium text-gray-900 dark:text-white">{title}</p>
        <p className="text-xs text-gray-600 dark:text-gray-400">{time}</p>
      </div>
    </div>
  )
}

function StatusItem({ label, status }: any) {
  const isOperational = status === 'operational'
  
  return (
    <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
      <span className="text-sm font-medium text-gray-900 dark:text-white">{label}</span>
      <div className="flex items-center space-x-2">
        <div className={`w-2 h-2 rounded-full ${isOperational ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
        <span className="text-sm text-gray-600 dark:text-gray-400 capitalize">{status}</span>
      </div>
    </div>
  )
}
