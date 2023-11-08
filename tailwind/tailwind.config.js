/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../collection/templates/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  variants: {
    extend: {
      scale: ['hover'],
    },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    ],
  }
}