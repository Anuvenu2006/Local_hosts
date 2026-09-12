import type {
  BurrowStats,
  ChipEvent,
  ChipThought,
  Crime,
  FileCategory,
  StolenFile } from
'../types/chip';

export const initialThought: ChipThought = {
  text: 'That file looks VERY interesting...',
  interest: 87,
  category: 'SECRET',
  confidence: 91,
  reason: 'Contains sensitive-looking project information.',
  target: 'project_notes.docx'
};

export const initialStats: BurrowStats = {
  filesStolen: 8,
  crimesCommitted: 12,
  mischief: 94,
  greed: 76,
  suspicion: 81
};

export const initialCrimes: Crime[] = [
{
  id: 12,
  fileName: 'application_form.pdf',
  category: 'ACADEMIC',
  interest: 100,
  status: 'STOLEN',
  time: '09:41:52'
},
{
  id: 11,
  fileName: 'project_notes.docx',
  category: 'SECRET',
  interest: 87,
  status: 'STOLEN',
  time: '09:38:14'
},
{
  id: 10,
  fileName: 'tax_return_2025.pdf',
  category: 'FINANCIAL',
  interest: 74,
  status: 'STOLEN',
  time: '09:31:40'
},
{
  id: 9,
  fileName: 'grocery_list.txt',
  category: 'BORING',
  interest: 12,
  status: 'ABORTED',
  time: '09:24:09'
},
{
  id: 8,
  fileName: 'hackathon_pitch.key',
  category: 'SECRET',
  interest: 96,
  status: 'STOLEN',
  time: '09:18:33'
}];


export const initialStolenFiles: StolenFile[] = [
{ id: 'f1', name: 'application_form.pdf', category: 'ACADEMIC', size: '412 KB' },
{ id: 'f2', name: 'project_notes.docx', category: 'SECRET', size: '88 KB' },
{ id: 'f3', name: 'tax_return_2025.pdf', category: 'FINANCIAL', size: '1.2 MB' },
{ id: 'f4', name: 'hackathon_pitch.key', category: 'SECRET', size: '6.4 MB' },
{ id: 'f5', name: 'passwords_final.txt', category: 'PERSONAL', size: '2 KB' },
{ id: 'f6', name: 'roommate_rent.xlsx', category: 'FINANCIAL', size: '54 KB' },
{ id: 'f7', name: 'thesis_draft_v9.docx', category: 'ACADEMIC', size: '740 KB' },
{ id: 'f8', name: 'acorn_map.png', category: 'PERSONAL', size: '320 KB' }];


export const initialEvents: ChipEvent[] = [
{ id: 'e1', time: '09:42:01', message: 'Chip noticed a new file', tone: 'neutral' },
{ id: 'e2', time: '09:42:03', message: 'Chip started investigating', tone: 'neutral' },
{ id: 'e3', time: '09:42:05', message: 'Camera detected human', tone: 'alert' },
{ id: 'e4', time: '09:42:05', message: 'Chip froze', tone: 'alert' },
{ id: 'e5', time: '09:42:08', message: 'Human looked away', tone: 'neutral' },
{ id: 'e6', time: '09:42:09', message: 'Chip resumed investigation', tone: 'neutral' },
{ id: 'e7', time: '09:42:11', message: 'FILE STOLEN', tone: 'crime' }];


interface CandidateFile {
  name: string;
  category: FileCategory;
  size: string;
  interest: number;
  confidence: number;
  reason: string;
  thought: string;
}

export const candidateFiles: CandidateFile[] = [
{
  name: 'seed_round_deck.pdf',
  category: 'SECRET',
  size: '4.1 MB',
  interest: 93,
  confidence: 88,
  reason: 'Filename implies money that is not yet in a nut.',
  thought: 'Nobody would miss ONE deck...'
},
{
  name: 'final_exam_answers.docx',
  category: 'ACADEMIC',
  size: '126 KB',
  interest: 100,
  confidence: 95,
  reason: 'High-value academic contraband, lightly guarded.',
  thought: 'This is the greatest acorn ever grown.'
},
{
  name: 'bank_statement_sep.pdf',
  category: 'FINANCIAL',
  size: '288 KB',
  interest: 81,
  confidence: 84,
  reason: 'Numbers this large belong underground.',
  thought: 'Humans keep so many numbers in one place.'
},
{
  name: 'birthday_surprise.txt',
  category: 'PERSONAL',
  size: '3 KB',
  interest: 68,
  confidence: 79,
  reason: 'Emotional value detected. Chip enjoys leverage.',
  thought: 'A secret about a party? Mine now.'
},
{
  name: 'meeting_notes_boring.md',
  category: 'BORING',
  size: '11 KB',
  interest: 24,
  confidence: 61,
  reason: 'Contains the phrase "circle back". Low nutrition.',
  thought: 'This smells like a wasted trip...'
}];


export const categoryStyles: Record<FileCategory, {text: string;bg: string;ring: string;}> = {
  SECRET: { text: 'text-secret', bg: 'bg-secret/10', ring: 'ring-secret/30' },
  ACADEMIC: { text: 'text-amber-300', bg: 'bg-amber-400/10', ring: 'ring-amber-400/30' },
  FINANCIAL: { text: 'text-moss-400', bg: 'bg-moss-400/10', ring: 'ring-moss-400/30' },
  PERSONAL: { text: 'text-moon-200', bg: 'bg-moon-100/10', ring: 'ring-moon-200/25' },
  BORING: { text: 'text-moon-400', bg: 'bg-moon-400/10', ring: 'ring-moon-400/20' }
};

export const stateCopy: Record<
  string,
  {label: string;blurb: string;}> =
{
  idle: { label: 'IDLE', blurb: 'Sitting outside the burrow, plotting gently.' },
  curious: { label: 'CURIOUS', blurb: 'Something new appeared in the sandbox folder.' },
  investigating: { label: 'INVESTIGATING', blurb: 'Approaching the desk. Sniffing for value.' },
  watched: { label: 'WATCHED', blurb: 'Human is looking. Chip has become furniture.' },
  stealing: { label: 'STEALING', blurb: 'Paws on the document. No going back.' },
  escaping: { label: 'ESCAPING', blurb: 'Sprinting home with stolen goods.' },
  burrowing: { label: 'BURROWING', blurb: 'Disappearing underground with the loot.' },
  celebrating: { label: 'CELEBRATING', blurb: 'A small, smug victory dance.' }
};