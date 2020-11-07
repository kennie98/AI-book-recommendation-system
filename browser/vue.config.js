module.exports = {
  publicPath: '/',
  configureWebpack: {
    module: {
      rules: [
        {
          test: /config.*config\.js$/,
          use: [
            {
              loader: 'file-loader',
              options: {
                name: 'config.js',
              },
            },
          ],
        },
      ],
    },
  },
};
