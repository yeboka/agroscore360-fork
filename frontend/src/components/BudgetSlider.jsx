/**
 * BudgetSlider — interactive budget input + allocation summary chips.
 * Parent passes `budget` and `setBudget`; this component just renders the UI.
 */
import React from 'react'
import { useLang } from '../App.jsx'

const MIN_BUDGET  = 50_000_000      //   50 M KZT
const MAX_BUDGET  = 5_000_000_000   //    5 B KZT
const STEP        = 50_000_000      //   50 M step

function fmtKZT(n) {
  if (n >= 1e9) return (n / 1e9).toFixed(2) + ' B ₸'
  if (n >= 1e6) return (n / 1e6).toFixed(0) + ' M ₸'
  return n.toLocaleString() + ' ₸'
}

function pct(value, max) {
  return Math.min(100, Math.round((value / max) * 100))
}

export default function BudgetSlider({ budget, setBudget, allocation }) {
  const { t } = useLang()
  const { allocated = 0, approvedCount = 0, reserveCount = 0, rejectedCount = 0 } = allocation

  const remaining  = Math.max(0, budget - allocated)
  const allocPct   = pct(allocated, budget)

  return (
    <div className="glass-card p-5 space-y-4">
      {/* Title row */}
      <div className="flex items-center justify-between gap-3">
        <div>
          <h2 className="font-bold text-white text-base">{t('budgetTitle')}</h2>
          <p className="text-xs text-slate-400 mt-0.5">{t('budgetHint')}</p>
        </div>
        {/* Current budget display */}
        <div className="text-right flex-shrink-0">
          <div className="text-2xl font-bold text-brand-400">{fmtKZT(budget)}</div>
          <div className="text-xs text-slate-500">{t('budgetLabel')}</div>
        </div>
      </div>

      {/* Slider */}
      <div className="space-y-1">
        <input
          type="range"
          min={MIN_BUDGET}
          max={MAX_BUDGET}
          step={STEP}
          value={budget}
          onChange={e => setBudget(Number(e.target.value))}
          className="w-full h-2 rounded-full appearance-none cursor-pointer
                     bg-surface-border accent-brand-500"
          style={{
            background: `linear-gradient(to right, #16a34a ${pct(budget, MAX_BUDGET)}%, #334155 ${pct(budget, MAX_BUDGET)}%)`
          }}
        />
        <div className="flex justify-between text-xs text-slate-500">
          <span>{fmtKZT(MIN_BUDGET)}</span>
          <span>{fmtKZT(MAX_BUDGET)}</span>
        </div>
      </div>

      {/* Allocation bar */}
      <div>
        <div className="flex justify-between text-xs mb-1.5 text-slate-400">
          <span>{t('allocated')}: <span className="text-brand-400 font-semibold">{fmtKZT(allocated)}</span></span>
          <span>{t('remaining')}: <span className="text-slate-300 font-semibold">{fmtKZT(remaining)}</span></span>
        </div>
        <div className="w-full h-3 bg-surface-border rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-brand-600 to-brand-500 rounded-full transition-all duration-500"
            style={{ width: `${allocPct}%` }}
          />
        </div>
        <div className="text-right text-xs text-slate-500 mt-1">{allocPct}% utilised</div>
      </div>

      {/* Summary chips */}
      <div className="grid grid-cols-3 gap-3">
        <div className="flex flex-col items-center gap-1 py-3 rounded-xl bg-green-500/10 border border-green-500/20">
          <span className="text-2xl font-bold text-green-400">{approvedCount}</span>
          <span className="text-xs text-green-300/80 font-medium">{t('approvedCount')}</span>
        </div>
        <div className="flex flex-col items-center gap-1 py-3 rounded-xl bg-yellow-500/10 border border-yellow-500/20">
          <span className="text-2xl font-bold text-yellow-400">{reserveCount}</span>
          <span className="text-xs text-yellow-300/80 font-medium">{t('reserveCount')}</span>
        </div>
        <div className="flex flex-col items-center gap-1 py-3 rounded-xl bg-red-500/10 border border-red-500/20">
          <span className="text-2xl font-bold text-red-400">{rejectedCount}</span>
          <span className="text-xs text-red-300/80 font-medium">{t('rejectedCount')}</span>
        </div>
      </div>
    </div>
  )
}
