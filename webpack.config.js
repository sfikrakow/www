const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const {CleanWebpackPlugin} = require('clean-webpack-plugin');
const CompressionPlugin = require("compression-webpack-plugin");

module.exports = {
    context: __dirname,
    entry: [
        './assets/js/main.js',
        './assets/sass/main.scss'
    ],
    output: {
        path: path.resolve('./assets/bundles/'),
        publicPath: "/static/bundles/",
        filename: "[name]-[fullhash].js"
    },
    module: {
        rules: [
            {
                test: /\.m?js$/,
                exclude: /(node_modules|bower_components)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            },
            {
                test: /\.(sa|sc|c)ss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {loader: 'css-loader', options: {sourceMap: true}},
                    'postcss-loader',
                    'sass-loader'
                ]
            },
            {
                test: /\.(png|jpe?g|gif)$/i,
                use: [
                    {
                        loader: 'file-loader',
                    },
                ],
            },
        ]
    },
    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new MiniCssExtractPlugin({filename: "[name]-[fullhash].css"}),
        new CleanWebpackPlugin(),
        new CompressionPlugin({
            test: /\.(js|css|html|svg)$/,
            threshold: 10240,
        }),
    ]
}
