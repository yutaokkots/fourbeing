/* eslint-env node */
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "src/**/*.{jsx,js}"],
  theme: {
    extend:{
      colors: {
        'ocean' : '#8cb1c6',
        'land': '#d6b469',
        'sunset': '#f6851f',
        'cardamom':'#9e5224',
        'vanilla':'#fcf5eb'
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