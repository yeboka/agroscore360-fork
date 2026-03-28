/**
 * ShapModal — XAI side-panel that opens when a farmer row is clicked.
 * Renders:
 *   - Farmer metadata (app number, region, subsidy direction)
 *   - Efficiency score ring
 *   - SHAP horizontal bar chart (Recharts) + progress bar fallback
 *   - Engineered feature values with color-coded gauges
 */
import React from 'react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ReferenceLine, ResponsiveContainer, Cell
} from 'recharts'
import { useLang } from '../App.jsx'

// ── Score ring SVG ───────────────────────────────────────────────────────────
function ScoreRing({ score }) {
  const r   = 44
  const c   = 2 * Math.PI * r
  const arc = c * (score / 100)
  const color = score >= 70 ? '#22c55e' : score >= 50 ? '#eab308' : '#ef4444'

  return (
    <svg width="120" height="120" viewBox="0 0 120 120" className="drop-shadow-xl">
      <circle cx="60" cy="60" r={r} fill="none" stroke="#1e293b" strokeWidth="10"/>
      <circle
        cx="60" cy="60" r={r} fill="none"
        stroke={color} strokeWidth="10"
        strokeDasharray={`${arc} ${c}`}
        strokeLinecap="round"
        transform="rotate(-90 60 60)"
        style={{ transition: 'stroke-dasharray 0.8s ease' }}
      />
      <text x="60" y="55" textAnchor="middle" fill="white" fontSize="22" fontWeight="700">
        {score.toFixed(0)}
      </text>
      <text x="60" y="72" textAnchor="middle" fill="#94a3b8" fontSize="11">
        /100
      </text>
    </svg>
  )
}

// ── Feature gauge bar ────────────────────────────────────────────────────────
function FeatureBar({ label, value, min, max, unit = '', invert = false }) {
  const pct   = Math.min(100, Math.max(0, ((value - min) / (max - min)) * 100))
  const good  = invert ? pct < 40 : pct > 60
  const mid   = pct >= 40 && pct <= 60
  const color = good ? 'bg-green-500' : mid ? 'bg-yellow-500' : 'bg-red-500'

  return (
    <div className="space-y-1">
      <div className="flex justify-between items-center text-xs">
        <span className="text-slate-400">{label}</span>
        <span className="font-semibold text-white">{typeof value === 'number' ? value.toFixed(2) : value}{unit}</span>
      </div>
      <div className="w-full h-2 bg-surface-border rounded-full overflow-hidden">
        <div className={`h-full rounded-full transition-all duration-700 ${color}`}
             style={{ width: `${pct}%` }}/>
      </div>
    </div>
  )
}

// ── Custom SHAP Tooltip ──────────────────────────────────────────────────────
function ShapTooltip({ active, payload }) {
  if (!active || !payload?.length) return null
  const d = payload[0]
  return (
    <div className="bg-surface-card border border-surface-border rounded-xl px-3 py-2 text-xs shadow-xl">
      <div className="font-semibold text-white mb-1">{d.payload.label}</div>
      <div className={d.value >= 0 ? 'text-green-400' : 'text-red-400'}>
        SHAP: {d.value >= 0 ? '+' : ''}{d.value.toFixed(4)}
      </div>
    </div>
  )
}

