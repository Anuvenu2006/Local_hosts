export default {content: [
  './index.html',
  './src/**/*.{js,ts,jsx,tsx}'
],
  theme: {
    extend: {
      colors: {
        ink: '#050b09',
        pine: {
          950: '#07110e',
          900: '#0b1a15',
          850: '#0f221c',
          800: '#132a22',
          700: '#1b382e',
          600: '#264a3c',
          500: '#356050',
        },
        charcoal: {
          900: '#101413',
          800: '#181e1c',
          700: '#222a27',
        },
        moss: {
          400: '#8fc47a',
          500: '#6fae5c',
          600: '#4f8a41',
        },
        moon: {
          100: '#fbf4e2',
          200: '#f2e6c8',
          300: '#ddcda6',
          400: '#b9ab8b',
        },
        amber: {
          300: '#f7cd83',
          400: '#efb45a',
          500: '#dd9a36',
        },
        fur: {
          400: '#e0a06a',
          500: '#cf8446',
          600: '#b96b34',
          700: '#96522a',
        },
        alarm: '#e4695d',
        secret: '#c58cf0',
      },
      fontFamily: {
        display: ['Fraunces', 'Georgia', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
      borderRadius: {
        '4xl': '2rem',
      },
      boxShadow: {
        glass: '0 24px 60px -24px rgba(0,0,0,0.75), inset 0 1px 0 0 rgba(255,255,255,0.05)',
        moon: '0 0 80px 24px rgba(246,236,210,0.18)',
        warm: '0 0 40px 6px rgba(239,180,90,0.28)',
      },
    },
  },
}
