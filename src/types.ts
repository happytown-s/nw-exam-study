export interface Option {
  text: string;
  correct: boolean;
}

export interface Question {
  category: string;
  question: string;
  options: Option[];
  explanation: string;
  cheatsheet?: string;
}

export interface QuizStats {
  total: number;
  correct: number;
  byCategory: Record<string, { total: number; correct: number }>;
}
