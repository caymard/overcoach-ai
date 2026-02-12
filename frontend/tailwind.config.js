/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        overwatch: {
          orange: '#F99E1A',
          blue: '#00CCFF',
          tank: '#FAA528',
          damage: '#F6475D',
          support: '#FCBD42',
        }
      }
    },
  },
  plugins: [],
}