// ── Main Modal ────────────────────────────────────────────────────────────────
export default function ShapModal({ farmer, onClose }) {
  const { t } = useLang()
  if (!farmer) return null

  const shap = farmer.shap_values ?? {}

  // Build chart data from SHAP values, sorted by absolute value
  const shapData = Object.entries(shap)
    .map(([key, val]) => ({ key, label: t(`feat_${key}`), value: val }))
    .sort((a, b) => Math.abs(b.value) - Math.abs(a.value))

  const scoreColor = farmer.efficiency_score >= 70
    ? 'text-green-400' : farmer.efficiency_score >= 50
    ? 'text-yellow-400' : 'text-red-400'

  // Shorten long subsidy name for display
  const shortName = farmer.subsidy_name?.length > 60
    ? farmer.subsidy_name.slice(0, 57) + '…'
    : farmer.subsidy_name

  return (
    /* Backdrop */
    <div
      className="fixed inset-0 z-50 flex justify-end animate-fade-in"
      style={{ background: 'rgba(0,0,0,0.6)', backdropFilter: 'blur(4px)' }}
      onClick={onClose}
    >
      {/* Panel */}
      <div
        className="relative w-full max-w-lg h-full bg-surface-card border-l border-surface-border
                   overflow-y-auto animate-slide-up flex flex-col"
        onClick={e => e.stopPropagation()}
      >
        {/* Header */}
        <div className="sticky top-0 z-10 bg-surface-card/95 backdrop-blur border-b border-surface-border
                        px-6 py-4 flex items-start justify-between gap-3">
          <div>
            <h2 className="font-bold text-white text-lg">{t('xaiTitle')}</h2>
            <p className="text-xs text-slate-400 mt-0.5">{t('xaiSubtitle')}</p>
          </div>
          <button
            onClick={onClose}
            className="flex-shrink-0 p-2 rounded-xl hover:bg-surface-border transition-colors text-slate-400 hover:text-white"
            aria-label="close"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-5 h-5">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        {/* Body */}
        <div className="flex-1 p-6 space-y-6">

          {/* Score + identity */}
          <div className="flex items-center gap-6">
            <ScoreRing score={farmer.efficiency_score}/>
            <div className="min-w-0 flex-1">
              <div className={`text-3xl font-extrabold ${scoreColor}`}>
                {farmer.efficiency_score.toFixed(1)}
              </div>
              <div className="text-xs text-slate-400 mt-0.5 mb-3">{t('efficiencyScore')}</div>
              <div className="space-y-1">
                <p className="text-xs text-slate-500">
                  <span className="text-slate-300 font-medium">{t('appNumber')}:</span>{' '}
                  {farmer.app_number}
                </p>
                <p className="text-xs text-slate-500">
                  <span className="text-slate-300 font-medium">{t('region')}:</span>{' '}
                  {farmer.region}
                </p>
                <p className="text-xs text-slate-500 leading-relaxed">
                  <span className="text-slate-300 font-medium">{t('direction')}:</span>{' '}
                  {shortName}
                </p>
                <p className="text-xs text-slate-500">
                  <span className="text-slate-300 font-medium">{t('amount')}:</span>{' '}
                  ₸ {farmer.amount.toLocaleString()}
                </p>
              </div>
            </div>
          </div>

          <hr className="border-surface-border"/>

          {/* Feature values */}
          <div>
            <h3 className="text-sm font-semibold text-white mb-3">{t('farmerDetails')}</h3>
            <div className="space-y-3">
              <FeatureBar label={t('infraIndex')}   value={farmer.infrastructure_index}       min={1}   max={10}  />
              <FeatureBar label={t('survivalRate')} value={farmer.herd_survival_rate}         min={50}  max={99}  unit="%" />
              <FeatureBar label={t('obligations')}  value={farmer.historical_obligations_met} min={0}   max={1}   />
              <FeatureBar label={t('climateRisk')}  value={farmer.climate_risk_factor}        min={0}   max={1}   invert />
            </div>
          </div>

          <hr className="border-surface-border"/>

          {/* SHAP chart */}
          <div>
            <h3 className="text-sm font-semibold text-white mb-1">{t('featureImpact')}</h3>
            <p className="text-xs text-slate-500 mb-4">{t('shapExplain')}</p>

            {shapData.length > 0 ? (
              <ResponsiveContainer width="100%" height={220}>
                <BarChart
                  data={shapData}
                  layout="vertical"
                  margin={{ top: 0, right: 20, left: 0, bottom: 0 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" horizontal={false}/>
                  <XAxis type="number" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false}/>
                  <YAxis
                    type="category" dataKey="label" width={140}
                    tick={{ fill: '#cbd5e1', fontSize: 11 }} axisLine={false} tickLine={false}
                    tickFormatter={v => v.length > 20 ? v.slice(0, 18) + '…' : v}
                  />
                  <Tooltip content={<ShapTooltip/>}/>
                  <ReferenceLine x={0} stroke="#475569" strokeWidth={1.5}/>
                  <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                    {shapData.map((entry) => (
                      <Cell
                        key={entry.key}
                        fill={entry.value >= 0 ? '#22c55e' : '#ef4444'}
                        opacity={0.85}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-xs text-slate-500">No SHAP data available.</p>
            )}

            {/* Legend */}
            <div className="flex items-center gap-4 mt-3 text-xs text-slate-400">
              <span className="flex items-center gap-1.5">
                <span className="w-3 h-3 rounded-sm bg-green-500"/>
                {t('positiveImpact')}
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-3 h-3 rounded-sm bg-red-500"/>
                {t('negativeImpact')}
              </span>
            </div>
          </div>

        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-surface-card/95 backdrop-blur border-t border-surface-border px-6 py-4">
          <button onClick={onClose} className="btn-primary w-full">{t('close')}</button>
        </div>
      </div>
    </div>
  )
}
