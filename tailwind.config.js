/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // search template at root level
    "./**/templates//**/*.html" // template inside apps
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

