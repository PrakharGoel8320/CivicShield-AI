import { useState } from 'react'
import type { ReactNode } from 'react'
import Layout from '../components/Layout'
import { motion } from 'framer-motion'
import axios from 'axios'
import { Upload as UploadIcon, FileText, CheckCircle2, AlertCircle, Loader } from 'lucide-react'

const API_URL = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000').replace(/\/+$/, '')

export default function Upload() {
  const [files, setFiles] = useState<File[]>([])
  const [uploading, setUploading] = useState(false)
  const [uploadComplete, setUploadComplete] = useState(false)
  const [uploadedResults, setUploadedResults] = useState<any[]>([])
  const [availableDatasets, setAvailableDatasets] = useState<any[]>([])
  const [error, setError] = useState<string | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFiles = Array.from(e.target.files)
      setFiles(selectedFiles)
      setError(null)
      setUploadComplete(false)
      setUploadedResults([])
    }
  }

  const fetchAvailableDatasets = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/datasets`)
      setAvailableDatasets(response.data.datasets || [])
    } catch {
      setAvailableDatasets([])
    }
  }

  const handleUpload = async () => {
    if (files.length === 0) {
      setError('Please select one or more files first')
      return
    }

    setUploading(true)
    setError(null)

    try {
      const responses = []
      for (const file of files) {
        const formData = new FormData()
        formData.append('file', file)

        const response = await axios.post(`${API_URL}/api/upload`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        responses.push(response.data)
      }

      setUploadedResults(responses)
      setUploadComplete(true)
      fetchAvailableDatasets()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload file')
    } finally {
      setUploading(false)
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    const droppedFiles = Array.from(e.dataTransfer.files)
    const validFiles = droppedFiles.filter(
      (f) => f.name.endsWith('.csv') || f.name.endsWith('.xlsx') || f.name.endsWith('.xls')
    )

    if (validFiles.length > 0) {
      setFiles(validFiles)
      setError(null)
      setUploadComplete(false)
      setUploadedResults([])
    } else {
      setError('Please drop CSV or Excel files')
    }
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Upload Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card"
        >
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Upload Dataset
          </h2>

          {/* Drag and Drop Area */}
          <div
            onDragOver={handleDragOver}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-xl p-12 text-center transition-colors ${
              files.length > 0
                ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                : 'border-gray-300 dark:border-gray-600 hover:border-primary-400'
            }`}
          >
            <div className="flex flex-col items-center">
              <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full flex items-center justify-center mb-4">
                <UploadIcon className="w-8 h-8 text-primary-600" />
              </div>

              {files.length > 0 ? (
                <div className="space-y-2">
                  <div className="flex items-center justify-center space-x-2 text-primary-600">
                    <FileText className="w-5 h-5" />
                    <span className="font-semibold">{files.length} file(s) selected</span>
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400 max-h-24 overflow-auto">
                    {files.map((file) => (
                      <p key={file.name}>{file.name}</p>
                    ))}
                  </div>
                </div>
              ) : (
                <>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    Drop your file here or click to browse
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    Supports CSV and Excel files
                  </p>
                </>
              )}

              <input
                type="file"
                accept=".csv,.xlsx,.xls"
                multiple
                onChange={handleFileChange}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="btn-primary cursor-pointer mt-4"
              >
                Select File
              </label>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg flex items-center space-x-2"
            >
              <AlertCircle className="w-5 h-5 text-red-600" />
              <span className="text-red-600 dark:text-red-400">{error}</span>
            </motion.div>
          )}

          {/* Upload Button */}
          {files.length > 0 && !uploadComplete && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-6"
            >
              <button
                onClick={handleUpload}
                disabled={uploading}
                className="btn-primary w-full flex items-center justify-center space-x-2"
              >
                {uploading ? (
                  <>
                    <Loader className="w-5 h-5 animate-spin" />
                    <span>Uploading...</span>
                  </>
                ) : (
                  <>
                    <UploadIcon className="w-5 h-5" />
                    <span>Upload Selected Files</span>
                  </>
                )}
              </button>
            </motion.div>
          )}
        </motion.div>

        {/* Upload Success */}
        {uploadComplete && uploadedResults.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card"
          >
            <div className="flex items-center space-x-3 mb-6">
              <CheckCircle2 className="w-8 h-8 text-green-500" />
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                Upload Successful!
              </h2>
            </div>

            <div className="mb-6 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
              <p className="text-sm text-green-700 dark:text-green-300">
                Uploaded {uploadedResults.length} file(s). All uploaded datasets are now available for training target selection.
              </p>
              <p className="text-xs text-green-700/80 dark:text-green-300/80 mt-1">
                Total datasets available in this session: {availableDatasets.length}
              </p>
            </div>

            {/* Dataset Info */}
            <div className="space-y-3 mb-6">
              {uploadedResults.map((datasetInfo) => (
                <div key={datasetInfo.dataset_name || datasetInfo.filename} className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                  <p className="font-semibold text-gray-900 dark:text-white mb-2">{datasetInfo.dataset_name || datasetInfo.filename}</p>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Rows</p>
                      <p className="font-bold text-gray-900 dark:text-white">{datasetInfo.rows.toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Columns</p>
                      <p className="font-bold text-gray-900 dark:text-white">{datasetInfo.columns}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Missing</p>
                      <p className="font-bold text-gray-900 dark:text-white">
                        {(Object.values(datasetInfo.missing_values) as any[]).reduce((a: any, b: any) => a + b, 0) as number}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Data Preview */}
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Last Uploaded Dataset Preview
            </h3>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-800">
                  <tr>
                    {uploadedResults[uploadedResults.length - 1].column_names.slice(0, 5).map((col: string) => (
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
                  {uploadedResults[uploadedResults.length - 1].preview.slice(0, 5).map((row: any, idx: number) => (
                    <tr key={idx}>
                      {uploadedResults[uploadedResults.length - 1].column_names.slice(0, 5).map((col: string) => (
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

            {/* Next Steps */}
            <div className="mt-6 space-y-3">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Next Steps
              </h3>
              <a
                href="/analytics"
                className="block p-4 bg-gray-50 dark:bg-gray-800 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <p className="font-semibold text-gray-900 dark:text-white">View Analytics</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Explore your data with visualizations and statistics
                </p>
              </a>
              <a
                href="/train"
                className="block p-4 bg-gray-50 dark:bg-gray-800 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <p className="font-semibold text-gray-900 dark:text-white">Train ML Models</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Start training machine learning models on your data
                </p>
              </a>
            </div>
          </motion.div>
        )}
      </div>
    </Layout>
  )
}
