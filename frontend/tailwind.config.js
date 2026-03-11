/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'steel': {
          900: '#0a0e1a',
          800: '#0f1628',
          700: '#1a2240',
          600: '#243058',
          500: '#2e3f70',
        },
        'metal': {
          400: '#8899bb',
          300: '#aabbd4',
          200: '#c8d6e8',
          100: '#e8f0f8',
        },
        'accent': {
          orange: '#ff6b35',
          cyan: '#00d4ff',
          green: '#39ff14',
        }
      },
      fontFamily: {
        'mono': ['JetBrains Mono', 'Courier New', 'monospace'],
        'display': ['Rajdhani', 'Impact', 'sans-serif'],
      }
    },
  },
  plugins: [],
}