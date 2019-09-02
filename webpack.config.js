const path = require('path');
const webpack = require('webpack');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin')


module.exports = {
  entry: './static_src/index.js',
  output: {
    path: path.resolve(__dirname, 'static_compiled'),
    filename: 'bundle.js',
    library: 'cambridge'
  },
  plugins: [
    new CopyWebpackPlugin([
      { from: "node_modules/animate.css/animate.min.css" }
    ]),
    new UglifyJSPlugin()  // heroku has NODE_ENV=production by default
  ],
  module: {
    rules: [
      // Using this instead of ProvidePlugin so we can use them in external scripts
      {
        test: require.resolve('knockout'),
        use: [{
          loader: 'expose-loader',
          options: 'ko'
        }]
      },
      {
        test: require.resolve('jquery'),
        use: [{
          loader: 'expose-loader',
          options: 'jQuery'
        },{
          loader: 'expose-loader',
          options: '$'
        }]
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
        loaders: ["style-loader","css-loader"]
      },
      {
        test: /\.s[ac]ss$/i,
        loader: [
          // Creates `style` nodes from JS strings
          'style-loader',
          // Translates CSS into CommonJS
          'css-loader',
          // Compiles Sass to CSS
          'sass-loader',
        ],
      },
      {
        test: /\.woff2?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        loader: 'url-loader?limit=10000',
        options: {
          outputPath:'fonts',
          publicPath:'static'
        }
      },
      {
        test: /\.(ttf|eot|svg)(\?[\s\S]+)?$/,
        loader: 'file-loader',
        options:  {
          outputPath:'fonts',
          publicPath:'static'
        }
      },
    ]
  }
};
