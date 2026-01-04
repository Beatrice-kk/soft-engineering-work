const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  assetsDir: 'static', // 静态资源目录
  transpileDependencies: true,
  
  // 添加 devServer 配置
  devServer: {
    host: '0.0.0.0', // 允许外部访问
    port: 8090,      // 指定开发服务器端口
    allowedHosts: 'all', // 允许所有主机请求，解决 Invalid Host header 问题
  },
})