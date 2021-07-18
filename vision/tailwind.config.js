module.exports = {
  purge: {
    content: ['./public/index.html', './src/**/*.html', './src/**/*.vue'],
    options: {
      whitelistPatternsChildren: [/chart-container$/, /graph-svg-tip$/]
    }
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}