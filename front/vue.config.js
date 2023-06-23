const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  pages: {
    index: {
      entry: "src/main.js",
      title: "特定警察",
    }
  },
  transpileDependencies: [
    'vuetify'
  ],
  configureWebpack: {
    watchOptions :{
      aggregateTimeout: 300,
      poll: 1000
    }
  }
})
