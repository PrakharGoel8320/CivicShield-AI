import { useState, useEffect } from 'react'
import Layout from '../components/Layout'
import { motion } from 'framer-motion'
import axios from 'axios'
import dynamic from 'next/dynamic'
import { MapPin, Loader, AlertCircle } from 'lucide-react'

const API_URL = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000').replace(/\/+$/, '')

// Dynamically import Leaflet components (client-side only)
const MapContainer = dynamic(
  () => import('react-leaflet').then((mod) => mod.MapContainer),
  { ssr: false }
) as any
const TileLayer = dynamic(
  () => import('react-leaflet').then((mod) => mod.TileLayer),
  { ssr: false }
) as any
const Marker = dynamic(
  () => import('react-leaflet').then((mod) => mod.Marker),
  { ssr: false }
) as any
const Popup = dynamic(
  () => import('react-leaflet').then((mod) => mod.Popup),
  { ssr: false }
) as any

export default function MapView() {
  const [loading, setLoading] = useState(true)
  const [mapData, setMapData] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const [center, setCenter] = useState<[number, number]>([37.7749, -122.4194])
  const [targetOptions, setTargetOptions] = useState<any[]>([])
  const [selectedTargetOptionId, setSelectedTargetOptionId] = useState('')
  const [selectedDatasetName, setSelectedDatasetName] = useState('')
  const [selectedTargetColumn, setSelectedTargetColumn] = useState('')

  useEffect(() => {
    initializeMap()
  }, [])

  const initializeMap = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/ml/target-options`)
      const options = response.data.target_options || []
      setTargetOptions(options)

      if (options.length > 0) {
        await handleTargetOptionChange(options[0].id, options)
      } else {
        setError('No target options found. Upload datasets first.')
        setLoading(false)
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load target options')
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
      setMapData(null)
      return
    }

    setSelectedDatasetName(selectedOption.dataset_name)
    setSelectedTargetColumn(selectedOption.target_column)
    await fetchMapData(selectedOption.dataset_name)
  }

  const fetchMapData = async (datasetName: string) => {
    try {
      setLoading(true)
      setError(null)
      const response = await axios.get(`${API_URL}/api/map/data`, {
        params: { dataset_name: datasetName }
      })
      setMapData(response.data)

      // Calculate center from data
      if (response.data.data.length > 0) {
        const lats = response.data.data.map((point: any) => point[response.data.lat_column])
        const lons = response.data.data.map((point: any) => point[response.data.lon_column])
        const avgLat = lats.reduce((a: number, b: number) => a + b, 0) / lats.length
        const avgLon = lons.reduce((a: number, b: number) => a + b, 0) / lons.length
        setCenter([avgLat, avgLon])
      }
    } catch (err: any) {
      setMapData(null)
      setError(err.response?.data?.detail || 'Failed to load map data')
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
            <p className="text-gray-600 dark:text-gray-400">Loading map data...</p>
          </div>
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
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Map Target Selection</h2>
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
          {selectedDatasetName && selectedTargetColumn && (
            <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
              Showing map context for target <span className="font-semibold text-gray-900 dark:text-white">{selectedTargetColumn}</span> in dataset <span className="font-semibold text-gray-900 dark:text-white">{selectedDatasetName}</span>.
            </p>
          )}
        </motion.div>

        {error || !mapData ? (
          <div className="card text-center py-12">
            <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              {error || 'No Map Data Available'}
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              The selected dataset needs latitude and longitude columns for map visualization.
            </p>
            <a href="/upload" className="btn-primary inline-block">
              Upload New Dataset
            </a>
          </div>
        ) : (
          <>
        {/* Map Info */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card"
        >
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                Geographical Visualization
              </h2>
              <p className="text-gray-600 dark:text-gray-400">
                Showing {mapData.data.length} of {mapData.total_points} locations
              </p>
            </div>
            <div className="flex items-center space-x-2 px-4 py-2 bg-primary-100 dark:bg-primary-900/30 rounded-lg">
              <MapPin className="w-5 h-5 text-primary-600" />
              <span className="font-semibold text-primary-600">
                {mapData.total_points.toLocaleString()} Points
              </span>
            </div>
          </div>
        </motion.div>

        {/* Map */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <div className="h-[600px] rounded-lg overflow-hidden">
            {typeof window !== 'undefined' && (
              <MapContainer
                center={center}
                zoom={10}
                style={{ height: '100%', width: '100%' }}
              >
                <TileLayer
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {mapData.data.map((point: any, idx: number) => {
                  const lat = point[mapData.lat_column]
                  const lon = point[mapData.lon_column]
                  
                  if (lat && lon && !isNaN(lat) && !isNaN(lon)) {
                    return (
                      <Marker key={idx} position={[lat, lon]}>
                        <Popup>
                          <div className="p-2">
                            <p className="font-semibold mb-2">Location {idx + 1}</p>
                            {Object.entries(point)
                              .slice(0, 5)
                              .map(([key, value]: [string, any]) => (
                                <p key={key} className="text-sm">
                                  <strong>{key}:</strong> {String(value).slice(0, 50)}
                                </p>
                              ))}
                          </div>
                        </Popup>
                      </Marker>
                    )
                  }
                  return null
                })}
              </MapContainer>
            )}
          </div>
        </motion.div>

        {/* Map Statistics */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          <div className="card">
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
              Total Locations
            </h3>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">
              {mapData.total_points.toLocaleString()}
            </p>
          </div>
          <div className="card">
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
              Displayed Points
            </h3>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">
              {mapData.data.length}
            </p>
          </div>
          <div className="card">
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
              Coordinates
            </h3>
            <p className="text-sm text-gray-900 dark:text-white">
              <strong>Lat:</strong> {mapData.lat_column}
              <br />
              <strong>Lon:</strong> {mapData.lon_column}
            </p>
          </div>
        </motion.div>
          </>
        )}
      </div>
    </Layout>
  )
}
