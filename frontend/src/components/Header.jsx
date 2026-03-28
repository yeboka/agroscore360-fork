/**
 * Header — top nav bar with logo, ministry branding, and language switcher.
 */
import React from 'react'
import { useLang } from '../App.jsx'

const LANGS = [
  { code: 'ru', label: 'RU' },
  { code: 'kk', label: 'KZ' },
  { code: 'en', label: 'EN' },
]

export default function Header() {
  const { lang, setLang, t } = useLang()

  return (
    <header className="sticky top-0 z-40 border-b border-surface-border bg-surface-card/80 backdrop-blur-xl">
      <div className="max-w-screen-2xl mx-auto px-6 py-3 flex items-center justify-between gap-4">

        {/* Logo + title */}
        <div className="flex items-center gap-3 min-w-0">
          {/* Emblem */}
          <div className="flex-shrink-0 w-9 h-9 rounded-xl bg-gradient-to-br from-brand-600 to-brand-700
                          flex items-center justify-center shadow-lg shadow-brand-900/40">
            <svg viewBox="0 0 24 24" fill="none" className="w-5 h-5 text-white" stroke="currentColor" strokeWidth="2">
              <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>
              <polyline points="9 22 9 12 15 12 15 22"/>
            </svg>
          </div>

          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg text-white tracking-tight">{t('appName')}</span>
              <span className="hidden sm:inline-flex badge bg-brand-600/20 text-brand-500 border border-brand-600/30">
                Beta
              </span>
            </div>
            <p className="text-xs text-slate-500 truncate hidden md:block">{t('ministry')}</p>
          </div>
        </div>

        {/* Right side */}
        <div className="flex items-center gap-3">
          {/* Live indicator */}
          <div className="hidden sm:flex items-center gap-1.5 text-xs text-slate-400">
            <span className="w-2 h-2 rounded-full bg-brand-500 animate-pulse"/>
            <span>Live</span>
          </div>

          {/* Lang switcher */}
          <div className="flex items-center gap-1 bg-surface-DEFAULT border border-surface-border rounded-xl p-1">
            {LANGS.map(({ code, label }) => (
              <button
                key={code}
                onClick={() => setLang(code)}
                className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all duration-150
                  ${lang === code
                    ? 'bg-brand-600 text-white shadow'
                    : 'text-slate-400 hover:text-white'}`}
              >
                {label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </header>
  )
}
