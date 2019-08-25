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
      { from: "node_modules/bootstrap/dist/", to: "bootstrap"},
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
        test: /\.(jpe?g|png|gif)$/i,
        loader:"file-loader",
        query:{
          name:'[name].[ext]',
          outputPath:'images/'
          //the images will be emmited to public/assets/images/ folder
          //the images will be put in the DOM <style> tag as eg. background: url(assets/images/image.png);
        }
      },
      {
        test: /\.css$/,
        loaders: ["style-loader","css-loader"]
      },
      {
        test: /\.s[ac]ss$/i,
        use: [
          // Creates `style` nodes from JS strings
          'style-loader',
          // Translates CSS into CommonJS
          'css-loader',
          // Compiles Sass to CSS
          'sass-loader',
        ],
      },
    ]
  }
};
