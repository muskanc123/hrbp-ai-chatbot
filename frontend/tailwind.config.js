/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f5f7ff',
          100: '#ebf0ff',
          200: '#d6e0ff',
          300: '#b3c5ff',
          400: '#8da5ff',
          500: '#6366F1',
          600: '#5558E3',
          700: '#4a4bc7',
          800: '#3d3ea3',
          900: '#333481',
        },
      },
      fontFamily: {
        'exo': ['"Exo 2"', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
