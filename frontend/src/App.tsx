import React from 'react';
import { Camera, CameraOff, Pause, Play } from 'lucide-react';

import { Header } from './components/Header';
import { ForestScene } from './components/ForestScene';
import { useChipSimulation } from './hooks/useChipSimulation';

export function App() {

  const chip = useChipSimulation();

  return (
    <div className="chip-app relative h-screen w-screen overflow-hidden bg-ink text-moon-100">

      {/* ==========================================
          🌲 MAIN CHIP ENVIRONMENT
          ========================================== */}

      <ForestScene
        state={chip.state}
        cameraActive={chip.cameraActive}
        paused={chip.paused}
        targetFile={chip.thought.target}
      />


      {/* ==========================================
          🐿️ TOP HUD
          ========================================== */}

      <Header
        cameraActive={chip.cameraActive}
        watcherActive={chip.watcherActive}
        paused={chip.paused}
      />


      {/* ==========================================
          🎮 MINIMAL BOTTOM CONTROLS
          ========================================== */}

      <div className="chip-controls-overlay">

        <nav
          className="scene-control-bar"
          aria-label="Chip controls"
        >

          {/* CAMERA */}

          <button
            type="button"
            onClick={chip.toggleCamera}
            className="scene-control-button"
          >
            {chip.cameraActive ? (
              <Camera size={15} />
            ) : (
              <CameraOff size={15} />
            )}

            <span>
              {chip.cameraActive ? 'CAMERA ON' : 'CAMERA OFF'}
            </span>
          </button>


          {/* PAUSE */}

          <button
            type="button"
            onClick={chip.togglePaused}
            className={`scene-control-button ${
              chip.paused ? 'is-paused' : ''
            }`}
          >

            {chip.paused ? (
              <Play size={15} />
            ) : (
              <Pause size={15} />
            )}

            <span>
              {chip.paused ? 'RESUME CHIP' : 'PAUSE CHIP'}
            </span>

          </button>

        </nav>

      </div>


      {/* ==========================================
          🧪 SMALL DEBUG LABEL
          ========================================== */}

      <div className="scene-credit pointer-events-none absolute bottom-2 left-1/2 z-30 -translate-x-1/2 font-mono text-[9px] tracking-[0.16em] text-moon-400/45">

        CHIP DAEMON · SANDBOX ONLY

      </div>

    </div>
  );
}