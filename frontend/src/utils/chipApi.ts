import type { ChipSnapshot } from '../types/chip';

/**
 * Transport layer stub for the Python backend.
 *
 * The UI is driven entirely by a `ChipSnapshot`, so connecting a real backend
 * means replacing the local simulation source in `useChipSimulation` with either
 * `subscribeToChip` (WebSocket push) or `fetchChipSnapshot` (HTTP polling).
 */

const env = (import.meta as unknown as {env?: Record<string, string | undefined>;}).env ?? {};

export const CHIP_WS_URL = env.VITE_CHIP_WS_URL ?? 'ws://localhost:8000/ws/chip';
export const CHIP_HTTP_URL = env.VITE_CHIP_API_URL ?? 'http://localhost:8000/api/chip';

export type ChipServerMessage =
{type: 'snapshot';payload: ChipSnapshot;} |
{type: 'state';payload: {state: ChipSnapshot['state'];};} |
{type: 'event';payload: ChipSnapshot['events'][number];} |
{type: 'crime';payload: ChipSnapshot['crimes'][number];} |
{type: 'thought';payload: ChipSnapshot['thought'];};

export type ChipClientCommand =
{type: 'pause';} |
{type: 'resume';} |
{type: 'set_camera';payload: {active: boolean;};};

interface SubscribeHandlers {
  onMessage: (message: ChipServerMessage) => void;
  onStatus?: (status: 'connecting' | 'open' | 'closed') => void;
}

/** Opens a WebSocket to the Chip daemon. Returns a disposer. */
export function subscribeToChip(handlers: SubscribeHandlers, url: string = CHIP_WS_URL): () => void {
  if (typeof WebSocket === 'undefined') return () => {};

  handlers.onStatus?.('connecting');
  const socket = new WebSocket(url);

  socket.onopen = () => handlers.onStatus?.('open');
  socket.onclose = () => handlers.onStatus?.('closed');
  socket.onmessage = (raw) => {
    try {
      handlers.onMessage(JSON.parse(raw.data) as ChipServerMessage);
    } catch {

      /* ignore malformed frames */}
  };

  return () => socket.close();
}

/** One-shot snapshot read, for polling or first paint before the socket opens. */
export async function fetchChipSnapshot(url: string = CHIP_HTTP_URL): Promise<ChipSnapshot | null> {
  try {
    const response = await fetch(`${url}/snapshot`);
    if (!response.ok) return null;
    return (await response.json()) as ChipSnapshot;
  } catch {
    return null;
  }
}

/** Sends a control command (pause / resume / camera toggle) to the daemon. */
export async function sendChipCommand(
command: ChipClientCommand,
url: string = CHIP_HTTP_URL)
: Promise<void> {
  try {
    await fetch(`${url}/command`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(command)
    });
  } catch {

    /* offline-first: the local simulation keeps running */}
}