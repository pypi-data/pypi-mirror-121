// This file is auto-generated from the corresponding file in /dev_mode
const merge = require('webpack-merge').default;
const config = require('./webpack.prod.minimize.config');

config[0] = merge(config[0], {
  // Turn off source maps
  devtool: false
});

module.exports = config;
