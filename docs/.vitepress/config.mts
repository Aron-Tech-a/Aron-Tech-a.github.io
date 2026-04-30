import { defineConfig } from 'vitepress'
import { withMermaid } from "vitepress-plugin-mermaid";

const isGithubActions = process.env.GITHUB_ACTIONS === 'true'

// https://vitepress.dev/reference/site-config
export default withMermaid({
  title: "aron",
  description: "欢迎来到我的站点",
  base: isGithubActions ? '/Aron-Tech-a.github.io/' : '/',
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Examples', link: '/markdown-examples' },
      { text: '教程', link: '/tutorials/mineru-windows-install.md' },
      { text: 'BLE', link: '/ble/ananlyzer.md' }
    ],

    sidebar: [
      {
        text: '教程',
        items: [
          { text: 'Windows 上安装、运行与测试 MinerU', link: '/tutorials/mineru-windows-install.md' }
        ]
      },
      {
        text: 'Examples',
        items: [
          { text: 'BLE Stack 工程深度分析', link: '/ble/ananlyzer.md' },
          { text: 'Markdown Examples', link: '/markdown-examples' },
          { text: 'Runtime API Examples', link: '/api-examples' },
          { text: 'undefined reference to lwip_inet_ntop/lwip_inet_pton', link: '/ble/lwip_inet_ntop.md' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/Aron-Tech-a' }
    ]
  }
})
