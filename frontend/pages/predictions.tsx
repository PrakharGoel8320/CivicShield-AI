import { useState, useEffect } from 'react'
import Layout from '../components/Layout'
import { motion } from 'framer-motion'
import axios from 'axios'
import { Target, Loader, CheckCircle2, AlertCircle } from 'lucide-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Predictions() {
  const [targetOptions, setTargetOptions] = useState<any[]>([])
  const [trainedModels, setTrainedModels] = useState<any[]>([])
  const [selectedTargetOptionId, setSelectedTargetOptionId] = useState('')
  const [selectedDatasetName, setSelectedDatasetName] = useState('')
  const [targetColumn, setTargetColumn] = useState('')
  const [columns, setColumns] = useState<string[]>([])
  const [inputData, setInputData] = useState<Record<string, any>>({})
  const [selectedModelId, setSelectedModelId] = useState('')
  const [predicting, setPredicting] = useState(false)
  const [prediction, setPrediction] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    initializePredictions()
  }, [])

  const initializePredictions = async () => {
    try {
      const [optionsResponse, modelsResponse] = await Promise.all([
        axios.get(`${API_URL}/api/ml/target-options`),
        axios.get(`${API_URL}/api/ml/trained-models`),
      ])

      const options = optionsResponse.data.target_options || []
      const models = modelsResponse.data.models || []

      setTargetOptions(options)
      setTrainedModels(models)

      if (options.length > 0) {
        handleTargetOptionChange(options[0].id, options, models)
      } else {
        setError('No target options found. Upload datasets first on the Upload page.')
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Unable to load targets/models. Please upload data and train models first.')
    }
  }

  const getModelsForTarget = (target: string, dataset: string, modelsOverride?: any[]) => {
    const modelList = modelsOverride || trainedModels
    return modelList.filter((m) => m.target_column === target && m.dataset_name === dataset)
  }

  const setupInputs = (featureColumns: string[], target: string, modelMeta?: any) => {
    setColumns(featureColumns)
    setTargetColumn(target)

    const initial: Record<string, any> = {}
    featureColumns.forEach((col) => {
      const median = modelMeta?.feature_stats?.[col]?.median
      initial[col] = typeof median === 'number' ? Number(median.toFixed(3)) : ''
    })
    setInputData(initial)
  }

  const handleTargetOptionChange = (optionId: string, optionsOverride?: any[], modelsOverride?: any[]) => {
    const options = optionsOverride || targetOptions
    const selectedOption = options.find((option) => option.id === optionId)

    setSelectedTargetOptionId(optionId)
    setPrediction(null)
    setError(null)

    if (!selectedOption) {
      setSelectedDatasetName('')
      setTargetColumn('')
      setSelectedModelId('')
      setColumns([])
      setInputData({})
      return
    }

    const datasetName = selectedOption.dataset_name
    const target = selectedOption.target_column
    const recommendedFeatures = selectedOption.feature_columns || []

    setSelectedDatasetName(datasetName)
    setTargetColumn(target)

    const matchingModels = getModelsForTarget(target, datasetName, modelsOverride)

    if (matchingModels.length > 0) {
      const firstModel = matchingModels[0]
      setSelectedModelId(firstModel.model_id)
      setupInputs(firstModel.feature_columns || recommendedFeatures, firstModel.target_column || target, firstModel)
    } else {
      setSelectedModelId('')
      setupInputs(recommendedFeatures, target)
      setError('No trained model found for this target yet. Train models for this target first.')
    }
  }

  const handleModelChange = (modelId: string) => {
    setSelectedModelId(modelId)
    setPrediction(null)
    setError(null)

    const model = trainedModels.find(
      (m) => m.model_id === modelId && m.target_column === targetColumn && m.dataset_name === selectedDatasetName
    )

    if (model) {
      setupInputs(model.feature_columns || [], model.target_column || targetColumn, model)
    }
  }

  const filteredModels = trainedModels.filter(
    (m) => m.target_column === targetColumn && m.dataset_name === selectedDatasetName
  )

  const handlePredict = async () => {
    if (!selectedModelId) {
      setError('Please select a trained model')
      return
    }

    const missingColumns = columns.filter((col) => inputData[col] === '' || inputData[col] === null || Number.isNaN(inputData[col]))
    if (missingColumns.length > 0) {
      setError(`Please enter valid numeric values for: ${missingColumns.join(', ')}`)
      return
    }

    setPredicting(true)
    setError(null)

    try {
      const response = await axios.post(`${API_URL}/api/ml/predict`, {
        model_id: selectedModelId,
        input_data: inputData,
      })

      setPrediction(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to make prediction')
    } finally {
      setPredicting(false)
    }
  }

  const handleInputChange = (column: string, value: string) => {
    setInputData({
      ...inputData,
      [column]: value === '' ? '' : parseFloat(value),
    })
  }

  const selectedModelMeta = filteredModels.find((m) => m.model_id === selectedModelId)

  return (
    <Layout>
      <div className="max-w-4xl mx-auto space-y-6">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="card">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Select Target</h2>
          <select
            value={selectedTargetOptionId}
            onChange={(e) => handleTargetOptionChange(e.target.value)}
            className="input-field"
          >
            <option value="">Select target column...</option>
            {targetOptions.map((option) => (
              <option key={option.id} value={option.id}>
                {option.target_column} ({option.dataset_name})
              </option>
            ))}
          </select>
          {selectedDatasetName && targetColumn && (
            <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
              Predicting target <span className="font-semibold text-gray-900 dark:text-white">{targetColumn}</span> from dataset{' '}
              <span className="font-semibold text-gray-900 dark:text-white">{selectedDatasetName}</span>.
            </p>
          )}
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="card">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Select Model</h2>
          {filteredModels.length === 0 && (
            <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg mb-4">
              <p className="text-yellow-700 dark:text-yellow-300 text-sm">
                No trained model available for the selected target. Go to Train Models page and train this target first.
              </p>
            </div>
          )}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {filteredModels.map((model) => (
              <label
                key={model.model_id}
                className={`flex items-center p-4 rounded-lg cursor-pointer transition-all ${
                  selectedModelId === model.model_id
                    ? 'bg-primary-100 dark:bg-primary-900/30 border-2 border-primary-500'
                    : 'bg-gray-50 dark:bg-gray-800 border-2 border-transparent hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                <input
                  type="radio"
                  name="model"
                  value={model.model_id}
                  checked={selectedModelId === model.model_id}
                  onChange={(e) => handleModelChange(e.target.value)}
                  className="mr-3"
                />
                <span className="text-sm font-semibold text-gray-900 dark:text-white">
                  {model.name.replace(/_/g, ' ').toUpperCase()}
                </span>
              </label>
            ))}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Input Features</h2>
          {targetColumn && (
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              This model predicts: <span className="font-semibold text-gray-900 dark:text-white">{targetColumn}</span>
            </p>
          )}
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
            Showing only the feature names used during model training.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {columns.map((column) => (
              <div key={column}>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{column}</label>
                <input
                  type="number"
                  step="any"
                  value={inputData[column] ?? ''}
                  onChange={(e) => handleInputChange(column, e.target.value)}
                  className="input-field"
                />
                {selectedModelMeta?.feature_stats?.[column] && (
                  <p className="text-xs text-gray-500 mt-1">
                    Train range: {Number(selectedModelMeta.feature_stats[column].min).toFixed(3)} to{' '}
                    {Number(selectedModelMeta.feature_stats[column].max).toFixed(3)} | suggested median:{' '}
                    {Number(selectedModelMeta.feature_stats[column].median).toFixed(3)}
                  </p>
                )}
              </div>
            ))}
          </div>

          {error && (
            <div className="mt-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg flex items-center space-x-2">
              <AlertCircle className="w-5 h-5 text-red-600" />
              <span className="text-red-600 dark:text-red-400">{error}</span>
            </div>
          )}

          <button
            onClick={handlePredict}
            disabled={predicting || !selectedModelId}
            className="btn-primary w-full mt-6 flex items-center justify-center space-x-2"
          >
            {predicting ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                <span>Predicting...</span>
              </>
            ) : (
              <>
                <Target className="w-5 h-5" />
                <span>Make Prediction</span>
              </>
            )}
          </button>
        </motion.div>

        {prediction && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="card bg-gradient-to-br from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 border-2 border-green-200 dark:border-green-800"
          >
            <div className="flex items-center space-x-3 mb-6">
              <CheckCircle2 className="w-8 h-8 text-green-500" />
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Prediction Result</h2>
            </div>

            <div className="text-center py-6">
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">Predicted Value</p>
              <p className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
                {Array.isArray(prediction.predictions) ? prediction.predictions[0].toFixed(4) : prediction.predictions}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Model: {(filteredModels.find((m) => m.model_id === selectedModelId)?.name || '').replace(/_/g, ' ').toUpperCase()}
              </p>
            </div>

            {prediction.probabilities && (
              <div className="mt-6 p-4 bg-white dark:bg-gray-800 rounded-lg">
                <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Prediction Probabilities</h3>
                <div className="space-y-2">
                  {prediction.probabilities[0].map((prob: number, idx: number) => (
                    <div key={idx} className="flex items-center justify-between">
                      <span className="text-sm text-gray-600 dark:text-gray-400">Class {idx}</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-32 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                          <div className="h-full bg-primary-600" style={{ width: `${prob * 100}%` }}></div>
                        </div>
                        <span className="text-sm font-semibold text-gray-900 dark:text-white">{(prob * 100).toFixed(2)}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {prediction.warnings && prediction.warnings.length > 0 && (
              <div className="mt-6 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                <h3 className="text-sm font-semibold text-yellow-700 dark:text-yellow-300 mb-2">Input Warnings</h3>
                <div className="space-y-1">
                  {prediction.warnings.map((warning: string, idx: number) => (
                    <p key={idx} className="text-sm text-yellow-700 dark:text-yellow-300">{warning}</p>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        )}
      </div>
    </Layout>
  )
}
