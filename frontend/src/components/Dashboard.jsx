/**
 * Dashboard — main page layout.
 * Composes: Header, StatsBar, BudgetSlider, FarmerTable, ShapModal.
 */
import React, { useState, useMemo } from "react";
import Header from "./Header.jsx";
import StatsBar from "./StatsBar.jsx";
import BudgetSlider from "./BudgetSlider.jsx";
import FarmerTable from "./FarmerTable.jsx";
import ShapModal from "./ShapModal.jsx";
import { useLang } from "../App.jsx";
import { useData } from "../App.jsx";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

const DEFAULT_BUDGET = 500_000_000; // 500M KZT default

// ── Error screen ─────────────────────────────────────────────────────────────
function ErrorScreen({ message }) {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="glass-card p-8 max-w-md text-center space-y-4">
        <div className="w-16 h-16 rounded-2xl bg-red-500/20 flex items-center justify-center mx-auto">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            className="w-8 h-8 text-red-400"
          >
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
        </div>
        <h2 className="text-xl font-bold text-white">Backend not reachable</h2>
        <p className="text-slate-400 text-sm">{message}</p>
        <p className="text-slate-500 text-xs">
          Make sure the FastAPI server is running on port 8000:
          <br />
          <code className="text-brand-400">
            uvicorn main:app --reload --port 8000
          </code>
        </p>
        <button
          onClick={() => window.location.reload()}
          className="btn-primary mx-auto"
        >
          Retry
        </button>
      </div>
    </div>
  );
}

// ── Score Distribution mini-chart ────────────────────────────────────────────
function ScoreDistribution({ stats }) {
  if (!stats?.score_distribution) return null;
  const { bins, counts } = stats.score_distribution;
  const data = bins.map((b, i) => ({ name: b, count: counts[i] }));
  const COLORS = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#16a34a"];

  return (
    <div className="glass-card p-5">
      <h3 className="text-sm font-semibold text-white mb-4">
        Score Distribution
      </h3>
      <ResponsiveContainer width="100%" height={130}>
        <BarChart
          data={data}
          margin={{ top: 0, right: 0, left: -20, bottom: 0 }}
        >
          <XAxis
            dataKey="name"
            tick={{ fill: "#94a3b8", fontSize: 10 }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            tick={{ fill: "#94a3b8", fontSize: 10 }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip
            contentStyle={{
              background: "#1e293b",
              border: "1px solid #334155",
              borderRadius: 12,
              fontSize: 12,
            }}
            cursor={{ fill: "#334155", opacity: 0.4 }}
          />
          <Bar dataKey="count" radius={[4, 4, 0, 0]}>
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i]} opacity={0.85} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

// ── Main Dashboard ────────────────────────────────────────────────────────────
export default function Dashboard() {
  const { t } = useLang();
  const { farmers, stats, loading, error } = useData();

  const [budget, setBudget] = useState(DEFAULT_BUDGET);
  const [selectedFarmer, setSelectedFarmer] = useState(null);

  // Compute allocation summary for BudgetSlider chips
  const allocation = useMemo(() => {
    let runningBudget = budget;
    let allocated = 0;
    let approvedCount = 0;
    let reserveCount = 0;
    let rejectedCount = 0;

    for (const f of farmers) {
      if (f.efficiency_score < 50) {
        rejectedCount++;
      } else if (runningBudget >= f.amount) {
        allocated += f.amount;
        runningBudget -= f.amount;
        approvedCount++;
      } else {
        reserveCount++;
      }
    }
    return { allocated, approvedCount, reserveCount, rejectedCount };
  }, [farmers, budget]);

  if (error) return <ErrorScreen message={error} />;

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="flex-1 max-w-screen-2xl mx-auto w-full px-4 md:px-6 py-6 space-y-6">
        {/* Page title */}
        <div className="animate-fade-in">
          <h1 className="text-2xl font-extrabold text-white">
            {t("appSubtitle")}
          </h1>
          <p className="text-sm text-slate-500 mt-1">{t("ministry")}</p>
        </div>

        {/* KPI row */}
        <StatsBar />

        {/* Two-column: budget + distribution */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2">
            <BudgetSlider
              budget={budget}
              setBudget={setBudget}
              allocation={allocation}
            />
          </div>
          <ScoreDistribution stats={stats} />
        </div>

        {/* Table */}
        <FarmerTable
          farmers={farmers}
          budget={budget}
          loading={loading}
          onSelectFarmer={setSelectedFarmer}
        />
      </main>

      {/* Footer */}
      <footer className="border-t border-surface-border py-4 text-center text-xs text-slate-600">
        {t("footerNote")}
      </footer>

      {/* XAI modal */}
      {selectedFarmer && (
        <ShapModal
          farmer={selectedFarmer}
          onClose={() => setSelectedFarmer(null)}
        />
      )}
    </div>
  );
}
