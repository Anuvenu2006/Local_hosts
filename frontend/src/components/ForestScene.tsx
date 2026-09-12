import React from 'react';
import { motion } from 'framer-motion';
import { EyeIcon, VideoIcon } from 'lucide-react';
import { Chip } from './Chip';
import { stateCopy } from '../data/chipData';
import type { ChipState } from '../types/chip';

interface ForestSceneProps {
  state: ChipState;
  cameraActive: boolean;
  paused: boolean;
  targetFile: string;
}

/** Chip's stage position per state (percentages of the scene box). */
const marks: Record<ChipState, {left: number;scale: number;opacity: number;slow?: boolean;}> = {
  idle: { left: 20, scale: 1, opacity: 1 },
  curious: { left: 28, scale: 1.02, opacity: 1 },
  investigating: { left: 47, scale: 1.06, opacity: 1, slow: true },
  watched: { left: 47, scale: 1.06, opacity: 1 },
  stealing: { left: 52, scale: 1.12, opacity: 1 },
  escaping: { left: 31, scale: 1.02, opacity: 1, slow: true },
  burrowing: { left: 12, scale: 0.58, opacity: 0.22 },
  celebrating: { left: 20, scale: 1.05, opacity: 1 }
};

const STATE_ORDER: ChipState[] = [
'idle',
'curious',
'investigating',
'watched',
'stealing',
'escaping',
'burrowing',
'celebrating'];


const stars = Array.from({ length: 46 }, (_, i) => ({
  left: i * 37.7 % 100,
  top: i * 21.3 % 52,
  size: i % 7 === 0 ? 2.2 : 1.4,
  delay: i % 9 * 0.5
}));

const fireflies = Array.from({ length: 14 }, (_, i) => ({
  left: 6 + i * 13.7 % 88,
  bottom: 8 + i * 9.3 % 34,
  delay: i % 10 * 0.9,
  duration: 7 + i % 5
}));

const backTrees = Array.from({ length: 13 }, (_, i) => ({
  x: i * 96 - 20,
  h: 150 + i * 53 % 110,
  w: 74 + i * 29 % 36
}));

