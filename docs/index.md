---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "Aron Notes"
  text: "把工程经验变成可复用知识"
  tagline: 从 BLE 协议分析到图算法可视化，这里记录真实问题、解决过程和可执行结论。
  actions:
    - theme: brand
      text: 开始阅读
      link: /ble/ananlyzer
    - theme: alt
      text: 查看全部文章
      link: /markdown-examples
    - theme: alt
      text: GitHub
      link: https://github.com/Aron-Tech-a
    - theme: alt
      text: 最近文章
      link: /#timeline

features:
  - title: BLE 深度分析
    details: 追踪协议栈行为，拆解关键数据结构和运行时链路，定位问题更快。
    link: /ble/ananlyzer
    icon: "\U0001F52C"
  - title: 网络栈实战问题
    details: 记录真实编译与链接问题，给出可落地的排障路径和修复方案。
    link: /ble/lwip_inet_ntop
    icon: "\U0001F6E0"
  - title: 可视化布局探索
    details: 使用 Cytoscape 相关方案展示布局、约束和交互，直观理解复杂关系。
    link: /api-examples
    icon: "\U0001F9ED"

---

<script setup>
import { computed } from 'vue'
import { useData } from 'vitepress'

const { site, theme } = useData()

const normalizePostLink = (link) => {
  const normalizedLink = link.replace(/\.md(?=($|[?#]))/, '.html')

  if (!normalizedLink.startsWith('/')) {
    return normalizedLink
  }

  const base = site.value.base || '/'
  return base === '/' ? normalizedLink : `${base.replace(/\/$/, '')}${normalizedLink}`
}

const posts = computed(() => {
  const groups = Array.isArray(theme.value.sidebar)
    ? theme.value.sidebar
    : []

  const items = groups
    .flatMap((group) => Array.isArray(group.items) ? group.items : [])
    .filter((item) => item.link && item.link !== '/markdown-examples' && item.link !== '/api-examples')
    .slice(0, 6)

  return items.map((item, index) => ({
    title: item.text,
    url: normalizePostLink(item.link),
    dateText: `TOP ${String(index + 1).padStart(2, '0')}`,
    summary: '来自导航配置的自动聚合入口，可在 config.mts 的 sidebar 中维护顺序。'
  }))
})
</script>

<section class="home-gallery">
  <h2>可视化实验集</h2>
  <p>这些图不是装饰，它们对应了真实布局算法与约束策略的验证过程。</p>
  <div class="home-gallery-grid">
    <article class="gallery-card">
      <h3>架构分层</h3>
      <p>从基础库到扩展层，明确每一层职责、依赖方向和复用边界。</p>
    </article>
    <article class="gallery-card">
      <h3>约束驱动布局</h3>
      <p>通过相对位置和对齐约束，让图布局符合真实业务语义。</p>
    </article>
    <article class="gallery-card">
      <h3>重叠消解策略</h3>
      <p>观察节点边界冲突，调参与迭代，提升可读性与可交互性。</p>
    </article>
    <article class="gallery-card">
      <h3>工程化沉淀</h3>
      <p>将探索结果写成可复用文档，形成可追踪的知识资产。</p>
    </article>
  </div>
</section>

<section id="timeline" class="home-timeline">
  <h2>最近文章时间线</h2>
  <p>从 sidebar 自动聚合并按配置顺序展示；改导航顺序即可调整时间线顺序。</p>
  <ol class="timeline-list">
    <li v-for="post in posts" :key="post.url" class="timeline-item">
      <span class="timeline-date">{{ post.dateText }}</span>
      <a class="timeline-title" :href="post.url">{{ post.title }}</a>
      <p class="timeline-summary">{{ post.summary }}</p>
    </li>
  </ol>
</section>
