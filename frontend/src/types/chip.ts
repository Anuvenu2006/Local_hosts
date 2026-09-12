export type ChipState =
'idle' |
'curious' |
'investigating' |
'watched' |
'stealing' |
'escaping' |
'burrowing' |
'celebrating';

export type FileCategory = 'SECRET' | 'ACADEMIC' | 'FINANCIAL' | 'PERSONAL' | 'BORING';

export type CrimeStatus = 'STOLEN' | 'ABORTED' | 'IN PROGRESS';

export interface ChipThought {
  text: string;
  interest: number;
  category: FileCategory;
  confidence: number;
  reason: string;
  target: string;
}

export interface Crime {
  id: number;
  fileName: string;
  category: FileCategory;
  interest: number;
  status: CrimeStatus;
  time: string;
}

export interface StolenFile {
  id: string;
  name: string;
  category: FileCategory;
  size: string;
}

export interface BurrowStats {
  filesStolen: number;
  crimesCommitted: number;
  mischief: number;
  greed: number;
  suspicion: number;
}

export type EventTone = 'neutral' | 'alert' | 'crime' | 'good';

export interface ChipEvent {
  id: string;
  time: string;
  message: string;
  tone: EventTone;
}

export interface ChipSnapshot {
  paused: boolean;
  state: ChipState;
  thought: ChipThought;
  stats: BurrowStats;
  crimes: Crime[];
  stolenFiles: StolenFile[];
  events: ChipEvent[];
  cameraActive: boolean;
  watcherActive: boolean;
}