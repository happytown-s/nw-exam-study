import { useState } from 'react';
import type { QuizStats } from '../types';

function loadStats(key: string): QuizStats | null {
  const raw = localStorage.getItem(key);
  return raw ? JSON.parse(raw) : null;
}

interface TabData {
  label: string;
  statsKey: string;
  totalQuestions: number;
  color: string;
}

const tabs: TabData[] = [
  { label: 'Subject A Quiz', statsKey: 'nw-quiz-stats', totalQuestions: 250, color: '#3498db' },
  { label: 'Calc Training', statsKey: 'nw-calc-stats', totalQuestions: 121, color: '#2980b9' },
  { label: 'Subject B', statsKey: 'nw-b-stats', totalQuestions: 100, color: '#f39c12' },
];

function getWrongCount(): number {
  const raw = localStorage.getItem('nw-quiz-wrong');
  if (!raw) return 0;
  return (JSON.parse(raw) as number[]).length;
}

export default function Progress() {
  const [activeTab, setActiveTab] = useState(0);
  const [refresh, setRefresh] = useState(0);

  const current = tabs[activeTab];
  const stats = loadStats(current.statsKey);
  const wrongCount = getWrongCount();

  const totalAnswered = stats ? stats.total : 0;
  const totalCorrect = stats ? stats.correct : 0;
  const accuracy = totalAnswered > 0 ? Math.round((totalCorrect / totalAnswered) * 100) : 0;
  const coverage = Math.round((totalAnswered / current.totalQuestions) * 100);
  const categories = stats ? Object.entries(stats.byCategory).sort(([a], [b]) => a.localeCompare(b)) : [];

  return (
    <div>
      <div className="flex gap-2 mb-4">
        {tabs.map((tab, i) => (
          <button
            key={tab.statsKey}
            onClick={() => { setActiveTab(i); setRefresh(r => r + 1); }}
            className="flex-1 py-2 rounded-lg text-xs font-medium"
            style={{
              backgroundColor: i === activeTab ? tab.color : '#1a1a3e',
              color: i === activeTab ? '#fff' : '#94a3b8',
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-3 mb-4">
        <div className="p-3 rounded-lg text-center" style={{ backgroundColor: '#1a1a3e' }}>
          <div className="text-2xl font-bold" style={{ color: current.color }}>{totalAnswered}</div>
          <div className="text-xs" style={{ color: '#94a3b8' }}>Answered</div>
        </div>
        <div className="p-3 rounded-lg text-center" style={{ backgroundColor: '#1a1a3e' }}>
          <div className="text-2xl font-bold" style={{ color: accuracy >= 70 ? '#2ecc71' : accuracy >= 40 ? '#f39c12' : '#e74c3c' }}>
            {accuracy}%
          </div>
          <div className="text-xs" style={{ color: '#94a3b8' }}>Accuracy</div>
        </div>
        <div className="p-3 rounded-lg text-center" style={{ backgroundColor: '#1a1a3e' }}>
          <div className="text-2xl font-bold" style={{ color: '#2ecc71' }}>{totalCorrect}</div>
          <div className="text-xs" style={{ color: '#94a3b8' }}>Correct</div>
        </div>
        <div className="p-3 rounded-lg text-center" style={{ backgroundColor: '#1a1a3e' }}>
          <div className="text-2xl font-bold" style={{ color: '#e74c3c' }}>
            {current.statsKey === 'nw-quiz-stats' ? wrongCount : totalAnswered - totalCorrect}
          </div>
          <div className="text-xs" style={{ color: '#94a3b8' }}>
            {current.statsKey === 'nw-quiz-stats' ? 'Wrong (saved)' : 'Incorrect'}
          </div>
        </div>
      </div>

      <div className="mb-4">
        <div className="flex justify-between text-xs mb-1" style={{ color: '#94a3b8' }}>
          <span>Coverage</span>
          <span>{totalAnswered} / {current.totalQuestions} ({coverage}%)</span>
        </div>
        <div className="w-full h-2 rounded-full" style={{ backgroundColor: '#1a1a3e' }}>
          <div className="h-full rounded-full transition-all" style={{ width: `${Math.min(coverage, 100)}%`, backgroundColor: current.color }} />
        </div>
      </div>

      <div className="mb-4">
        <div className="flex justify-between text-xs mb-1" style={{ color: '#94a3b8' }}>
          <span>Accuracy</span>
          <span>{accuracy}%</span>
        </div>
        <div className="w-full h-2 rounded-full" style={{ backgroundColor: '#1a1a3e' }}>
          <div className="h-full rounded-full transition-all" style={{ width: `${accuracy}%`, backgroundColor: accuracy >= 70 ? '#2ecc71' : accuracy >= 40 ? '#f39c12' : '#e74c3c' }} />
        </div>
      </div>

      <h3 className="text-sm font-medium mb-2" style={{ color: '#94a3b8' }}>Breakdown by Category</h3>
      <div className="space-y-2">
        {categories.map(([cat, cs]) => {
          const catTotal = (cs as { total: number; correct: number }).total;
          const catCorrect = (cs as { total: number; correct: number }).correct;
          const pct = catTotal > 0 ? Math.round((catCorrect / catTotal) * 100) : 0;
          return (
            <div key={cat}>
              <div className="flex justify-between text-xs mb-0.5">
                <span style={{ color: '#e2e8f0' }}>{cat}</span>
                <span style={{ color: '#64748b' }}>{catTotal > 0 ? `${catCorrect}/${catTotal} (${pct}%)` : 'Not started'}</span>
              </div>
              <div className="w-full h-1.5 rounded-full" style={{ backgroundColor: '#1a1a3e' }}>
                <div className="h-full rounded-full" style={{ width: `${pct}%`, backgroundColor: pct >= 70 ? '#2ecc71' : pct >= 40 ? '#f39c12' : '#e74c3c' }} />
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-4 flex gap-2">
        <button
          onClick={() => {
            tabs.forEach(t => localStorage.removeItem(t.statsKey));
            localStorage.removeItem('nw-quiz-wrong');
            setRefresh(r => r + 1);
          }}
          className="px-4 py-2 rounded-lg text-xs"
          style={{ backgroundColor: '#2a2a5e', color: '#e74c3c' }}
        >
          Reset All Progress
        </button>
      </div>
    </div>
  );
}