export function ForestScene({ state, cameraActive, paused, targetFile }: ForestSceneProps) {
  const mark = marks[state];
  const copy = stateCopy[state];

  return (
    <section
      aria-label="Forest playground"
      className="relative h-screen w-full overflow-hidden scene-sky">
      
      {/* ---------------- sky ---------------- */}
      {stars.map((star, i) =>
      <span
        key={`star-${i}`}
        className="absolute rounded-full bg-moon-100 animate-twinkle"
        style={{
          left: `${star.left}%`,
          top: `${star.top}%`,
          width: star.size,
          height: star.size,
          animationDelay: `${star.delay}s`
        }}
        aria-hidden />

      )}

      {/* moon + moonlight */}
      <div className="pointer-events-none absolute right-[9%] top-[6%]" aria-hidden>
        <div className="scene-moonglow absolute left-1/2 top-1/2 h-[420px] w-[420px] -translate-x-1/2 -translate-y-1/2 animate-moon-breathe" />
        <div className="relative h-[76px] w-[76px] rounded-full bg-moon-100 shadow-moon">
          <div className="absolute left-[22%] top-[30%] h-3 w-3 rounded-full bg-moon-300/60" />
          <div className="absolute left-[56%] top-[58%] h-2 w-2 rounded-full bg-moon-300/50" />
          <div className="absolute left-[62%] top-[22%] h-1.5 w-1.5 rounded-full bg-moon-300/40" />
        </div>
      </div>

      {/* ---------------- distant treeline ---------------- */}
      <svg
        viewBox="0 0 1200 320"
        preserveAspectRatio="none"
        className="pointer-events-none absolute inset-x-0 bottom-[30%] h-[54%] w-full animate-canopy"
        aria-hidden>
        
        {backTrees.map((tree, i) =>
        <g key={`tree-${i}`} opacity={i % 3 === 0 ? 0.55 : 0.8}>
            <path
            d={`M${tree.x} 320 L${tree.x + tree.w / 2} ${320 - tree.h} L${tree.x + tree.w} 320 Z`}
            fill={i % 2 === 0 ? '#081511' : '#0a1a14'} />
          
            <path
            d={`M${tree.x + 8} 268 L${tree.x + tree.w / 2} ${300 - tree.h} L${tree.x + tree.w - 8} 268 Z`}
            fill={i % 2 === 0 ? '#0a1a14' : '#0c2019'} />
          
          </g>
        )}
      </svg>

      {/* foreground trunks framing the stage */}
      <svg
        viewBox="0 0 1200 560"
        preserveAspectRatio="none"
        className="pointer-events-none absolute inset-0 h-full w-full"
        aria-hidden>
        
        <path d="M-10 560 L-10 60 C 40 120 20 200 58 260 C 90 312 60 420 96 560 Z" fill="#06100d" />
        <path d="M1210 560 L1210 40 C 1160 110 1186 210 1148 276 C 1114 336 1150 440 1120 560 Z" fill="#06100d" />
        <path d="M40 132 C 96 108 150 130 186 106 C 152 152 96 154 44 148 Z" fill="#071310" />
        <path d="M1164 96 C 1108 76 1050 100 1012 76 C 1050 122 1108 122 1160 114 Z" fill="#071310" />
      </svg>

      {/* ---------------- ground ---------------- */}
      <div className="absolute inset-x-0 bottom-0 h-[38%]" aria-hidden>
        <svg viewBox="0 0 1200 220" preserveAspectRatio="none" className="h-full w-full">
          <path
            d="M0 48 C 170 18 320 56 500 42 C 680 28 860 58 1040 34 C 1110 24 1160 32 1200 28 L1200 220 L0 220 Z"
            fill="#0d1d17" />
          
          <path
            d="M0 76 C 180 52 330 86 520 70 C 700 56 880 84 1060 62 C 1120 56 1164 62 1200 58 L1200 220 L0 220 Z"
            fill="#0a1712" />
          
          <path
            d="M0 128 C 220 108 420 136 640 122 C 860 108 1040 128 1200 116 L1200 220 L0 220 Z"
            fill="#07110e" />
          
        </svg>
      </div>

      {/* grass tufts, rocks, mushrooms */}
      <div className="pointer-events-none absolute inset-x-0 bottom-0 h-[38%]" aria-hidden>
        {Array.from({ length: 26 }, (_, i) =>
        <svg
          key={`grass-${i}`}
          className="absolute animate-grass"
          style={{
            left: `${2 + i * 7.3 % 96}%`,
            bottom: `${2 + i * 11 % 26}%`,
            width: 26,
            height: 22,
            animationDelay: `${i % 6 * 0.7}s`
          }}
          viewBox="0 0 26 22">
          
            <path d="M4 22 C 6 14 8 10 5 3" stroke="#16332a" strokeWidth="2" fill="none" strokeLinecap="round" />
            <path d="M12 22 C 12 13 14 9 18 4" stroke="#1a3b30" strokeWidth="2" fill="none" strokeLinecap="round" />
            <path d="M19 22 C 20 16 22 13 21 8" stroke="#132a23" strokeWidth="2" fill="none" strokeLinecap="round" />
          </svg>
        )}

        {/* rocks */}
        <svg className="absolute left-[34%] bottom-[8%] h-6 w-14" viewBox="0 0 56 24">
          <path d="M2 24 C 4 10 18 2 30 6 C 42 10 52 16 54 24 Z" fill="#16211d" />
          <path d="M10 24 C 14 14 24 8 32 10" stroke="#223029" strokeWidth="2" fill="none" />
        </svg>
        <svg className="absolute left-[44%] bottom-[20%] h-4 w-9" viewBox="0 0 36 16">
          <path d="M1 16 C 4 6 14 1 22 4 C 29 7 34 11 35 16 Z" fill="#131e1a" />
        </svg>

        {/* mushrooms */}
        {[
        { left: 29, bottom: 26, scale: 1 },
        { left: 30.8, bottom: 24.6, scale: 0.7 },
        { left: 63, bottom: 6, scale: 0.85 }].
        map((m, i) =>
        <svg
          key={`shroom-${i}`}
          className="absolute"
          style={{ left: `${m.left}%`, bottom: `${m.bottom}%`, width: 26 * m.scale, height: 28 * m.scale }}
          viewBox="0 0 26 28">
          
            <rect x="10" y="13" width="6" height="14" rx="3" fill="#e8dcc2" />
            <path d="M1 14 C 1 5 7 1 13 1 C 19 1 25 5 25 14 Z" fill="#c2564c" />
            <circle cx="8" cy="9" r="2" fill="#f4e6cd" />
            <circle cx="16" cy="7" r="1.6" fill="#f4e6cd" />
            <circle cx="19" cy="11" r="1.2" fill="#f4e6cd" />
          </svg>
        )}
      </div>

      {/* ---------------- Chip's burrow ---------------- */}
      <div className="absolute left-[4%] bottom-[9%] w-[210px]" aria-label="Chip's burrow">
        <div className="burrow-glow pointer-events-none absolute left-[44%] bottom-[6%] h-[190px] w-[190px] -translate-x-1/2 animate-moon-breathe" />
        <svg viewBox="0 0 210 130" className="relative h-auto w-full">
          {/* mound */}
          <path d="M0 130 C 8 74 46 36 104 34 C 162 32 200 74 210 130 Z" fill="#122219" />
          <path d="M14 130 C 22 84 54 50 104 48 C 154 46 188 84 196 130 Z" fill="#162b20" />
          {/* grass fringe on the mound */}
          <path
            d="M18 62 C 26 52 36 58 44 48 C 50 58 60 52 68 44 C 74 56 86 50 94 42 C 102 54 114 48 122 40 C 130 52 142 48 150 40 C 158 52 170 56 180 66 C 150 44 60 44 18 62 Z"
            fill="#1c3a2c" />
          
          {/* entrance */}
          <path d="M74 130 C 74 96 86 84 105 84 C 124 84 136 96 136 130 Z" fill="#040807" />
          <path d="M80 130 C 80 100 90 90 105 90 C 120 90 130 100 130 130 Z" fill="#0a0d0b" />
          <path d="M86 130 C 88 110 96 102 105 102 C 114 102 122 110 124 130 Z" fill="#efb45a" opacity="0.16" />
          {/* dirt pile + pebbles */}
          <ellipse cx="150" cy="124" rx="18" ry="6" fill="#1b2b21" />
          <circle cx="58" cy="122" r="4" fill="#1c2a23" />
          <circle cx="48" cy="126" r="3" fill="#182420" />
          {/* acorn stash by the door */}
          <g transform="translate(158 104)">
            <ellipse cx="7" cy="12" rx="6.4" ry="7.4" fill="#c08a4e" />
            <path d="M0 7 C 0 2 4 0 7 0 C 10 0 14 2 14 7 Z" fill="#7d4e28" />
          </g>
        </svg>
        <div className="mt-1 flex justify-center">
          <span className="rounded-lg border border-amber-400/25 bg-pine-950/70 px-2.5 py-1 font-display text-[10px] font-semibold tracking-[0.18em] text-amber-300/90 backdrop-blur-md">
            CHIP&apos;S BURROW
          </span>
        </div>
      </div>

      {/* ---------------- human at the forest bench ---------------- */}
      <div
        className="absolute left-[50%] bottom-[7%] w-[430px] -translate-x-1/2"
        aria-label="Human sitting on a steel bench using a laptop"
      >
        <div className="desk-glow pointer-events-none absolute left-[52%] bottom-[22%] h-[230px] w-[230px] -translate-x-1/2" />

        <svg viewBox="0 0 430 250" className="relative h-auto w-full">
          {/* warm ground shadow */}
          <ellipse
            cx="214"
            cy="225"
            rx="168"
            ry="18"
            fill="#020604"
            opacity="0.65"
          />

          {/* ==============================
              FOREST STEEL BENCH
              ============================== */}

          {/* backrest */}
          <rect
            x="92"
            y="128"
            width="230"
            height="13"
            rx="6.5"
            fill="#34403b"
          />
          <rect
            x="92"
            y="128"
            width="230"
            height="4"
            rx="2"
            fill="#52605a"
            opacity="0.55"
          />

          {/* metal back supports */}
          <path
            d="M112 138 L112 204"
            stroke="#1b2421"
            strokeWidth="8"
            strokeLinecap="round"
          />
          <path
            d="M300 138 L300 204"
            stroke="#1b2421"
            strokeWidth="8"
            strokeLinecap="round"
          />

          {/* wooden/metal seat */}
          <rect
            x="78"
            y="169"
            width="258"
            height="16"
            rx="7"
            fill="#39453f"
          />
          <rect
            x="82"
            y="169"
            width="250"
            height="4"
            rx="2"
            fill="#69756e"
            opacity="0.45"
          />

          {/* bench legs */}
          <path
            d="M108 184 L92 220"
            stroke="#202a26"
            strokeWidth="9"
            strokeLinecap="round"
          />
          <path
            d="M306 184 L322 220"
            stroke="#202a26"
            strokeWidth="9"
            strokeLinecap="round"
          />

          {/* foot rails */}
          <path
            d="M88 218 L326 218"
            stroke="#151d1a"
            strokeWidth="5"
            strokeLinecap="round"
            opacity="0.8"
          />

          {/* ==============================
              HUMAN — LARGER, BETTER PROPORTIONS
              ============================== */}

          <g>
            {/* legs */}
            <path
              d="M251 168 C 237 178 220 183 201 187"
              stroke="#344750"
              strokeWidth="20"
              strokeLinecap="round"
            />
            <path
              d="M201 187 L194 215"
              stroke="#2b3b43"
              strokeWidth="17"
              strokeLinecap="round"
            />
            <path
              d="M194 216 L173 219"
              stroke="#171f22"
              strokeWidth="12"
              strokeLinecap="round"
            />

            {/* torso */}
            <path
              d="M253 169 C 244 148 242 125 251 108 C 261 91 285 91 294 108 C 301 125 294 153 284 171 Z"
              fill="#3f6171"
            />

            {/* jacket highlight */}
            <path
              d="M261 111 C 267 101 282 101 288 112"
              stroke="#6e8995"
              strokeWidth="3"
              fill="none"
              opacity="0.45"
            />

            {/* arm reaching toward laptop */}
            <path
              d="M265 121 L229 145"
              stroke="#4b7181"
              strokeWidth="15"
              strokeLinecap="round"
            />
            <path
              d="M229 145 L194 151"
              stroke="#4b7181"
              strokeWidth="12"
              strokeLinecap="round"
            />

            {/* hand */}
            <circle
              cx="188"
              cy="152"
              r="7"
              fill="#e0b191"
            />

            {/* neck */}
            <path
              d="M267 99 L268 108"
              stroke="#d8a987"
              strokeWidth="9"
              strokeLinecap="round"
            />

            {/* head */}
            <circle
              cx="270"
              cy="82"
              r="22"
              fill="#e8bd9b"
            />

            {/* hair */}
            <path
              d="M247 78 C 249 57 266 51 282 58 C 293 63 296 76 292 87 C 288 74 278 66 259 72 Z"
              fill="#221a17"
            />

            {/* ear */}
            <path
              d="M249 83 L242 89 L249 92"
              fill="#e0b191"
            />

            {/* eye */}
            <circle
              cx="255"
              cy="82"
              r="2"
              fill="#221a17"
            />

            {/* laptop-facing nose */}
            <path
              d="M250 86 L244 90 L250 92"
              fill="#d49d7e"
            />
          </g>

          {/* ==============================
              LAPTOP ON BENCH
              ============================== */}

          <g>
            {/* laptop base */}
            <path
              d="M128 171 L211 171 L218 164 L136 164 Z"
              fill="#2b3533"
            />

            {/* laptop screen */}
            <rect
              x="137"
              y="115"
              width="76"
              height="51"
              rx="4"
              fill="#182321"
              transform="rotate(-4 175 140)"
            />

            <rect
              x="141"
              y="119"
              width="68"
              height="43"
              rx="3"
              fill="#9fd2f2"
              opacity="0.42"
              transform="rotate(-4 175 140)"
            />

            {/* webcam */}
            <circle
              cx="176"
              cy="114"
              r="2.4"
              fill={cameraActive ? '#8fc47a' : '#4a5450'}
            />

            {/* tiny screen glow */}
            <rect
              x="148"
              y="126"
              width="38"
              height="3"
              rx="1.5"
              fill="#d9eee6"
              opacity="0.3"
              transform="rotate(-4 175 140)"
            />
          </g>

          {/* ==============================
              SUSPICIOUS DOCUMENT
              ============================== */}

          <g
            transform="rotate(-7 105 153)"
            opacity={targetFile ? 1 : 0}
            style={{ transition: 'opacity 180ms ease-out' }}
          >
            <rect
              x="78"
              y="136"
              width="58"
              height="34"
              rx="3"
              fill="#f6f1e4"
            />

            <rect
              x="78"
              y="136"
              width="58"
              height="34"
              rx="3"
              fill="none"
              stroke="#cbc0a6"
              strokeWidth="1"
            />

            <rect
              x="84"
              y="143"
              width="34"
              height="2.6"
              rx="1.3"
              fill="#b3a68b"
            />

            <rect
              x="84"
              y="150"
              width="42"
              height="2.6"
              rx="1.3"
              fill="#b3a68b"
            />

            <rect
              x="84"
              y="157"
              width="27"
              height="2.6"
              rx="1.3"
              fill="#b3a68b"
            />

            <circle
              cx="126"
              cy="161"
              r="5"
              fill="#e4695d"
            />

            <path
              d="M123 161 L129 161"
              stroke="#f6f1e4"
              strokeWidth="1.4"
            />
          </g>

          {/* ==============================
              LITTLE FOREST DETAILS
              ============================== */}

          <ellipse
            cx="342"
            cy="219"
            rx="16"
            ry="5"
            fill="#18251f"
          />

          <circle
            cx="350"
            cy="211"
            r="5"
            fill="#7d4e28"
          />
        </svg>

        {/* watched file label */}
        <div className="pointer-events-none absolute left-[17%] top-[38%] max-w-[175px] -translate-y-full">
          <div className="rounded-xl border border-amber-400/25 bg-pine-950/80 px-2.5 py-1.5 backdrop-blur-md shadow-lg">
            <p className="font-mono text-[10px] leading-tight text-amber-300">
              {targetFile}
            </p>
            <p className="text-[9px] uppercase tracking-[0.14em] text-moon-400">
              watched file
            </p>
          </div>
        </div>
      </div>

      {/* detection cone when the human notices Chip */}
      {state === 'watched' && cameraActive ?
      <motion.div
        className="pointer-events-none absolute inset-0"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.2, ease: 'easeOut' }}
        aria-hidden>
        
          <svg viewBox="0 0 1200 560" preserveAspectRatio="none" className="h-full w-full">
            <path d="M960 330 L560 400 L560 470 L960 372 Z" fill="#e4695d" opacity="0.12" />
          </svg>
        </motion.div> :
      null}

      {/* ---------------- fireflies ---------------- */}
      <div className="pointer-events-none absolute inset-0" aria-hidden>
        {fireflies.map((fly, i) =>
        <span
          key={`fly-${i}`}
          className="absolute h-1.5 w-1.5 rounded-full bg-amber-300 shadow-warm animate-firefly"
          style={{
            left: `${fly.left}%`,
            bottom: `${fly.bottom}%`,
            animationDelay: `${fly.delay}s`,
            animationDuration: `${fly.duration}s`
          }} />

        )}
      </div>

      {/* ---------------- Chip ---------------- */}
      <motion.div
        className="absolute bottom-[11.5%] z-10"
        style={{ left: `${marks.idle.left}%` }}
        initial={false}
        animate={{
          left: `${mark.left}%`,
          scale: mark.scale,
          opacity: mark.opacity,
          y: state === 'investigating'
            ? [0, -18, 0, -28, 0]
            : state === 'stealing'
              ? [0, -12, 0, -8, 0]
              : state === 'escaping'
                ? [0, -8, 0]
                : state === 'celebrating'
                  ? [0, -18, 0, -12, 0]
                  : 0,
        }}
        transition={{
          left: {
            duration:
              state === 'investigating' ? 1.7 :
              state === 'escaping' ? 1.8 :
              state === 'burrowing' ? 0.8 :
              0.75,
            ease: [0.23, 1, 0.32, 1]
          },
          scale: { duration: 0.35 },
          opacity: { duration: 0.35 },
          y:
            state === 'investigating'
              ? { duration: 1.7, ease: 'easeInOut' }
              : state === 'stealing'
                ? { duration: 0.9, ease: 'easeInOut' }
                : state === 'escaping'
                  ? { duration: 0.7, repeat: 2, ease: 'easeInOut' }
                  : state === 'celebrating'
                    ? { duration: 1.1, ease: 'easeInOut' }
                    : { duration: 0.45 },
        }}
      >
        <Chip state={state} size={125} />

        {/* File visibly appears in Chip's paws during the grab. */}
        {(state === 'stealing' || state === 'escaping') && targetFile && (
          <motion.div
            className="pointer-events-none absolute left-[72px] top-[30px] z-20"
            initial={{ opacity: 0, scale: 0.45, rotate: -12, x: -8 }}
            animate={{
              opacity: 1,
              scale: state === 'stealing' ? [0.45, 1.08, 1] : [1, 1.04, 0.96],
              rotate: state === 'stealing' ? [-12, 8, 0] : [-4, 8, -3],
              x: state === 'escaping' ? [0, 7, -3] : 0,
            }}
            transition={{ duration: 0.55, ease: 'easeOut' }}
          >
            <div className="relative h-9 w-12 rounded-[4px] border border-amber-200/70 bg-[#f6f1e4] shadow-[0_5px_14px_rgba(0,0,0,0.35)]">
              <div className="absolute left-1.5 top-2 h-0.5 w-7 rounded bg-[#b3a68b]" />
              <div className="absolute left-1.5 top-4 h-0.5 w-8 rounded bg-[#b3a68b]" />
              <div className="absolute left-1.5 top-6 h-0.5 w-5 rounded bg-[#b3a68b]" />
              <span className="absolute -right-2 -top-2 text-sm">🌰</span>
            </div>
          </motion.div>
        )}

        {/* Little physical cues make the investigation feel alive. */}
        {state === 'investigating' && (
          <motion.div
            className="pointer-events-none absolute -left-3 -top-10 whitespace-nowrap"
            initial={{ opacity: 0, y: 8, scale: 0.9 }}
            animate={{ opacity: [0, 1, 1, 0], y: [8, 0, -5, -12], scale: [0.9, 1, 1.03, 1.05] }}
            transition={{ duration: 1.7, ease: 'easeOut' }}
          >
            <span className="font-mono text-[11px] font-semibold tracking-[0.12em] text-amber-300 drop-shadow-lg">
              sniff... sniff... 👃
            </span>
          </motion.div>
        )}

        {state === 'stealing' && (
          <motion.div
            className="pointer-events-none absolute -left-1 -top-10 whitespace-nowrap"
            initial={{ opacity: 0, scale: 0.75, y: 5 }}
            animate={{ opacity: [0, 1, 1], scale: [0.75, 1.12, 1], y: [5, -3, 0] }}
            transition={{ duration: 0.55 }}
          >
            <span className="font-display text-[12px] font-bold tracking-[0.12em] text-amber-300 drop-shadow-lg">
              MINE! 😈
            </span>
          </motion.div>
        )}

        {state === 'escaping' && (
          <motion.div
            className="pointer-events-none absolute -left-2 -top-10 whitespace-nowrap"
            initial={{ opacity: 0, x: 10, scale: 0.85 }}
            animate={{ opacity: [0, 1, 1, 0], x: [10, 0, -12, -24], scale: [0.85, 1.08, 1, 0.95] }}
            transition={{ duration: 1.35, ease: 'easeOut' }}
          >
            <span className="font-display text-[12px] font-bold tracking-[0.1em] text-amber-300 drop-shadow-lg">
              GOT IT! RUN! 🌰💨
            </span>
          </motion.div>
        )}

        {state === 'burrowing' && (
          <motion.div
            className="pointer-events-none absolute left-8 top-[-6px] whitespace-nowrap"
            initial={{ opacity: 0, y: 5, scale: 0.8 }}
            animate={{ opacity: [0, 1, 1, 0], y: [5, -2, -8, -16], scale: [0.8, 1, 1.05, 1.1] }}
            transition={{ duration: 1.35, ease: 'easeOut' }}
          >
            <span className="font-mono text-[11px] font-bold tracking-[0.08em] text-amber-300 drop-shadow-lg">
              INTO THE BURROW! 🌰
            </span>
          </motion.div>
        )}

        {state === 'celebrating' && (
          <motion.div
            className="pointer-events-none absolute -left-5 -top-12 whitespace-nowrap"
            initial={{ opacity: 0, scale: 0.65, y: 8 }}
            animate={{ opacity: [0, 1, 1, 0], scale: [0.65, 1.15, 1, 1.08], y: [8, -4, 0, -8] }}
            transition={{ duration: 1.5, ease: 'easeOut' }}
          >
            <span className="font-display text-[13px] font-black tracking-[0.12em] text-amber-300 drop-shadow-lg">
              I DID IT! 🎉🌰
            </span>
          </motion.div>
        )}
      </motion.div>

      {/* ---------------- lighting vignette ---------------- */}
      <div className="scene-vignette pointer-events-none absolute inset-0" aria-hidden />

      {/* ---------------- camera overlay ---------------- */}
      {cameraActive ?
      <div className="pointer-events-none absolute inset-0" aria-hidden>
          <div className="absolute inset-3 rounded-[22px] border border-moss-400/10" />
          {[
        'left-4 top-4 border-l-2 border-t-2 rounded-tl-lg',
        'right-4 top-4 border-r-2 border-t-2 rounded-tr-lg',
        'left-4 bottom-4 border-l-2 border-b-2 rounded-bl-lg',
        'right-4 bottom-4 border-r-2 border-b-2 rounded-br-lg'].
        map((pos) =>
        <span key={pos} className={`absolute h-5 w-5 border-moss-400/40 ${pos}`} />
        )}
          <div className="absolute inset-x-3 top-3 h-16 overflow-hidden rounded-t-[22px]">
            <div className="animate-scanline h-px w-full bg-moon-100/15" />
          </div>
        </div> :
      null}

      {/* ---------------- HUD ---------------- */}
      <div className="absolute left-5 top-[104px] z-20 flex items-center gap-2 sm:top-[112px]">
        <div className="flex items-center gap-2 rounded-xl border border-moon-200/10 bg-pine-950/70 px-2.5 py-1.5 backdrop-blur-md">
          <VideoIcon size={12} className={cameraActive ? 'text-alarm' : 'text-moon-400'} />
          <span className="font-mono text-[10px] tracking-[0.12em] text-moon-200">
            {cameraActive ? 'CAM 01 · REC' : 'CAM 01 · OFF'}
          </span>
        </div>
        {state === 'watched' ?
        <motion.div
          initial={{ opacity: 0, x: -6 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.18, ease: 'easeOut' }}
          className="flex items-center gap-2 rounded-xl border border-alarm/40 bg-alarm/15 px-2.5 py-1.5 backdrop-blur-md">
          
            <EyeIcon size={12} className="text-alarm" />
            <span className="font-mono text-[10px] tracking-[0.12em] text-alarm">HUMAN LOOKING</span>
          </motion.div> :
        null}
      </div>

      {/* state readout + animation rail */}
      <div className="absolute inset-x-5 bottom-[92px] z-20 flex items-end justify-between gap-4">
        <div className="max-w-[360px] rounded-2xl border border-moon-200/10 bg-pine-950/70 px-4 py-2.5 backdrop-blur-xl shadow-lg">
          <p className="font-display text-[12px] font-semibold tracking-[0.14em] text-amber-300">
            {paused ? 'PAUSED' : copy.label}
          </p>
          <p className="mt-0.5 text-[11px] leading-snug text-moon-300">
            {paused ? 'Chip is sulking under a leaf until you resume him.' : copy.blurb}
          </p>
        </div>

        <ol className="flex items-center gap-1.5 rounded-2xl border border-moon-200/10 bg-pine-950/70 px-3 py-2.5 backdrop-blur-xl">
          {STATE_ORDER.map((s) => {
            const active = s === state && !paused;
            return (
              <li key={s} className="flex items-center gap-1.5">
                <span
                  className={`h-1.5 w-1.5 rounded-full transition-colors duration-200 ease-out ${
                  active ? 'bg-amber-300' : 'bg-moon-400/30'}`
                  } />
                
                <span
                  className={`font-mono text-[9px] tracking-[0.1em] transition-colors duration-200 ease-out ${
                  active ? 'text-amber-300' : 'text-moon-400/55'}`
                  }>
                  
                  {stateCopy[s].label}
                </span>
              </li>);

          })}
        </ol>
      </div>
    </section>);

}