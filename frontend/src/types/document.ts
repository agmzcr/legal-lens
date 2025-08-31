export interface Document {
  id: number;
  title: string;
  summary: string;
  content: string;
  clauses: { title: string; content: string }[];
  red_flags: string[];
}