const VueLoaderPlugin = require("vue-loader/lib/plugin");

require("dotenv").config();
const ENV = process.env.APP_ENV;
const isProd = ENV === "prod";

const KB = 1024;
const entrypoints_dir = __dirname + "/frontend_src";

function setMode() {
    if (isProd) {
        return "production";
    } else {
        return "development";
    }
}

const config = {
    mode: setMode(),
    entry: {
        'app': entrypoints_dir + "/index.js"
    },
    output: {
        path: __dirname + "/ontology/static/ontology/bundle",
        filename: "[name].js",
        chunkFilename: "[name].chunk.js",
        publicPath: "/static/ontology/bundle/"
    },
    plugins: [
        new VueLoaderPlugin(),
    ],
    externals: {
        vue: 'Vue27',
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ["@babel/preset-env"],
                        plugins: ['@babel/plugin-transform-runtime']
                    }
                },
                exclude: [/node_modules/]
            },
            {
                test: /\.((css)|(scss))$/i,
                use: ["style-loader", "css-loader", "sass-loader"]
            },
            {
                test: /.woff2$/,
                use: {
                    loader: "url-loader",
                    options: {
                        limit: 100 * KB
                    }
                }
            },
            {
                test: /.(png|jpg|jpeg|gif|svg|woff|ttf|eot)$/,
                use: {
                    loader: "url-loader",
                    options: {
                        limit: 10 * KB
                    }
                }
            },
            {
                test: /\.vue$/,
                loader: "vue-loader"
            }
        ]
    },
};

module.exports = config;
