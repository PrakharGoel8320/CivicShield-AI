import { useState, useEffect } from 'react'
import type { ReactNode } from 'react'
import Layout from '../components/Layout'
import { motion } from 'framer-motion'
import axios from 'axios'
import dynamic from 'next/dynamic'
import { Bar } from 'react-chartjs-2'
import { BarChart3, Loader, TrendingUp } from 'lucide-react'

// @ts-ignore - react-plotly.js doesn't have type definitions
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false }) as any

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Visualizations() {
  const [loading, setLoading] = useState(true)
  const [correlation, setCorrelation] = useState<any>(null)
  const [columns, setColumns] = useState<string[]>([])
  const [selectedColumn, setSelectedColumn] = useState<string>('')
  const [distributionData, setDistributionData] = useState<any>(null)
  const [targetOptions, setTargetOptions] = useState<any[]>([])
  const [selectedTargetOptionId, setSelectedTargetOptionId] = useState('')
  const [selectedDatasetName, setSelectedDatasetName] = useState('')
  const [selectedTargetColumn, setSelectedTargetColumn] = useState('')

  useEffect(() => {
    initializeVisualizations()
  }, [])

  useEffect(() => {
    if (selectedColumn) {
      fetchDistribution(selectedColumn)
    }
  }, [selectedColumn])

  const initializeVisualizations = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/ml/target-options`)
      const options = response.data.target_options || []
      setTargetOptions(options)

      if (options.length > 0) {
        await handleTargetOptionChange(options[0].id, options)
      } else {
        setCorrelation(null)
        setLoading(false)
      }
    } catch (error) {
      console.error('Error loading target options:', error)
      setCorrelation(null)
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
      setCorrelation(null)
      return
    }

    setSelectedDatasetName(selectedOption.dataset_name)
    setSelectedTargetColumn(selectedOption.target_column)
    await fetchCorrelation(selectedOption.dataset_name)
  }

  const fetchCorrelation = async (datasetName: string) => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_URL}/api/visualization/correlation`, {
        params: { dataset_name: datasetName }
      })
      setCorrelation(response.data)
      setColumns(response.data.columns)
      if (response.data.columns.length > 0) {
        setSelectedColumn(response.data.columns[0])
      }
    } catch (error) {
      console.error('Error fetching correlation:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchDistribution = async (column: string) => {
    try {
      const response = await axios.get(`${API_URL}/api/visualization/distribution/${column}`, {
        params: { dataset_name: selectedDatasetName }
      })
      setDistributionData(response.data)
    } catch (error) {
      console.error('Error fetching distribution:', error)
    }
  }

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <Loader className="w-12 h-12 text-primary-600 animate-spin mx-auto mb-4" />
            <p className="text-gray-600 dark:text-gray-400">Loading visualizations...</p>
          </div>
        </div>
      </Layout>
    )
  }

  if (!correlation) {
    return (
      <Layout>
        <div className="card text-center py-12">
          <BarChart3 className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            No Data Available
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Upload a dataset to view visualizations
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
            Visualization Target Selection
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
              Showing visualizations for target <span className="font-semibold text-gray-900 dark:text-white">{selectedTargetColumn}</span> from dataset <span className="font-semibold text-gray-900 dark:text-white">{selectedDatasetName}</span>.
            </p>
          )}
        </motion.div>

        {/* Correlation Heatmap */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card"
        >
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Correlation Heatmap
          </h2>
          <div className="h-96 overflow-auto">
            <Plot
              data={[
                {
                  z: Object.values(correlation.correlation).map((col: any) =>
                    Object.values(col)
                  ),
                  x: columns,
                  y: columns,
                  type: 'heatmap',
                  colorscale: 'RdBu',
                  zmid: 0,
                },
              ]}
              layout={{
                autosize: true,
                height: 600,
                xaxis: { title: 'Features' },
                yaxis: { title: 'Features' },
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
              }}
              style={{ width: '100%', height: '100%' }}
              config={{ responsive: true }}
            />
          </div>
        </motion.div>

        {/* Distribution Analysis */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              Distribution Analysis
            </h2>
            <select
              value={selectedColumn}
              onChange={(e) => setSelectedColumn(e.target.value)}
              className="input-field max-w-xs"
            >
              {columns.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
          </div>

          {distributionData && (
            <div className="h-96">
              {distributionData.type === 'numerical' ? (
                <Bar
                  data={{
                    labels: distributionData.bins
                      .slice(0, -1)
                      .map((bin: number, idx: number) =>
                        `${bin.toFixed(2)} - ${distributionData.bins[idx + 1].toFixed(2)}`
                      ),
                    datasets: [
                      {
                        label: 'Frequency',
                        data: distributionData.hist,
                        backgroundColor: 'rgba(59, 130, 246, 0.6)',
                        borderColor: 'rgba(59, 130, 246, 1)',
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
                      title: {
                        display: true,
                        text: `Distribution of ${selectedColumn}`,
                      },
                    },
                  }}
                />
              ) : (
                <Bar
                  data={{
                    labels: distributionData.categories,
                    datasets: [
                      {
                        label: 'Count',
                        data: distributionData.counts,
                        backgroundColor: 'rgba(168, 85, 247, 0.6)',
                        borderColor: 'rgba(168, 85, 247, 1)',
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
                      title: {
                        display: true,
                        text: `Distribution of ${selectedColumn}`,
                      },
                    },
                  }}
                />
              )}
            </div>
          )}

          {/* Statistics */}
          {distributionData?.stats && (
            <div className="mt-6 grid grid-cols-2 md:grid-cols-5 gap-4">
              {Object.entries(distributionData.stats).map(([key, value]: [string, any]) => (
                <div
                  key={key}
                  className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg text-center"
                >
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                    {key.toUpperCase()}
                  </p>
                  <p className="text-xl font-bold text-gray-900 dark:text-white">
                    {typeof value === 'number' ? value.toFixed(2) : value}
                  </p>
                </div>
              ))}
            </div>
          )}
        </motion.div>

        {/* Scatter Plot Matrix (if we have data) */}
        {columns.length >= 2 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="card"
          >
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
              Feature Relationships
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {columns.slice(0, 4).map((col, idx) => (
                <div key={idx} className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                  <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                    Correlation with {col}
                  </h3>
                  <div className="space-y-2">
                    {Object.entries(correlation.correlation[col] || {})
                      .sort(([, a]: any, [, b]: any) => Math.abs(b) - Math.abs(a))
                      .slice(0, 5)
                      .map(([feature, value]: [string, any]) => (
                        <div key={feature} className="flex items-center justify-between">
                          <span className="text-sm text-gray-600 dark:text-gray-400">
                            {feature}
                          </span>
                          <div className="flex items-center space-x-2">
                            <div className="w-24 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                              <div
                                className={`h-full ${
                                  value >= 0 ? 'bg-green-600' : 'bg-red-600'
                                }`}
                                style={{ width: `${Math.abs(value) * 100}%` }}
                              ></div>
                            </div>
                            <span className="text-sm font-semibold text-gray-900 dark:text-white w-12 text-right">
                              {value.toFixed(2)}
                            </span>
                          </div>
                        </div>
                      ))}
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </Layout>
  )
}
