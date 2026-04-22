import { useState, useEffect, useCallback } from 'react';
import type { Question, QuizStats } from '../types';
import calcData from '../data/calc-training.json';

const STORAGE_STATS = 'nw-calc-stats';
const questions: Question[] = calcData as Question[];

const categories = [...new Set(questions.map(q => q.category))].sort();

function getStats(): QuizStats {
  const raw = localStorage.getItem(STORAGE_STATS);
  if (raw) return JSON.parse(raw);
  const stats: QuizStats = { total: 0, correct: 0, byCategory: {} };
  categories.forEach(c => { stats.byCategory[c] = { total: 0, correct: 0 }; });
  return stats;
}

function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

export default function CalcTraining() {
  const [mode, setMode] = useState<'menu' | 'quiz'>('menu');
  const [filterCategory, setFilterCategory] = useState<string>('all');
  const [count, setCount] = useState(10);
  const [pool, setPool] = useState<Question[]>([]);
  const [idx, setIdx] = useState(0);
  const [selected, setSelected] = useState<number | null>(null);
  const [answered, setAnswered] = useState(false);
  const [results, setResults] = useState<boolean[]>([]);
  const [showExplanation, setShowExplanation] = useState(false);
  const [stats, setStats] = useState<QuizStats>(getStats());

  useEffect(() => {
    localStorage.setItem(STORAGE_STATS, JSON.stringify(stats));
  }, [stats]);

  const startQuiz = useCallback((qList: Question[]) => {
    setPool(shuffle(qList).slice(0, count));
    setIdx(0);
    setSelected(null);
    setAnswered(false);
    setResults([]);
    setShowExplanation(false);
    setMode('quiz');
  }, [count]);

  const handleAnswer = (optionIdx: number) => {
    if (answered) return;
    setSelected(optionIdx);
    setAnswered(true);
    const q = pool[idx];
    const isCorrect = q.options[optionIdx].correct;
    const newResults = [...results, isCorrect];
    setResults(newResults);

    const cat = q.category;
    const newStats = { ...stats };
    newStats.total += 1;
    newStats.correct += isCorrect ? 1 : 0;
    newStats.byCategory = { ...newStats.byCategory };
    newStats.byCategory[cat] = {
      total: (newStats.byCategory[cat]?.total || 0) + 1,
      correct: (newStats.byCategory[cat]?.correct || 0) + (isCorrect ? 1 : 0),
    };
    setStats(newStats);
  };

  const nextQuestion = () => {
    if (idx + 1 >= pool.length) {
      setMode('menu');
      return;
    }
    setIdx(idx + 1);
    setSelected(null);
    setAnswered(false);
    setShowExplanation(false);
  };

  const currentQ = pool[idx];
  const correctCount = results.filter(Boolean).length;
  const progress = pool.length > 0 ? ((idx + (answered ? 1 : 0)) / pool.length) * 100 : 0;
  const accuracy = stats.total > 0 ? Math.round((stats.correct / stats.total) * 100) : 0;

  if (mode === 'quiz') {
    if (!currentQ) { setMode('menu'); return null; }
    return (
      <div>
        <div className="mb-3">
          <div className="flex justify-between text-xs mb-1" style={{ color: '#94a3b8' }}>
            <span>{idx + 1} / {pool.length}</span>
            <span>{correctCount} correct</span>
          </div>
          <div className="w-full h-1.5 rounded-full" style={{ backgroundColor: '#1a1a3e' }}>
            <div className="h-full rounded-full transition-all" style={{ width: `${progress}%`, backgroundColor: '#2980b9' }} />
          </div>
        </div>

        <div className="text-xs mb-2 px-2 py-1 rounded inline-block" style={{ backgroundColor: '#1a1a3e', color: '#3498db' }}>
          {currentQ.category}
        </div>

        <h2 className="text-base font-medium mb-4" style={{ color: '#e2e8f0' }}>
          {currentQ.question}
        </h2>

        <div className="space-y-2 mb-4">
          {currentQ.options.map((opt, i) => {
            let bgColor = '#1a1a3e';
            let borderColor = '#2a2a5e';
            let textColor = '#e2e8f0';
            if (answered) {
              if (opt.correct) { bgColor = '#1a3a2a'; borderColor = '#2ecc71'; textColor = '#2ecc71'; }
              else if (i === selected && !opt.correct) { bgColor = '#3a1a1a'; borderColor = '#e74c3c'; textColor = '#e74c3c'; }
              else { bgColor = '#0f0f23'; borderColor = '#1a1a3e'; textColor = '#64748b'; }
            }
            return (
              <button key={i} onClick={() => handleAnswer(i)} disabled={answered}
                className="w-full text-left p-3 rounded-lg border transition-colors text-sm"
                style={{ backgroundColor: bgColor, borderColor, color: textColor }}>
                {opt.text}
              </button>
            );
          })}
        </div>

        {answered && (
          <div className="mb-4">
            <button onClick={() => setShowExplanation(!showExplanation)}
              className="text-xs underline mb-2" style={{ color: '#3498db', background: 'none', border: 'none', cursor: 'pointer' }}>
              {showExplanation ? 'Hide' : 'Show'} Explanation
            </button>
            {showExplanation && (
              <div className="space-y-2">
                <div className="p-3 rounded-lg text-sm" style={{ backgroundColor: '#1a1a3e', color: '#94a3b8' }}>
                  {currentQ.explanation}
                </div>
                {currentQ.cheatsheet && (
                  <div className="p-3 rounded-lg text-sm" style={{ backgroundColor: '#1a2a3e', color: '#3498db', border: '1px solid #2980b9' }}>
                    <strong>Cheatsheet:</strong> {currentQ.cheatsheet}
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {answered && (
          <button onClick={nextQuestion}
            className="w-full py-3 rounded-lg font-medium text-sm"
            style={{ backgroundColor: '#3498db', color: '#fff' }}>
            {idx + 1 >= pool.length ? 'Finish' : 'Next'}
          </button>
        )}
      </div>
    );
  }

  return (
    <div>
      <div className="mb-4 p-3 rounded-lg" style={{ backgroundColor: '#1a1a3e' }}>
        <div className="grid grid-cols-3 text-center text-sm">
          <div>
            <div className="text-xl font-bold" style={{ color: '#3498db' }}>{stats.total}</div>
            <div style={{ color: '#94a3b8' }}>Total</div>
          </div>
          <div>
            <div className="text-xl font-bold" style={{ color: '#2ecc71' }}>{accuracy}%</div>
            <div style={{ color: '#94a3b8' }}>Accuracy</div>
          </div>
          <div>
            <div className="text-xl font-bold" style={{ color: '#f39c12' }}>{questions.length}</div>
            <div style={{ color: '#94a3b8' }}>Questions</div>
          </div>
        </div>
      </div>

      <div className="mb-3">
        <label className="block text-sm mb-1" style={{ color: '#94a3b8' }}>Category:</label>
        <select value={filterCategory} onChange={e => setFilterCategory(e.target.value)}
          className="w-full p-2 rounded-lg text-sm" style={{ backgroundColor: '#1a1a3e', color: '#e2e8f0', border: '1px solid #2a2a5e' }}>
          <option value="all">All Categories</option>
          {categories.map(c => <option key={c} value={c}>{c} ({questions.filter(q => q.category === c).length})</option>)}
        </select>
      </div>

      <div className="mb-4">
        <label className="block text-sm mb-1" style={{ color: '#94a3b8' }}>Questions: {count}</label>
        <input type="range" min="5" max="30" step="5" value={count} onChange={e => setCount(Number(e.target.value))} className="w-full" />
      </div>

      <button onClick={() => {
        const filtered = filterCategory === 'all' ? questions : questions.filter(q => q.category === filterCategory);
        startQuiz(filtered);
      }} className="w-full py-3 rounded-lg font-medium text-sm mb-4"
        style={{ backgroundColor: '#3498db', color: '#fff' }}>
        Start Calc Training
      </button>

      <div className="space-y-1">
        <h3 className="text-sm font-medium mb-2" style={{ color: '#94a3b8' }}>Category Accuracy</h3>
        {categories.map(cat => {
          const cs = stats.byCategory[cat] || { total: 0, correct: 0 };
          const pct = cs.total > 0 ? Math.round((cs.correct / cs.total) * 100) : 0;
          return (
            <div key={cat} className="flex items-center gap-2 text-xs">
              <span className="w-36 truncate" style={{ color: '#94a3b8' }}>{cat}</span>
              <div className="flex-1 h-1.5 rounded-full" style={{ backgroundColor: '#1a1a3e' }}>
                <div className="h-full rounded-full" style={{ width: `${pct}%`, backgroundColor: pct >= 70 ? '#2ecc71' : pct >= 40 ? '#f39c12' : '#e74c3c' }} />
              </div>
              <span className="w-16 text-right" style={{ color: '#64748b' }}>{cs.total > 0 ? `${pct}%` : '-'}</span>
            </div>
          );
        })}
      </div>

      <div className="mt-4">
        <button onClick={() => { localStorage.removeItem(STORAGE_STATS); setStats(getStats()); }}
          className="px-4 py-2 rounded-lg text-xs" style={{ backgroundColor: '#2a2a5e', color: '#e74c3c' }}>
          Reset Progress
        </button>
      </div>
    </div>
  );
}
