/**
 * AgroScore 360 — Root App
 * Manages global state: language, farmer data, stats, loading.
 */
import React, { useState, useEffect, createContext, useContext } from 'react'
import Dashboard from './components/Dashboard.jsx'
import { useTranslation } from './i18n/translations.js'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/$/, '')

// ── Language Context ────────────────────────────────────────────────────────
export const LangContext = createContext({ lang: 'ru', t: (k) => k, setLang: () => {} })
export const useLang = () => useContext(LangContext)

// ── Data Context ─────────────────────────────────────────────────────────────
export const DataContext = createContext({ farmers: [], stats: {}, loading: true, error: null })
export const useData = () => useContext(DataContext)

export default function App() {
  const [lang, setLang] = useState('ru')
  const t = useTranslation(lang)

  const [farmers, setFarmers]   = useState([])
  const [stats,   setStats]     = useState({})
  const [loading, setLoading]   = useState(true)
  const [error,   setError]     = useState(null)

  useEffect(() => {
    const controller = new AbortController()
    setLoading(true)
    setError(null)

    Promise.all([
      fetch(`${API_BASE_URL}/farmers`, { signal: controller.signal }).then(r => r.json()),
      fetch(`${API_BASE_URL}/stats`,   { signal: controller.signal }).then(r => r.json()),
    ])
      .then(([farmersData, statsData]) => {
        setFarmers(farmersData)
        setStats(statsData)
        setLoading(false)
      })
      .catch(err => {
        if (err.name !== 'AbortError') {
          setError(err.message)
          setLoading(false)
        }
      })

    return () => controller.abort()
  }, [])

  return (
    <LangContext.Provider value={{ lang, t, setLang }}>
      <DataContext.Provider value={{ farmers, stats, loading, error }}>
        <Dashboard />
      </DataContext.Provider>
    </LangContext.Provider>
  )
}
