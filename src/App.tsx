import { useState } from 'react';
import Quiz from './components/Quiz';
import CalcTraining from './components/CalcTraining';
import SubjectBTraining from './components/SubjectBTraining';
import Progress from './components/Progress';

type Tab = 'quiz' | 'calc' | 'subjectb' | 'progress';

const tabs: { key: Tab; label: string }[] = [
  { key: 'quiz', label: '問題集' },
  { key: 'calc', label: '計算トレーニング' },
  { key: 'subjectb', label: '科目B' },
  { key: 'progress', label: '進捗' },
];

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('quiz');

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#0f0f23' }}>
      <header className="sticky top-0 z-50 border-b" style={{ backgroundColor: '#1a1a3e', borderColor: '#2a2a5e' }}>
        <div className="max-w-3xl mx-auto px-4">
          <h1 className="text-center text-lg font-bold py-2" style={{ color: '#3498db' }}>
            NW Exam Study
          </h1>
          <nav className="flex">
            {tabs.map((tab) => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className="flex-1 py-2 px-1 text-sm font-medium transition-colors"
                style={{
                  color: activeTab === tab.key ? '#3498db' : '#94a3b8',
                  borderBottom: activeTab === tab.key ? '2px solid #3498db' : '2px solid transparent',
                }}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 py-4">
        {activeTab === 'quiz' && <Quiz />}
        {activeTab === 'calc' && <CalcTraining />}
        {activeTab === 'subjectb' && <SubjectBTraining />}
        {activeTab === 'progress' && <Progress />}
      </main>
    </div>
  );
}

export default App;
