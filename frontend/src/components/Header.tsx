import React from 'react';
import { CameraIcon, CameraOffIcon, FolderSearchIcon, PauseIcon } from 'lucide-react';

interface HeaderProps {
  cameraActive: boolean;
  watcherActive: boolean;
  paused: boolean;
}

function StatusPill({ icon, label, value, active }: {
  icon: React.ReactNode;
  label: string;
  value: string;
  active: boolean;
}) {
  return (
    <div className={`scene-status-pill ${active ? 'is-active' : 'is-off'}`}>
      <span className="status-icon">{icon}</span>
      <span className="status-label">{label}</span>
      <span className="status-value">{value}</span>
    </div>
  );
}

export function Header({ cameraActive, watcherActive, paused }: HeaderProps) {
  return (
    <header className="scene-header absolute inset-x-0 top-0 z-40 flex items-start justify-between px-5 pt-5 sm:px-7 sm:pt-6 lg:px-9">
      <div className="scene-brand">
        <div className="scene-brand-title">
          <span className="scene-brand-chip">🐿️ CHIP</span>
          <span className="scene-brand-divider">/</span>
          <span className="scene-brand-thief">THE FILE THIEF</span>
        </div>
        <p className="scene-brand-tagline">Your files are safe. Probably.</p>
      </div>

      <div className="scene-statuses">
        <StatusPill
          icon={cameraActive ? <CameraIcon size={13} /> : <CameraOffIcon size={13} />}
          label="CAM"
          value={cameraActive ? 'ONLINE' : 'OFF'}
          active={cameraActive}
        />
        <StatusPill
          icon={<FolderSearchIcon size={13} />}
          label="WATCHER"
          value={watcherActive ? 'ARMED' : 'OFF'}
          active={watcherActive}
        />
        <div className={`scene-status-pill ${paused ? 'is-paused' : 'is-active'}`}>
          <span className="status-icon">{paused ? <PauseIcon size={13} /> : <span className="live-dot" />}</span>
          <span className="status-value">{paused ? 'PAUSED' : 'CHIP ACTIVE'}</span>
        </div>
      </div>
    </header>
  );
}
