import { useState, useEffect } from 'react'
import type { ReactNode } from 'react'
import Layout from '../components/Layout'
import { motion } from 'framer-motion'
import axios from 'axios'
import { Bar, Doughnut } from 'react-chartjs-2'
import { TrendingUp, Database, Activity, Loader } from 'lucide-react'

const API_URL = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000').replace(/\/+$/, '')

export default function Analytics() {
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState<any>(null)
  const [preview, setPreview] = useState<any[]>([])
  const [columns, setColumns] = useState<string[]>([])
  const [targetOptions, setTargetOptions] = useState<any[]>([])
  const [selectedTargetOptionId, setSelectedTargetOptionId] = useState('')
  const [selectedDatasetName, setSelectedDatasetName] = useState('')
  const [selectedTargetColumn, setSelectedTargetColumn] = useState('')

  useEffect(() => {
    initializeAnalytics()
  }, [])

  const initializeAnalytics = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/ml/target-options`)
      const options = response.data.target_options || []
      setTargetOptions(options)

      if (options.length > 0) {
        await handleTargetOptionChange(options[0].id, options)
      } else {
        setStats(null)
        setLoading(false)
      }
    } catch (error) {
      console.error('Error loading target options:', error)
      setStats(null)
      setLoading(false)
    }
  }

  const handleTargetOptionChange = async (optionId: string, optionsOverride?: any[]) => {
    const options = optionsOverride || targetOptions
    const selectedOption = options.find((option) => option.id === optionId)

    setSelectedTargetOptionId(optionId)

    if (!selectedOption) {
      setSelectedDatasetName('')
      setSelectedTargetColumn('')
      setStats(null)
      return
    }

    setSelectedDatasetName(selectedOption.dataset_name)
    setSelectedTargetColumn(selectedOption.target_column)
    await fetchAnalytics(selectedOption.dataset_name)
  }

  const fetchAnalytics = async (datasetName: string) => {
    try {
      setLoading(true)
      const [statsRes, previewRes] = await Promise.all([
        axios.get(`${API_URL}/api/data/statistics`, { params: { dataset_name: datasetName } }),
        axios.get(`${API_URL}/api/data/preview`, { params: { limit: 10, dataset_name: datasetName } })
      ])

      setStats(statsRes.data)
      setPreview(previewRes.data.data)
      setColumns(Object.keys(previewRes.data.data[0] || {}))
    } catch (error) {
      console.error('Error fetching analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <Loader className="w-12 h-12 text-primary-600 animate-spin mx-auto mb-4" />
            <p className="text-gray-600 dark:text-gray-400">Loading analytics...</p>
          </div>
        </div>
      </Layout>
    )
  }

  if (!stats) {
    return (
      <Layout>
        <div className="card text-center py-12">
          <Database className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            No Data Available
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Upload a dataset to view analytics
          </p>
          <a href="/upload" className="btn-primary inline-block">
            Upload Dataset
          </a>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="space-y-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card"
        >
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
            Analytics Target Selection
          </h2>
          <select
            value={selectedTargetOptionId}
            onChange={(e) => handleTargetOptionChange(e.target.value)}
            className="input-field"
          >
            {targetOptions.map((option) => (
              <option key={option.id} value={option.id}>
                {option.target_column} ({option.dataset_name})
              </option>
            ))}
          </select>
          {selectedTargetColumn && (
            <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
              Showing analytics for target <span className="font-semibold text-gray-900 dark:text-white">{selectedTargetColumn}</span> from dataset <span className="font-semibold text-gray-900 dark:text-white">{selectedDatasetName}</span>.
            </p>
          )}
        </motion.div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            icon={<Database className="w-8 h-8" />}
            title="Total Rows"
            value={stats.basic_info.total_rows.toLocaleString()}
            color="blue"
          />
          <StatCard
            icon={<Activity className="w-8 h-8" />}
            title="Total Columns"
            value={stats.basic_info.total_columns.toString()}
            color="green"
          />
          <StatCard
            icon={<TrendingUp className="w-8 h-8" />}
            title="Duplicates"
            value={stats.basic_info.duplicates.toString()}
            color="purple"
          />
          <StatCard
            icon={<Database className="w-8 h-8" />}
            title="Memory Usage"
            value={`${stats.basic_info.memory_usage.toFixed(2)} MB`}
            color="orange"
          />
        </div>

        {/* Data Preview Table */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card"
        >
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
            Data Preview
          </h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead className="bg-gray-50 dark:bg-gray-800">
                <tr>
                  {columns.slice(0, 6).map((col) => (
                    <th
                      key={col}
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                    >
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
                {preview.map((row, idx) => (
                  <tr key={idx}>
                    {columns.slice(0, 6).map((col) => (
                      <td
                        key={col}
                        className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
                      >
                        {String(row[col]).slice(0, 50)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>

        {/* Missing Values Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
            Missing Values Analysis
          </h2>
          <div className="h-64">
            {Object.keys(stats.missing_values).length > 0 && (
              <Bar
                data={{
                  labels: Object.keys(stats.missing_values).slice(0, 10),
                  datasets: [
                    {
                      label: 'Missing Values',
                      data: Object.values(stats.missing_values).slice(0, 10),
                      backgroundColor: 'rgba(239, 68, 68, 0.6)',
                      borderColor: 'rgba(239, 68, 68, 1)',
                      borderWidth: 1,
                    },
                  ],
                }}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      display: false,
                    },
                  },
                  scales: {
                    y: {
                      beginAtZero: true,
                    },
                  },
                }}
              />
            )}
          </div>
        </motion.div>

        {/* Column Type Distribution */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
            Column Type Distribution
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
                Data Types
              </h3>
              <div className="space-y-2">
                {Object.entries(
                  ((Object.values(stats.column_types) as any[]).reduce((acc: any, type: any) => {
                    acc[type] = (acc[type] || 0) + 1
                    return acc
                  }, {}) as Record<string, number>)
                ).map(([type, count]: [string, number]) => (
                  <div key={type} className="flex items-center justify-between">
                    <span className="text-gray-700 dark:text-gray-300">{type}</span>
                    <span className="font-semibold text-gray-900 dark:text-white">{count}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="h-48">
              <Doughnut
                data={{
                  labels: Object.keys(
                    ((Object.values(stats.column_types) as any[]).reduce((acc: any, type: any) => {
                      acc[type] = (acc[type] || 0) + 1
                      return acc
                    }, {}) as Record<string, number>)
                  ),
                  datasets: [
                    {
                      data: Object.values(
                        ((Object.values(stats.column_types) as any[]).reduce((acc: any, type: any) => {
                          acc[type] = (acc[type] || 0) + 1
                          return acc
                        }, {}) as Record<string, number>)
                      ),
                      backgroundColor: [
                        'rgba(59, 130, 246, 0.6)',
                        'rgba(168, 85, 247, 0.6)',
                        'rgba(34, 197, 94, 0.6)',
                        'rgba(249, 115, 22, 0.6)',
                      ],
                      borderWidth: 2,
                    },
                  ],
                }}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                }}
              />
            </div>
          </div>
        </motion.div>
      </div>
    </Layout>
  )
}

interface StatCardProps {
  icon: ReactNode
  title: string
  value: string
  color: 'blue' | 'green' | 'purple' | 'orange'
}

function StatCard({ icon, title, value, color }: StatCardProps) {
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
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {value}
          </p>
        </div>
        <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${colorClasses[color as keyof typeof colorClasses]} flex items-center justify-center text-white`}>
          {icon}
        </div>
      </div>
    </motion.div>
  )
}
