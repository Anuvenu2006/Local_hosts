import { useCallback, useEffect, useState } from 'react';
import { fetchChipSnapshot, sendChipCommand } from '../utils/chipApi';
import type { ChipSnapshot } from '../types/chip';

const EMPTY: ChipSnapshot = {
  state: 'idle', paused: false,
  thought: { text: 'Connecting to Chip...', interest: 0, category: 'BORING', confidence: 0, reason: 'Waiting for the Python backend.', target: '' },
  stats: { filesStolen: 0, crimesCommitted: 0, mischief: 20, greed: 50, suspicion: 20 },
  crimes: [], stolenFiles: [], events: [], cameraActive: false, watcherActive: false,
};

export function useChipSimulation() {
  const [chip, setChip] = useState<ChipSnapshot>(EMPTY);
  useEffect(() => {
    let alive = true;
    const poll = async () => {
      const snapshot = await fetchChipSnapshot();
      if (alive && snapshot) setChip(snapshot);
    };
    poll();
    const timer = window.setInterval(poll, 500);
    return () => { alive = false; window.clearInterval(timer); };
  }, []);
  const togglePaused = useCallback(async () => {
    await sendChipCommand({ type: chip.paused ? 'resume' : 'pause' });
  }, [chip.paused]);
  const toggleCamera = useCallback(async () => {
    await sendChipCommand({ type: 'set_camera', payload: { active: !chip.cameraActive } });
  }, [chip.cameraActive]);
  return { ...chip, rawState: chip.state, togglePaused, toggleCamera, setWatcherActive: () => {} };
}
