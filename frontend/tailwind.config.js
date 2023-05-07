/* eslint-env node */
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "src/**/*.{jsx,js}"],
  theme: {
    extend:{
      colors: {
        'midnight': '#091123',
        'afterhour':'#212A3E',
        'moonlight':'#F1F6F9',
        'regal': '#34172D',
        'lining':'#d678a4',

      },       
        fontFamily:{
        'serif': ['Marko One', 'serif'],
        'sans': ['Jaldi', 'sans-serif']
      },
      screens:{
        'sm' :'640px',
        'md' :'768px',
        'lg' :'1024px',
        'xl' :'1280px'
      },

    },
  },
  plugins: [],
}