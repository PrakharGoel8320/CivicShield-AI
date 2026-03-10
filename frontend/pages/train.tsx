import { useState, useEffect } from 'react'
import type { ReactNode } from 'react'
import Layout from '../components/Layout'
import { motion } from 'framer-motion'
import axios from 'axios'
import { Brain, CheckCircle2, Loader, AlertCircle, TrendingUp } from 'lucide-react'
import { Bar } from 'react-chartjs-2'

const API_URL = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000').replace(/\/+$/, '')

export default function Train() {
  const [targetOptions, setTargetOptions] = useState<any[]>([])
  const [selectedTargetOptionId, setSelectedTargetOptionId] = useState('')
  const [selectedDatasetName, setSelectedDatasetName] = useState('')
  const [targetColumn, setTargetColumn] = useState('')
  const [availableFeatureColumns, setAvailableFeatureColumns] = useState<string[]>([])
  const [featureColumns, setFeatureColumns] = useState<string[]>([])
  const [selectedModels, setSelectedModels] = useState<string[]>(['random_forest'])
  const [training, setTraining] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const availableModels = [
    { id: 'linear_regression', name: 'Linear Regression', type: 'regression' },
    { id: 'random_forest', name: 'Random Forest', type: 'both' },
    { id: 'decision_tree', name: 'Decision Tree', type: 'both' },
    { id: 'gradient_boosting', name: 'Gradient Boosting', type: 'both' },
    { id: 'svm', name: 'Support Vector Machine', type: 'both' },
  ]

  const handleTargetOptionChange = (optionId: string) => {
    setSelectedTargetOptionId(optionId)
    const selectedOption = targetOptions.find((option) => option.id === optionId)

    if (!selectedOption) {
      setSelectedDatasetName('')
      setTargetColumn('')
      setAvailableFeatureColumns([])
      setFeatureColumns([])
      return
    }

    setSelectedDatasetName(selectedOption.dataset_name)
    setTargetColumn(selectedOption.target_column)
    const mappedFeatures = selectedOption.feature_columns || []
    setAvailableFeatureColumns(mappedFeatures)
    setFeatureColumns(mappedFeatures)
  }

  useEffect(() => {
    fetchTargetOptions()
  }, [])

  const fetchTargetOptions = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/ml/target-options`)
      const options = response.data.target_options || []
      setTargetOptions(options)

      // Preselect first available option for faster workflow.
      if (options.length > 0) {
        handleTargetOptionChange(options[0].id)
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'No uploaded datasets found. Upload one or more CSV files first.')
    }
  }

  const handleTrain = async () => {
    if (!targetColumn || featureColumns.length === 0) {
      setError('Please select target and feature columns')
      return
    }

    setTraining(true)
    setError(null)

    try {
      const response = await axios.post(`${API_URL}/api/ml/train`, {
        dataset_name: selectedDatasetName,
        target_column: targetColumn,
        feature_columns: featureColumns,
        model_types: selectedModels,
        test_size: 0.2,
      })

      setResults(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to train models')
    } finally {
      setTraining(false)
    }
  }

  const toggleFeatureColumn = (col: string) => {
    if (featureColumns.includes(col)) {
      setFeatureColumns(featureColumns.filter((c) => c !== col))
    } else {
      setFeatureColumns([...featureColumns, col])
    }
  }

  const toggleModel = (modelId: string) => {
    if (selectedModels.includes(modelId)) {
      setSelectedModels(selectedModels.filter((m) => m !== modelId))
    } else {
      setSelectedModels([...selectedModels, modelId])
    }
  }

  return (
    <Layout>
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Configuration */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card"
        >
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Configure ML Training
          </h2>

          {/* Target Column Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Target Column (What to predict)
            </label>
            <select
              value={selectedTargetOptionId}
              onChange={(e) => handleTargetOptionChange(e.target.value)}
              className="input-field"
            >
              <option value="">Select target column from uploaded files...</option>
              {targetOptions.map((option) => (
                <option key={option.id} value={option.id}>
                  {option.target_column} ({option.dataset_name})
                </option>
              ))}
            </select>
            {targetOptions.length === 0 && (
              <p className="mt-2 text-xs text-amber-700 dark:text-amber-400">
                No target options available yet. Upload one or more supported training datasets first.
              </p>
            )}
            {selectedDatasetName && (
              <p className="mt-2 text-xs text-gray-600 dark:text-gray-400">
                Training dataset: <span className="font-semibold">{selectedDatasetName}</span>
              </p>
            )}
          </div>

          {/* Feature Columns Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Feature Columns (Input variables)
            </label>
            {targetColumn && featureColumns.length > 0 && (
              <div className="mb-3 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
                <p className="text-sm text-blue-700 dark:text-blue-300">
                  Recommended features for <strong>{targetColumn}</strong> are pre-selected below
                </p>
              </div>
            )}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
              {availableFeatureColumns
                .map((col) => {
                  return (
                    <label
                      key={col}
                      className="flex items-center p-3 rounded-lg cursor-pointer transition bg-green-50 dark:bg-green-900/20 border-2 border-green-300 dark:border-green-700 hover:bg-green-100 dark:hover:bg-green-900/30"
                    >
                      <input
                        type="checkbox"
                        checked={featureColumns.includes(col)}
                        onChange={() => toggleFeatureColumn(col)}
                        className="mr-2"
                      />
                      <span className="text-sm text-gray-900 dark:text-white">
                        {col}
                        <span className="ml-1 text-xs text-green-600 dark:text-green-400">✓</span>
                      </span>
                    </label>
                  )
                })}
            </div>
            {selectedTargetOptionId && availableFeatureColumns.length === 0 && (
              <p className="mt-3 text-xs text-amber-700 dark:text-amber-400">
                No mapped features were found for this target in the selected dataset.
              </p>
            )}
          </div>

          {/* Model Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Select Models to Train
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {availableModels.map((model) => (
                <label
                  key={model.id}
                  className="flex items-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  <input
                    type="checkbox"
                    checked={selectedModels.includes(model.id)}
                    onChange={() => toggleModel(model.id)}
                    className="mr-3"
                  />
                  <div>
                    <p className="text-sm font-semibold text-gray-900 dark:text-white">
                      {model.name}
                    </p>
                    <p className="text-xs text-gray-600 dark:text-gray-400">{model.type}</p>
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg flex items-center space-x-2">
              <AlertCircle className="w-5 h-5 text-red-600" />
              <span className="text-red-600 dark:text-red-400">{error}</span>
            </div>
          )}

          {/* Train Button */}
          <button
            onClick={handleTrain}
            disabled={training || !targetColumn || featureColumns.length === 0 || selectedModels.length === 0}
            className="btn-primary w-full flex items-center justify-center space-x-2"
          >
            {training ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                <span>Training Models...</span>
              </>
            ) : (
              <>
                <Brain className="w-5 h-5" />
                <span>Train Models</span>
              </>
            )}
          </button>
        </motion.div>

        {/* Results */}
        {results && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div className="card">
              <div className="flex items-center space-x-3 mb-6">
                <CheckCircle2 className="w-8 h-8 text-green-500" />
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                  Training Complete!
                </h2>
              </div>

              {/* Model Results */}
              <div className="space-y-4">
                {results.models.map((model: any, idx: number) => (
                  <div
                    key={idx}
                    className="p-6 bg-gray-50 dark:bg-gray-800 rounded-lg"
                  >
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                      {model.name.replace(/_/g, ' ').toUpperCase()}
                    </h3>

                    {/* Metrics */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                      {Object.entries(model.metrics).map(([key, value]: [string, any]) => (
                        <div key={key} className="text-center">
                          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                            {key.toUpperCase()}
                          </p>
                          <p className="text-xl font-bold text-gray-900 dark:text-white">
                            {typeof value === 'number' ? value.toFixed(4) : value}
                          </p>
                        </div>
                      ))}
                    </div>

                    {/* Feature Importance */}
                    {model.feature_importance && Object.keys(model.feature_importance).length > 0 && (
                      <div className="mt-4">
                        <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                          Feature Importance
                        </h4>
                        <div className="h-48">
                          <Bar
                            data={{
                              labels: Object.keys(model.feature_importance).slice(0, 10),
                              datasets: [
                                {
                                  label: 'Importance',
                                  data: Object.values(model.feature_importance).slice(0, 10),
                                  backgroundColor: 'rgba(59, 130, 246, 0.6)',
                                  borderColor: 'rgba(59, 130, 246, 1)',
                                  borderWidth: 1,
                                },
                              ],
                            }}
                            options={{
                              responsive: true,
                              maintainAspectRatio: false,
                              indexAxis: 'y',
                              plugins: {
                                legend: {
                                  display: false,
                                },
                              },
                            }}
                          />
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* Next Steps */}
              <div className="mt-6">
                <a
                  href="/predictions"
                  className="btn-primary inline-flex items-center space-x-2"
                >
                  <TrendingUp className="w-5 h-5" />
                  <span>Make Predictions</span>
                </a>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </Layout>
  )
}
