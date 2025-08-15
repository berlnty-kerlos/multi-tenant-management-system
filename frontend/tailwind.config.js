/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
       "./index.html",
       "./src/**/*.{js,jsx,ts,tsx}"
      ],
  theme: {
    extend: {
      colors: {
        primary: '#1F2937',     // dark gray
        secondary: '#958AC1',   // your purple
        accent: '#A6D609',      // lime
      },
    },
  },
  plugins: [],
};
