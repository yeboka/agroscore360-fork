/**
 * FarmerTable — sortable, filterable, color-coded applicant table.
 *
 * Row colors:
 *   🟢 Green  — score ≥ 70 AND fits within remaining budget  → Approved
 *   🟡 Yellow — score ≥ 50 BUT budget exhausted               → Reserve
 *   🔴 Red    — score < 50                                     → Rejected
 *
 * Clicking a row fires onSelectFarmer(farmer) to open the XAI modal.
 */
import React, { useMemo, useState } from "react";
import { useLang } from "../App.jsx";

// ── Helpers ─────────────────────────────────────────────────────────────────
function fmtKZT(n) {
  if (n >= 1e9) return (n / 1e9).toFixed(2) + "B";
  if (n >= 1e6) return (n / 1e6).toFixed(1) + "M";
  if (n >= 1e3) return (n / 1e3).toFixed(0) + "K";
  return n.toLocaleString();
}

function ScoreBadge({ score }) {
  const [bg, text] =
    score >= 70
      ? ["bg-green-500/15 border-green-500/30", "text-green-400"]
      : score >= 50
      ? ["bg-yellow-500/15 border-yellow-500/30", "text-yellow-400"]
      : ["bg-red-500/15 border-red-500/30", "text-red-400"];
  return (
    <span className={`badge border ${bg} ${text} font-bold text-sm`}>
      {score.toFixed(1)}
    </span>
  );
}

function StatusBadge({ rowStatus, t }) {
  const cfg = {
    approved: {
      cls: "bg-green-500/15 border-green-500/30 text-green-400",
      dot: "bg-green-400",
    },
    reserve: {
      cls: "bg-yellow-500/15 border-yellow-500/30 text-yellow-400",
      dot: "bg-yellow-400",
    },
    rejected: {
      cls: "bg-red-500/15 border-red-500/30 text-red-400",
      dot: "bg-red-400",
    },
  }[rowStatus] ?? {
    cls: "bg-slate-500/15 border-slate-500/30 text-slate-400",
    dot: "bg-slate-400",
  };

  return (
    <span className={`badge border ${cfg.cls}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${cfg.dot}`} />
      {t(rowStatus)}
    </span>
  );
}

// Short direction label (strip "Субсидирование " prefix)
function shortDir(dir) {
  return dir
    .replace(/^Субсидирование затрат по /, "")
    .replace(/^Субсидирование в /, "")
    .replace(/^Субсидирование /, "");
}

// ── Skeleton row ─────────────────────────────────────────────────────────────
function SkeletonRow() {
  return (
    <tr>
      {[40, 80, 120, 100, 50, 90, 70, 80].map((w, i) => (
        <td key={i} className="px-3 py-3">
          <div className={`h-4 shimmer-bg rounded`} style={{ width: w }} />
        </td>
      ))}
    </tr>
  );
}

