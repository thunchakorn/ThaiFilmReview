/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/templates/*.{html,js}',
    './**/templates/**/*.{html,js}',
    './**/templates/**/**/*.{html,js}',
  ],
  theme: {
    extend: {},
    fontFamily: {
      sans: ['Kanit', 'Arial Narrow', 'Arial', 'sans-serif'],
    },
  },
  daisyui: {
    themes: [
      {
        light: {
          ...require('daisyui/src/theming/themes')['light'],
          primary: '#f2cd3f',
          'base-100': '#ffffff',
          'base-200': '#fefcf4',
          'base-300': '#fefcf4',
        },
      },
      {
        dark: {
          ...require('daisyui/src/theming/themes')['dark'],
          primary: '#f2cd3f',
        },
      },
    ],
  },
  darkMode: ['selector', '[data-theme="dark"]'],
  plugins: [require('daisyui')],
}
