const path = require('path');
const webpack = require('webpack');
const TerserPlugin = require("terser-webpack-plugin");


module.exports = {
  entry: {
    main: './static_src/main.js',
    drag_list: './static_src/drag_list.js',
    voter_history: './static_src/voter_history.js'
  },
  output: {
    path: path.resolve(__dirname, 'static_compiled'),
    filename: '[name].js',
    library: '[name]'
  },
  module: {
    rules: [
      // Using this instead of ProvidePlugin so we can use them in external scripts
      {
        test: require.resolve('jquery'),
        loader: 'expose-loader',
        options: {
          exposes: ['jQuery', '$']
        }, 
      },
      {
        test: /\.m?js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      },
      {
        test: /\.(jpe?g|png|gif|svg)$/i,
        loader: "file-loader",
        options:{
          name:'[name].[ext]',
          outputPath:'images/'
        }
      },
      {
        test: /\.css$/,
        use: [
          "style-loader",
          // Translates CSS into CommonJS
          "css-loader",
        ]
      },
      {
        test: /\.s[ac]ss$/i,
        use: [
          // Creates `style` nodes from JS strings
          "style-loader",
          // Translates CSS into CommonJS
          "css-loader",
          // Compiles Sass to CSS
          "sass-loader",
        ]
      },
    ]
  }
};
