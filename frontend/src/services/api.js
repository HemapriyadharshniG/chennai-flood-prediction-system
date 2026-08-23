import axios from 'axios';

/**
 * Axios API client instance for Chennai Flood Prediction backend services.
 */
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Fetch list of Chennai zones with risk assessments and metadata
 * @returns {Promise<Array>} List of zones
 */
export async function fetchZones() {
  const response = await apiClient.get('/api/zones');
  return response.data;
}

/**
 * Fetch current real-time rainfall data across weather stations in Chennai
 * @returns {Promise<Object>} Current rainfall observation data
 */
export async function fetchCurrentRainfall() {
  const response = await apiClient.get('/api/rainfall/current');
  return response.data;
}

/**
 * Fetch street-level flood vulnerability and spatial data
 * @returns {Promise<Array>} List of street features with inundation indicators
 */
export async function fetchStreets() {
  const response = await apiClient.get('/api/streets');
  return response.data;
}

/**
 * Fetch historical flood/rainfall records for a specific zone
 * @param {string|number} zoneId - Identifier for the target zone
 * @returns {Promise<Array>} Historical flood records
 */
export async function fetchHistory(zoneId) {
  const response = await apiClient.get(`/api/history/${zoneId}`);
  return response.data;
}

/**
 * Submit simulation or custom rainfall parameters to predict flood risks
 * @param {Object} payload - Prediction parameters (e.g. rainfall_mm, duration_hours, zone_id)
 * @returns {Promise<Object>} Predicted flood risk calculation and depth
 */
export async function submitPrediction(payload) {
  const response = await apiClient.post('/api/predict', payload);
  return response.data;
}

export default apiClient;
