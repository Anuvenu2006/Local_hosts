import React from 'react';
import { motion } from 'framer-motion';
import type { ChipState } from '../types/chip';

interface ChipProps {
  state: ChipState;
  size?: number;
}

const CARRYING: ChipState[] = ['stealing', 'escaping', 'burrowing', 'celebrating'];

/** Head tilt / lean per state — keeps the character readable at a glance. */
const pose: Record<ChipState, {headRotate: number;bodyRotate: number;tailClass: string;}> = {
  idle: { headRotate: 0, bodyRotate: 0, tailClass: 'chip-tail' },
  curious: { headRotate: -13, bodyRotate: -2, tailClass: 'chip-tail' },
  investigating: { headRotate: 9, bodyRotate: -7, tailClass: 'chip-tail' },
  watched: { headRotate: -3, bodyRotate: 0, tailClass: '' },
  stealing: { headRotate: 12, bodyRotate: -10, tailClass: 'chip-tail' },
  escaping: { headRotate: -6, bodyRotate: -14, tailClass: '' },
  burrowing: { headRotate: 4, bodyRotate: -18, tailClass: '' },
  celebrating: { headRotate: -8, bodyRotate: 3, tailClass: 'chip-tail' }
};

export function Chip({ state, size = 132 }: ChipProps) {
  const carrying = CARRYING.includes(state);
  const facingRight = state === 'investigating' || state === 'stealing' || state === 'curious';
  const { headRotate, bodyRotate, tailClass } = pose[state];

  const hop =
  state === 'celebrating' ?
  { y: [0, -16, 0], rotate: [0, -4, 0] } :
  state === 'escaping' ?
  { y: [0, -7, 0] } :
  state === 'investigating' ?
  { y: [0, -3, 0] } :
  { y: 0 };

  const hopTransition =
  state === 'celebrating' ?
  { duration: 0.62, repeat: Infinity, ease: 'easeOut' as const } :
  state === 'escaping' ?
  { duration: 0.28, repeat: Infinity, ease: 'linear' as const } :
  state === 'investigating' ?
  { duration: 0.9, repeat: Infinity, ease: 'easeInOut' as const } :
  { duration: 0.25 };

  return (
    <div className="relative" style={{ width: size, height: size }}>
      {/* contact shadow */}
      <div
        className="absolute left-1/2 bottom-[6%] h-[8%] w-[58%] -translate-x-1/2 rounded-[50%] bg-black/55 blur-[3px]"
        aria-hidden />
      

      {/* alarm bubble when the camera catches the human looking */}
      {state === 'watched' ?
      <motion.div
        initial={{ opacity: 0, y: 6, scale: 0.96 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.18, ease: [0.23, 1, 0.32, 1] }}
        className="absolute -top-1 left-1/2 -translate-x-1/2 rounded-xl border border-alarm/50 bg-alarm/20 px-2 py-0.5 font-display text-[15px] font-bold text-alarm backdrop-blur-md">
        
          !
        </motion.div> :
      null}

      {state === 'celebrating' ?
      <>
          <span className="absolute left-[8%] top-[8%] h-1.5 w-1.5 rounded-full bg-amber-300 shadow-warm animate-twinkle" />
          <span
          className="absolute right-[10%] top-[16%] h-1 w-1 rounded-full bg-moon-100 animate-twinkle"
          style={{ animationDelay: '0.6s' }} />
        
          <span
          className="absolute left-[26%] top-[0%] h-1 w-1 rounded-full bg-moss-400 animate-twinkle"
          style={{ animationDelay: '1.1s' }} />
        
        </> :
      null}

      <motion.div
        className="h-full w-full"
        animate={{ ...hop, scaleX: facingRight ? -1 : 1 }}
        transition={{ ...hopTransition, scaleX: { duration: 0.22, ease: 'easeOut' } }}>
        
        <motion.div
          className="h-full w-full"
          animate={{ rotate: bodyRotate }}
          transition={{ duration: 0.28, ease: [0.23, 1, 0.32, 1] }}>
          
          <svg viewBox="0 0 100 100" className="h-full w-full overflow-visible" role="img" aria-label={`Chip the squirrel, ${state}`}>
            {/* ---- tail ---- */}
            <g className={tailClass}>
              <path
                d="M62 78 C 86 80 95 56 84 39 C 77 28 62 28 62 41"
                fill="none"
                stroke="#96522a"
                strokeWidth="21"
                strokeLinecap="round" />
              
              <path
                d="M62 78 C 86 80 95 56 84 39 C 77 28 62 28 62 41"
                fill="none"
                stroke="#cf8446"
                strokeWidth="12"
                strokeLinecap="round" />
              
              <path
                d="M66 76 C 84 76 89 57 80 43"
                fill="none"
                stroke="#e6b07d"
                strokeWidth="4"
                strokeLinecap="round"
                opacity="0.75" />
              
            </g>

            <g className={state === 'watched' ? undefined : 'chip-breathe'}>
              {/* ---- hind foot + body ---- */}
              <ellipse cx="58" cy="85" rx="9.5" ry="4.6" fill="#96522a" />
              <ellipse cx="52" cy="66" rx="16" ry="19" fill="#cf8446" />
              <ellipse cx="47" cy="70" rx="10" ry="13.5" fill="#f3dcbd" />

              {/* ---- front paws (+ stolen document) ---- */}
              {carrying ?
              <g transform="rotate(-8 40 72)">
                  <rect x="27" y="62" width="24" height="19" rx="2.5" fill="#f6f1e4" />
                  <rect x="27" y="62" width="24" height="19" rx="2.5" fill="none" stroke="#c9bfa6" strokeWidth="0.8" />
                  <rect x="30" y="66" width="16" height="1.6" rx="0.8" fill="#b9ad92" />
                  <rect x="30" y="70" width="18" height="1.6" rx="0.8" fill="#b9ad92" />
                  <rect x="30" y="74" width="11" height="1.6" rx="0.8" fill="#b9ad92" />
                  <circle cx="47" cy="77" r="2.4" fill="#e4695d" />
                </g> :
              null}
              <ellipse cx="40" cy="77" rx="5.6" ry="4.2" fill="#b96b34" />
              <ellipse cx="49" cy="80" rx="5.6" ry="4.2" fill="#b96b34" />
            </g>

            {/* ---- head ---- */}
            <motion.g
              animate={{ rotate: headRotate }}
              transition={{ duration: 0.3, ease: [0.23, 1, 0.32, 1] }}
              style={{ transformBox: 'fill-box', transformOrigin: '62% 88%' }}>
              
              {/* ears */}
              <g>
                <ellipse cx="36" cy="33" rx="5.2" ry="7.6" fill="#b96b34" transform="rotate(-18 36 33)" />
                <ellipse cx="36.4" cy="34" rx="2.6" ry="4.4" fill="#e7a97f" transform="rotate(-18 36 34)" />
                <ellipse cx="50" cy="30" rx="4.6" ry="6.8" fill="#96522a" transform="rotate(10 50 30)" />
              </g>

              {/* skull */}
              <circle cx="43" cy="46" r="14.2" fill="#cf8446" />
              {/* muzzle */}
              <ellipse cx="32" cy="52" rx="8.4" ry="6.6" fill="#f7e7cf" />
              <ellipse cx="27.2" cy="50.4" rx="2.3" ry="1.9" fill="#3a2420" />
              {/* whiskers */}
              <g stroke="#f3dcbd" strokeWidth="0.7" strokeLinecap="round" opacity="0.8">
                <path d="M26 53 L18 55" />
                <path d="M26 51.5 L17.5 51" />
              </g>

              {/* eyes */}
              <g className={state === 'watched' ? undefined : 'chip-blink'}>
                <circle cx="34" cy="43" r={state === 'watched' ? 4 : 3.4} fill="#241a16" />
                <circle cx="35.1" cy="41.8" r="1.2" fill="#ffffff" opacity="0.9" />
                <circle cx="45.4" cy="41.6" r={state === 'watched' ? 3.2 : 2.7} fill="#241a16" />
                <circle cx="46.3" cy="40.6" r="0.9" fill="#ffffff" opacity="0.8" />
              </g>

              {/* brow — reads as curiosity / focus */}
              {state === 'curious' || state === 'investigating' || state === 'stealing' ?
              <path d="M30 37 L38 35" stroke="#96522a" strokeWidth="1.5" strokeLinecap="round" /> :
              null}

              {/* cheek blush */}
              <ellipse cx="38" cy="51" rx="3.4" ry="2.2" fill="#e08d5c" opacity="0.5" />
            </motion.g>
          </svg>
        </motion.div>
      </motion.div>
    </div>);

}