// ── Main Component ────────────────────────────────────────────────────────────
export default function FarmerTable({
  farmers,
  budget,
  loading,
  onSelectFarmer,
}) {
  const { t } = useLang();

  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("all"); // all | approved | reserve | rejected
  const [sortKey, setSortKey] = useState("efficiency_score");
  const [sortDir, setSortDir] = useState("desc");
  const [page, setPage] = useState(0);
  const PAGE_SIZE = 15;

  // ── Compute allocation status for each farmer ───────────────────────────
  const farmersWithStatus = useMemo(() => {
    // Already sorted by score desc from API; respect user sort later
    let runningBudget = budget;
    return farmers.map((f) => {
      let rowStatus;
      if (f.efficiency_score < 50) {
        rowStatus = "rejected";
      } else if (runningBudget >= f.amount) {
        rowStatus = "approved";
        runningBudget -= f.amount;
      } else {
        rowStatus = "reserve";
      }
      return { ...f, rowStatus };
    });
  }, [farmers, budget]);

  // ── Filter + search + sort ───────────────────────────────────────────────
  const visible = useMemo(() => {
    const q = search.toLowerCase();
    return farmersWithStatus
      .filter((f) => {
        if (filter !== "all" && f.rowStatus !== filter) return false;
        if (
          q &&
          !f.region.toLowerCase().includes(q) &&
          !f.subsidy_direction.toLowerCase().includes(q) &&
          !f.app_number.toLowerCase().includes(q)
        )
          return false;
        return true;
      })
      .sort((a, b) => {
        const av = a[sortKey] ?? 0;
        const bv = b[sortKey] ?? 0;
        return sortDir === "asc"
          ? av > bv
            ? 1
            : av < bv
            ? -1
            : 0
          : av < bv
          ? 1
          : av > bv
          ? -1
          : 0;
      });
  }, [farmersWithStatus, filter, search, sortKey, sortDir]);

  const totalPages = Math.ceil(visible.length / PAGE_SIZE);
  const pageSlice = visible.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);

  // Reset to page 0 on filter/search change
  const handleSearch = (v) => {
    setSearch(v);
    setPage(0);
  };
  const handleFilter = (v) => {
    setFilter(v);
    setPage(0);
  };

  function handleSort(key) {
    if (key === sortKey) setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    else {
      setSortKey(key);
      setSortDir("desc");
    }
    setPage(0);
  }

  function SortIcon({ col }) {
    if (sortKey !== col) return <span className="ml-1 text-slate-600">↕</span>;
    return (
      <span className="ml-1 text-brand-400">
        {sortDir === "asc" ? "↑" : "↓"}
      </span>
    );
  }

  const FILTERS = ["all", "approved", "reserve", "rejected"];

  const rowBg = {
    approved: "hover:bg-green-500/5  border-l-2 border-l-green-500/60",
    reserve: "hover:bg-yellow-500/5 border-l-2 border-l-yellow-500/60",
    rejected: "hover:bg-red-500/5   border-l-2 border-l-red-500/30 opacity-75",
  };

  return (
    <div className="glass-card overflow-hidden">
      {/* Toolbar */}
      <div className="p-4 border-b border-surface-border flex flex-wrap gap-3 items-center justify-between">
        {/* Search */}
        <div className="relative flex-1 min-w-48 max-w-xs">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"
          >
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
          <input
            value={search}
            onChange={(e) => handleSearch(e.target.value)}
            placeholder={t("searchPlaceholder")}
            className="w-full pl-9 pr-3 py-2 bg-surface-DEFAULT border border-surface-border rounded-xl
                       text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500
                       transition-colors"
          />
        </div>

        {/* Filter tabs */}
        <div className="flex items-center gap-1 bg-surface-DEFAULT border border-surface-border rounded-xl p-1">
          {FILTERS.map((f) => (
            <button
              key={f}
              onClick={() => handleFilter(f)}
              className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all
                ${
                  filter === f
                    ? f === "approved"
                      ? "bg-green-600 text-white"
                      : f === "reserve"
                      ? "bg-yellow-600 text-white"
                      : f === "rejected"
                      ? "bg-red-600 text-white"
                      : "bg-brand-600 text-white"
                    : "text-slate-400 hover:text-white"
                }`}
            >
              {t("filter" + f.charAt(0).toUpperCase() + f.slice(1))}
            </button>
          ))}
        </div>

        {/* Count */}
        <span className="text-xs text-slate-500">{visible.length} results</span>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-surface-border bg-surface-DEFAULT/50">
              {[
                { label: t("rank"), key: "id" },
                { label: t("appNumber"), key: "app_number" },
                { label: t("region"), key: "region" },
                { label: t("direction"), key: "subsidy_direction" },
                { label: t("headCount"), key: "head_count", align: "right" },
                { label: t("amount"), key: "amount", align: "right" },
                { label: t("score"), key: "efficiency_score", align: "center" },
                { label: t("statusCol"), key: "rowStatus", align: "center" },
              ].map((col) => (
                <th
                  key={col.key}
                  onClick={() => handleSort(col.key)}
                  className={`px-3 py-3 font-semibold text-slate-400 cursor-pointer
                              select-none whitespace-nowrap hover:text-white transition-colors
                              text-${col.align ?? "left"}`}
                >
                  {col.label}
                  <SortIcon col={col.key} />
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-surface-border/50">
            {loading ? (
              Array(8)
                .fill(0)
                .map((_, i) => <SkeletonRow key={i} />)
            ) : pageSlice.length === 0 ? (
              <tr>
                <td colSpan={8} className="text-center py-12 text-slate-500">
                  No results found.
                </td>
              </tr>
            ) : (
              pageSlice.map((f, idx) => (
                <tr
                  key={f.id}
                  onClick={() => onSelectFarmer(f)}
                  className={`cursor-pointer transition-colors ${
                    rowBg[f.rowStatus] ?? ""
                  }`}
                >
                  <td className="px-3 py-3 text-slate-500 font-mono text-xs">
                    {page * PAGE_SIZE + idx + 1}
                  </td>
                  <td className="px-3 py-3 font-mono text-xs text-slate-300 whitespace-nowrap">
                    {f.app_number}
                  </td>
                  <td className="px-3 py-3 text-slate-200 max-w-[140px] truncate">
                    {f.region}
                  </td>
                  <td className="px-3 py-3 text-slate-400 max-w-[180px] truncate text-xs">
                    {shortDir(f.subsidy_direction)}
                  </td>
                  <td className="px-3 py-3 text-right text-slate-300 font-mono">
                    {f.head_count.toLocaleString()}
                  </td>
                  <td className="px-3 py-3 text-right font-mono text-slate-200 whitespace-nowrap">
                    ₸ {fmtKZT(f.amount)}
                  </td>
                  <td className="px-3 py-3 text-center">
                    <ScoreBadge score={f.efficiency_score} />
                  </td>
                  <td className="px-3 py-3 text-center">
                    <StatusBadge rowStatus={f.rowStatus} t={t} />
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {!loading && totalPages > 1 && (
        <div className="px-4 py-3 border-t border-surface-border flex items-center justify-between gap-3">
          <span className="text-xs text-slate-500">
            Page {page + 1} of {totalPages}
          </span>
          <div className="flex gap-2">
            <button
              disabled={page === 0}
              onClick={() => setPage((p) => p - 1)}
              className="px-3 py-1.5 rounded-lg text-xs border border-surface-border text-slate-400
                         hover:text-white hover:border-brand-500 disabled:opacity-30 disabled:cursor-not-allowed
                         transition-colors"
            >
              ← Prev
            </button>
            {/* Page numbers (show up to 5 around current) */}
            {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
              const p = Math.max(0, Math.min(page - 2, totalPages - 5)) + i;
              return (
                <button
                  key={p}
                  onClick={() => setPage(p)}
                  className={`w-8 h-8 rounded-lg text-xs font-semibold transition-colors
                    ${
                      p === page
                        ? "bg-brand-600 text-white"
                        : "border border-surface-border text-slate-400 hover:text-white"
                    }`}
                >
                  {p + 1}
                </button>
              );
            })}
            <button
              disabled={page === totalPages - 1}
              onClick={() => setPage((p) => p + 1)}
              className="px-3 py-1.5 rounded-lg text-xs border border-surface-border text-slate-400
                         hover:text-white hover:border-brand-500 disabled:opacity-30 disabled:cursor-not-allowed
                         transition-colors"
            >
              Next →
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
