/**
 * StatsBar — four KPI cards at the top of the dashboard.
 * Shows: total applicants, avg score, total KZT requested, high-score count.
 */
import React from 'react'
import { useLang } from '../App.jsx'
import { useData } from '../App.jsx'

function fmt(n) {
  if (n >= 1e9) return (n / 1e9).toFixed(1) + 'B'
  if (n >= 1e6) return (n / 1e6).toFixed(1) + 'M'
  if (n >= 1e3) return (n / 1e3).toFixed(0) + 'K'
  return String(n)
}

const CARDS = [
  {
    key:   'totalApplicants',
    valueKey: 'total_applicants',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-5 h-5">
        <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/>
        <path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/>
      </svg>
    ),
    color: 'from-blue-600/20 to-blue-500/5 border-blue-500/20',
    textColor: 'text-blue-400',
  },
  {
    key:   'avgScore',
    valueKey: 'avg_score',
    suffix: '/100',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-5 h-5">
        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
      </svg>
    ),
    color: 'from-brand-600/20 to-brand-500/5 border-brand-500/20',
    textColor: 'text-brand-400',
  },
  {
    key:   'totalRequested',
    valueKey: 'total_requested_kzt',
    prefix: '₸ ',
    isMoney: true,
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-5 h-5">
        <line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
      </svg>
    ),
    color: 'from-amber-600/20 to-amber-500/5 border-amber-500/20',
    textColor: 'text-amber-400',
  },
  {
    key:   'highScoreCount',
    valueKey: 'high_score_count',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-5 h-5">
        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
      </svg>
    ),
    color: 'from-purple-600/20 to-purple-500/5 border-purple-500/20',
    textColor: 'text-purple-400',
  },
]

function SkeletonCard() {
  return (
    <div className="glass-card p-5 animate-pulse">
      <div className="h-4 w-24 shimmer-bg rounded mb-3"/>
      <div className="h-8 w-20 shimmer-bg rounded"/>
    </div>
  )
}

export default function StatsBar() {
  const { t }             = useLang()
  const { stats, loading } = useData()

  if (loading) return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {[0,1,2,3].map(i => <SkeletonCard key={i}/>)}
    </div>
  )

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {CARDS.map(card => {
        const raw = stats[card.valueKey] ?? 0
        const display = card.isMoney
          ? (card.prefix ?? '') + fmt(raw)
          : (card.prefix ?? '') + (typeof raw === 'number' ? raw.toLocaleString() : raw) + (card.suffix ?? '')

        return (
          <div key={card.key}
               className={`glass-card p-5 bg-gradient-to-br ${card.color} animate-slide-up`}>
            <div className="flex items-start justify-between gap-2">
              <div className="min-w-0">
                <p className="text-xs text-slate-400 font-medium truncate">{t(card.key)}</p>
                <p className={`text-2xl font-bold mt-1 ${card.textColor}`}>{display}</p>
              </div>
              <div className={`flex-shrink-0 p-2 rounded-xl bg-surface-DEFAULT/60 ${card.textColor}`}>
                {card.icon}
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
